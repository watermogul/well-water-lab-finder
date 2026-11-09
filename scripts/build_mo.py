"""Missouri: Missouri DNR certified drinking-water laboratory lists, fetched 2026-11-08.
  - Certified Microbiological Laboratories (DNR page; labs certified by Missouri DHSS for drinking-water microbiology)
  - Certified Chemical Laboratories (DNR page; labs certified by DNR for drinking-water chemistry)
Both pages offer "Download spreadsheet of all Laboratories" (MoDNR-Certified-Microbio-Labs.xlsx, MoDNR-Certified-Chem-Labs.xlsx).
Structured fields come from the spreadsheets; the chemistry parameter list per lab comes from the HTML page (the
spreadsheet glues parameter names together). Raw files are in $SRC_DIR (not committed):
  micro.xlsx, chem.xlsx, chemical.html, chemical-p1.html, microbiological*.html
A lab on both lists is merged only when street line 1 and 5-digit ZIP match exactly. Contact names/emails are not published.
Nothing is inferred: grouping uses the "Commercial" column DNR prints and the lab's state."""
import os, sys, re, html
from datetime import datetime, date
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone
import openpyxl

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-mo')
LAND = 'https://dnr.mo.gov/water/business-industry-other-entities/certified-laboratories'
MICRO = LAND + '/microbiological'
CHEM = LAND + '/chemical'
DHSS_PDW = 'https://health.mo.gov/prevention/environmental-factors/private-drinking-water'
DHSS_KIT = 'https://health.mo.gov/prevention/environmental-factors/private-drinking-water/well-water-test-kit-information-and-services'
SPHL_BACT = 'https://health.mo.gov/state-public-health-laboratory/private-drinking-water-bacteriological-testing'
SPHL_METALS = 'https://health.mo.gov/state-public-health-laboratory/metals-water'
LPHA = 'https://health.mo.gov/local/find-your-local-public-health-agency'
V = '2026-11-08'
TODAY = date(2026, 11, 8)
more_lib.V = V

def rows(f):
    ws = openpyxl.load_workbook(os.path.join(SRC_DIR, f)).active
    r = list(ws.iter_rows(values_only=True)); h = r[0]
    return [dict(zip(h, x)) for x in r[1:] if any(x)]

micro, chem = rows('micro.xlsx'), rows('chem.xlsx')
assert len(micro) == 68 and len(chem) == 26, (len(micro), len(chem))

# chemistry parameters from the HTML (bullet-separated); keyed by certificate number
params = {}
for f in ['chemical.html', 'chemical-p1.html']:
    t = open(os.path.join(SRC_DIR, f), encoding='utf-8').read()
    for b in re.split(r'Certificate No:\s*', t)[1:]:
        num = html.unescape(re.sub(r'<[^>]+>', '', b.split('<br')[0])).strip()
        m = re.search(r'field-chemical-testing-parameter">(.*?)</td>', b, re.S)
        ps = [html.unescape(p).replace('\u2010', '-').strip() for p in html.unescape(m.group(1)).split('\u2022')] if m else []
        params[num] = [re.sub(r'\s+', ' ', p.replace('\xa0', ' ')).strip() for p in ps if p.strip()]
assert len(params) == 26, len(params)
# cross-check micro HTML count
mcount = sum(open(os.path.join(SRC_DIR, f), encoding='utf-8').read().count('Certificate No:') for f in ['microbiological.html', 'microbiological-p1.html', 'microbiological-p2.html'])
assert mcount == 68, mcount

def z5(z): return str(z).strip()[:5].zfill(5)
def key(r): return (re.sub(r'\W', '', str(r['Address line1']).lower()), z5(r['Zip Code']))
def exp(r): return datetime.strptime(r['Expiration Date'], '%b %d, %Y').date()

CHEM_CHIPS = [('Nitrate', 'Nitrate'), ('Arsenic', 'Arsenic'), ('Lead', 'Lead'), ('Fluoride', 'Fluoride'), ('Uranium', 'Uranium'),
              ('Perfluorooctanoic Acid (PFOA)', 'PFAS (PFOA)')]
labs = {}
for r in micro:
    labs.setdefault(key(r), {'base': r, 'micro': [], 'chem': []})['micro'].append(r)
for r in chem:
    labs.setdefault(key(r), {'base': r, 'micro': [], 'chem': []})['chem'].append(r)

