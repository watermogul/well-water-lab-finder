"""Massachusetts: MassDEP "Certified Laboratories Offering Analytical Services for Private Well Owners and Residential Customers" spreadsheet
(XLSX linked from https://www.mass.gov/how-to/find-a-certified-laboratory-for-water-testing; served as
LaboratoryAvailabilitySurveyPrivateWellOwners_121825-a11y.xlsx, cell A1 "Created and published on 12/18/2025", Last-Modified 2025-12-19,
md5 eb11a4429bcdbd9075411bb7b34f9ee2). Sheet 1 = 22 labs that offer residential services, sheet 2 = 14 that do not.
Every lab was then looked up in MassDEP's Online Searchable Laboratory Certification Listing (LabCert, "updated daily") on 2026-11-23 with
Matrix = "Potable (DrinkingWater)", one analyte at a time (scripts/ma_labcert_harvest.py -> labcert_potable.json), so the chips show the
drinking-water analytes each lab was certified for that night, not the spreadsheet's self-reported categories.
Replaces the thin /labs/massachusetts/ state-guide (removed from stateGuides.json).

mass.gov returns 403 to curl and WebFetch drops link targets, so mass.gov pages and the XLSX were fetched in headless Chrome
(scripts/fetch_in_chrome.mjs). LabCert (eeaonline.eea.state.ma.us) answers plain requests.
SRC_DIR (not committed; all fetched 2026-11-23): ma-labs.xlsx, xlsx_rows.json (openpyxl dump, /workspace/plumbvenv), labcert.html,
labcert_potable.json, howto.html, private-wells.html, protect-your-family-...html, private-drinking-water-testing-...html, pfas-...-faq.html.
Contact names and e-mail addresses printed by MassDEP are not published (site convention)."""
import os, sys, re, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-ma')
V = '2026-11-23'
more_lib.V = V
HOWTO = 'https://www.mass.gov/how-to/find-a-certified-laboratory-for-water-testing'
XLSX = 'https://www.mass.gov/doc/massdep-certified-laboratories-offering-analytical-services-for-private-well-owners-and-residential-customers/download'
LABCERT = 'https://eeaonline.eea.state.ma.us/DEP/Labcert/Labcert.aspx'
PW = 'https://www.mass.gov/private-wells'
PYF = 'https://www.mass.gov/info-details/protect-your-family-a-guide-to-water-quality-testing-for-private-wells'
USE = 'https://www.mass.gov/info-details/private-drinking-water-testing-and-the-use-of-massdep-certified-laboratories'
PFAS = 'https://www.mass.gov/info-details/pfas-in-private-well-drinking-water-supplies-faq'
GUIDE = 'https://www.mass.gov/info-details/private-well-guidelines'
SN = 'MassDEP: Certified Laboratories Offering Analytical Services for Private Well Owners and Residential Customers (XLSX, "Created and published on 12/18/2025")'
SD = '2025-12-18'
SN2 = 'MassDEP Online Searchable Laboratory Certification Listing (database "updated daily"; searched 2026-11-23 with Matrix = Potable)'

assert hashlib.md5(open(os.path.join(SRC_DIR, 'ma-labs.xlsx'), 'rb').read()).hexdigest() == 'eb11a4429bcdbd9075411bb7b34f9ee2', 'MassDEP XLSX changed: re-extract and re-check'
X = json.load(open(os.path.join(SRC_DIR, 'xlsx_rows.json')))
S1, S2 = X['Labs-Residential Services'], X['Labs-No Residential Services']
assert S1[0][0].startswith('Created and published on 12/18/2025')
assert S1[2][0] == 'Laboratory Name' and S2[1][0] == 'Laboratory Name'
RES, NORES = S1[3:], S2[2:]
assert len(RES) == 22 and len(NORES) == 14
assert all(r[6] == 'Yes' for r in RES) and all(r[6] == 'No' for r in NORES)

