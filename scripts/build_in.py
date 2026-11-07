"""Indiana: "Indiana Certified Drinking Water Laboratories" (Revised 11/7/2025), section "Labs that accept samples
from the public" (IN-STATE), fetched 2026-11-06 from in.gov/idem. Rows come from $SRC_DIR/in_tables.json
(scripts/extract_in_tables.py). Two rows the table extractor mangles are entered by hand from `pdftotext -layout`
of the same PDF (see FIXES). Labs in the "do not accept samples from the public" section are counted, not listed.
Websites printed in the PDF are wrapped mid-word and were not checked, so they are not published."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone, COMMON_CAVEAT_PRICES, looks_public, key_chips

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-in')
URL = 'https://www.in.gov/idem/cleanwater/files/dw_cert_lab_in-state.pdf'
IDOH_CERT = 'https://www.in.gov/health/laboratories/drinking-water-laboratory-certification'
IDOH_WELL = 'https://www.in.gov/health/laboratories/testing/well-water'
IDOH_EPH = 'https://www.in.gov/health/eph/well-water-quality-and-testing/'
SN = 'Indiana Certified Drinking Water Laboratories, "Labs that accept samples from the public" (Revised 11/7/2025)'
V = '2026-11-06'
SOURCE_DATE = '2025-11-07'
more_lib.V = V

rows = json.load(open(os.path.join(SRC_DIR, 'in_tables.json')))
PHONE = re.compile(r'^(1-)?\d{3}-\d{3}-\s?\d{4}$')
ID = re.compile(r'^([MC]-[0-9A-Z]{2}-[0-9]{2}\s*)+$')

public_rows, nopub = [], 0
section = 'public'
for r in rows:
    cells = [c for c in r['cells'] if c]
    joined = ' '.join(cells)
    if 'do not accept samples' in joined:
        section = 'nopublic'; continue
    if not cells or not ID.match(cells[-1]):
        continue
    if section == 'nopublic':
        nopub += 1; continue
    public_rows.append(cells)

# Hand fixes, transcribed from pdftotext -layout of the same PDF:
FIXES_ADD = [
    # pdfplumber drops this row (page 6, Monroe County)
    ['Dillman Road Quality Control Laboratory', '100 West Dillman Road Bloomington, IN 47403', '812-824-4900', 'bloomington.in.gov',
     'total coliform/E.coli, Heterotrophic plate count', 'Monroe', 'M-53-01'],
]
FIX_REPLACE = {
    # row is split across pages 7-8; address and certification completed from layout text
    'Vanderburgh County Health Department': ['Vanderburgh County Health Department', '420 Mulberry Street Evansville, IN 47713', '812-435-5568',
        'health.vanderburghcounty.in.gov', 'total coliform/E.coli, Enumeration of E. coli, Heterotrophic plate count', 'Vanderburgh', 'M-82-02'],
}
public_rows = [FIX_REPLACE.get(c[0], c) for c in public_rows] + FIXES_ADD
assert len(public_rows) == 49, len(public_rows)

def fix_spaces(s):
    s = re.sub(r'\s+,', ',', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

CITIES = sorted(['Ft. Wayne', 'Columbus', 'Fowler', 'Logansport', 'Clarksville', 'Frankfort', 'Waterloo', 'Muncie', 'Jasper',
    'Goshen', 'Elkhart', 'Marion', 'Westfield', 'Greenfield', 'Brownsburg', 'Kokomo', 'Rensselaer', 'Madison', 'Warsaw',
    'Crown Point', 'East Chicago', 'Merrillville', 'LaPorte', 'Indianapolis', 'Bloomington', 'Crawfordsville', 'Monrovia',
    'Spencer', 'Valparaiso', 'Wanatah', 'South Bend', 'Granger', 'Mishawaka', 'Farmersburg', 'Evansville', 'Richmond',
    'Bluffton', 'Monticello'], key=len, reverse=True)

out = []
for c in public_rows:
    name, addr, phone = c[0], c[1], c[2]
    ids, county, cert = c[-1], c[-2], c[-3]
    assert PHONE.match(phone), (name, phone)
    name = fix_spaces(name).replace(' )', ')')
    addr = fix_spaces(addr)
    # rejoin words the PDF wraps mid-word in narrow columns
    for a, b in [('Crawfordsvil le', 'Crawfordsville'), ('Farmersbur g', 'Farmersburg'), ('Brownsburg ,', 'Brownsburg,')]:
        addr = addr.replace(a, b)
    county = county.replace('Montgomer y', 'Montgomery')
    cert = fix_spaces(cert).replace('1,2- Dibromo3Chloropr opane', '1,2-Dibromo-3-chloropropane').replace('1,2- Dibromoethane', '1,2-Dibromoethane')
    cm = re.search(r'^(.*?)\s*,?\s*IN\.?\s+(\d{5})$', addr)
    assert cm, (name, addr)
    before, zipc = cm.group(1).strip().rstrip(','), cm.group(2)
    city = next((c for c in CITIES if before.endswith(' ' + c)), None)
    assert city, (name, addr)
    street = before[: -len(city)].strip().rstrip(',')
    address = '%s, %s, IN %s' % (street, city, zipc)
    p = re.sub(r'\D', '', phone)
    if len(p) == 11 and p.startswith('1'): p = p[1:]
    phone = clean_phone(p)
    parts = [x.strip() for x in cert.split(',') if x.strip()]
    chips = key_chips(parts)
    # 'vinyl chloride' is a VOC, not the chloride ion
    if 'Chloride' in chips and not any(re.search(r'\bchloride\b', x, re.I) and not re.search(r'vinyl', x, re.I) for x in parts):
        chips.remove('Chloride')
    if any(re.search(r'\bVOCs\b', x) for x in parts) and 'Volatile organic compounds (VOCs)' not in chips:
        chips.append('Volatile organic compounds (VOCs)')
    if any(re.search(r'heterotrophic', x, re.I) for x in parts): chips.append('Heterotrophic plate count')
    if any(re.search(r'TTHM|HAA5', x) for x in parts): chips.append('Disinfection byproducts (TTHMs/HAA5s)')
    if any(re.search(r'asbestos', x, re.I) for x in parts): chips.append('Asbestos')
    ids_list = ids.split()
    detail = 'County (as printed): %s. Indiana lab ID(s): %s (M- = microbiology, C- = chemistry). Certified for (as printed): %s.' % (county, ', '.join(ids_list), cert)
    # 'Utility Services' is a company name, not a utility
    if name != 'Utility Services' and (looks_public(name) or name.startswith('Indiana Dept. of Health')):
        group = 'public'
    else:
        group = 'main'
    lab = dict(name=name, address=address, city=city, phone=phone, accredited_for=chips, detail=detail, group=group,
               source_name=SN, source_url=URL, source_date=SOURCE_DATE, last_verified=V, lab_id=' '.join(ids_list), county=county)
    if name == 'Elkhart Public Works & Utilities Laboratory':
        lab['note'] = 'The PDF prints lab ID M-20-01 for both this lab and City of Goshen Water Lab; shown as printed. Confirm with the lab.'
    if name in ('EMSL Analytical, Inc.', 'Pace Analytical Services, LLC'):
        lab['note'] = 'The PDF prints chemistry lab ID C-49-06 for both EMSL Analytical (Indianapolis) and Pace Analytical (Indianapolis); shown as printed. Confirm with the lab.'
    if name == 'Indiana Dept. of Health Laboratories':
        lab['note'] = 'IDOH also sells private-well kits directly; see the fees quoted at the top of this page (IDOH Laboratory well water page).'
    if 'Dillman' in name or name.startswith('Vanderburgh'):
        lab['note'] = (lab.get('note', '') + ' This row was transcribed by hand from the PDF because it wraps across columns or pages.').strip()
    if street.upper().startswith('PO BOX') or street.upper().startswith('P.O. BOX'):
        lab['note'] = (lab.get('note', '') + ' The list prints only a P.O. box; call for a drop-off address.').strip()
    out.append(lab)

order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))

write_state(
    'indiana', 'Indiana', 'IN', out,
    {'name': SN, 'page_url': URL, 'program_url': IDOH_CERT, 'report_date': 'List revised November 7, 2025'},
    {
        'title': 'Indiana certified drinking-water labs that accept samples from the public',
        'description': 'The 49 in-state Indiana labs on the state list of certified drinking-water labs that accept samples from the public (revised 11/7/2025), with county, lab ID, tests and the source on every listing. Plus IDOH lab well-kit fees.',
        'intro': [
            'Indiana publishes a PDF titled "Indiana Certified Drinking Water Laboratories" (revised 11/7/2025), hosted on the IDEM website and linked from the Indiana Department of Health (IDOH) drinking-water lab certification program. It splits in-state labs into "Labs that accept samples from the public" and labs that do not. This page lists all 49 labs in the first group, with the county and the tests each is certified for, as printed.',
            'IDOH also tests private wells itself. Its Laboratory well water page (checked 2026-11-06) lists, for private citizens using well water for drinking: $10.00 for bacteria, $10.00 for nitrate, $10.00 for fluoride and $20.00 for arsenic, lead and copper, not including shipping. Kits are ordered online through Access Indiana and samples go to the IDOH Laboratory, 550 W 16th St, Suite B, Indianapolis. The same page recommends testing well water every year for bacteria and nitrate, and at least every 5 years for fluoride, arsenic, lead and copper.',
            'IDOH\'s well water quality page notes that glacial deposits of arsenic and naturally occurring methane exist throughout Indiana, and recommends at minimum annual testing of private wells.',
        ],
        'caveats': [
            'The state list is dated November 7, 2025. Certifications can change. Confirm with the lab before you collect a sample.',
            '"Accepts samples from the public" is the state\'s wording. It does not tell you a lab\'s price, hours or kit process. Call first.',
            'Many labs are certified for bacteria only. If you need nitrate, arsenic, lead or other chemistry, check the tests printed on each listing.',
            'The %d in-state labs the PDF lists under "Labs that do not accept samples from the public" (mostly water utilities) are not shown.' % nopub,
            'Out-of-state labs approved for Indiana drinking water are in a separate table on the IDOH certification page (linked below); they are not transcribed here.',
            'Websites printed in the PDF are wrapped mid-word and were not checked, so they are not linked. ' + COMMON_CAVEAT_PRICES.replace(', turnaround times or websites', ' or turnaround times').replace('so none are shown', 'so none are shown except the IDOH fees quoted above'),
            'Two lab IDs are printed for two different labs each (M-20-01 for two Elkhart County labs; C-49-06 for two Indianapolis labs); all are shown as printed.',
        ],
        'main_heading': 'Commercial and independent labs that accept samples from the public',
        'public_heading': 'Utility, city and health-department labs that also accept samples from the public',
        'public_note': 'These are on the state\'s "accept samples from the public" list, but they are run by a water utility, city, county health department or IDOH. Several are bacteria only. Call for fees and hours.',
        'chips_label': 'Certified on the Indiana list for (well-relevant tests):',
        'resources': [
            {'label': 'Indiana Certified Drinking Water Laboratories (PDF, revised 11/7/2025)', 'url': URL},
            {'label': 'IDOH Laboratory: Drinking water laboratory certification (includes out-of-state lab table)', 'url': IDOH_CERT},
            {'label': 'IDOH Laboratory: Well water testing (fees and kit ordering)', 'url': IDOH_WELL},
            {'label': 'IDOH Environmental Public Health: Well water quality and testing', 'url': IDOH_EPH},
        ],
    },
)
from collections import Counter
print('groups', dict(Counter(l['group'] for l in out)), 'not-public rows', nopub)
for l in out:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', l['accredited_for'])
