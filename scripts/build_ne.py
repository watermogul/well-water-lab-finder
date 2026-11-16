"""Nebraska: DHHS "Certified Labs" PDF (linked from the DHHS Laboratory Certification page), fetched 2026-11-15.
Replaces the thin /labs/nebraska/ state-guide with a full listing.
SRC_DIR must contain certified_labs.pdf (PDF created 2024-05-22; server Last-Modified Sat, 23 May 2026 03:25:19 GMT;
md5 e7ebffe44e8bccfd9f48876a137a72c4). The builder asserts the PDF text still holds the 5 certificate numbers
and addresses transcribed below, so a changed list fails loudly."""
import os, sys, re, json, subprocess
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-ne')
V = '2026-11-15'
more_lib.V = V
URL = 'https://dhhs.ne.gov/Public%20Health%20Lab%20Documents/certified%20labs.pdf'
SN = 'Nebraska DHHS: Certified Labs (PDF)'
SD = '2024-05-22'  # PDF creation date; the PDF prints no date
CERT_PAGE = 'https://dhhs.ne.gov/Pages/Lab-Certification-Requirements.aspx'
NPHEL = 'https://dhhs.ne.gov/Pages/Public-Health-Lab.aspx'
PRICE_PAGE = 'https://dhhs.ne.gov/Pages/Lab-Price-List.aspx'
FEES = 'https://dhhs.ne.gov/Public%20Health%20Lab%20Documents/AnalyteFees.pdf'
NEWWELL = 'https://dhhs.ne.gov/Public%20Health%20Lab%20Documents/TOTAL%20WATER%20QUALITY%20(NEW%20WELL).pdf'
KITFORM = 'https://www.nebraska.gov/dhhs/water-test-kits/private.html'
DWEE = 'https://dwee.nebraska.gov/news-events/press-releases/all-about-dwee-sample-private-drinking-water-wells'
UNL = 'https://extensionpubs.unl.edu/publication/g1614/na/html/view'
UNL_WT = 'https://water.unl.edu/water-testing'
SWNPHD = 'https://www.swhealth.ne.gov/environmentalhealth/privatewellwater'
CDHD = 'https://www.cdhd.ne.gov/vnews/display.v/ART/66144a8eef54c'
MWL = 'https://midwestlabs.com/environmental'
AAL = 'https://www.amaglab.com/'
AAL_W = 'https://www.amaglab.com/copy-of-feed-3'

txt = subprocess.run(['pdftotext', '-layout', os.path.join(SRC_DIR, 'certified_labs.pdf'), '-'], capture_output=True, text=True, check=True).stdout
flat = re.sub(r'\s+', ' ', txt)
assert len(re.findall(r'NE-04-\d\d', txt)) == 5, re.findall(r'NE-04-\d\d', txt)

