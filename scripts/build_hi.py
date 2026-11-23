"""Hawaii: Hawaii DOH State Laboratories Division (SLD), Drinking Water Certification Program. Since mid-2026 the Safe Drinking Water
Branch's "Certified / Approved Drinking Water Labs" PDF (https://health.hawaii.gov/sdwb/files/2026/07/Certified-Labs.pdf, created
2026-07-23) is a one-page pointer to two SLD lists, which are re-uploaded in place under a 2026/03 path:
  chem:  https://health.hawaii.gov/statelab/files/2026/03/sld-hm-certified-labs-chem.pdf  (headed "November 16th, 2026"; PDF created
         2026-11-17; md5 0f5549c2820f56aa2946ee8fb153c60b; 13 labs x ~210 analyte rows matrix)
  micro: https://health.hawaii.gov/statelab/files/2026/03/sld-hm-certified_labs_micro.pdf (undated; PDF created 2026-11-18;
         md5 0d934ffe3b27f99ad443a521b18a3b37; 10 labs)
Both fetched 2026-11-22. Tables were extracted with pdfplumber into SRC_DIR/chem_rows.json and micro_rows.json (see extract step in the
Extract note below); this builder reads those JSON files and asserts the PDF md5s.
Chem chips are computed from the analyte rows where a lab's cell is non-empty (methods as printed). Replaces the thin /labs/hawaii/
state-guide. Contact info for county/DOH labs is not on the micro list; it comes from DOH's previous directory (revision Nov 20, 2025,
https://health.hawaii.gov/sdwb/files/2025/12/Certified_Labs_202512.pdf, still hosted, fetched 2026-11-22) and SLD district-lab pages.

Extract (needs pdfplumber, e.g. /workspace/plumbvenv):
  for each page: page.extract_tables() -> rows of cells with newlines replaced by spaces -> json."""
import os, sys, re, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-hi')
V = '2026-11-22'
more_lib.V = V
SDWB_LIST = 'https://health.hawaii.gov/sdwb/files/2026/07/Certified-Labs.pdf'
CHEM = 'https://health.hawaii.gov/statelab/files/2026/03/sld-hm-certified-labs-chem.pdf'
MICRO = 'https://health.hawaii.gov/statelab/files/2026/03/sld-hm-certified_labs_micro.pdf'
OLD = 'https://health.hawaii.gov/sdwb/files/2025/12/Certified_Labs_202512.pdf'
DWCP = 'https://health.hawaii.gov/statelab/dwcp/'
PRIV = 'https://health.hawaii.gov/sdwb/files/2024/10/PrivateWaterWells_rev2024-10-21.pdf'
RAIN = 'https://health.hawaii.gov/sdwb/raincatchment/'
GWV = 'https://health.hawaii.gov/sdwb/groundwater-contamination-viewer/'
SDWB = 'https://health.hawaii.gov/sdwb/'
AECOS = 'https://www.aecos.com/AECOS_Laboratory.html'
FQ = 'https://fqlabs.com/'
FQFAQ = 'https://fqlabs.com/faqs/'
KDHL = 'https://health.hawaii.gov/statelab/kauai-district-health-laboratory/'
MDHL = 'https://health.hawaii.gov/statelab/maui-district-health-laboratory/'
HDHL = 'https://health.hawaii.gov/statelab/hawaii-district-health-laboratory/'

SN_CHEM = 'Hawaii DOH State Laboratories Division: Certified Chemistry & Radiochemistry Drinking Water Labs (PDF headed November 16, 2026)'
SN_MICRO = 'Hawaii DOH State Laboratories Division: Drinking Water Microbiology Laboratories Certified by the Hawaii Department of Health (PDF, undated; file created November 18, 2026)'
SD_CHEM = '2026-11-16'
SD_MICRO = '2026-11-18'

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()
assert md5(os.path.join(SRC_DIR, 'sld-hm-certified-labs-chem.pdf')) == '0f5549c2820f56aa2946ee8fb153c60b', 'chem list changed: re-extract'
assert md5(os.path.join(SRC_DIR, 'sld-hm-certified_labs_micro.pdf')) == '0d934ffe3b27f99ad443a521b18a3b37', 'micro list changed: re-extract'

R = json.load(open(os.path.join(SRC_DIR, 'chem_rows.json')))
M = json.load(open(os.path.join(SRC_DIR, 'micro_rows.json')))

