"""Iowa: Iowa DNR LabCert "List of Certified Labs" (programs.iowadnr.gov/labcert/Home/LabListing, page shows
"Date Generated" = the fetch date), fetched 2026-11-07. Only labs whose Program column includes "Drinking Water" are
listed. Certification period/status come from each lab's LabCert "Lab Details" page; the well-test chips come from the
LabCert public analyte search run with Program = Drinking Water for six analytes (total coliform, E. coli, nitrate,
arsenic, manganese, lead). Raw files are in $SRC_DIR (not committed):
  e4d99e.html (LabListing), details.json (+ d_<lab#>.html), analytes.json (+ s_<analyte>.html).
Nothing is inferred: grouping uses the DNR "Lab Type" column and the printed state."""
import os, sys, re, json, html
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-ia')
LIST_URL = 'https://programs.iowadnr.gov/labcert/Home/LabListing'
SEARCH_URL = 'https://programs.iowadnr.gov/labcert/Home/PublicSearch'
DETAIL_URL = 'https://programs.iowadnr.gov/labcert/Home/LabDetails/'
DNR_WELL = 'https://www.iowadnr.gov/environmental-protection/water-quality/private-well-program/well-testing'
PWG_GUIDE = 'https://www.iowadnr.gov/media/4621/download?inline'
HHS_PWG = 'https://hhs.iowa.gov/health-prevention/environmental-health/private-well-grants'
SHL_PW = 'https://shl.uiowa.edu/environmental-testing/private-well-water'
COUNTY_SHEET = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSN9_vM3stj69X3-4qojMfxrkIGuP4dkCfZYo1DI9g8FSyJrs4SbfRYuDRPulMxStPClHPxdB1io1GR/pubhtml'
SN = 'Iowa DNR LabCert: List of Certified Labs (Drinking Water program)'
V = '2026-11-07'
SOURCE_DATE = '2026-11-07'  # the LabCert list is generated live; the page printed "Date Generated: 11/7/2026"
more_lib.V = V

raw = open(os.path.join(SRC_DIR, 'e4d99e.html'), encoding='utf-8').read()
assert 'Date Generated: 11/7/2026' in raw
tb = raw[raw.find('<table'):raw.rfind('</table>')]
rows = []
for r in re.findall(r'<tr[^>]*>(.*?)</tr>', tb, flags=re.S):
    cells = re.findall(r'<td[^>]*>(.*?)</td>', r, flags=re.S)
    if not cells: continue
    cells = [html.unescape(html.unescape(re.sub(r'<[^>]+>', ' ', c))).strip() for c in cells]
    rows.append(cells)
total_listed = len(rows)
dw = [c for c in rows if 'Drinking Water' in c[5]]
det = json.load(open(os.path.join(SRC_DIR, 'details.json')))
an = json.load(open(os.path.join(SRC_DIR, 'analytes.json')))
assert len(dw) == len(det) == 58, (len(dw), len(det))
CHIP = [('tc', 'Total coliform'), ('ecoli', 'E. coli'), ('nitrate', 'Nitrate'), ('arsenic', 'Arsenic'), ('manganese', 'Manganese'), ('lead', 'Lead')]
PERIOD = re.compile(r'^(\w+ \d\d, \d{4}) to (\w+ \d\d, \d{4})$')
from datetime import datetime

out = []
for typ, name, num, addr, phone, programs in dw:
    parts = [p for p in re.split(r'\s{2,}', addr) if p]
    assert len(parts) == 4, (name, addr)
    street, city, st, zipc = parts
    d = det[num]
    a2 = d.get('addr2')
    address = '%s%s, %s, %s %s' % (street, (', ' + a2) if a2 and a2 != 'N/A' else '', city, st, zipc)
    name = re.sub(r'\s+', ' ', name).replace(' -Cinnaminson', ' - Cinnaminson')
    chips = [lab for k, lab in CHIP if num in an[k]]
    (period, status, progs), = d['certs']
    pm = PERIOD.match(period); assert pm, period
    end = datetime.strptime(pm.group(2), '%B %d, %Y').date()
    start = datetime.strptime(pm.group(1), '%B %d, %Y').date()
    detail = 'Iowa DNR lab number %s. Lab type (as listed): %s. Certification period: %s. Status: %s. Programs: %s.' % (
        num, typ, period, status, re.sub(r'\s*,\s*', ', ', programs).strip(' ,'))
    notes = []
    if status != 'Certified':
        notes.append('DNR shows this lab\'s status as "%s", not "Certified". Ask the lab what that means for your tests.' % status)
    if end < datetime(2026, 11, 7).date():
        notes.append('The certification period shown on the DNR record ended %s, but the record still shows status "%s" on %s. Confirm current certification with the lab or DNR.' % (pm.group(2), status, V))
    if start > datetime(2026, 11, 7).date():
        notes.append('The DNR record shows a certification period that starts %s (after the date we checked). Shown as printed.' % pm.group(1))
    if num == '419':
        notes.append('ZIP code shown as printed by DNR (80779); it does not look like a New Jersey ZIP. Confirm the address with the lab.')
    if num == '096':
        notes.append('Street line shown as printed by DNR ("Water Pollution Control", then 7525 Berthram Rd SE).')
    if a2 and re.match(r'(?i)p\.?o\.? box', a2):
        notes.append('The DNR record includes a P.O. box; call for a drop-off address.')
    if not chips:
        notes.append('Not returned by the DNR drinking-water search for any of the six common well tests we checked (coliform, E. coli, nitrate, arsenic, manganese, lead). It may be certified for other drinking-water tests.')
    if st != 'IA':
        group = 'limited'
    elif typ == 'Commercial':
        group = 'main'
    else:
        group = 'public'
    if name.startswith('State Hygienic Laboratory'):
        notes.append('The State Hygienic Laboratory at the University of Iowa runs a private-well testing service; see its Private Well Water page (linked under Official sources).')
    lab = dict(name=name, address=address, city=city, phone=clean_phone(phone), accredited_for=chips, detail=detail, group=group,
               source_name=SN, source_url=LIST_URL, source_date=SOURCE_DATE, last_verified=V, lab_id=num,
               source_url_2=DETAIL_URL + d['detail_id'], source_name_2='DNR lab details record')
    if notes: lab['note'] = ' '.join(notes)
    out.append(lab)