COL = 'Total coliform/E. coli (Colilert, SM 9223B)'
rows = [
  dict(cert='NE-04-01', name='Central District Health Department', street='1137 South Locust', cityline='Grand Island, NE 68801', city='Grand Island',
       chips=[COL], group='main', phone='(308) 385-5175',
       note='Takes private-well samples. Its water testing page (fetched 2026-11-15) says to request a sample kit by calling the laboratory office at 308-385-5175 or emailing waterlab@cdhd.ne.gov, recommends testing private wells every year for coliform bacteria, and lists test costs of coliform $27.00 and nitrate, hardness, fluoride and pH $25.00 each. On the DHHS list it is certified only for coliform/E. coli, so ask whether the other tests are certified if you need certified results.',
       s2=(CDHD, 'Central District Health Department: Water Testing page (fetched 2026-11-15)')),
  dict(cert='NE-04-03', name='Enviro Services Inc.', street='818 S. Beltline Hwy East', cityline='Scottsbluff, NE 69361', city='Scottsbluff',
       chips=[COL], group='main', phone=None,
       note='We could not load this lab\'s own website on 2026-11-15, so no phone number, prices or homeowner services are shown. It is on the DHHS list and on the Southwest Nebraska Public Health Department\'s list of certified labs for well owners.',
       s2=(SWNPHD, 'Southwest Nebraska Public Health Dept: Private Well Water (lists Nebraska certified labs)')),
  dict(cert='NE-04-04', name='Metropolitan Utilities District (as printed: "Metropolitan Utilities Districts")', street='2710 Grebe Street', cityline='Omaha, NE 68111', city='Omaha',
       chips=[COL], group='public', phone=None,
       note='This is Omaha\'s public water and gas utility lab. The DHHS list does not say whether it accepts samples from private-well owners, and we found no primary source that says it does. Call first.',
       s2=None),
  dict(cert='NE-04-05', name='Midwest Laboratories, Inc.', street='13611 B Street', cityline='Omaha, NE 68144', city='Omaha',
       chips=['Total coliform/E. coli (Quanti-Tray 2000, SM 9223B)', 'Nitrate as N (EPA 300.0)', 'Nitrite as N (SM 4500-NO2-B)', 'Nitrate/nitrite as N (EPA 353.2)', 'Copper (EPA 200.8)', 'Lead (EPA 200.7, as printed)', 'VOCs (EPA 524.2)', 'Fluoride (EPA 300.0; printed "Floride")'],
       group='main', phone='(402) 334-7770',
       note='DHHS marks this lab "(by reciprocity)". Its environmental testing page (fetched 2026-11-15) lists water packages including W4 (nitrate-nitrite nitrogen by EPA 353.2, total coliform, E. coli) at $38.50, W3 Water Quality (coliform, E. coli, nitrate, hardness, iron, manganese, sodium, fluoride, pH and more) at $82.00, and W5: FHA Loan (total coliform, fecal coliform, E. coli, nitrate, nitrite, lead) at $104.50, and says bacteria samples must be received within 24 hours of sampling. It accepts drop-off Monday through Friday, 8 am to 4 pm, at the Omaha address. Confirm which tests on a package are run under its Nebraska certification.',
       s2=(MWL, 'Midwest Laboratories: Environmental testing packages (fetched 2026-11-15)')),
  dict(cert='NE-04-06', name='American Agricultural Laboratory', street='700 East D Street', cityline='McCook, NE 69001', city='McCook',
       chips=[COL, 'Nitrate/nitrite (EPA 353.2)'], group='main', phone='(308) 345-3670',
       note='Its own website (fetched 2026-11-15) prints the address as 700 West D Street, McCook, and says the lab was acquired by Brookside Laboratories, Inc. on September 1, 2026; the DHHS list predates that, so ask whether its Nebraska certification is unchanged. Its water page lists a "Household Suitability" package (minerals, nitrate, iron, manganese, total coliform and E. coli) and a nitrate plus total coliform/E. coli "purity" package. We did not show its prices because the page does not pair each price clearly with a package.',
       s2=(AAL_W, 'American Agricultural Laboratory: Water analysis packages (fetched 2026-11-15)')),
]
labs = []
for r in rows:
    for piece in (r['cert'], r['street'], r['cityline']):
        assert piece in flat, piece
    lab = dict(name=r['name'], address=r['street'] + ', ' + r['cityline'], city=r['city'], phone=r['phone'],
               accredited_for=r['chips'], group=r['group'],
               detail='Nebraska DHHS certification number %s.' % r['cert'],
               note=r['note'], source_name=SN, source_url=URL, source_date=SD, last_verified=V)
    if r['s2']:
        lab['source_url_2'], lab['source_name_2'] = r['s2']
    labs.append(lab)

# State lab: not on the certified-labs PDF (DHHS runs the program); its own page says it is EPA-certified.
labs.insert(0, dict(
    name='Nebraska Public Health Environmental Laboratory (NPHEL, state lab)',
    address='3701 South 14th Street, Lincoln, NE 68502', city='Lincoln', phone='(402) 471-3935',
    accredited_for=['Not on the DHHS list: EPA-certified state lab (per its own page)'],
    group='main',
    detail='Not on the DHHS certified-labs PDF because DHHS runs the certification program; the NPHEL page says the lab "is certified by the United States Environmental Protection Agency (U.S. EPA)" and is audited on site every three years. Phone shown is the sample-kit line; main laboratory (402) 471-2122.',
    note='Order kits online (Private Citizen Water Test Kit Request Form) or by phone. The kit form says coliform samples must be collected and mailed the same day, Monday through Thursday, and samples more than 30 hours old will not be tested; unused kits not returned within 90 days are billed. The Nebraska Department of Water, Energy and Environment (DWEE) said in a November 18, 2024 notice that bacteria kits cost $17 and nitrate kits $16. NPHEL\'s posted Analyte/Price List is still headed "pricing effective 7/1/13 - 12/31/23" (it lists Colilert coliform/E. coli $15, nitrate/nitrite $16, arsenic $19, uranium $19), and its Total Water Quality (New Well) fee list totals $3,472. Call to confirm current prices. For home loans, NPHEL asks for at least one and preferably two weeks. For help reading private-well results, DWEE: (402) 471-4982.',
    source_name='Nebraska DHHS: Public Health Environmental Lab page', source_url=NPHEL, source_date='2026-11-15',
    source_url_2=PRICE_PAGE, source_name_2='NPHEL Customer Service / Analyte-Price List page',
    last_verified=V))

c = Counter(l['group'] for l in labs)
assert len(labs) == 6 and c['main'] == 5 and c['public'] == 1, c

