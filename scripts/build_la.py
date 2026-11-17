"""Louisiana: LDH Laboratory Certification Program lists, fetched 2026-11-16.
Replaces the thin /labs/louisiana/ state-guide with a full listing.
SRC_DIR (default /workspace/src-la) must contain:
  chem.pdf  - "2026 List of Laboratories Certified by Louisiana for Drinking Water Analyses - Chemistry", "Current as of 2/12/2026"
              (https://ldh-oph.qualtraxcloud.com/ShowDocument.aspx?ID=2668, served as "Website Lab Scopes-2668-18.pdf",
              PDF created 2026-02-12, md5 b47684353eb2f51f4d1fa97f71449044, 117 pages, 32 labs)
  micro.pdf - "List of Laboratories Certified by Louisiana for Drinking Water Analysis - Microbiology", "March 2026"
              (https://ldh-oph.qualtraxcloud.com/ShowDocument.aspx?ID=2809, PDF modified 2026-03-11,
              md5 bb7c846fdfa43ffb9b8749813de5733b, 18 labs)
  chem_1025.pdf - LDH private-well page table "Certified Drinking Water Chemistry Laboratories as of 10/17/25" (used only for phone numbers)
Chemistry rows are parsed from the PDF text; microbiology rows are transcribed below and asserted against the PDF text,
so a changed list fails loudly."""
import os, sys, re, json, subprocess
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, key_chips

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-la')
V = '2026-11-16'
more_lib.V = V
CHEM = 'https://ldh-oph.qualtraxcloud.com/ShowDocument.aspx?ID=2668'
CHEM_N = 'LDH: Laboratories certified for chemistry tests on drinking water (current as of 2/12/2026)'
CHEM_D = '2026-02-12'
MICRO = 'https://ldh-oph.qualtraxcloud.com/ShowDocument.aspx?ID=2809'
MICRO_N = 'LDH: Laboratories certified for microbiology tests on drinking water (March 2026)'
MICRO_D = '2026-03 (PDF modified 2026-03-11)'
CERT_PAGE = 'https://ldh.la.gov/page/laboratory-certification'
WELL_PAGE = 'https://ldh.la.gov/page/well-testing-information'
SUMMARY = 'https://ldh.la.gov/assets/oph/Center-EH/envepi/PWI/Certified_Drinking_Water_Chemistry_Labs_10.25.25.pdf'
SUMMARY_N = 'LDH private-well page: Certified Drinking Water Chemistry Laboratories as of 10/17/25 (phone numbers)'
SITES = 'https://ldh.la.gov/assets/oph/Center-EH/envepi/PWI/Documents/FINAL_Sample_Locations.pdf'
ORDER = 'https://www.la.egov.com/ldh/privatewell/'
BRO = 'https://ldh.la.gov/assets/oph/Center-EH/envepi/PWI/Documents/PrvtWtrWllBro_2022.pdf'
WTI = 'https://watertestinc.com/'
WTI_B = 'https://watertestinc.com/bacterial-analysis/'

def pdftext(fn):
    return subprocess.run(['pdftotext', '-layout', os.path.join(SRC_DIR, fn), '-'], capture_output=True, text=True, check=True).stdout

# ---------- chemistry (parsed) ----------
t = pdftext('chem.pdf')
assert 'Current as of 2/12/2026' in t
lines = t.split('\n')
starts = [i for i, l in enumerate(lines) if 'Contact Person:' in l]
chem = []
for a, b in zip(starts, starts[1:] + [len(lines)]):
    blk = '\n'.join(lines[a:b])
    if 'Certificate #' not in blk:
        continue  # certifying-agency block
    head = []
    for l in lines[a:b]:
        if 'EPA ID' in l: break
        if l.strip(): head.append(re.split(r'\s{3,}', l.strip())[0])
    name = head[0]
    ci = [i for i, x in enumerate(head) if i > 0 and re.search(r', ?[A-Z]{2}( \d{5})?$', x)]
    addr = head[1:ci[0] + 1]
    cityline = addr[-1]
    m = re.match(r'(.+?), ?([A-Z]{2})', cityline)
    city, st = m.group(1), m.group(2)
    cert = re.search(r'Certificate #:\s*(\S+)', blk).group(1)
    acc = re.search(r'Accepts Commercial Samples:\s*(\w+)', blk).group(1)
    exp = re.search(r'Expiration Date:\s*([\d/]+)', blk).group(1)
    ab = re.search(r'Primary AB:\s*(\S+)', blk).group(1)
    an = []
    body = blk[blk.find('Analyte'):].split('\n')[4:]
    for l in body:
        if re.match(r'\s*_{10,}', l) or 'CERTIFYING AGENCY' in l: break
        s = l.strip()
        if not s: continue
        an.append(re.split(r'\s{2,}', s)[0])
    chem.append(dict(name=name, street=', '.join(addr[:-1]), cityline=cityline, city=city, st=st, cert=cert,
                     accepts=acc, exp=exp, ab=ab, analytes=sorted(set(an))))
