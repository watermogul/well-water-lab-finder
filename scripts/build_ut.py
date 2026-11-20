"""Utah: Utah DEQ Division of Drinking Water (DDW) "Utah's Certified Laboratories - Drinking Water" (public Google Sheet linked
as "List of certified labs" from https://deq.utah.gov/ddw/lab-sampling-resources). The sheet prints no revision date.
Fetched 2026-11-19 as CSV (export?format=csv&gid=0; md5 2e68757ac50b580bcec6b3bb0062e157): 29 Utah labs + 34 out-of-state labs,
with DDW's columns "Commercial Samples?", "CMDP Certified?", "Drinking Water PFAS Certified?", TNI/EPA/state codes, phone,
address, and one TRUE/FALSE column per analyte. Replaces the thin /labs/utah/ state-guide with a full listing.
SRC_DIR must contain (all fetched 2026-11-19; not committed):
  certlabs.csv      - the DDW sheet export
  ddw.html          - DDW Lab and sampling resources page (links the sheet)
  uphl_pw.html      - Utah Public Health Laboratory (UPHL) Private Wells page (annual tests + required tests by health department)
  fees.html         - UPHL Service Fee Schedule; envchem.html - UPHL Environmental Health Laboratory Services
  csm.txt           - pdftotext of UPHL Client Services Manual (May 2025 edition)
  bacti_form.txt    - pdftotext of UPHL Water Bacteriological Analysis Test Request Form (PDF created 2026-08-03)
  davis.html, brhd.html, brhd_fees2026.txt, brhd_min.txt, swu_lab.html, swu_fees.html, seu_lab.html, seu_fees.txt,
  tricounty.html, summit.html, chemtech.html, chemtech_dw.html - local health department and lab pages (see EXTRA)
Grouping is editorial and explained on the page. The builder asserts 63 labs, so a changed sheet fails loudly."""
import os, sys, re, csv, json, html
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, key_chips, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-ut')
V = '2026-11-19'
more_lib.V = V
SHEET = 'https://docs.google.com/spreadsheets/d/1gKtMq6dn5sjj2IZM-Ba1AODTjfcNBRz_MkQ31Z6j8RY/edit#gid=0'
SN = 'Utah DEQ Division of Drinking Water: Utah\'s Certified Laboratories - Drinking Water (online sheet, no revision date printed)'
SD = V  # the sheet prints no date; source date = the day we downloaded it
DDW = 'https://deq.utah.gov/ddw/lab-sampling-resources'
MAP = 'https://experience.arcgis.com/experience/4ca0332471c0456f8cc9044c962220bd'
UPW = 'https://uphl.utah.gov/environmental-chemistry-program/env_chem_privatewells/'
UFEE = 'https://uphl.utah.gov/uphl-service-fee-schedule/'
UENV = 'https://uphl.utah.gov/environmental-chemistry-program/'
UFORMS = 'https://uphl.utah.gov/environmental-chemistry-program/Env_Chem_TestRequestForms/'
DAVIS = 'https://www.daviscountyutah.gov/health/environmental-health-division/services/environmental-health-laboratory-new'
BRHD = 'https://brhdut.gov/services/environmental/'
BRHD_FEES = 'https://www.utah.gov/pmn/files/1498709.pdf'
BRHD_MIN = 'https://www.utah.gov/pmn/files/1504063.pdf'
SWU = 'https://swuhealth.gov/water-lab/'
SWU_FEES = 'https://swuhealth.gov/fees/'
SEU = 'https://seuhealth.gov/water-lab/'
SEU_FEES = 'https://seuhealth.gov/wp-content/uploads/2025/12/Adopted-2026-EH-Fee-Schedule.pdf'
TRI = 'https://tricountyhealthut.gov/environmental_health/test_your_home.php'
SUMMIT = 'https://summitcountyhealth.org/water/'
CTF = 'https://chemtechford.com/'
CTF_DW = 'https://chemtechford.com/drinking-water/'

def flat(fn):
    t = open(os.path.join(SRC_DIR, fn), errors='ignore').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))
def raw(fn):
    return re.sub(r'\s+', ' ', open(os.path.join(SRC_DIR, fn), errors='ignore').read())