# ---------- chemistry matrix ----------
hdr = {r[0].split(' ')[0]: r for r in R[2:7]}
names, addrs, phones, eff, exp = R[2][2:], R[3][2:], R[4][2:], R[5][2:], R[6][2:]
assert len(names) == 13 and R[2][0] == 'Laboratory Name' and R[4][0] == 'Phone'
analytes = [r for r in R[7:] if r[1] and r[1] != 'KEY:' and 'Analytes' not in r[1] and 'has not expired' not in r[1]]
assert len(analytes) == 210, len(analytes)

KEYS = [  # (chip label, regex on analyte row name)
 ('Nitrate', r'^Nitrate$'), ('Nitrite', r'^Nitrite$'), ('Arsenic', r'^Arsenic$'), ('Lead', r'^Lead$'), ('Copper', r'^Copper$'),
 ('Fluoride', r'^Fluoride$'), ('Iron', r'^Iron$'), ('Manganese', r'^Manganese$'), ('Sodium', r'^Sodium$'), ('Chloride', r'^Chloride$'),
 ('Sulfate', r'^Sulfate$'), ('Hardness', r'^Hardness'), ('pH', r'^pH$'), ('Total dissolved solids', r'Total Dissolved Solids'),
 ('Turbidity', r'^Turbidity$'), ('Uranium', r'^Uranium$'), ('Gross alpha', r'^Gross Alpha$'), ('Radium', r'^Radium'), ('Radon', r'^Radon'),
 ('Volatile organic compounds (VOCs)', r'^Regulated Volatile Organic Compounds$'),
 ('Pesticides / herbicides', r'^(Atrazine|Alachlor|Simazine|2,4-D|Glyphosate|Chlordane|Metolachlor|Aldicarb|Carbofuran|Dalapon|Picloram|Endothall|Diquat)$'),
 ('1,2,3-TCP', r'1,2,3-Trichloropropane'), ('DBCP / EDB (soil fumigants)', r'\((DBCP|EDB)\)'),
 ('PFAS', r'Perfluoro|perfluoro|HFPO|ADONA|FTS\)|FOSAA'),
 ('Asbestos', r'^Asbestos$'),
]
chem = {}
for ci, nm in enumerate(names):
    have = [a[1] for a in analytes if a[2 + ci]]
    chips = [lab for lab, rx in KEYS if any(re.search(rx, h) for h in have)]
    chem[nm] = dict(n=len(have), chips=chips, have=have, addr=addrs[ci], phone=phones[ci], eff=eff[ci], exp=exp[ci])

def short(s): return re.sub(r'\s+', ' ', s).strip()

# Hand-entered display names / cities for the 13 chem columns (names as printed are kept in `listed`).
CH = [
 ('BSK Associates', 'BSK Associates (Fresno, CA)', 'Fresno', '687 North Laverne Avenue, Fresno, CA 93727'),
 ('EMSL Analytical, Inc. - Cinnaminson, New Jersey', 'EMSL Analytical (Cinnaminson, NJ)', 'Cinnaminson', '200 Route 130 North, Cinnaminson, NJ 08077'),
 ('Enthalpy Analytical, Orange, CA', 'Enthalpy Analytical (Orange, CA)', 'Orange', '931 West Barkley Avenue, Orange, CA 92868'),
 ('Eurofins Built Env. Testing East (Eurofins CEI, Inc)', 'Eurofins Built Environment Testing East (Cary, NC)', 'Cary', '730 SE Maynard Road, Cary, NC 27511'),
 ('Eurofins Drinking Water and Wastewater West, LLC - Pomona, CA (formerly Eurofins Eaton Anaytical)', 'Eurofins Drinking Water and Wastewater West (Pomona, CA)', 'Pomona', '941 Corporate Center Drive, Pomona, CA 91768'),
 ('Eurofins South Bend (aka Eurofins Drinking Water and Wastewater Central, LLC - South Bend, IN)', 'Eurofins South Bend (South Bend, IN)', 'South Bend', '110 South Hill Street, South Bend, IN 46617'),
 ('Eurofins St. Louis, MO', 'Eurofins St. Louis (Earth City, MO)', 'Earth City', '13715 Rider Trail North, Earth City, MO 63045'),
 ('GEL Laboratories, LLC', 'GEL Laboratories (Charleston, SC)', 'Charleston', '2040 Savage Road, Charleston, SC 29407'),
 ('Pace Analytical Services, LLC – Greensburg PA', 'Pace Analytical (Greensburg, PA)', 'Greensburg', '1638 Roseytown Rd, Suites 2, 3, & 4, Greensburg, PA 15601'),
 ('Pace Analytical Services, LLC – Ormond Beach, Fl', 'Pace Analytical (Ormond Beach, FL)', 'Ormond Beach', '8 East Tower Circle, Ormond Beach, FL 32174'),
 ('SGS North America Inc. - Orlando, FL', 'SGS North America (Orlando, FL)', 'Orlando', '4405 Vineland Road, Suite C-15, Orlando, FL 32811'),
 ('SGS North America Inc. - Wheat Ridge, CO', 'SGS North America (Wheat Ridge, CO)', 'Wheat Ridge', '4036 Youngfield Street, Wheat Ridge, CO 80033'),
 ('Weck Laboratories, Inc.', 'Weck Laboratories (City of Industry, CA)', 'City of Industry', '14859 Clark Avenue, City of Industry, CA 91745-1396'),
]
assert [c[0] for c in CH] == names, names
for (listed, disp, city, addr), nm in zip(CH, names):
    # every street number in our address must be in the printed cell
    assert addr.split(' ')[0] in chem[nm]['addr'], (addr, chem[nm]['addr'])