write_state('nebraska', 'Nebraska', 'NE', labs,
    {'name': SN, 'page_url': URL, 'program_url': CERT_PAGE,
     'report_date': 'PDF prints no date (file created May 22, 2024; server last-modified May 23, 2026); fetched November 15, 2026'},
    {
     'title': 'Nebraska certified labs for well water testing (DHHS list, Nov 2026)',
     'description': 'All 5 labs on Nebraska DHHS\'s certified drinking-water lab list plus the state lab (NPHEL), what each is certified for, published private-well test prices, and how to order a state kit.',
     'intro': [
      'The Nebraska Department of Health and Human Services (DHHS) certifies labs to test public drinking water under Title 179, Chapter 20. Its Laboratory Certification page links one "Certified Labs" PDF. We transcribed it on November 15, 2026. It lists 5 labs, all in Nebraska: three are certified only for total coliform/E. coli, one (American Agricultural Laboratory) also for nitrate/nitrite, and one (Midwest Laboratories, by reciprocity) for bacteria, nitrate, nitrite, copper, lead, VOCs and fluoride. The PDF prints no date; the file was created May 22, 2024.',
      'The state lab is not on that PDF because DHHS runs the program. The Nebraska Public Health Environmental Laboratory (NPHEL) in Lincoln says it is certified by the U.S. EPA, and it sells kits to private well owners. The Nebraska Department of Water, Energy and Environment (DWEE) recommends testing a private well every year for bacteria and nitrate and, in a November 2024 notice, gave kit prices of $17 for bacteria and $16 for nitrate. Order kits online or call (402) 471-3935.',
      'Private wells in Nebraska do not have to be tested by law, with some exceptions such as licensed childcare and foster homes, according to Nebraska Extension. Lenders and county health departments may require a test when a property with a well is sold. Nebraska Extension (NebGuide G1614, revised October 2022) recommends a certified lab when results may be used for a loan, legal action, or before spending a lot on treatment.',
      'Local options: Central District Health Department in Grand Island tests private wells (coliform $27, nitrate $25 on its own page). The Southwest Nebraska Public Health Department hands out free nitrate/nitrite test strips each May and September and says to confirm any problem with a certified lab; it also says some Natural Resources Districts (NRDs) offer testing for well owners.',
     ],
     'caveats': [
      'Certification is per test. Most labs on the DHHS list are certified only for coliform bacteria. If you need certified results for nitrate, arsenic, uranium or anything else, ask the lab before you sample.',
      'The DHHS list is for labs that test public water systems. It does not say which labs take homeowner samples. Where a lab\'s own page says it does, the listing says so and links that page.',
      'Bacteria samples are time-limited: NPHEL will not test coliform samples more than 30 hours old, and Midwest Laboratories says 24 hours. Mail early in the week.',
      'The DHHS PDF is from 2024 and prints no revision date. American Agricultural Laboratory changed owners on September 1, 2026, after the PDF was made. DHHS\'s lab certification manager can confirm the current list: (402) 471-8407.',
      'Prices come only from each lab\'s or agency\'s own page, with the date we checked. NPHEL\'s posted price list is headed with a 2013-2023 pricing period, so its prices may be out of date. Confirm before you send a sample.',
      'The grouping is ours: the first group is labs with a primary source showing they serve or list homeowners (or a commercial lab), the second is a public utility lab.',
     ],
     'main_heading': 'State lab, county health lab and commercial labs',
     'public_heading': 'Public utility lab on the same list',
     'public_note': 'Omaha\'s Metropolitan Utilities District lab is certified for coliform/E. coli. We found no source saying it takes samples from private-well owners. Call first.',
     'chips_label': 'Certification (DHHS list wording unless noted):',
     'resources': [
      {'label': 'Nebraska DHHS: Certified Labs (PDF)', 'url': URL},
      {'label': 'Nebraska DHHS: Laboratory Certification program page', 'url': CERT_PAGE},
      {'label': 'Nebraska Public Health Environmental Laboratory (NPHEL)', 'url': NPHEL},
      {'label': 'NPHEL: Private Citizen Water Test Kit Request Form', 'url': KITFORM},
      {'label': 'NPHEL: Customer Service, Analyte/Price List and kit ordering', 'url': PRICE_PAGE},
      {'label': 'NPHEL: Analyte/Price List (PDF, headed "pricing effective 7/1/13 - 12/31/23")', 'url': FEES},
      {'label': 'NPHEL: Total Water Quality (New Well) fee list (PDF)', 'url': NEWWELL},
      {'label': 'Nebraska DWEE: Sample private drinking water wells (Nov 18, 2024)', 'url': DWEE},
      {'label': 'Nebraska Extension NebGuide G1614: Certified Water Testing Laboratories in Nebraska (rev. Oct 2022)', 'url': UNL},
      {'label': 'UNL Water: Drinking water testing', 'url': UNL_WT},
      {'label': 'Southwest Nebraska Public Health Department: Private well water', 'url': SWNPHD},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('nebraska', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed nebraska from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', l['accredited_for'])