# ---- source assertions (fail loudly if a page changed) ----
ddw = flat('ddw.html')
assert 'List of certified labs' in ddw and '1gKtMq6dn5sjj2IZM-Ba1AODTjfcNBRz_MkQ31Z6j8RY' in open(os.path.join(SRC_DIR, 'ddw.html')).read()
upw = flat('uphl_pw.html')
assert 'At a minimum, well owners should have the following tests performed on an annual basis: Nitrate, pH, Total Dissolved Solids, and Total Coliforms/E.coli.' in upw
assert 'Information from official local health department resources supersedes the information presented below' in upw
fee = flat('fees.html')
for s in ['Total Coliforms/E.coli SM 9223B (Colilert/Colisure) $20.90', 'Nitrate EPA 353.2_NO3 $17.60', 'Nitrate + Nitrite EPA 353.2_NO32 $20.00',
          'pH (Test of acidity) EPA 150.1 $12.00', 'Solids, Total Dissolved (TDS) SM 2540C $14.03', 'Arsenic (As) EPA 200.8 $13.20',
          'Lead (Pb) EPA 200.8 $13.20', 'Fluoride EPA 300.0 $25.00', 'Per-and Polyfluoroalkyl Substances (PFAS) EPA 533 $505.00',
          'Digestion Fee, Per Sample (Samples with Turbidity >1 & Air Filter Samples) EPA 200.8 $24.20']:
    assert s in fee, s
assert 'Uranium' not in fee
csm = raw('csm.txt')
assert 'May 2025 Edition' in csm and 'must begin within 30 hours after collection' in csm and '801-965-2405' in csm
form = raw('bacti_form.txt')
assert 'Do Not Check Box if Private Investigative' in form and 'Not State Lab Container' in form
davis = flat('davis.html')
assert 'Well (private) Sample Fee $12' in davis and 'must be paid prior to the sample being collected and tested' in davis
assert 'rejected for coliform analysis if more 30 hours has elapsed' in davis and 'Monday –Thursday for coliform' in davis
assert 'You may bring a water sample from anywhere, including from out-of-state' in davis
brhd = flat('brhd.html')
assert '$25 Presence/Absence Bacteriological Sample $30 Quantitative Bacteriological Sample $30 Nitrate Sample' in brhd
assert '85 East 1800 North Logan' in brhd and 'Monday – Thursday 8:00 AM to 6:00 PM Friday: 8:00 AM to 1:00 PM' in brhd
bf = raw('brhd_fees2026.txt'); bm = raw('brhd_min.txt')
assert re.search(r'Coliform - eColi Quantitative 30\.00 35\.00', bf) and re.search(r'Nitrate 30\.00 35\.00', bf)
assert 'Oct 19, 2026' in bm and 'The board moved to approve the fee Schedule' in bm
swu = flat('swu_lab.html'); swuf = flat('swu_fees.html')
assert 'private drinking water systems, pools, and spas upon request' in swu and 'Nitrate Samples: Accepted on Wednesday and Thursday only' in swu
assert 'Samples are not accepted on Fridays , weekends , holidays , or the business day before a holiday' in swu
assert 'must reach the laboratory and be analyzed within 24 hours of collection' in swu and 'available at no cost' in swu
assert 'Bacteria Analysis (Drinking Water) $30 (per sample)' in swuf and 'Nitrate Testing $30 (per sample)' in swuf
seu = flat('seu_lab.html'); seuf = raw('seu_fees.txt')
assert 'Private well owners and public water systems may submit water samples to the SEUHD Water Lab' in seu
assert 'EFFECTIVE 01-01-2026' in seuf and re.search(r'WATER SAMPLES \$30\.00', seuf)
tri = flat('tricounty.html')
assert 'test the water for total coliform bacteria and E. coli for only $25 per sample' in tri and 'Monday through Wednesday from 8 a.m. to 4 pm' in tri
summ = flat('summit.html')
assert 'Individuals may test their water if they have a private well' in summ and 'drinking water safety tests starting at $27 per test' in summ
ctf = flat('chemtech.html'); ctfdw = flat('chemtech_dw.html')
assert '1384 West 130 South Orem' in ctf and 'will not be accepted on 11/24, 11/25, 12/23/ 12/24, 12/30 or 12/31' in ctf
assert 'full suite of drinking water methods' in ctfdw and 'Colilert' in ctfdw

# ---- parse the sheet ----
rows = list(csv.reader(open(os.path.join(SRC_DIR, 'certlabs.csv'), encoding='utf-8')))
H = [h.strip() for h in rows[0]]
assert H[:13] == ['Laboratory', 'Commercial Samples?', 'CMDP Certified?', 'Drinking Water PFAS Certified?', 'TNI Lab Code', 'EPA Code',
                  'State ID', 'Contact', 'Email', 'Phone #', 'Latitude', 'Longitude', 'Address'], H[:13]