def exp_text(e):
    e = short(e).replace('Etended', 'Extended')
    return e

# ---------- micro list ----------
assert M[0][0] == 'Laboratory' and len(M) == 11
micro = {}
for r in M[1:]:
    micro[r[0]] = dict(contact=r[1], exp=r[2], hpc=r[3], tc=r[4], fc=r[5], ec=r[6], ent=r[7], typ=r[8])
def micro_detail(key):
    m = micro[key]
    parts = ['DOH microbiology list (as printed): certification type "%s", expires %s' % (m['typ'], m['exp'])]
    tc = m['tc'].rstrip(', ')
    parts.append('total coliforms by ' + tc)
    if m['ec']: parts.append('E. coli by ' + m['ec'].rstrip(', '))
    if m['hpc']: parts.append('heterotrophic bacteria by ' + m['hpc'])
    if m['fc']: parts.append('fecal coliforms by ' + m['fc'])
    if m['ent']: parts.append('enterococci by ' + m['ent'])
    return '; '.join(parts) + '.'

MICRO_CHIPS = ['Total coliform', 'E. coli']
labs = []

def base(name, address, city, phone, chips, detail, group, sn, su, sd):
    return dict(name=name, address=address, city=city, phone=clean_phone(phone) if phone else None, accredited_for=chips,
                detail=detail, group=group, source_name=sn, source_url=su, source_date=sd, last_verified=V)

# main: in-state commercial labs
l = base('AECOS Laboratory', '45-939 Kamehameha Highway, Suite 104, Kaneohe, HI 96744', 'Kaneohe', '(808) 234-7770', MICRO_CHIPS,
         micro_detail('AECOS, Inc. - Kaneohe, HI') + ' Listed as "AECOS, Inc. - Kaneohe, HI". Not on the November 2026 chemistry list.',
         'main', SN_MICRO, MICRO, SD_MICRO)
l.update(website=AECOS, source_url_2=RAIN, source_name_2='Hawaii DOH Safe Drinking Water Branch: Rainwater Catchment page (last update July 23, 2026) and AECOS Laboratory page (fetched 2026-11-22)',
         note='AECOS says its lab does "soil, water quality, and drinking water analyses." DOH\'s previous lab directory (revision November 20, 2025) listed AECOS under "In-state Laboratories (accepts private samples)". DOH\'s Rainwater Catchment page says DOH subsidizes one lead and copper test per year for homes on rainwater catchment: the owner pays shipping and $25.00, DOH pays the rest, and "AECOS Laboratory, Inc. is currently the only lab approved by DOH, and is participating in this program." AECOS does not post prices for other tests; call for bacteria, nitrate or other tests and ask which ones it is certified for.')
labs.append(l)
l = base('FQLabs', '3170-A Ualena Street, Honolulu, HI 96819', 'Honolulu', '(808) 839-9444', MICRO_CHIPS,
         micro_detail('FQLabs - Honolulu, HI') + ' Not on the November 2026 chemistry list.', 'main', SN_MICRO, MICRO, SD_MICRO)