DB = json.load(open(os.path.join(SRC_DIR, 'labcert_potable.json')))  # analyte -> [[id, name, address, phone, director, homeowner Y/N]]
assert len(DB['ALL']) == 81
DBALL = {r[0]: r for r in DB['ALL']}
CHIPMAP = [('Total coliform', ['TOTAL COLIFORM']), ('E. coli', ['E. COLI']), ('Nitrate', ['NITRATE-N']), ('Nitrite', ['NITRITE-N']),
           ('Arsenic', ['ARSENIC']), ('Lead', ['LEAD']), ('Copper', ['COPPER']), ('Fluoride', ['FLUORIDE']), ('Iron', ['IRON']),
           ('Manganese', ['MANGANESE']), ('Sodium', ['SODIUM']), ('Chloride', ['CHLORIDE']), ('Sulfate', ['SULFATE']), ('pH', ['PH']),
           ('Total dissolved solids', ['TOTAL DISSOLVED SOLIDS']), ('Turbidity', ['TURBIDITY']), ('Uranium', ['URANIUM']),
           ('Gross alpha', ['GROSS ALPHA']), ('Radium-226', ['RADIUM-226']), ('Radium-228', ['RADIUM-228']),
           ('Volatile organic compounds (VOCs)', ['VOLATILE ORGANIC COMPOUNDS']), ('Pesticides / herbicides', ['ATRAZINE', '2,4-D', 'SIMAZINE', 'ALACHLOR']),
           ('PFAS', ['PFAS']), ('1,4-Dioxane', ['1,4-DIOXANE']), ('Perchlorate', ['PERCHLORATE'])]
CERT = {a: {r[0] for r in rows} for a, rows in DB.items()}
def chips(i):
    return [lab for lab, an in CHIPMAP if any(i in CERT[a] for a in an)]

DISPLAY = {'Pace Analytical Services, LLC- Melville, NY': 'Pace Analytical Services, LLC'}
LABNAMES = open(os.path.join(SRC_DIR, 'labcert.html'), encoding='utf-8', errors='ignore').read()
def title(s):
    s = s.strip()
    return DISPLAY.get(s, s)
def addr(r):
    z = str(r[5]).strip()
    if re.fullmatch(r'\d{4}', z): z = '0' + z
    return '%s, %s, %s %s' % (re.sub(r'\s+', ' ', r[2].strip()), r[3].strip().title() if r[3].isupper() else r[3].strip(), r[4].strip(), z)
def lines(s):
    return '; '.join(x.strip() for x in (s or '').split('\n') if x.strip())

def db_note(i, sheet_name, sheet_phone):
    d = DBALL.get(i)
    if not d:
        return None
    bits = ['MassDEP\'s certification database (searched 2026-11-23) lists lab %s' % i]
    if d[1].replace(',', '').replace('.', '').lower() != sheet_name.replace(',', '').replace('.', '').lower():
        bits.append('under the name "%s"' % d[1])
    bits.append('at %s' % d[2].replace('-0000', ''))
    bits.append('with the homeowner-sample flag "%s"' % d[5])
    s = ' '.join(bits) + '.'
    if re.sub(r'\D', '', d[3])[:10] != re.sub(r'\D', '', sheet_phone)[:10]:
        s += ' The database prints a different phone, %s; the phone above is the residential contact number from the spreadsheet.' % d[3]
    return s

labs = []
INSTATE_MAIN, OOS, LIM, PUB = [], [], [], []
for r in RES:
    i = r[1].strip()
    ch = chips(i)
    det = ('MassDEP spreadsheet (12/18/2025): offers services to residential customers: Yes; multi-contaminant package for residents: %s; '
           'analyses offered (lab\'s own categories): %s; preferred contact: %s; transport: %s; availability: %s.') % (
           r[7], lines(r[8]).replace('Microbioogy', 'Microbiology'), r[9], lines(r[10]), lines(r[11]).split(';')[0])
    if 'Flexible' in (r[11] or ''):
        det = det.rstrip('.') + ' (the lab director can schedule a time case by case).'
    dn = db_note(i, r[0], r[14])
    if dn: det += ' ' + dn
    else: det += ' MassDEP\'s database returned no drinking-water (potable) certifications for lab %s on 2026-11-23.' % i
    l = dict(name=title(r[0]), address=addr(r), city=r[3].strip(), phone=r[14].strip() if 'ext' in r[14] else clean_phone(r[14]), accredited_for=ch,
             detail=det, source_name=SN, source_url=XLSX, source_date=SD, last_verified=V, source_url_2=LABCERT, source_name_2=SN2, lab_id_ma=i)
    if l['name'] != r[0].strip(): l['detail'] += ' Listed on the spreadsheet as "%s".' % r[0].strip()
    if not ch:
        l['group'] = 'limited'
        l['note'] = ('The spreadsheet says this lab offers bacteria and chemistry testing to residents, but on 2026-11-23 MassDEP\'s database showed it only with non-drinking-water (non-potable) certifications. '
                     'Ask the lab which drinking-water tests it is certified for before using it for a Board of Health, sale or mortgage test.')
        LIM.append(l)
    elif r[4].strip() == 'MA':
        l['group'] = 'main'; INSTATE_MAIN.append(l)
    else:
        l['group'] = 'outofstate'; OOS.append(l)
    labs.append(l)