recs, section = [], None
for r in rows[1:]:
    name = r[0].strip()
    if not name: continue
    if name in ('UTAH LABS', 'OUT OF STATE LABS'):
        section = name; continue
    rec = dict(zip(H, [c.strip() for c in r]))
    rec['_sec'] = section
    rec['_true'] = [H[j] for j in range(13, len(H)) if r[j].strip() == 'TRUE']
    recs.append(rec)
c0 = Counter(x['_sec'] for x in recs)
assert len(recs) == 63 and c0['UTAH LABS'] == 29 and c0['OUT OF STATE LABS'] == 34, c0

def chips(rec):
    t = [x for x in rec['_true'] if x not in ('METHOD 1633', 'Other')]
    out = [k for k in key_chips(t) if k != 'PFAS']
    if rec['Drinking Water PFAS Certified?'] == 'PFAS CERTIFIED': out.append('PFAS (DDW: "PFAS certified")')
    return out

def addr(a):
    a = re.sub(r',\s*(\d{5}(?:-\d{4})?)$', r' \1', a.strip())
    return a

def city(a):
    m = re.search(r'([A-Za-z.]+(?: [A-Za-z.]+)?),?\s*(?:UT|Utah|[A-Z]{2}|Virginia|Ontario)\b', a)
    return m.group(1) if m else ''

SHEET_FIX = {  # obvious typos in DDW's sheet, shown with the sheet's spelling in the detail line
}