assert len(chem) == 32, len(chem)

# phone numbers from LDH's 10/17/25 private-well table (keyed by a distinctive name fragment)
summ = re.sub(r'\s+', ' ', pdftext('chem_1025.pdf'))
PHONES = {
 'American Water Central': '(618) 235-3600', 'Curtis Environmental': '(985) 653-0000', 'Element Materials Technology Lafayette': '(337) 235-0483',
 'EMSL Analytical, Inc. - Cinnaminson': '(800) 220-3675', 'Environmental Hazard': '(804) 275-4788', 'Eurofins Pomona': '(866) 888-6653',
 'Eurofins South Bend': '(574) 233-4777', 'Eurofins Orlando': '(407) 851-2560', 'Eurofins Pensacola': '(850) 474-1001',
 'GEL Laboratories': '(843) 556-8171', 'Jefferson Parish': '(504) 838-4313', 'National Testing': '(800) 458-3330',
 'Pace Analytical National Center': '(615) 758-5858', 'Madisonville': '(606) 432-3171', 'Minneapolis': '(317) 313-4499',
 'Ormond Beach': '(386) 672-5668', 'Scott': '(337) 237-4775', 'Wheat Ridge': '(303) 425-6021', 'Kilgore': '(903) 984-0551',
 'Waypoint': '(901) 213-2400',
}
for p in PHONES.values():
    assert p in summ, p
def phone_for(name):
    for k, p in PHONES.items():
        if k in name: return p
    return None


def chem_card(c, group):
    chips = key_chips(c['analytes'])
    if not chips:
        a = set(c['analytes'])
        if a == {'Asbestos'}: chips = ['Asbestos only']
        elif a == {'2,3,7,8-TCDD (Dioxin)'}: chips = ['Dioxin (2,3,7,8-TCDD) only']
        elif 'Total Trihalomethanes (THMs)' in a: chips = ['Disinfection byproducts only (trihalomethanes and haloacetic acids)']
        else: chips = ['Only: ' + ', '.join(c['analytes'])]
    det = ('LDH chemistry certificate %s, expires %s; primary accreditation body %s; "Accepts Commercial Samples: %s" (as printed). '
           'LDH lists %d certified analyte names for this lab.' % (c['cert'], c['exp'], c['ab'], c['accepts'], len(c['analytes'])))
    lab = dict(name=c['name'], address=(c['street'] + ', ' + c['cityline']) if c['street'] else c['cityline'], city=c['city'],
               phone=phone_for(c['name']), accredited_for=chips, group=group, detail=det,
               source_name=CHEM_N, source_url=CHEM, source_date=CHEM_D, last_verified=V)
    if lab['phone']:
        lab['source_url_2'], lab['source_name_2'] = SUMMARY, SUMMARY_N
    return lab

