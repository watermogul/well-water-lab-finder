"""South Dakota: SD Department of Agriculture & Natural Resources (DANR) Drinking Water Program, "Laboratory Certification" web page
(https://danr.sd.gov/OfficeOfWater/DrinkingWater/LaboratoryCert.aspx). The page prints no revision date; fetched 2026-11-21
(HTML md5 4b73b1482f8880d8c3d09ccc1bdc2d9c). South Dakota runs its own drinking-water lab certification program (rules ARSD 74:04:07);
the page lists 4 in-state labs and, under "OTHER LABS CERTIFIED BY SOUTH DAKOTA", 12 out-of-state labs, each with broad categories
("Inorganics", "SOC's", "Microbiology" ...) rather than an analyte matrix. Replaces the thin /labs/south-dakota/ state-guide.

Rows below are hand-entered from the page text (16 "Certified for:" blocks). The builder re-parses the saved HTML, asserts 16 blocks and
that every lab name/phone appears, so a changed list fails loudly. Contact names printed by DANR are not published (site convention).

SRC_DIR (not committed; all fetched 2026-11-21) holds: danr_labcert.html, danr_pws.html (Private Well Sampling), danr_newwell.html
(New Well Sampling Program), map_brochure.pdf (Midwest Assistance Program brochure linked from danr_pws, revised 10/24/2023),
doh_well.html (SD DOH Test a Private Well / bottle order, content last updated 2026-10-05), doh_env.html + doh_fees.html +
doh_micro.html + doh_inorg.html (SD DOH Environmental Testing pages, content last updated 2026-09-22), doh_contact.html (2026-04-07),
mctl_well.html / mctl_contact.html / mctl_newwell.pdf (Mid Continent Testing Labs), aet_sf.html (AET Sioux Falls location page).
City of Sioux Falls Health Laboratory page returned 403 to curl; its text was read via WebFetch on 2026-11-21."""
import os, sys, re, html, hashlib, json
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-sd')
V = '2026-11-21'
more_lib.V = V
PAGE = 'https://danr.sd.gov/OfficeOfWater/DrinkingWater/LaboratoryCert.aspx'
SN = 'SD DANR Drinking Water Program: Laboratory Certification (web page, no revision date printed)'
SD = V  # page undated; date = date fetched
PWS = 'https://danr.sd.gov/OfficeOfWater/DrinkingWater/PrivateWellSampling.aspx'
NEWWELL = 'https://danr.sd.gov/OfficeOfWater/DrinkingWater/NewWellSamplingProgram.aspx'
MAP = 'https://danr.sd.gov/OfficeOfWater/DrinkingWater/docs/Well%20Assessment%20Brochure%20revised%2010.24.23.pdf'
DOH_WELL = 'https://doh.sd.gov/laboratory/environmental-testing/test-a-private-well/'
DOH_ENV = 'https://doh.sd.gov/laboratory/environmental-testing/'
DOH_FEES = 'https://doh.sd.gov/laboratory/environmental-testing/environmental-testing-fees/'
SF = 'https://www.siouxfalls.gov/health-safety/health-services/public-health/health-laboratory'
MCTL = 'https://www.thechemistrylab.com/private-well-testing'
MCTL_NW = 'https://thechemistrylab.com/PDF/NewWell.pdf'

src = open(os.path.join(SRC_DIR, 'danr_labcert.html'), encoding='utf-8', errors='ignore').read()
assert hashlib.md5(open(os.path.join(SRC_DIR, 'danr_labcert.html'), 'rb').read()).hexdigest() == '4b73b1482f8880d8c3d09ccc1bdc2d9c', 'DANR page changed: re-check rows'
txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', src)))
assert txt.count('Certified for:') == 16

def chips(s):
    return [c.strip() for c in s.split('|')]