for r in NORES:
    i = r[1].strip()
    ch = chips(i)
    d = DBALL.get(i)
    det = 'MassDEP spreadsheet (12/18/2025): offers services to residential customers: No.'
    if d:
        det += ' ' + db_note(i, r[0], d[3]).split(' The database prints')[0]
        ph = clean_phone(d[3])
    elif ('value="%s"' % i) not in LABNAMES:
        det += ' We did not find this lab (%s) in MassDEP\'s certification database on 2026-11-23; it may no longer be certified.' % i
        ph = None
    else:
        det += ' MassDEP\'s database returned no drinking-water (potable) certifications for lab %s on 2026-11-23.' % i
        ph = None
    l = dict(name=title(r[0]), address=addr(r), city=r[3].strip().title(), phone=ph, accredited_for=ch, detail=det, group='public',
             source_name=SN, source_url=XLSX, source_date=SD, last_verified=V, source_url_2=LABCERT, source_name_2=SN2, lab_id_ma=i)
    PUB.append(l); labs.append(l)

from collections import Counter
cnt = Counter(l['group'] for l in labs)
assert cnt == Counter({'main': 12, 'outofstate': 9, 'limited': 1, 'public': 14}), cnt
res = [l for l in labs if l['group'] != 'public']
def has(l, *a): return all(x in l['accredited_for'] for x in a)
full = [l for l in res if has(l, 'Total coliform', 'E. coli', 'Nitrate', 'Arsenic', 'Lead')]
full_in = [l['name'] + ' (' + l['city'] + ')' for l in full if l['group'] == 'main']
full_out = [l['name'] + ' (' + l['city'] + ', ' + l['address'].split(', ')[-1][:2] + ')' for l in full if l['group'] == 'outofstate']
bact_in = [l for l in INSTATE_MAIN if has(l, 'Total coliform')]
pfas = [l['name'] for l in res if 'PFAS' in l['accredited_for']]
ura = [l['name'] for l in res if 'Uranium' in l['accredited_for']]
galpha = [l['name'] for l in res if 'Gross alpha' in l['accredited_for']]
voc = [l['name'] for l in res if 'Volatile organic compounds (VOCs)' in l['accredited_for']]
print('full in', full_in, 'full out', full_out); print('pfas', pfas); print('uranium', ura); print('galpha', galpha); print('bact in', len(bact_in))
def j(xs):
    return ', '.join(xs[:-1]) + (' and ' if len(xs) > 1 else '') + xs[-1]