out = []; expired_n = 0
for k, L in labs.items():
    b = L['base']
    names = []
    for r in L['micro'] + L['chem']:
        if r['Lab Name'] not in names: names.append(r['Lab Name'])
    a2 = b['Address line2']
    street = b['Address line1'] + ((', ' + a2) if a2 else '')
    zipc = str(b['Zip Code']).strip()
    address = '%s, %s, %s %s' % (street, b['City'], b['State'], zipc)
    parts, notes, chips = [], [], []
    commercial = False
    for r in L['micro']:
        parts.append('Microbiological list: certificate %s, expiration date %s, listed as commercial: %s.' % (r['Certificate No.'], r['Expiration Date'], r['Commercial']))
        commercial |= r['Commercial'] == 'Yes'
    if L['micro']: chips.append('Bacteria (microbiological list)')
    for r in L['chem']:
        num = str(r['Certificate No.']).strip()
        p = params[num]
        parts.append('Chemical list: certificate %s, expiration date %s, listed as commercial: %s, %d testing parameters listed.' % (num, r['Expiration Date'], r['Commercial'], len(p)))
        commercial |= r['Commercial'] == 'Yes'
        for full, lab in CHEM_CHIPS:
            if full in p and lab not in chips: chips.append(lab)
    for r in L['micro'] + L['chem']:
        if exp(r) < TODAY:
            expired_n += 1
            notes.append('The expiration date DNR shows for certificate %s (%s) has already passed, but the lab was still on the list on %s. Confirm current certification with the lab or DNR before you test.' % (str(r['Certificate No.']).strip(), r['Expiration Date'], V))
    if L['chem'] and not any(c in chips for c in ['Nitrate', 'Arsenic', 'Lead']):
        notes.append('Its entry on the DNR chemical list does not include nitrate, arsenic or lead. See that list for the parameters it does cover.')
    if len(names) > 1:
        notes.append('Listed under more than one name at the same address (%s); shown together here.' % '; '.join(names))
    if re.match(r'(?i)p\.?\s*o\.? box', str(b['Address line1'])) or (a2 and re.match(r'(?i)p\.?\s*o\.? box', a2)):
        notes.append('The DNR record includes a P.O. box; call for a drop-off address.')
    if b['Lab Name'].startswith('Missouri Department of Health & Senior Services-State Public Health Laboratory'):
        notes.append('For homeowners, DHSS says the State Public Health Laboratory tests private wells using kits you get from your local public health agency (or the DHSS online kit request form); see the Missouri section at the top of this page.')
    phones = []
    for r in L['micro'] + L['chem']:
        ph = clean_phone(r['Contact Phone Number'])
        if ph and ph not in phones: phones.append(ph)
    if len(phones) > 1:
        notes.append('Other contact phone(s) on the DNR lists: %s.' % ', '.join(phones[1:]))
    if b['State'] != 'MO':
        group = 'limited'
    elif commercial:
        group = 'main'
    else:
        group = 'public'
    srcs = []
    if L['micro']: srcs.append((MICRO, 'Missouri DNR: Certified Microbiological Laboratories'))
    if L['chem']: srcs.append((CHEM, 'Missouri DNR: Certified Chemical Laboratories'))
    lab = dict(name=names[0], address=address, city=b['City'], phone=phones[0] if phones else None, accredited_for=chips,
               detail=' '.join(parts), group=group, source_url=srcs[0][0], source_name=srcs[0][1],
               source_date=V, last_verified=V, lab_id=', '.join(str(r['Certificate No.']).strip() for r in L['micro'] + L['chem']))
    if len(srcs) > 1:
        lab['source_url_2'], lab['source_name_2'] = srcs[1]
    if notes: lab['note'] = ' '.join(notes)
    out.append(lab)

order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))
from collections import Counter
c = Counter(l['group'] for l in out)
both = sum(1 for L in labs.values() if L['micro'] and L['chem'])
mo_main = c['main']
print('labs', len(out), dict(c), 'both lists', both, 'expired certs', expired_n)

