"""Alabama: ADEM drinking-water laboratory certification lists, fetched 2026-11-09.
  - Certified Bacteriological Laboratories (Revised: April 7, 2026)        BacteriologicalLabs.pdf
  - In State Certified Chemical Laboratories (Revised: April 7, 2026)      InStateChemicalLabs.pdf
  - Out of State Certified Laboratories [chemical] (Revised: October 03, 2025)  OutofStateChemicalLabs_0.pdf
  - Certified PFAS Labs, EPA Method 537.1 (Updated: October 03, 2025)      CertifiedPFASLabs.pdf
Tables were extracted with pdfplumber into $SRC_DIR/al_tables.json (see /tmp/venv note in extract_in_tables.py).
Contact names, faxes and emails are not published. Entries are merged only when the street number and 5-digit ZIP
match exactly (or the row is an exact duplicate). Grouping is editorial (ADEM has no commercial flag) and is disclosed."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-al')
V = '2026-11-09'
more_lib.V = V
PROG = 'https://adem.alabama.gov/water/drinking-water-branch/information-public-water-systems/adem-drinking-water-laboratory-certification-program'
BASE = 'https://adem.alabama.gov/sites/default/files/'
LISTS = {
    'micro': ('BacteriologicalLabs.pdf', BASE + '2026-04/BacteriologicalLabs.pdf', 'ADEM: Certified Bacteriological Laboratories (revised April 7, 2026)', '2026-04-07'),
    'chem': ('InStateChemicalLabs.pdf', BASE + '2026-04/InStateChemicalLabs.pdf', 'ADEM: In State Certified Chemical Laboratories (revised April 7, 2026)', '2026-04-07'),
    'oos': ('OutofStateChemicalLabs_0.pdf', BASE + '2025-10/OutofStateChemicalLabs_0.pdf', 'ADEM: Out of State Certified Laboratories (chemical, revised October 3, 2025)', '2025-10-03'),
    'pfas': ('CertifiedPFASLabs.pdf', BASE + '2025-10/CertifiedPFASLabs.pdf', 'ADEM: Certified PFAS Labs, EPA Method 537.1 (updated October 3, 2025)', '2025-10-03'),
}
CONSUMERS = 'https://adem.alabama.gov/water/drinking-water-branch/information-consumers'
ADPH_WELL = 'https://www.alabamapublichealth.gov/environmental/well-water.html'
ADPH_BCL = 'https://www.alabamapublichealth.gov/bcl/sanitary-bacteriology.html'
ADPH_FORM = 'https://www.alabamapublichealth.gov/bcl/assets/private-water-sample-form-ada.pdf'
HOUSTON = 'https://www.alabamapublichealth.gov/houston/well-water.html'
ACES_WHERE = 'https://www.aces.edu/blog/topics/private-well-program/where-to-get-your-well-water-tested/'
ACES_STEP = 'https://www.aces.edu/blog/topics/fish-water/step-by-step-guide-to-getting-your-well-water-tested/'

T = json.load(open(os.path.join(SRC_DIR, 'al_tables.json')))
def rows(k):
    r = T[LISTS[k][0]]
    if r[0][0] == 'LABORATORY': r = r[1:]
    out = []
    for x in r:
        if len(x) == 8: x = x[:7] + [''] + x[7:]   # PFAS list has no FAX column
        out.append(dict(zip(['name', 'contact', 'street', 'city', 'state', 'zip', 'phone', 'fax', 'email'], x)))
    return out
data = {k: rows(k) for k in LISTS}
# pdfplumber drops the name cell of the Madisonville, KY row; the name is taken from pdftotext -layout of the same PDF.
lay = open(os.path.join(SRC_DIR, 'OutofStateChemicalLabs_0.txt')).read()
for r in data['oos']:
    if not r['name']:
        assert r['street'] == '825 Industrial Road' and 'Pace Analytical Services, Madisonville , KY' in lay
        r['name'] = 'Pace Analytical Services, Madisonville, KY'
assert [len(data[k]) for k in ['micro', 'chem', 'oos', 'pfas']] == [31, 6, 32, 12], [len(v) for v in data.values()]

def phones(s):
    out = []
    for p in re.split(r'[\n,]+', s or ''):
        p = p.strip()
        if not p: continue
        m = re.match(r'^(\(?\d{3}\)?[\s.-]*\d{3}-\d{4})(.*)$', p)
        if m and m.group(2).strip():
            out.append(clean_phone(m.group(1)) + ' ' + m.group(2).strip())
        else:
            out.append(clean_phone(p))
    return out
def z5(z): return z.strip()[:5]
def key(r):
    num = re.match(r'\s*(P\s*O\s*Box\s*\d+|\d+)', r['street'], re.I)
    return (re.sub(r'\W', '', num.group(1).lower()) if num else r['street'].lower(), z5(r['zip']))

LABEL = {'micro': 'Bacteria (ADEM bacteriological list)', 'chem': 'Chemistry (ADEM in-state chemical list)',
         'oos': 'Chemistry (ADEM out-of-state chemical list)', 'pfas': 'PFAS (ADEM PFAS list, EPA Method 537.1)'}
labs, dups = {}, 0
for k in ['micro', 'chem', 'oos', 'pfas']:
    seen = set()
    for r in data[k]:
        sig = (r['street'].lower(), r['zip'], r['phone'], r['contact'])
        if sig in seen: dups += 1; continue
        seen.add(sig)
        L = labs.setdefault(key(r), {'rows': [], 'lists': []})
        L['rows'].append(r); L['lists'].append(k)
assert dups == 1, dups  # Bessemer Utilities Lab / LAboratory printed twice with identical address, phone and contact

# Editorial groups (ADEM prints no commercial flag). Names clearly of testing businesses:
COMMERCIAL = re.compile(r'^(Environmental Resource Analysts|Guardian Systems|Pace Analytical|Polyenvironmental|Safety Environmental Services|Southern Environmental Testing|Sutherland Environmental)', re.I)
ADPH_ADDR = {('204', '36066'): 'Prattville', ('757', '36608'): 'Mobile'}  # addresses printed on ADPH form CL-27

out = []
for k, L in labs.items():
    b = L['rows'][0]
    names = []
    for r in L['rows']:
        if r['name'] not in names: names.append(r['name'])
    streets = []
    for r in L['rows']:
        if r['street'] not in streets: streets.append(r['street'])
    address = '%s, %s, %s %s' % (b['street'], b['city'], b['state'], b['zip'])
    ph = []
    for r in L['rows']:
        for p in phones(r['phone']):
            if p not in ph: ph.append(p)
    chips = [LABEL[x] for x in dict.fromkeys(L['lists'])]
    parts = ['On %s.' % '; '.join(LISTS[x][2].replace('ADEM: ', "ADEM's ") for x in dict.fromkeys(L['lists']))]
    notes = []
    if len(names) > 1:
        notes.append('Listed under more than one name at this address (%s); shown together here.' % '; '.join(names))
    if len(streets) > 1:
        notes.append('Street printed differently on the lists (%s).' % '; '.join(streets))
    if re.match(r'(?i)p\.?\s*o\.?\s*box', b['street']):
        notes.append('ADEM prints a P.O. box; call for a drop-off address.')
    if len(ph) > 1:
        notes.append('Other phone(s) on the ADEM lists: %s.' % ', '.join(ph[1:]))
    if b['name'].lower().startswith('bessemer utilities'):
        notes.append('Printed twice on the bacteriological list (as "Bessemer Utilities Lab" and "Bessemer Utilities LAboratory") with the same address and phone; shown once.')
    adph = ADPH_ADDR.get(k)
    if b['state'] != 'AL':
        group = 'limited'
    elif adph or COMMERCIAL.match(b['name']):
        group = 'main'
    else:
        group = 'public'
    if adph:
        notes.append('This is an Alabama Department of Public Health (ADPH) Bureau of Clinical Laboratories lab (same address as on ADPH\'s private-water sample form). For private wells it tests for total coliform bacteria including E. coli only, using bottles from your county health department; ADPH\'s form says the fee is currently waived. See the Alabama section at the top of this page.')
    if adph == 'Prattville':
        notes.append('ADPH\'s form prints (334) 290-3201 for the Prattville Laboratory.')
    if b['name'].startswith('Houston County Regional Water Lab'):
        notes.append('The Houston County Health Department well-water page (last updated August 21, 2025) tells residents to contact this lab for self-collection instructions and lists a $15.00 testing fee per sample.')
    if b['name'].startswith('Living Water Services'):
        notes.append('The name does not show whether this is a commercial lab or a water system\'s own lab. Call first.')
    if b['name'].startswith(('Alliance Technical Group', 'Summit Environmental Technologies')):
        notes.append('Alliance Technical Group (out-of-state chemical list, ZIP 44223) and Summit Environmental Technologies (PFAS list, ZIP 44313) are both printed at 3310 Win Street with the same phone, but with different ZIPs, so we did not merge them.')
    srcs = [(LISTS[x][1], LISTS[x][2], LISTS[x][3]) for x in dict.fromkeys(L['lists'])]
    lab = dict(name=names[0], address=address, city=b['city'], phone=ph[0] if ph else None, accredited_for=chips,
               detail=' '.join(parts), group=group, source_url=srcs[0][0], source_name=srcs[0][1],
               source_date=srcs[0][2], last_verified=V)
    if len(srcs) > 1:
        lab['source_url_2'], lab['source_name_2'] = srcs[1][0], srcs[1][1]
    if len(srcs) > 2:
        lab['detail'] += ' Also on ' + '; '.join(s[1] for s in srcs[2:]) + '.'
    if notes: lab['note'] = ' '.join(notes)
    out.append(lab)

order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))
from collections import Counter
c = Counter(l['group'] for l in out)
instate = c['main'] + c['public']
print('labs', len(out), dict(c), 'dups dropped', dups)

write_state(
    'alabama', 'Alabama', 'AL', out,
    {'name': 'ADEM certified drinking-water laboratory lists (bacteriological, in-state chemical, out-of-state chemical, PFAS)',
     'page_url': PROG, 'program_url': PROG,
     'report_date': 'In-state lists revised April 7, 2026; out-of-state and PFAS lists October 3, 2025'},
    {
        'title': 'Alabama certified drinking-water labs for private well testing (ADEM lists, April 2026)',
        'description': 'All %d labs on ADEM\'s four certified drinking-water lab lists (in-state lists revised 4/7/2026), plus the free ADPH state lab bacteria test for private wells and what it does not cover.' % len(out),
        'intro': [
            'Alabama\'s Department of Environmental Management (ADEM) certifies labs to test drinking water and posts four lists on its Laboratory Certification Program page: certified bacteriological labs and in-state certified chemical labs (both revised April 7, 2026), out-of-state certified chemical labs (revised October 3, 2025), and labs certified for PFAS by EPA Method 537.1 (updated October 3, 2025). ADEM says consumers "may also consider the use of a certified laboratory to test private wells", that the lists "contain both commercial laboratories that provide services to the public and water systems that have their own laboratories", and that "You should check with the lab to verify that they are currently certified before using."',
            'Together the four lists have %d entries. After dropping one duplicate row and combining entries with the same street number and ZIP, that gives the %d labs below: %d in Alabama and %d out of state.' % (sum(len(v) for v in data.values()), len(out), instate, c['limited']),
            'Free state bacteria test first: the Alabama Department of Public Health (ADPH) says about 800,000 people, or 20 percent of Alabamians, depend on private water supplies such as wells. ADPH\'s Bureau of Clinical Laboratories tests private well water for total coliform bacteria, including E. coli, at its Prattville and Mobile labs. Its collection instructions for private water samples (form CL-27, file updated September 2026) say "The fee is currently waived for each private water sample tested by the laboratory." You must use the sterilized bottles from your county health department or the lab office, fill to the 100 mL mark after running the water at least 3 minutes, and deliver the sample yourself, Monday through Thursday, 7:30 am to 4:00 pm. Samples over 30 hours old when received are not tested. ADPH\'s well water page says results are available about 24 hours after the sample is received, and that your county health department can send an environmentalist to collect the sample, for which "There may be a collection fee."',
            'What the free test does not cover: the same ADPH form says the Bureau of Clinical Laboratories "does not perform any chemical analysis of private well water," and that its report "does not meet any regulatory or financial institution requirements such as mortgage". For nitrate, metals or other chemistry, use a lab on ADEM\'s chemical lists below; Alabama Extension (ACES) gives the same advice. If a lender or buyer needs a report, ask a certified private lab whether its report meets their requirements. ADEM says it has no authority over private wells and no funding to test them.',
            'County fees vary. For example, the Houston County Health Department page (last updated August 21, 2025) lists a $30.00 fee for an environmentalist to collect the sample and a $15.00 testing fee per sample at the Houston County Regional Water Laboratory. That is a county lab, not the ADPH state lab, and its page is older than the ADPH form. Call your county health department for its current process and fees.',
        ],
        'caveats': [
            'Certification is not the same as taking homeowner samples. ADEM\'s lists do not say which labs accept samples from the public, test prices, or what each lab is certified for beyond the list it is on. Call first and ask about bottles, fees, hold times and drop-off hours.',
            'The out-of-state chemical and PFAS lists were last revised October 3, 2025, more than a year before we checked them. Confirm current Alabama certification with the lab or ADEM (Drinking Water Branch, (334) 271-7773, as printed on ADEM\'s page).',
            'ADEM does not mark labs as commercial. We put in-state labs in the first group when their name is clearly a testing business, plus the two ADPH state labs. Everything else in Alabama (mostly water utilities and water boards) is in the second group. Out-of-state labs are in the third group. This grouping is ours, by name.',
            'Chips show only which ADEM list a lab is on. ADEM\'s lists do not break certification down by test (for example nitrate or arsenic), so we do not show that.',
            'Phone numbers are as printed by ADEM. Contact names, emails and fax numbers are not shown. Typos in the source (for example "Laboartory", "Laboratroy", "Norhtington", "Cuyahoga Falla") are kept as printed.',
            'We did not verify prices, turnaround times or websites for any lab, so none are shown.',
        ],
        'main_heading': 'Alabama commercial labs and ADPH state labs',
        'public_heading': 'Alabama water-utility and other labs on ADEM\'s lists',
        'public_note': 'Most of these are run by a city water works, water board or utility for its own compliance testing. ADEM does not say whether any take homeowner samples. Call first.',
        'limited_heading': 'Out-of-state labs on ADEM\'s chemical and PFAS lists',
        'limited_note': 'These labs are outside Alabama but are on ADEM\'s out-of-state chemical list (October 3, 2025) or PFAS list (October 3, 2025). Ask about shipping, bottles and hold times before you collect.',
        'chips_label': 'On ADEM\'s certified lists:',
        'resources': [
            {'label': 'ADEM: Drinking Water Laboratory Certification Program (all four lists)', 'url': PROG},
            {'label': 'ADEM: Certified Bacteriological Laboratories (PDF, revised April 7, 2026)', 'url': LISTS['micro'][1]},
            {'label': 'ADEM: In State Certified Chemical Laboratories (PDF, revised April 7, 2026)', 'url': LISTS['chem'][1]},
            {'label': 'ADEM: Out of State Certified Laboratories (PDF, revised October 3, 2025)', 'url': LISTS['oos'][1]},
            {'label': 'ADEM: Certified PFAS Labs (PDF, updated October 3, 2025)', 'url': LISTS['pfas'][1]},
            {'label': 'ADEM: Information for Consumers (private wells)', 'url': CONSUMERS},
            {'label': 'ADPH: Well Water (testing and well disinfection)', 'url': ADPH_WELL},
            {'label': 'ADPH Bureau of Clinical Laboratories: Sanitary Bacteriology (private well forms)', 'url': ADPH_BCL},
            {'label': 'ADPH: Collection Instructions for Private Water Samples (PDF, fee waived, 30-hour rule)', 'url': ADPH_FORM},
            {'label': 'ADPH Houston County: Well Water Testing (county fees, updated August 21, 2025)', 'url': HOUSTON},
            {'label': 'Alabama Extension: Where to Get Your Well Water Tested (county health department contacts)', 'url': ACES_WHERE},
            {'label': 'Alabama Extension: Step-by-Step Guide to Getting Your Well Water Tested', 'url': ACES_STEP},
        ],
    })