l.update(website=FQ, source_url_2=FQFAQ, source_name_2='FQLabs home page and FAQs (fetched 2026-11-22)',
         note='DOH lists FQLabs\' drinking-water microbiology certification as "Provisional", for one method (Colilert presence/absence). DOH\'s previous directory (November 20, 2025) listed FQ Labs under "accepts private samples". FQLabs says it offers "microbiological and chemical testing of food, drinking water, wastewater, sludge and soil," lists hours of Monday to Friday, 8:30 a.m. to 5:00 p.m., and says customers on the outer islands get sample kits shipped "using airline cargo regularly"; call for shipping instructions. No prices posted.')
labs.append(l)

# public: county water departments and DOH district labs (micro only)
OLDN = 'Contact details from DOH\'s previous lab directory (revision November 20, 2025), which listed this lab under "In-state Laboratories (does not accept private samples)".'
PUB = [
 ('County of Hawaiʻi, Department of Water Supply', 'Hawaiʻi County Department of Water Supply lab', '889 Leilani Street, Hilo, HI 96720', 'Hilo', '(808) 961-8670', OLDN, OLD, 'DOH Safe Drinking Water Branch: previous lab directory (revision November 20, 2025; still hosted)'),
 ('County of Honolulu, Honolulu Board of Water Supply', 'Honolulu Board of Water Supply lab', '630 South Beretania Street, Honolulu, HI 96843', 'Honolulu', '(808) 748-5841', OLDN + ' That directory printed (808) 748-5840 for the chemistry lab and (808) 748-5841 for the micro lab.', OLD, 'DOH Safe Drinking Water Branch: previous lab directory (revision November 20, 2025; still hosted)'),
 ('County of Kauaʻi, Department of Water', 'Kauaʻi County Department of Water lab', '4398 Pua Loke Street, Lihue, HI 96766', 'Lihue', '(808) 245-5400', OLDN, OLD, 'DOH Safe Drinking Water Branch: previous lab directory (revision November 20, 2025; still hosted)'),
 ('County of Maui, Department of Water Supply', 'Maui County Department of Water Supply lab', '614 Palapala Drive, Kahului, HI 96732', 'Kahului', '(808) 270-7816', OLDN, OLD, 'DOH Safe Drinking Water Branch: previous lab directory (revision November 20, 2025; still hosted)'),
 ('DOH Hawaiʻi District Health Laboratory', 'DOH Hawaiʻi District Health Laboratory', 'Hawaiʻi Island (address not printed on the DOH list)', 'Hawaii Island', None, 'DOH\'s page says this lab "provides diagnostic, regulatory and consultative laboratory services to private laboratories, private purveyors and various Federal, State and County agencies" and lists fecal indicators (total and fecal coliforms, E. coli) among its tests. It does not say it takes homeowner samples, and the page prints no phone number.', HDHL, 'Hawaii DOH State Laboratories Division: Hawaii District Health Laboratory page (fetched 2026-11-22)'),
 ('DOH Kauaʻi District Health Laboratory', 'DOH Kauaʻi District Health Laboratory', 'Kauaʻi (address not printed on the DOH list)', 'Kauai', '(808) 241-3353', 'DOH\'s page says this lab supports Department of Health programs and "does testing to monitor drinking water and recreational waters." It does not say it takes homeowner samples. Phone from that page.', KDHL, 'Hawaii DOH State Laboratories Division: Kauai District Health Laboratory page (fetched 2026-11-22)'),
 ('DOH Maui District Health Laboratory', 'DOH Maui District Health Laboratory', 'Maui (address not printed on the DOH list)', 'Maui', '(808) 984-2131', 'DOH\'s page says this lab "provides laboratory support services to various medical and environmental programs within the Department of Health" and tests "for regulatory purposes." It does not say it takes homeowner samples. Phone from that page.', MDHL, 'Hawaii DOH State Laboratories Division: Maui District Health Laboratory page (fetched 2026-11-22)'),
]
for key, disp, addr, city, ph, note, s2, s2n in PUB:
    assert key in micro, key
    d = micro_detail(key)
    if disp != key: d += ' Listed as "%s".' % key
    l = base(disp, addr, city, ph, MICRO_CHIPS, d, 'public', SN_MICRO, MICRO, SD_MICRO)
    l.update(note=note, source_url_2=s2, source_name_2=s2n)
    labs.append(l)