write_state(
    'missouri', 'Missouri', 'MO', out,
    {'name': 'Missouri DNR certified drinking-water laboratory lists (microbiological and chemical)', 'page_url': LAND,
     'program_url': MICRO, 'report_date': 'Live DNR lists, copied November 8, 2026'},
    {
        'title': 'Missouri certified drinking-water labs for private well testing (Missouri DNR lists)',
        'description': 'All %d labs on Missouri DNR\'s certified microbiological and chemical drinking-water lab lists (copied 11/8/2026), with certificate numbers, expiration dates, which common well tests each list covers, and how to get a state lab kit through your local health agency.' % len(out),
        'intro': [
            'Missouri DNR publishes two live lists of labs certified for drinking-water testing: a microbiological (bacteria) list, whose labs are certified by the Missouri Department of Health and Senior Services (DHSS), and a chemical list, whose labs are certified by DNR. On November 8, 2026 the lists had %d and %d entries. We merged entries that share the same street address and ZIP, which gives the %d labs below (%d appear on both lists).' % (len(micro), len(chem), len(out), both),
            'DNR\'s own wording matters for well owners: "Analysis of water samples from private residences or private wells does not have to be done by a certified laboratory." DNR adds that other labs that chose not to be certified "may produce equivalent results if they have adequate quality assurance or quality control in place." DNR also says labs listed as commercial "do perform compliance analyses for hire" and suggests contacting more than one lab for pricing.',
            'State lab option first: DHSS says the Missouri State Public Health Laboratory (MSPHL) offers both bacteria and chemical private drinking water testing, and recommends testing your well once each year for total coliform bacteria, E. coli and nitrates. Kits come from your local public health agency (LPHA) or State District Health Offices, and DHSS also has an online kit request form. For bacteria, the MSPHL page says a $10 handling fee (check or money order only) must be included with the sample, results are presence/absence, and samples must reach the lab with testing started within 48 hours of collection; the MSPHL statewide courier to Jefferson City is free. DHSS says it does not offer private well testing for real estate transactions; for that, use a private lab such as those below.',
            'For chemistry, the MSPHL Metals in Water page says private-water samples "must be submitted by an Environmental Public Health Specialist, Lead Assessor, or Environmental Specialist employed by a Public Health Agency", and that when public health is not at risk, testing should be done by a private lab certified by DNR. DHSS notes Missouri\'s history of lead mining and recommends a metals test if you live where mining is happening or has happened. The MSPHL chemistry fee field reads "N/A"; we did not find a chemistry price on DHSS pages, so none is shown.',
        ],
        'caveats': [
            'The DNR lists are live and change. We copied them on November 8, 2026 (spreadsheets plus the web pages). Confirm certification with the lab before you collect a sample.',
            'Being certified does not mean a lab takes samples from homeowners. Neither list says which labs do. Call first and ask about bottles, fees, hold times and drop-off hours.',
            'Groups use only the "Commercial" column DNR prints and the lab\'s state: Missouri labs marked commercial on either list, then Missouri labs not marked commercial (mostly city water plants), then out-of-state labs.',
            'Chips: "Bacteria" means the lab is on the microbiological list (the list does not break that down by test). Nitrate, arsenic, lead, fluoride, uranium and PFAS (PFOA) chips mean that parameter appears in the lab\'s entry on the DNR chemical list. A missing chip means it did not appear there.',
            '%d certificate expiration dates shown by DNR had already passed on November 8, 2026 while the lab was still listed, including the State Public Health Laboratory\'s microbiological entry (Jul 31, 2026). These are noted on the listings as printed.' % expired_n,
            'Phone numbers are the contact numbers DNR lists. Contact names and emails are not shown. We did not verify prices, turnaround times or websites for any lab, so none are shown.',
        ],
        'main_heading': 'Missouri labs listed as commercial',
        'public_heading': 'Missouri water-utility and other labs not listed as commercial',
        'public_note': 'DNR does not mark these labs as commercial. Most are city or regional water plants doing their own system\'s compliance testing. The source does not say whether any take homeowner samples. Call first.',
        'limited_heading': 'Out-of-state labs on Missouri\'s lists',
        'limited_note': 'These labs are outside Missouri but appear on DNR\'s lists. Most are large commercial labs. Ask about shipping and sample hold times before you collect, especially for bacteria.',
        'chips_label': 'On Missouri\'s certified lists for:',
        'resources': [
            {'label': 'Missouri DNR: Certified Laboratories (overview)', 'url': LAND},
            {'label': 'Missouri DNR: Certified Microbiological Laboratories (live list, spreadsheet download)', 'url': MICRO},
            {'label': 'Missouri DNR: Certified Chemical Laboratories (live list with testing parameters, spreadsheet download)', 'url': CHEM},
            {'label': 'Missouri DHSS: Private Drinking Water', 'url': DHSS_PDW},
            {'label': 'Missouri DHSS: Well Water Test Kit Information and Services (kit request)', 'url': DHSS_KIT},
            {'label': 'Missouri State Public Health Laboratory: Private Drinking Water Bacteriological Testing ($10 handling fee, 48-hour rule)', 'url': SPHL_BACT},
            {'label': 'Missouri State Public Health Laboratory: Metals in Water', 'url': SPHL_METALS},
            {'label': 'Missouri DHSS: Find your local public health agency', 'url': LPHA},
        ],
    })