ROWS = [
 # in-state
 dict(name='South Dakota Public Health Laboratory', listed='South Dakota State Health Laboratory', address='Laboratory Building, 615 East Fourth Street, Pierre, SD 57501', city='Pierre',
      phone='605-773-3368', cert="Inorganics, SOC's, VOC's, Chlorite, HAA5, Perchlorate, TTHM's, Microbiology, E.Coli enumeration, Chlorite",
      chips=chips("Inorganics|SOCs|VOCs|Chlorite|HAA5|Perchlorate|TTHMs|Microbiology|E. coli enumeration"), group='main', order=0),
 dict(name='Sioux Falls Public Health Laboratory', address='521 North Main, Suite 100, Sioux Falls, SD 57104', city='Sioux Falls', phone='605-367-8777',
      cert='Microbiology', chips=['Microbiology'], group='main', order=1),
 dict(name='Mid Continent Testing Laboratory', address='2381 South Plaza Drive, PO Box 3388, Rapid City, SD 57709', city='Rapid City', phone='605-348-0111',
      cert="Inorganics, VOC's, Cyanide, Microbiology, E.Coli enumeration,TTHM's, HAA5's, SOC's (except 548 and PCB's), TOCs",
      chips=chips("Inorganics|VOCs|Cyanide|Microbiology|E. coli enumeration|TTHMs|HAA5s|SOCs (except method 548 and PCBs)|TOCs"), group='main', order=2),
 dict(name='American Engineering Testing', address='601 East 48th Street North, Sioux Falls, SD 57104', city='Sioux Falls', phone='605-332-5371',
      cert='Microbiology, E.Coli enumeration', chips=chips('Microbiology|E. coli enumeration'), group='limited', order=3),
 # out of state, in DANR's order
 dict(name='Pace Analytical Services-Pittsburgh', address='1638 Roseytown Rd, Suite 2, Greenburg, PA 15601', city='Greenburg', phone='724-880-5600',
      cert='Radiological', chips=['Radiological'], group='outofstate', order=10),
 dict(name='Energy Laboratories Inc. (Billings)', listed='Energy Laboratories Inc.', address='1107 South Broadway, PO Box 30916, Billings, MT 59107-0916', city='Billings', phone='406-252-6325',
      cert="Inorganics, SOC's(except Method 531.1, 547, 549.2), TTHM's, Cyanide,VOC's, HAA5's, Uranium, PFAS",
      chips=chips('Inorganics|SOCs (except methods 531.1, 547, 549.2)|TTHMs|Cyanide|VOCs|HAA5s|Uranium|PFAS'), group='outofstate', order=11),
 dict(name='Energy Laboratories Inc. (Casper)', listed='Energy Laboratories Inc.', address='2393 Salt Creek Hwy, PO Box 3258, Casper, WY 82602', city='Casper', phone='307-235-0515',
      cert="Some SOC's, Radiological, excluding Uranium, TOCs", chips=chips('Some SOCs|Radiological (excluding uranium)|TOCs'), group='outofstate', order=12,
      pre='DANR also prints a toll-free number, 888-235-0515. '),
 dict(name='Eurofins Eaton Analytical LLC (Pomona)', listed='Eurofins Eaton Analytical LLC', address='931 Corporate Center Drive, Pomona, CA 91768', city='Pomona', phone='866-888-6653',
      cert="Inorganics, VOC's, SOC's, TTHM's, HAA5's, Bromate, Chlorite", chips=chips('Inorganics|VOCs|SOCs|TTHMs|HAA5s|Bromate|Chlorite'), group='outofstate', order=13),
 dict(name='Pace Analytical (Sheridan)', listed='Pace Analytical', address='1673 Terra Ave, Sheridan, WY 82801', city='Sheridan', phone='307-672-8945',
      cert='Inorganics excluding Nickel, Uranium', chips=chips('Inorganics (excluding nickel)|Uranium'), group='outofstate', order=14),
 dict(name='Eurofins Eaton Analytical Inc (South Bend)', listed='Eurofins Eaton Analytical Inc', address='110 South Hill Street, South Bend, IN 46617', city='South Bend', phone='574-472-5523',
      cert="Inorganics, SOC's, TTHM's, Cyanide, Chlorite, HAA5, VOC's, Bromate, Radiological, Uranium",
      chips=chips('Inorganics|SOCs|TTHMs|Cyanide|Chlorite|HAA5|VOCs|Bromate|Radiological|Uranium'), group='outofstate', order=15),
 dict(name='Minnesota Valley Testing Laboratories (Bismarck)', listed='Minnesota Valley Testing Laboratories', address='2616 E Broadway Ave, Bismarck, ND 58501', city='Bismarck', phone='701-258-9720',
      cert="Inorganics, TOC's, Microbiology", chips=chips('Inorganics|TOCs|Microbiology'), group='outofstate', order=16,
      pre='DANR also prints 800-279-6885. '),
 dict(name='Element Materials Technology (Lafayette)', listed='Element Materials Technology', address='2417 West Pinhook Rd, Lafayette, LA 70508-3344', city='Lafayette', phone='888-786-7555',
      cert='Lead, Copper', chips=chips('Lead|Copper'), group='outofstate', order=17),
 dict(name='Element Materials Technology (Fort Wayne)', listed='Element Materials Technology', address='328 Ley Road, Suite 100, Ft Wayne, IN 46825', city='Fort Wayne', phone='260-471-7000',
      cert="Lead, Copper, IOC's, VOC's, SOC's, TTHM's, HAA5's, Cyanide, Microbiology",
      chips=chips('Lead|Copper|IOCs (inorganics)|VOCs|SOCs|TTHMs|HAA5s|Cyanide|Microbiology'), group='outofstate', order=18),
 dict(name='Foundation Analytical Laboratory', address='723 Sleezer Road, Cherokee, IA 51012', city='Cherokee', phone='712-255-6989',
      cert='Inorganics except Mercury, Lead, Copper, Cyanide', chips=chips('Inorganics (except mercury)|Lead|Copper|Cyanide'), group='outofstate', order=19),
 dict(name='Alliance Technical Group LLC', address='3310 Win Street, Cuyahoga, OH 44233', city='Cuyahoga', phone='330-253-8211',
      cert='Inorganics (Excluding: HG + F), Radiologicals, PFAS', chips=chips('Inorganics (excluding mercury and fluoride)|Radiologicals|PFAS'), group='outofstate', order=20,
      pre='DANR prints the city as "Cuyahoga, OH." with ZIP 44233; we did not check this against the lab\'s own site. "HG + F" on the list is read here as mercury and fluoride. '),
 dict(name='Symbio Laboratories', listed='Symbio Labratories', address='8310 Mirimar Mall, San Diego, CA 92121', city='San Diego', phone='858-257-0159',
      cert='PFAS', chips=['PFAS'], group='outofstate', order=21, pre='Name and street spelled on the DANR page as "Symbio Labratories" and "Mirimar Mall". '),
]
assert len(ROWS) == 16
for r in ROWS:
    nm = r.get('listed', r['name'])
    assert nm in txt, nm
    assert r['phone'] in txt, r['phone']
    assert re.sub(r'\s+', ' ', r['cert']).split(',')[0] in txt