# out-of-state: chemistry list (Eurofins Pomona also on micro list)
OOS = ('Out-of-state lab approved by Hawaii DOH for drinking-water chemistry. DOH does not say whether it accepts homeowner samples or ships bottles to Hawaii; '
       'we did not verify prices, hold times or homeowner service. Ask about bottles and shipping before collecting a sample.')
for (listed, disp, city, addr), nm in zip(CH, names):
    c = chem[nm]
    d = 'Hawaii DOH chemistry list (as printed): effective date of certification %s; certification expiration date %s. Certified for %d of the %d analyte rows on the list.' % (short(c['eff']), exp_text(c['exp']), c['n'], len(analytes))
    if listed != disp: d += ' Listed as "%s".' % short(listed)
    if nm == 'Eurofins St. Louis, MO':
        d += ' DOH prints a (330) area-code phone for this Missouri address; we did not check it against the lab\'s own site.'
    if 'Extended' in exp_text(c['exp']):
        d += ' The printed expiration date has passed, but DOH marks it "extended until renewal" and shades it as "Certification has not expired".'
    chips = list(c['chips'])
    l = base(disp, addr, city, c['phone'], chips, d, 'outofstate', SN_CHEM, CHEM, SD_CHEM)
    l['note'] = OOS
    if nm.startswith('Eurofins Drinking Water and Wastewater West'):
        key = 'Eurofins Eaton Analytical, LLC - Pomona, CA'
        l['accredited_for'] = MICRO_CHIPS + chips
        l['detail'] += ' Also on the microbiology list as "%s": %s' % (key, micro_detail(key))
        l['source_url_2'], l['source_name_2'] = MICRO, SN_MICRO
        l['note'] = OOS + ' Bacteria samples have short hold times (see our sampling guide), so shipping one from Hawaii to California may not work; ask the lab first.'
    labs.append(l)

from collections import Counter
assert Counter(l['group'] for l in labs) == Counter({'main': 2, 'public': 7, 'outofstate': 13})
nit = [l['name'] for l in labs if 'Nitrate' in l['accredited_for']]
ars = [l['name'] for l in labs if 'Arsenic' in l['accredited_for']]
print('nitrate:', len(nit), nit); print('arsenic:', len(ars))