# ---------- microbiology (transcribed, asserted) ----------
mt = re.sub(r'\s+', ' ', pdftext('micro.pdf'))
assert 'March 2026' in mt
PA = 'Total coliform & E. coli (presence/absence)'
MPN = 'E. coli count (MPN/Quanti-Tray, source water)'
MTF = 'Total coliform & E. coli (multiple-tube)'
MF = 'Total coliform & E. coli (membrane filter)'
HPC = 'Heterotrophic plate count'
micro = [
 # name, street, cityline, phone, chips, expiration, group
 ('LDH Central Laboratory (state lab)', '1209 Leesville Avenue', 'Baton Rouge, LA 70802', '(225) 219-5200', [PA, MTF, HPC], 'August 2028 (EPA)', 'ldh'),
 ('LDH Amite Regional Laboratory', '104 North 1st Street #A', 'Amite, LA 70422', '(985) 748-2011', [PA, 'Total coliform & E. coli (MPN 10-tube)', MTF, HPC], 'June 2027', 'ldh'),
 ('LDH Shreveport Regional Laboratory', '1035 Creswell Avenue', 'Shreveport, LA 71104', '(318) 676-7809', [PA], 'February 2028', 'ldh'),
 ('LDH Rapides Regional Laboratory', '5604-A Coliseum Blvd. Room A102', 'Alexandria, LA 71303', '(318) 487-5282 Ext. 197', [PA], 'October 2026', 'ldh'),
 ('LDH Lake Charles Regional Laboratory', '2827 4th Avenue, Room 132', 'Lake Charles, LA 70601', '(337) 475-3236', [PA], 'November 2026', 'ldh'),
 ('Baton Rouge Water Company Laboratory', '8755 Goodwood Boulevard', 'Baton Rouge, LA 70806', '(225) 952-7638', [PA], 'March 2027', 'public'),
 ('City of Alexandria Water Laboratory', '1212 Hudson Boulevard', 'Alexandria, LA 71302', '(318) 441-6251', [PA, 'Total coliform & E. coli (Colisure presence/absence)', HPC], 'January 2027', 'public'),
 ('City of Lake Charles Water Laboratory', '617 E. McNeese Street', 'Lake Charles, LA 70605', '(337) 491-1599', [PA], 'May 2027', 'public'),
 ('City of Marksville Water Laboratory', '227 East Bontemps Street', 'Marksville, LA 71351', '(318) 442-4000', ['Total coliform & E. coli (Colisure presence/absence)'], 'May 2026', 'public'),
 ('City of Shreveport T.L. Amiss Laboratory', '3205 Blanchard Road', 'Shreveport, LA 71103', '(318) 673-7654', [MF, PA, MPN, HPC], 'September 2027', 'public'),
 ('Jefferson Parish Water Quality Laboratory', '3600 Jefferson Hwy Bldg E', 'Jefferson, LA 70121-1728', '(504) 838-4313', [MF, HPC, 'E. coli count (membrane filter, source water)'], 'December 2027', 'public'),
 ('JRTC & Fort Johnson Environmental Laboratory', '1711 23rd Street Building 2516', 'Fort Polk, LA 71459', '(337) 531-9128', ['Total coliform & E. coli (Colitag presence/absence)'], 'February 2027', 'public'),
 ('Lafayette Utilities Systems Water Production Laboratory', 'P.O. Box 4017-C, 1210 Walker Road', 'Lafayette, LA 70502', '(337) 291-5913', [MF, HPC], 'February 2027', 'public'),
 ('Louisiana Water Company', '448 East Main Street', 'New Iberia, LA 70560', '(337) 374-1073', [MF, PA, HPC], 'July 2027', 'public'),
 ('Sewerage & Water Board of New Orleans', '8800 S. Claiborne Avenue', 'New Orleans, LA 70118', '(504) 865-0420', [MF, PA, MPN, HPC], 'January 2028', 'public'),
 ('St. Bernard Parish Water Lab', '1111 East St. Bernard Highway', 'Chalmette, LA 70043', '(504) 217-1681 ext. 0796', [PA], 'September 2027', 'public'),
 ('Terrebonne Parish Consolidated Waterworks District #1 Laboratory', 'P.O. Box 630', 'Houma, LA 70361', '(985) 446-7509', [PA, HPC], 'November 2026', 'public'),
 ('Water Test, Inc.', '21220 Highway 36', 'Covington, LA 70433', '(985) 892-8329', [PA], 'August 2026', 'main'),
]
for r in micro:
    for piece in (r[2].split(',')[0], r[5]):
        assert piece in mt, piece
    assert re.sub(r'\D', '', r[3])[:10] in re.sub(r'\D', '', mt), r[3]
assert len(micro) == 18
PASSED = {'May 2026', 'August 2026', 'October 2026'}
MONTH_NOW = {'November 2026'}

def exp_text(e):
    s = 'Microbiology certification expiration printed on LDH\'s March 2026 list: %s.' % e
    if e in PASSED:
        s += ' That date has passed and LDH has not posted a newer list, so ask the lab whether its certification was renewed.'
    elif e in MONTH_NOW:
        s += ' That is this month; ask the lab whether it has been renewed.'
    return s

LDH_NOTE = ('State public health lab. LDH\'s private well page says owner-collected bacteria samples cost $40 per sample when you take them to a parish health unit or LDH lab, '
            'and orders can be placed online or in person at a parish health unit. LDH\'s drop-off sheet (dated April 2023) says this lab takes water samples Monday-Thursday by 2:00 pm (excluding holidays). '
            'LDH lists it for bacteria only; it does not appear on the chemistry list.')