EXTRA = {
 'South Dakota Public Health Laboratory': dict(website=DOH_WELL, s2=(DOH_WELL, 'SD Department of Health: Test a Private Well, Environmental Testing and Environmental Testing Fees pages (content last updated 2026-10-05 / 2026-09-22; fetched 2026-11-21)'),
   pre='DANR lists it as "South Dakota State Health Laboratory"; the Department of Health now calls it the South Dakota Public Health Laboratory and gives the same street address (615 E 4th Street, Pierre). Toll-free 1-800-738-2301 (in SD only), per DOH. ',
   note='This is the state lab, and it tests private wells. The Department of Health says private persons need "a testing kit from the Department of Health or a special location"; its online Sample Bottle Order Form offers Bacteria/Nitrate, Lead, New Well and Other bottles, and says "Sample bottles and instructions are also available from County Extension offices." DOH\'s Environmental Testing Fees page (content last updated September 22, 2026) lists, per test: Total Coliform $20.00, E. coli $22.00, Nitrate $18.00, Arsenic $23.00, Lead $18.50, Copper $18.50, Iron $18.00, Manganese $18.00, Sulfate $17.00, Fluoride $16.00, Chloride $16.00, pH $12.00, Conductivity $12.00, Dissolved solids $18.00, Hardness $15.00 (no charge if calcium and magnesium are ordered), Selenium $23.00, Uranium $26.00, Gross alpha/beta $55.00, Radium-226 $85.00, Radium-228 $170.00; organics (pesticides, VOCs): "Contact the Lab". The page does not say which of these a Bacteria/Nitrate bottle is billed as; DOH says fee information comes with the bottles. DOH also says the lab has moved into a new facility and is "fully operational".'),
 'Sioux Falls Public Health Laboratory': dict(website=SF, s2=(SF, 'City of Sioux Falls: Health Laboratory page (read 2026-11-21; returns 403 to scripted fetch)'),
   note='The City of Sioux Falls says its Public Health Laboratory\'s testing "serves Falls Community Health, city departments, agencies, commercial businesses, private citizens, and the State of South Dakota," and its page links "How to Collect Water Samples - Well and Household" and a Water Testing Data Form. DANR lists it for microbiology only, so it is a bacteria option, not a nitrate one. The city page does not post fees or hours; call first.'),
 'Mid Continent Testing Laboratory': dict(website=MCTL, s2=(MCTL, 'Mid Continent Testing Labs: Private Well Testing page and New Well Sampling Program form (fetched 2026-11-21)'),
   note='Mid Continent\'s Private Well Testing page says its staff "is always prepared to help residential customers with well water testing," and explains bacteria, nitrate, sodium, sulfate, conductivity and common-ion results. It also has a New Well Sampling Program form that it says it supplies to the State with your results, to comply with the 1989 new-well testing law. No prices are posted; call 605-348-0111. The lab\'s site gives the mailing address as P.O. Box 3388 and fax 605-721-0265.'),
 'American Engineering Testing': dict(website='https://www.teamaet.com/locations/sioux-falls/', s2=('https://www.teamaet.com/locations/sioux-falls/', 'AET: Sioux Falls location page (fetched 2026-11-21)'),
   note='AET is an engineering and materials-testing firm. Its Sioux Falls page mentions its environmental chemistry lab and wastewater (NPDES) testing but says nothing about private wells or homeowner samples. Call before collecting a sample.'),
}
OOS_NOTE = 'Out-of-state lab. DANR does not say whether it accepts homeowner samples or ships bottles to South Dakota; we did not verify prices or homeowner service.'