# Lab or agency pages fetched 2026-11-19. Group 'main' = in Utah and either DDW marks "Commercial Samples? YES" or the
# lab's own page says it tests private-well samples.
EXTRA = {
 'Utah Department of Health Division of Lab Services (EPA cert.)': dict(group='main', order=0,
   display='Utah Public Health Laboratory (UPHL), Environmental Chemistry (listed by DDW as "Utah Department of Health Division of Lab Services (EPA cert.)")',
   address='4431 S 2700 W, Taylorsville, UT 84129 (address from UPHL\'s Client Services Manual; DDW prints "Taylorville, UT, 84119-8600")', website=UENV,
   note='The state lab. Its Private Wells page says well owners should test at least every year for nitrate, pH, total dissolved solids and total coliform/E. coli. Its posted fee schedule (no date printed): total coliform/E. coli $20.90; nitrate $17.60 (nitrate + nitrite $20.00); pH $12.00; total dissolved solids $14.03; arsenic, lead and most other metals $13.20 each (plus a $24.20 digestion fee per sample if turbidity is above 1); fluoride $25.00; PFAS (EPA 533) $505.00. Those four annual tests add up to $64.53 at the posted prices. Uranium is not on its fee schedule. Its water-bacteria form has a box for compliance samples that says "Do Not Check Box if Private Investigative", and it rejects samples that are "Not State Lab Container", so get bottles and forms from the lab first: sample receiving (801) 965-2405, Monday-Friday 8 am-5 pm (Client Services Manual, May 2025). Bacteria testing must begin within 30 hours of collection.',
   s2=(UFEE, 'UPHL Service Fee Schedule, Private Wells page and Water Bacteriological form (fetched 2026-11-19)')),
 'Davis County Environmental Health Laboratory': dict(group='main', order=1,
   address='22 S State Street, Clearfield, UT 84015', website=DAVIS,
   note='Davis County\'s lab page lists a "Well (private) Sample Fee" of $12 for coliform/E. coli, paid before the sample is collected and tested. Fill out its Water Sample for Bacteriologic Examination form, keep the sample between 34°F and 50°F, and bring it in before 3:00 pm Monday-Thursday (not the day before a legal holiday). Samples older than 30 hours are rejected. The page says you may bring a sample "from anywhere, including from out-of-state". It tests bacteria only; for nitrate or arsenic use another lab. Health department main line: (801) 525-5000.',
   s2=(DAVIS, 'Davis County Health Department: Environmental Health Laboratory page (fetched 2026-11-19)')),
 'Bear River District Health Department Water Laboratory': dict(group='main', order=1,
   address='Drop-off: Environmental Building, 85 East 1800 North, Logan, UT (DDW lists the lab at 655 E 1300 N, Logan, UT 84341)', website=BRHD,
   note='Bear River Health Department\'s page says it tests water for coliform/E. coli and nitrate: $25 presence/absence bacteria, $30 quantitative bacteria, $30 nitrate. Pick up a sterile bottle at the Environmental Health office; samples are received Monday-Thursday 8 am-6 pm and Friday 8 am-1 pm (holiday weeks differ). On October 19, 2026 its Board of Health approved a 2026 fee schedule that raises quantitative bacteria and nitrate from $30 to $35; the documents we found do not give an effective date, so confirm the price when you pick up a bottle.',
   s2=(BRHD, 'Bear River Health Department: Environmental services page (fetched 2026-11-19); 2026 fee schedule and Oct 19, 2026 board minutes on utah.gov/pmn')),
 'Southwest Utah Public Health Laboratory': dict(group='main', order=1,
   address='620 S 400 E, Suite 400, St. George, UT 84770', website=SWU,
   note='Its Water Lab page says it tests private drinking water "upon request" for coliform and E. coli (presence/absence) and nitrate. Fees: $30 per drinking-water bacteria sample, $30 per nitrate sample. Use its sterile bottles (free). Receiving: St. George Monday-Thursday 8 am-4 pm; Cedar City Tuesday 8 am-noon; Panguitch 1st Tuesday; Kanab 2nd and 4th Tuesday; Beaver 2nd Tuesday (not in November). No samples on Fridays, weekends, holidays or the business day before a holiday; nitrate only Wednesday and Thursday. Bacteria samples must arrive within 24 hours, kept below 50°F. The lab page gives (435) 986-2580; DDW lists (435) 986-2598.',
   s2=(SWU, 'Southwest Utah Public Health Department: Water Lab page and Fee Schedule (fetched 2026-11-19)')),
 'SE Utah District Health Department Laboratory': dict(group='main', order=1,
   display='Southeast Utah Health Department Water Lab (listed by DDW as "SE Utah District Health Department Laboratory")',
   address='149 E 100 S, Price, UT 84501', website=SEU,
   note='Its Water Lab page says private well owners may submit samples for coliform/E. coli (presence/absence or MPN count) and heterotrophic plate count. Its 2026 environmental health fee schedule (effective January 1, 2026) lists "Water samples" at $30. Bacteria only; call for bottles and receiving hours.',
   s2=(SEU_FEES, 'Southeast Utah Health Department: Water Lab page and Adopted 2026 EH Fee Schedule (fetched 2026-11-19)')),
 'TriCounty Health Department Environmental Laboratory': dict(group='main', order=1,
   address='133 S 500 E, Vernal, UT 84078', website=TRI,
   note='TriCounty Health\'s page says its Vernal lab tests water for total coliform and E. coli for $25 per sample, received at the Vernal office (main entrance) Monday-Wednesday 8 am-4 pm, and that it has collection bottles from the state lab for other tests. Vernal office: (435) 247-1177.',
   s2=(TRI, 'TriCounty Health Department: Test Your Home page (fetched 2026-11-19)')),
 'Summit County Health Department Laboratory': dict(group='main', order=1,
   address='85 N 50 E, Coalville, UT 84017', website=SUMMIT,
   note='Summit County\'s Water page says its in-house lab tests drinking water for bacteria, that individuals may test water from a private well, and that tests start "at $27 per test". It asks you to fill out its Water Sampling Procedure form; call (435) 336-3234 first.',
   s2=(SUMMIT, 'Summit County Health Department: Water page (fetched 2026-11-19)')),
 'Chemtech-Ford, Inc.': dict(group='main', order=2,
   address='9632 S 500 W, Sandy, UT 84070 (second location: 1384 West 130 South, Orem, UT 84058)', website=CTF,
   note='Its site describes "a full suite of drinking water methods" for regulated contaminants, metals and wet chemistry, and Colilert coliform/E. coli testing; hours Monday-Friday 8:00 am-5:30 pm in Sandy. It does not post homeowner prices or mention private wells, so call. Its home page says bacteria samples will not be accepted on 11/24, 11/25, 12/23, 12/24, 12/30 or 12/31 and that it closes 11/26-11/27, 12/25 and 1/1. DDW\'s sheet does not tick arsenic, copper or fluoride for this lab even though it ticks about 145 analytes; ask the lab what it is certified for.',
   s2=(CTF, 'Chemtech-Ford website (home and Drinking Water pages, fetched 2026-11-19)')),
}
CENTRAL_WASATCH_NOTE = 'A local health department lab. We did not find a page from this department saying it tests samples from private-well owners, and DDW marks it "Commercial Samples? NO". Call first.'