LDH_EXTRA = {
 'LDH Shreveport Regional Laboratory': ' The drop-off sheet prints 1035 Creswell Avenue, Room 352, Shreveport, LA 71101, phone 318-676-7807; the March 2026 certification list prints ZIP 71104 and phone (318) 676-7809.',
 'LDH Rapides Regional Laboratory': ' The drop-off sheet lists it as the Rapides Parish Laboratory at the Alexandria Regional Office, phone 318-487-5282 ext. 197 or 265.',
 'LDH Amite Regional Laboratory': ' The drop-off sheet prints the city as Amite City.',
}

def micro_card(r):
    name, street, cityline, phone, chips, exp, grp = r
    lab = dict(name=name, address=street + ', ' + cityline, city=cityline.split(',')[0], phone=phone,
               accredited_for=chips, group='main' if grp in ('ldh', 'main') else 'public',
               detail=exp_text(exp), source_name=MICRO_N, source_url=MICRO, source_date=MICRO_D, last_verified=V)
    if grp == 'ldh':
        lab['note'] = LDH_NOTE + LDH_EXTRA.get(name, '')
        lab['source_url_2'], lab['source_name_2'] = WELL_PAGE, 'LDH Private Well Testing Information page (fetched 2026-11-16) and sample drop-off locations PDF'
    if name == 'Water Test, Inc.':
        lab['website'] = WTI
        lab['note'] = ('The LDH list marks it "(PRIVATE WELLS ONLY)". Its own site (fetched 2026-11-16) says it takes bacteria samples Monday-Friday 8:00 AM to 3:00 PM, '
                       'results in 24 to 36 hours, payment in advance; certified results (accepted for FHA, VA, HUD, Rural Development, conventional loans and real estate closings) '
                       'are $145.00 for a routine bacteria test in St. Tammany Parish and $95.00 for a repeat, with a mileage charge outside St. Tammany; non-certified results are $95.00. '
                       'It also sells mineral and "extensive" tests (call for pricing); LDH certifies it for bacteria only, so ask which results are certified.')
        lab['source_url_2'], lab['source_name_2'] = WTI_B, 'Water Test, Inc.: Bacterial Analysis page (fetched 2026-11-16)'
    if name == 'Jefferson Parish Water Quality Laboratory':
        jp = [c for c in chem if c['cert'] == 'LA003'][0]
        lab['accredited_for'] = chips + key_chips(jp['analytes'])
        lab['detail'] += (' Also on the chemistry list: certificate LA003, expires %s, "Accepts Commercial Samples: %s" (as printed).' % (jp['exp'], jp['accepts']))
        lab['source_url_2'], lab['source_name_2'] = CHEM, CHEM_N
    return lab

labs = [micro_card(r) for r in micro]
inst = [c for c in chem if c['st'] == 'LA' and c['cert'] != 'LA003']
oos = [c for c in chem if c['st'] != 'LA']
assert len(inst) == 3 and len(oos) == 28, (len(inst), len(oos))
for c in inst:
    lab = chem_card(c, 'main')
    if c['cert'] == 'LA033':
        lab['note'] = ('LDH\'s October 2025 private-well table marked this lab for copper and lead, but the February 2026 certified scope lists only alkalinity, chlorite, '
                       'total organic carbon and turbidity. Ask the lab before you send a sample for metals.')
    labs.append(lab)

def oos_key(c):
    ch = key_chips(c['analytes'])
    return (-(('Nitrate' in ch) + ('Arsenic' in ch)), -len(ch), c['name'])
for c in sorted(oos, key=oos_key):
    lab = chem_card(c, 'outofstate')
    if c['cert'] == 'LA006':
        lab['note'] = 'LDH\'s October 2025 table prints this phone number (a 317 area code, not Minnesota). Confirm it with the lab.'
    labs.append(lab)

# main order: LDH labs, Water Test, then in-state commercial chemistry labs
c = Counter(l['group'] for l in labs)
assert len(labs) == 49 and c['main'] == 9 and c['public'] == 12 and c['outofstate'] == 28, c