write_state('hawaii', 'Hawaii', 'HI', labs,
    {'name': SN_CHEM + ' and ' + SN_MICRO, 'page_url': SDWB_LIST, 'program_url': DWCP,
     'report_date': 'chemistry list November 16, 2026; microbiology list file created November 18, 2026; both fetched November 22, 2026'},
    {
     'title': 'Hawaii certified labs for well and catchment water testing (all 22 on DOH\'s lists, Nov 2026)',
     'description': 'All 22 labs Hawaii DOH certifies or approves for drinking water: 2 in-state commercial labs for bacteria, 7 county and DOH labs, and 13 mainland labs for chemistry. Plus DOH\'s $25 subsidized lead and copper test for catchment homes.',
     'intro': [
      'Hawaii\'s Department of Health certifies drinking-water labs through the State Laboratories Division (SLD). The Safe Drinking Water Branch\'s "Certified / Approved Drinking Water Labs" page now points to two SLD lists: a chemistry and radiochemistry list headed November 16, 2026 (13 labs) and a microbiology list (10 labs, file created November 18, 2026). We copied both on November 22, 2026. Eurofins in Pomona, California is on both, so there are 22 labs in all.',
      'The short version for a private well or a rainwater catchment system: for bacteria (total coliform and E. coli), two commercial labs on Oʻahu are certified, AECOS Laboratory in Kaneohe and FQLabs in Honolulu. DOH\'s previous directory (November 2025) listed both as accepting private samples. For chemistry such as nitrate, arsenic or lead, every lab on the November 2026 chemistry list is on the mainland. SLD says it "approves" out-of-state labs for chemistry only and that Hawaii has no formal reciprocity agreements with other states.',
      'Rainwater catchment: DOH says home catchment systems are not regulated, but recommends a screening test from a DOH-certified or approved lab, with the sample taken after all treatment (for example at the kitchen tap). To pass, DOH says the water should have turbidity of 5 NTU or less, no E. coli, lead of 0.010 mg/L or less and copper of 1.3 mg/L or less. DOH also subsidizes one lead and copper test per year for a legal dwelling on catchment: you pay shipping and $25.00, and DOH says AECOS is currently the only participating lab.',
      'What to test a well for: DOH\'s Private Water Wells sheet (revised October 21, 2024) says there are no rules on private-well water quality in Hawaii, that the owner is responsible, and points to EPA\'s advice to test each year for total coliform bacteria and nitrates, plus pesticides, organic chemicals and heavy metals before first use. DOH suggests checking its Groundwater Contamination Viewer for known chemical contamination near you and comparing results with federal and state maximum contaminant levels.',
     ],
     'caveats': [
      'DOH\'s lists are written for public-water-system compliance testing. DOH\'s own wording: "Always confirm the laboratory\'s current certification status with them before submitting any water samples," and use a lab that subcontracts only to other Hawaii-certified labs. Questions: Safe Drinking Water Branch, (808) 586-4258.',
      'No in-state lab is on the November 2026 chemistry list. AECOS is DOH\'s approved lab for the subsidized catchment lead and copper test but appears only on the microbiology list; ask AECOS which chemistry tests it reports as certified before relying on a result for a loan or sale.',
      'Bacteria samples have short hold times (our sampling guide lists them by lab), so the mainland labs are realistic for chemistry, not bacteria. SLD says it does not offer out-of-state approval for microbiology, yet its list shows Eurofins Pomona with certification type "Reciprocity"; we show it as printed.',
      'Chips for mainland labs are computed from DOH\'s analyte matrix: a chip appears when the lab has a method printed for that analyte (for VOCs, the row "Regulated Volatile Organic Compounds"; for pesticides, any of the common pesticide rows; for PFAS, any PFAS row). Several printed expiration dates have passed but are marked "extended until renewal"; we show them as printed.',
      'The grouping is ours. County water departments and DOH district labs are on the microbiology list but are not set up for homeowners as far as we can tell (DOH\'s November 2025 directory said the county labs do not accept private samples). Their addresses and phones come from that older directory or from DOH\'s lab pages, as cited on each card.',
      'Prices: the only price we found from a primary source is DOH\'s $25 subsidized catchment lead and copper test. AECOS and FQLabs post no prices on their sites; we did not check the mainland labs\' sites for prices.',
     ],
     'main_heading': 'In-state commercial labs certified for bacteria (private samples accepted per DOH\'s 2025 directory)',
     'public_heading': 'County water department and DOH labs on the microbiology list',
     'public_note': 'Certified for bacteria to test public water systems and for DOH programs. DOH\'s November 2025 directory listed the county labs as not accepting private samples. The DOH district labs\' pages do not mention homeowner samples. Call first.',
     'oos_heading': 'Mainland labs approved by Hawaii DOH for chemistry',
     'oos_note': [
      '%d of these 13 labs have a method printed for nitrate and %d for arsenic. Uranium, gross alpha, radium and radon are covered by only some (see the chips on each card). None of them says on DOH\'s list whether it takes homeowner samples by mail from Hawaii; ask about bottles, shipping and hold times before collecting.' % (len([n for n in nit if n not in ('AECOS Laboratory', 'FQLabs')]), len(ars)),
     ],
     'chips_label': 'Certified or approved by Hawaii DOH for (well-relevant tests, from DOH\'s lists):',
     'resources': [
      {'label': 'Hawaii DOH Safe Drinking Water Branch: Certified / Approved Drinking Water Labs (July 2026 pointer PDF)', 'url': SDWB_LIST},
      {'label': 'Hawaii DOH SLD: Certified Chemistry & Radiochemistry Drinking Water Labs (November 16, 2026)', 'url': CHEM},
      {'label': 'Hawaii DOH SLD: Drinking Water Microbiology Laboratories (November 2026)', 'url': MICRO},
      {'label': 'Hawaii DOH SLD: Drinking Water Certification Program', 'url': DWCP},
      {'label': 'Hawaii DOH Safe Drinking Water Branch: Private Water Wells (revised October 21, 2024)', 'url': PRIV},
      {'label': 'Hawaii DOH Safe Drinking Water Branch: Rainwater Catchment (screening test and subsidized lead/copper test)', 'url': RAIN},
      {'label': 'Hawaii DOH Safe Drinking Water Branch: Groundwater Contamination Viewer', 'url': GWV},
      {'label': 'Hawaii DOH: previous lab directory (revision November 20, 2025; superseded)', 'url': OLD},
      {'label': 'AECOS Laboratory', 'url': AECOS},
      {'label': 'FQLabs', 'url': FQ},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('hawaii', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed hawaii from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['phone'], '|', ', '.join(l['accredited_for']))