labs = []
for r in ROWS:
    ex = EXTRA.get(r['name'], {})
    listed = r.get('listed', r['name'])
    parts = []
    if listed != r['name'] and 'pre' not in ex: parts.append('Listed by DANR as "%s".' % listed)
    parts.append('Certified for (as printed by DANR): "%s".' % r['cert'])
    detail = ' '.join(parts)
    pre = (ex.get('pre') or '') + (r.get('pre') or '')
    if pre: detail += ' ' + pre.strip()
    lab = dict(name=r['name'], address=r['address'], city=r['city'], phone=clean_phone(r['phone']), accredited_for=r['chips'],
               detail=detail, group=r['group'], source_name=SN, source_url=PAGE, source_date=SD, last_verified=V)
    if ex.get('website'): lab['website'] = ex['website']
    if ex.get('note'): lab['note'] = ex['note']
    elif r['group'] == 'outofstate': lab['note'] = OOS_NOTE
    if ex.get('s2'): lab['source_url_2'], lab['source_name_2'] = ex['s2']
    if r['name'] == 'Pace Analytical (Sheridan)':
        lab['note'] = OOS_NOTE + ' EPA Region 8\'s Wyoming list prints a different phone for this address, 307-461-4938 (see our Wyoming page).'
    if r['name'] == 'Energy Laboratories Inc. (Casper)':
        lab['note'] = OOS_NOTE + ' DANR\'s page prints no certification dates. On EPA Region 8\'s February 2026 Wyoming list, this lab\'s Wyoming certification end dates (3/31/2026 and 6/30/2026) had passed (see our Wyoming page); ask for a current South Dakota certificate.'
    lab['_o'] = r['order']
    labs.append(lab)
labs.sort(key=lambda l: ({'main': 0, 'limited': 1, 'outofstate': 2}[l['group']], l['_o']))
for l in labs: del l['_o']
from collections import Counter
assert Counter(l['group'] for l in labs) == Counter({'main': 3, 'limited': 1, 'outofstate': 12})