write_state('louisiana', 'Louisiana', 'LA', labs,
    {'name': 'LDH Laboratory Certification Program: chemistry list (current as of 2/12/2026) and microbiology list (March 2026)',
     'page_url': CERT_PAGE, 'program_url': CERT_PAGE,
     'report_date': 'Chemistry list "Current as of 2/12/2026"; microbiology list dated March 2026; both fetched November 16, 2026'},
    {
     'title': 'Louisiana certified labs for well water testing (all 49 on LDH\'s lists, Nov 2026)',
     'description': 'All 49 labs on the Louisiana Department of Health\'s certified drinking-water lab lists (bacteria and chemistry), the five LDH state labs that test private wells for $40, and what each lab is certified for.',
     'intro': [
      'The Louisiana Department of Health (LDH) certifies labs that test drinking water under the Safe Drinking Water Act. Its Laboratory Certification page links two lists, which we transcribed on November 16, 2026: a microbiology (bacteria) list dated March 2026 with 18 labs, and a chemistry list "current as of 2/12/2026" with 32 labs. One lab (Jefferson Parish) is on both, so this page has 49 labs.',
      'For most well owners the starting point is LDH itself. Its private well page says you can collect a bacteria sample yourself and take it to a parish health unit or LDH lab for $40 per sample, or have the parish sanitarian collect it. Orders can be placed online or in person at a parish health unit. Five LDH labs (Baton Rouge, Amite, Shreveport, Alexandria and Lake Charles) are on the bacteria list. For questions about sampling or results LDH gives 1-888-293-7020.',
      'The only private lab on the bacteria list is Water Test, Inc. in Covington, which LDH marks "private wells only". No lab in Louisiana is on both lists except the Jefferson Parish water utility lab, so for nitrate, arsenic or other chemistry most certified options are out-of-state commercial labs (listed below) or one of three in-state commercial labs.',
      'LDH\'s well-owner brochure recommends inspecting and testing a well every year for biological and chemical contaminants, and also after a hurricane, flood or major rainfall, when you notice a change in the water, or when a pregnant woman, infant, elderly person or someone with a weakened immune system lives in the home.',
     ],
     'caveats': [
      'Certification is per test. Each card shows the well-relevant tests the lab is certified for. Chemistry labs are not certified for bacteria in Louisiana unless they are also on the bacteria list.',
      'The lists are for labs that test public water systems. "Accepts Commercial Samples" is printed on the chemistry list, but neither list says which labs take homeowner samples. Call first.',
      'The bacteria list is dated March 2026, and several expiration dates on it (Water Test, Inc. August 2026; City of Marksville May 2026; LDH Rapides October 2026) have passed. LDH has not posted a newer list, so ask the lab. For questions about certification, LDH gives 225-219-5200.',
      'LDH\'s two pages give different sanitarian prices: the private well page says sanitarian-collected testing is $150, while the online order page (fetched the same night) lists "Sanitarian Services Well Testing" at $75 and a $150 loan letter. Confirm with your parish health unit.',
      'Bacteria samples are time-limited. Take samples to LDH Monday-Thursday before 2:00 pm, and to Water Test, Inc. Monday-Friday before 3:00 pm.',
      'The grouping is ours: state labs, the one private bacteria lab and in-state commercial chemistry labs first; water-utility and military labs second; out-of-state chemistry labs last, sorted by whether they are certified for nitrate and arsenic.',
     ],
     'main_heading': 'LDH state labs, the private-well bacteria lab and in-state commercial labs',
     'public_heading': 'Water-utility, parish and military labs on the same lists',
     'public_note': 'These labs test water for a utility, parish or base. The LDH lists do not say whether they take samples from private-well owners, and we found no source saying they do. Call first.',
     'oos_heading': 'Out-of-state labs on LDH\'s chemistry list',
     'oos_note': [
      'LDH certifies 28 chemistry labs outside Louisiana. Most are large commercial labs that test for water utilities. Some only test for specialty items such as asbestos, dioxin, PFAS, radiologicals or disinfection byproducts; each card says which.',
      'We list labs certified for both nitrate and arsenic first. Phone numbers come from LDH\'s October 2025 private-well table where it lists the lab; the February 2026 chemistry list prints only e-mail contacts. Ask each lab how to ship samples.',
     ],
     'chips_label': 'Certified by LDH for (well-relevant tests):',
     'resources': [
      {'label': 'LDH: Laboratory Certification program page', 'url': CERT_PAGE},
      {'label': 'LDH: Laboratories certified for chemistry tests on drinking water (current as of 2/12/2026)', 'url': CHEM},
      {'label': 'LDH: Laboratories certified for microbiology tests on drinking water (March 2026)', 'url': MICRO},
      {'label': 'LDH: Private Well Testing Information', 'url': WELL_PAGE},
      {'label': 'LDH: Order a private well test online', 'url': ORDER},
      {'label': 'LDH: Sample drop-off locations (LDH labs and parish health units, PDF)', 'url': SITES},
      {'label': 'LDH: Certified drinking water chemistry laboratories as of 10/17/25 (private-well table, PDF)', 'url': SUMMARY},
      {'label': 'LDH brochure: Private Water Well Testing in Louisiana (PDF)', 'url': BRO},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('louisiana', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed louisiana from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', '; '.join(l['accredited_for']))