labs = []
for rec in recs:
    name = rec['Laboratory']
    ex = EXTRA.get(name, {})
    ut = rec['_sec'] == 'UTAH LABS'
    if not ut: grp = 'outofstate'
    elif 'group' in ex: grp = ex['group']
    elif rec['Commercial Samples?'] == 'YES': grp = 'main'
    else: grp = 'public'
    n_true = len([x for x in rec['_true'] if x not in ('Other',)])
    detail = ('DDW sheet: commercial samples? %s; CMDP (EPA data portal) status: %s; drinking-water PFAS: %s; codes as printed: %s, %s, state ID %s. DDW ticks %d analyte columns for this lab%s.'
              % (rec['Commercial Samples?'].lower(), rec['CMDP Certified?'], 'certified' if rec['Drinking Water PFAS Certified?'] == 'PFAS CERTIFIED' else 'not certified',
                 rec['TNI Lab Code'], rec['EPA Code'], rec['State ID'], n_true, ' plus "Other"' if 'Other' in rec['_true'] else ''))
    if 'display' in ex: detail = 'Listed by DDW as "%s". ' % name + detail
    lab = dict(name=ex.get('display', name), address=ex.get('address', addr(rec['Address'])), city=city(rec['Address']),
               phone=clean_phone(rec['Phone #']), accredited_for=chips(rec), group=grp, detail=detail,
               source_name=SN, source_url=SHEET, source_date=SD, last_verified=V)
    if 'website' in ex: lab['website'] = ex['website']
    if 'note' in ex: lab['note'] = ex['note']
    elif ut and grp == 'public' and re.search(r'Health', name): lab['note'] = CENTRAL_WASATCH_NOTE
    if 's2' in ex: lab['source_url_2'], lab['source_name_2'] = ex['s2']
    lab['_order'] = ex.get('order', 3)
    labs.append(lab)

# out-of-state data quirks, noted rather than corrected
OOS_NOTES = {
 'SGS Korea Co., Ltd.': 'DDW prints the phone as (231) 460-8036 and no coordinates; the lab is in South Korea. Not a practical option for a well owner.',
 'Natural Waters of Viti Pte Limited': 'A bottled-water plant lab in Fiji. Not a practical option for a well owner.',
 'Andrew W. Breidenbach Environmental Research Center (AWBERC)': 'A U.S. EPA research center. DDW prints its codes as "XXXXX" and ticks no analytes.',
}
for l in labs:
    for k, v in OOS_NOTES.items():
        if l['name'] == k: l['note'] = v

def rank(l):
    a = l['accredited_for']
    return (-('Total coliform' in a), -('Nitrate' in a), -len(a), l['name'])
main = sorted([l for l in labs if l['group'] == 'main'], key=lambda l: (l['_order'], l['name']))
pub = sorted([l for l in labs if l['group'] == 'public'], key=lambda l: l['name'])
oos = sorted([l for l in labs if l['group'] == 'outofstate'], key=rank)
labs = main + pub + oos
N_NO3 = sum(1 for l in labs if l['group'] != 'outofstate' and 'Nitrate' in l['accredited_for'])
assert N_NO3 == 13, N_NO3
for l in labs: l.pop('_order')
c = Counter(l['group'] for l in labs)
print(c)
assert len(labs) == 63 and c['main'] == 11 and c['public'] == 18 and c['outofstate'] == 34, c