write_state('massachusetts', 'Massachusetts', 'MA', labs,
    {'name': SN + ', cross-checked against the ' + SN2, 'page_url': HOWTO, 'program_url': LABCERT,
     'report_date': 'spreadsheet created and published December 18, 2025; certification database searched November 23, 2026'},
    {
     'title': 'Massachusetts certified labs for well water testing (all 36 on MassDEP\'s private-well list, checked Nov 2026)',
     'description': 'All 36 labs on MassDEP\'s private-well lab spreadsheet: 22 that take residential samples, 14 that do not, each checked against MassDEP\'s certification database on Nov 23, 2026 for bacteria, nitrate, arsenic, PFAS and more.',
     'intro': [
      'MassDEP does not regulate private wells in Massachusetts; your local board of health does, and it may have its own testing rules. MassDEP does not test water for individuals, but it publishes a spreadsheet of certified labs that answered its survey on whether they serve private well owners and other residential customers ("Created and published on 12/18/2025"). On it, 22 labs say they take residential samples and 14 say they do not. We copied it on November 23, 2026 and looked up every lab the same night in MassDEP\'s online certification database, which MassDEP says is updated daily, searching drinking-water ("Potable") certifications one test at a time. The chips on each card come from that search, not from the labs\' own descriptions.',
      'The short version: %d of the %d in-state labs that take residential samples are certified for drinking-water bacteria. For bacteria, nitrate, arsenic and lead under one roof, the in-state choices are %s; out of state, %s also take residential samples (several by overnight mail or courier). Bacteria samples have short hold times, so a lab you can drive to usually matters for that test.' % (len(bact_in), len(INSTATE_MAIN), j(full_in), j(full_out)),
      'What to test: MassDEP\'s "Protect Your Family" guide says there is no state requirement to test a private well (a lender or local board of health may require it) but recommends testing for coliform bacteria and nitrate/nitrite initially and at least once a year, and for its "standard analysis" (arsenic, chloride, copper, fluoride, hardness, iron, lead, manganese, pH, sodium), radon, a gross alpha screen (bedrock wells only), VOCs and PFAS6 initially and at least once every ten years, or as your board of health requires. MassDEP also recommends testing before buying a home with a well, and a bacteria test after any well repair or pump or plumbing work (after disinfection and flushing).',
      'PFAS: MassDEP\'s public drinking-water standard is 20 ng/L (parts per trillion) for six specific PFAS, individually or summed ("PFAS6"), and its PFAS FAQ recommends that all private wells be tested for PFAS, especially within one to two miles of a known source. Of the labs that take residential samples, %d were certified for PFAS in drinking water on November 23, 2026: %s.' % (len(pfas), j(pfas)),
     ],
     'caveats': [
      'The spreadsheet is almost a year old. Several labs appear under different names in MassDEP\'s database (for example, Nashoba Analytical now appears as Eurofins Ayer, Northeast Environmental Laboratory as Eurofins Danvers, Granite State Analytical as Eurofins Derry, and Analytical Balance as Eurofins Providence (AB)). We show the spreadsheet name and note the database name on each card. Addresses and phones are the spreadsheet\'s; where the database prints a different phone, the card says so.',
      'The spreadsheet\'s "analyses offered" column is each lab\'s own broad description (for example "Chemistry (PFAS, Lead, etc.)"). It is not the same as certification: some labs that list chemistry are certified in drinking water only for bacteria, or for bacteria plus pH and turbidity. Use the chips, and ask the lab to confirm it is certified for each test you order. MassDEP recommends asking the lab to put its MassDEP certification number on the report.',
      'MassDEP\'s database has no radon test to search, so no lab here shows a radon chip; ask the lab whether it tests radon in water. MassDEP\'s lab-use guidance says there are no MassDEP certification procedures for iron and manganese in drinking water, yet the database returned "Potable" iron and manganese for some labs; we show what the database returned. The "Pesticides / herbicides" chip means at least one of atrazine, 2,4-D, simazine or alachlor.',
      'Practical Applications (Woburn) is on the residential list, but the database showed no drinking-water certifications for it on November 23, 2026, so it is shown separately.',
      'Prices: MassDEP says commercial labs set their own prices. We did not verify prices, turnaround times or websites for any lab, so none are shown. MassDEP\'s advice: get quotes from several certified labs and do not choose on price alone. Contact names and e-mail addresses printed by MassDEP are not shown.',
      'The grouping is ours: in-state labs that take residential samples, the one with no drinking-water certification found, out-of-state labs that take residential samples, and the labs that told MassDEP they do not.',
     ],
     'main_heading': 'Massachusetts labs that take residential (private-well) samples',
     'limited_heading': 'On the residential list, but no drinking-water certification found',
     'limited_note': 'MassDEP\'s spreadsheet says this lab takes residential samples, but the certification database showed only non-drinking-water certifications on November 23, 2026. Ask before using it for a drinking-water test.',
     'public_heading': 'Certified labs that told MassDEP they do NOT take residential samples',
     'public_note': 'These labs are on MassDEP\'s spreadsheet as not offering services to residential customers (many are water-utility or treatment-plant labs; MassDEP says those generally do not accept samples from private consumers other than local residents). Shown so you do not waste a call. Phones are from MassDEP\'s database.',
     'oos_heading': 'Out-of-state labs that take Massachusetts residential samples',
     'oos_note': [
      'These labs hold Massachusetts certification and told MassDEP they serve residential customers, mostly by overnight mail or courier. Uranium was certified at %d of the residential-list labs (%s) and gross alpha at %d (%s), both mostly out of state. Ask about bottles, shipping and hold times before collecting a sample.' % (len(ura), j(ura), len(galpha), j(galpha)),
     ],
     'chips_label': 'Certified by MassDEP for drinking water (database search, Nov 23, 2026):',
     'resources': [
      {'label': 'MassDEP: Find a Certified Laboratory for Water Testing (links the private-well lab spreadsheet)', 'url': HOWTO},
      {'label': 'MassDEP: Certified Laboratories Offering Analytical Services for Private Well Owners and Residential Customers (XLSX, December 18, 2025)', 'url': XLSX},
      {'label': 'MassDEP: Online Searchable Laboratory Certification Listing (choose Matrix "Potable (DrinkingWater)")', 'url': LABCERT},
      {'label': 'MassDEP: Protect Your Family: A Guide to Water Quality Testing for Private Wells', 'url': PYF},
      {'label': 'MassDEP: Private Drinking Water Testing and the use of MassDEP Certified Laboratories', 'url': USE},
      {'label': 'MassDEP: PFAS in Private Well Drinking Water Supplies FAQ', 'url': PFAS},
      {'label': 'MassDEP: Private Well Guidelines', 'url': GUIDE},
      {'label': 'MassDEP: Private Wells (all private-well resources)', 'url': PW},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('massachusetts', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed massachusetts from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', ', '.join(l['accredited_for']))