order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))
from collections import Counter
c = Counter(l['group'] for l in out)

write_state(
    'iowa', 'Iowa', 'IA', out,
    {'name': SN, 'page_url': LIST_URL, 'program_url': SEARCH_URL, 'report_date': 'Live DNR list, generated November 7, 2026'},
    {
        'title': 'Iowa certified drinking-water labs for private well testing (Iowa DNR list)',
        'description': 'All %d labs Iowa DNR certifies for drinking water (DNR LabCert list generated 11/7/2026), with lab number, certification period, which common well tests each is certified for, and how to get free testing through your county.' % len(out),
        'intro': [
            'Iowa DNR keeps its lab certification list in an online system called LabCert. On November 7, 2026 its "List of Certified Labs" showed %d labs; %d of them hold the Drinking Water program, and those are the labs listed here. Iowa DNR\'s Well Testing page says all water testing should be done by DNR certified drinking water laboratories.' % (total_listed, len(out)),
            'For each lab we also opened its DNR "Lab Details" record (certification period and status) and ran the DNR public search with Program set to Drinking Water for six common well tests: total coliform, E. coli, nitrate, arsenic, manganese and lead. The chips on each listing show which of those six the DNR search returned for that lab. A lab may be certified for other tests too; the DNR search is the full record.',
            'Free testing first: Iowa DNR\'s Well Testing page (page metadata updated 2026-02-04) says the Private Well Grants program provides free water testing to private well owners and users for bacteria (E. coli/coliform) and nitrate, recommended every year, and arsenic and manganese, recommended every 3 years. You arrange it through your county environmental health office (DNR links a county contact list). The DNR\'s guidance for counties (updated July 8, 2026) says the county health specialist must collect the samples, and homeowners cannot be reimbursed for sampling they did themselves. Iowa HHS, which administers the grants, says to contact your local environmental public health office to see if your county participates.',
            'The State Hygienic Laboratory at the University of Iowa says on its Private Well Water page that Iowa residents may be able to get well water tested at no cost through the Private Well Grants program, and recommends testing for total coliform bacteria, E. coli and nitrate every year, and for arsenic and manganese at least once during the life of the well. (DNR\'s page says every 3 years for arsenic and manganese; both are quoted as written.) DNR\'s page also says PFAS testing requires pre-approval from DNR.',
        ],
        'caveats': [
            'The DNR list is live and changes. We copied it on November 7, 2026. Confirm certification with the lab, or in the DNR search, before you collect a sample.',
            'Being certified for drinking water does not mean a lab takes samples from homeowners. Neither the DNR list nor the lab records say which labs do. Call first and ask about kits, fees and drop-off hours.',
            'Groups are based only on the "Lab Type" column DNR prints (Commercial, Government, Public, Industrial/Private) and the lab\'s state. Out-of-state labs certified by Iowa DNR are listed last.',
            'The six-test chips come from the DNR search on November 7, 2026. If a chip is missing, the DNR search did not return that lab for that test under the Drinking Water program.',
            'One record shows a certification period that ended October 1, 2026 while still marked "Certified", one shows a period that starts December 1, 2026, and three are marked "Provisional". These are noted on the listings.',
            'Websites appear on only a few DNR records and were not checked, so none are linked. We did not verify prices or turnaround times for any lab, so none are shown.',
            'The %d labs on the DNR list without the Drinking Water program (wastewater, sludge, contaminated-site and underground tank programs only) are not shown.' % (total_listed - len(out)),
        ],
        'main_heading': 'Commercial labs in Iowa certified for drinking water',
        'public_heading': 'Government, utility, health-department and other Iowa labs certified for drinking water',
        'public_note': 'DNR lists these as Government, Public or Industrial/Private labs. Several are city water or wastewater labs, county health departments, or the State Hygienic Laboratory. The source does not say whether each takes homeowner samples. Call first.',
        'limited_heading': 'Out-of-state labs certified by Iowa DNR for drinking water',
        'limited_note': 'These labs are outside Iowa but hold Iowa DNR drinking-water certification. Most are large commercial labs. Ask about shipping and sample hold times before you collect.',
        'chips_label': 'DNR search (Drinking Water program) returns this lab for:',
        'resources': [
            {'label': 'Iowa DNR LabCert: List of Certified Labs (live, generated 11/7/2026 when checked)', 'url': LIST_URL},
            {'label': 'Iowa DNR LabCert: public lab and analyte search', 'url': SEARCH_URL},
            {'label': 'Iowa DNR: Well Testing (Private Well Grants testing, what to test)', 'url': DNR_WELL},
            {'label': 'Iowa DNR: Private Well Grants guidance on qualifying expenses (PDF, updated July 8, 2026)', 'url': PWG_GUIDE},
            {'label': 'Iowa DNR: county environmental health contacts (Google Sheet linked from the DNR Well Testing page)', 'url': COUNTY_SHEET},
            {'label': 'Iowa HHS: Private Well Grants Program', 'url': HHS_PWG},
            {'label': 'State Hygienic Laboratory at the University of Iowa: Private Well Water', 'url': SHL_PW},
        ],
    })
print(dict(c))