write_state('south-dakota', 'South Dakota', 'SD', labs,
    {'name': SN, 'page_url': PAGE, 'program_url': DOH_WELL,
     'report_date': 'web page, no revision date printed; fetched November 21, 2026'},
    {
     'title': 'South Dakota certified labs for well water testing (all 16 on DANR\'s list, Nov 2026)',
     'description': 'All 16 labs South Dakota DANR certifies for drinking water (4 in-state, 12 out-of-state), which ones take private-well samples, and the state lab\'s posted per-test fees: total coliform $20, E. coli $22, nitrate $18.',
     'intro': [
      'South Dakota certifies drinking-water labs itself, through the Department of Agriculture & Natural Resources (DANR) Drinking Water Program. DANR\'s Laboratory Certification page lists every certified lab: 4 in South Dakota and 12 out-of-state labs under "Other labs certified by South Dakota". We copied that page on November 21, 2026; it prints no revision date. DANR certifies labs to analyze "compliance samples from public water systems," so the list does not say which labs take homeowner samples. We checked each in-state lab\'s own page for that.',
      'For a private well, the main route is the South Dakota Public Health Laboratory in Pierre (the "State Health Laboratory" on DANR\'s list). You order sample bottles from the Department of Health online, or pick them up at a County Extension office, and mail the sample back. In Sioux Falls, the city\'s Public Health Laboratory says it serves private citizens and posts well-sampling instructions (bacteria only). In Rapid City, Mid Continent Testing Laboratory has a private-well testing page.',
      'What to test for: DANR recommends retesting a well for bacteria "at least annually," and after heavy rains, snowmelt or flooding to submit "at least a bacteriological and nitrate analysis." Nitrate above 10 mg/L (as nitrogen) matters for infants six months and younger and for pregnant women, and boiling raises nitrate rather than removing it. If a bacteria test comes back unsafe, DANR says to boil drinking water until the well tests safe.',
      'New wells: DANR says the Centennial Environmental Protection Act of 1989 "requires that all new domestic wells drilled in South Dakota are tested for bacteria and several selected chemicals." The Department of Health\'s bottle order form has a "New Well" option, and Mid Continent has a New Well Sampling Program form.',
      'Cheapest published prices we found: the state lab\'s fee page (updated September 22, 2026) lists total coliform at $20, E. coli at $22 and nitrate at $18 per test, plus arsenic $23, lead $18.50, uranium $26 and others (full list under the lab below). No other South Dakota lab posts prices. DANR also links a Midwest Assistance Program brochure (revised October 2023) offering free well assessments with water testing to South Dakota well owners "while funding is available"; we did not confirm the program is still funded.',
     ],
     'caveats': [
      'DANR\'s page prints no revision date and no certification end dates. Ask the lab for its current South Dakota certificate if the result is for a loan, sale or permit.',
      'Chips show DANR\'s broad categories as printed, not individual tests. "Inorganics" (or "IOCs") usually covers metals and minerals such as nitrate, arsenic and lead, but DANR does not itemize them, so ask whether a lab is certified for the specific test you need. "SOCs" are synthetic organic chemicals such as pesticides; "VOCs" are volatile organic compounds such as solvents and fuel components; TTHMs, HAA5s, bromate and chlorite are disinfection byproducts that matter for chlorinated public water, not usually for wells.',
      'In South Dakota, only the state lab and Mid Continent are certified for inorganics (which typically include nitrate). The Sioux Falls city lab and American Engineering Testing are certified for bacteria only.',
      'The grouping is ours: the first group is in-state labs with a primary source showing they take private-well or private-citizen samples; the second is an in-state lab with no such page; the third is DANR\'s out-of-state list.',
      'Contact names on DANR\'s list are not shown. Prices come only from the labs\' or agencies\' own pages; we found posted prices only for the state lab.',
     ],
     'main_heading': 'South Dakota labs that take private-well samples',
     'limited_heading': 'In-state lab with no homeowner page found',
     'limited_note': 'Certified by DANR for bacteria only. We found no page saying it takes homeowner samples. Call first.',
     'oos_heading': 'Out-of-state labs certified by South Dakota',
     'oos_note': [
      'DANR certifies these labs for South Dakota drinking-water work. Several are certified for tests no in-state lab outside Pierre covers, such as uranium (Energy Laboratories Billings, Pace Sheridan, Eurofins South Bend) and PFAS (Energy Laboratories Billings, Alliance Technical Group, Symbio). Whether they take homeowner samples by mail is not stated; ask about bottles, shipping and hold times before collecting.',
     ],
     'chips_label': 'Certified by SD DANR for (categories as printed):',
     'resources': [
      {'label': 'SD DANR: Laboratory Certification (list of certified drinking-water labs)', 'url': PAGE},
      {'label': 'SD DANR: Private Well Sampling (what your results mean)', 'url': PWS},
      {'label': 'SD DANR: New Well Sampling Program', 'url': NEWWELL},
      {'label': 'SD Department of Health: Test a Private Well (sample bottle order form)', 'url': DOH_WELL},
      {'label': 'SD Department of Health: Environmental Testing Fees', 'url': DOH_FEES},
      {'label': 'SD Department of Health: Environmental Testing', 'url': DOH_ENV},
      {'label': 'Midwest Assistance Program: Private Well Assessment brochure (PDF on DANR\'s site, revised 10/24/2023)', 'url': MAP},
      {'label': 'City of Sioux Falls: Health Laboratory', 'url': SF},
      {'label': 'Mid Continent Testing Labs: Private Well Testing', 'url': MCTL},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('south-dakota', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed south-dakota from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', '; '.join(l['accredited_for']))