write_state('utah', 'Utah', 'UT', labs,
    {'name': SN, 'page_url': DDW, 'program_url': UPW,
     'report_date': 'online sheet, no revision date printed; downloaded November 19, 2026'},
    {
     'title': 'Utah certified labs for well water testing (all 63 on DDW\'s list, Nov 2026)',
     'description': 'All 63 labs on Utah DDW\'s certified drinking-water lab list, which ones take outside samples, what each is certified for, and posted well-water test prices from the state lab and six county and district health department labs.',
     'intro': [
      'Utah\'s Division of Drinking Water (DDW, part of Utah DEQ) links a "List of certified labs" from its Lab and sampling resources page. It is an online spreadsheet with no revision date. We downloaded it on November 19, 2026. It has 63 labs: 29 in Utah and 34 out of state. For each lab DDW shows whether it takes "Commercial Samples", whether it is PFAS-certified for drinking water, its phone and address, and a tick box for each certified analyte.',
      'For most well owners the useful labs are the state lab and the local health department labs. The Utah Public Health Laboratory (UPHL) in Taylorsville posts its prices: $20.90 for coliform/E. coli, $17.60 for nitrate, $12.00 for pH and $14.03 for total dissolved solids, and $13.20 per metal such as arsenic or lead. Six local health department labs on DDW\'s list post well-water bacteria tests from $12 (Davis County) to $30 (Southwest Utah, Southeast Utah). Bear River and Southwest Utah also test nitrate ($30).',
      'UPHL\'s Private Wells page says the EPA does not regulate private wells and that well owners should test at least every year for nitrate, pH, total dissolved solids and total coliform/E. coli. It also lists the tests each local health department requires or recommends for individual wells. Several (Salt Lake, Tooele, TriCounty, Utah County, Weber-Morgan) list arsenic and other metals; others require nothing. UPHL says official local health department information takes precedence over its table, so check with your county before a home sale or building permit.',
      'DDW ticks nitrate for %d of the 29 Utah labs, but only some of those take outside samples. Only two Utah labs are marked PFAS-certified for drinking water: UPHL and Chemtech-Ford.' % N_NO3,
     ],
     'caveats': [
      'DDW\'s list is for labs that test public water systems. "Commercial Samples?" is DDW\'s column; it does not define it. Several health department labs marked "NO" say on their own sites that they test private-well samples, so we list them first with their posted prices.',
      'The analyte tick boxes are DDW\'s and look incomplete for some labs (for example, Chemtech-Ford is not ticked for arsenic). Treat a missing tick as "ask", not "no". Chips on each card show only well-relevant analytes that DDW ticked.',
      'Most health department labs test bacteria only. For nitrate, arsenic or a full panel, use UPHL, a lab ticked for those tests, or ask your health department which lab it uses.',
      'Bacteria samples are time-limited: Southwest Utah requires arrival within 24 hours; Davis County rejects coliform samples older than 30 hours, and UPHL must start testing within 30 hours. Keep samples cold, and use the lab\'s own sterile bottle.',
      'Prices come only from each lab\'s or health department\'s own page or fee schedule, with the date we checked. Bear River\'s board approved $5 increases to two lab fees on October 19, 2026; its web page still shows the old prices.',
      'Addresses and phones are as printed by DDW unless the card says otherwise. Where a health department\'s own page gives a different drop-off address or phone, the card shows both.',
      'The grouping is ours. The first group is Utah labs that DDW marks as taking commercial samples or whose own pages say they take private-well samples. The second is the other Utah labs (city, water district, sewer district, industrial and two health department labs). Out-of-state labs are last, with bacteria and nitrate labs first.',
     ],
     'main_heading': 'Utah labs that take samples from the public: state lab, health departments and commercial labs',
     'public_heading': 'Other Utah labs on DDW\'s list (water utilities, districts, industry)',
     'public_note': 'DDW marks all of these "Commercial Samples? NO". Most test water for a city, water district, sewer district or company. Two are local health department labs (Central Utah, Wasatch County) that may help residents; call first.',
     'oos_heading': 'Out-of-state labs on DDW\'s list',
     'oos_note': [
      'DDW also lists 34 labs outside Utah. Most serve water utilities or do specialty tests such as radiochemistry, PFAS or asbestos. Labs with bacteria and nitrate ticks are listed first.',
      'Bacteria samples usually must reach a lab within about a day, so out-of-state labs are mostly useful for chemistry. Ask each lab how to ship samples.',
     ],
     'chips_label': 'Well-relevant analytes ticked on DDW\'s sheet:',
     'resources': [
      {'label': 'Utah DDW: Utah\'s Certified Laboratories - Drinking Water (online sheet)', 'url': SHEET},
      {'label': 'Utah DEQ Division of Drinking Water: Lab and sampling resources', 'url': DDW},
      {'label': 'Utah DDW: map of certified lab locations', 'url': MAP},
      {'label': 'Utah Public Health Laboratory: Private Wells (annual tests; tests by health department)', 'url': UPW},
      {'label': 'Utah Public Health Laboratory: Service Fee Schedule', 'url': UFEE},
      {'label': 'Utah Public Health Laboratory: Test Request Forms', 'url': UFORMS},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('utah', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed utah from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'][:60], '|', l['address'][:60], '|', l['phone'], '|', '; '.join(l['accredited_for']))
