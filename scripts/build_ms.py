"""Mississippi: MSDH "Water Supply Certification: In-State Labs" page (linked from MSDH's Private Well Water Testing page), fetched 2026-11-17.
Replaces the thin /labs/mississippi/ state-guide with a full listing.
SRC_DIR must contain (all fetched 2026-11-17; not committed):
  certlabs.html  - https://msdh.ms.gov/.../private-well-water-testing/water-supply-certification-labs (CMS updated_at 2026-10-10T18:08:51Z, md5 1d7892abbb10ecc4e13dfc5c0ae8a2b6)
  environmental-laboratory-certification-program.html - MSDH ELCP page (updated_at 2026-09-24T22:26:39Z), same 5 labs
  app_pw.html    - MSDH On-Site Wastewater online application, Private Well Sample ($10 + processing fee)
  mm_msdh_scope.pdf - Micro-Methods' posted MSDH 2026 certificate + scopes (image PDF, read by eye; issued March 6, 2026)
The builder asserts both MSDH pages still hold the 5 labs, addresses and EPA IDs transcribed below, so a changed list fails loudly."""
import os, sys, re, json, html
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-ms')
V = '2026-11-17'
more_lib.V = V
URL = 'https://msdh.ms.gov/safe-food-water-and-housing/water-supply/private-well-water-testing/water-supply-certification-labs'
SN = 'MSDH: Water Supply Certification: In-State Labs'
SD = '2026-10-10'  # page "updated_at" in MSDH's CMS data (2026-10-10 18:08 UTC); the page prints no date
WELL = 'https://msdh.ms.gov/safe-food-water-and-housing/water-supply/private-well-water-testing'
ELCP = 'https://msdh.ms.gov/safe-food-water-and-housing/water-supply/environmental-laboratory-certification-program'
APPLY = 'https://apps.msdh.ms.gov/WasteWaterOnlineApp/ApplicationEntry.aspx?id=pw'
ONSITE = 'https://msdh.ms.gov/safe-food-water-and-housing/on-site-wastewater-1'
DISINF = 'https://msdh.ms.gov/safe-food-water-and-housing/water-supply/private-well-disinfection'
MWON = 'https://extension.msstate.edu/natural-resources/water/mississippi-well-owner-network'
MWON_S = 'https://extension.msstate.edu/natural-resources/water/mississippi-well-owner-network/well-water-sample-instructions'
P3813 = 'https://extension.msstate.edu/publications/testing-residential-private-well-drinking-water-and-understanding-bacteriological-analyses'
NEWS25 = 'https://extension.msstate.edu/news/feature-story/2025/msu-extension-offers-free-water-well-testing-training'
MM = 'https://www.micromethodslab.com/'
MM_SCOPE = 'https://www.micromethodslab.com/MSDH%20Drinking%20Water%202026%20Laboratory%20Scope%20of%20Accreditation%20.pdf'
MM_COL = 'https://www.micromethodslab.com/pdfs/Coliform%20Sampling%20Instructions-web.pdf'
MM_AT = 'https://www.micromethodslab.com/analyticaltesting.html'

def page_text(fn):
    t = open(os.path.join(SRC_DIR, fn), errors='ignore').read()
    m = re.search(r'data-page="([^"]+)"', t)
    d = json.loads(html.unescape(m.group(1)))
    s = json.dumps(d['props']['page']['content'], ensure_ascii=False)
    s = html.unescape(re.sub(r'<[^>]+>|\\n', ' ', s.replace('\\/', '/')))
    return d['props']['page'].get('updated_at'), re.sub(r'\s+', ' ', s)

upd, flat = page_text('certlabs.html')
assert upd.startswith('2026-10-10'), upd
_, flat2 = page_text('environmental-laboratory-certification-program.html')
assert len(re.findall(r'EPA ID: MS\d{5}', flat)) == 5, re.findall(r'EPA ID: MS\d{5}', flat)
assert len(re.findall(r'EPA ID: MS\d{5}', flat2)) == 5
app = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', open(os.path.join(SRC_DIR, 'app_pw.html'), errors='ignore').read())))
assert 'An Invoice of $10 + a processing fee will be emailed within one(1) business day' in app

rows = [
  dict(epa='MS00021', name='Micro-Methods Laboratory', street='6500 Sunplex Drive', cityline='Ocean Springs, MS 39564', city='Ocean Springs',
       phone='(228) 875-6420', printed='Chemistry, Microbiology', group='main', website=MM,
       chips=['Total coliform (SM 9223)', 'E. coli (SM 9223)', 'Heterotrophic plate count (SM 9215 E)', 'Nitrate as N (SM 4110 B)', 'Nitrite as N (SM 4110 B)', 'Lead (EPA 200.8)', 'Copper (EPA 200.8)'],
       detail='MSDH EPA ID MS00021; MSDH list wording: "Chemistry, Microbiology". The test list above is from the MSDH 2026 certificate and scopes the lab posts on its own site (certificate number MS00021, issued January 1, 2026, expires December 31, 2026; scopes dated March 6, 2026; also conductivity and pH as lead/copper support tests).',
       note='Its analytical testing page says it runs total coliform and E. coli on well water, certified by MSDH, for home loan closings. Its coliform sampling sheet says: pick up a sterile container weekdays 8:00 to 4:30; drop off coliform samples Monday through Thursday, 8:00 to 4:00 (none on Friday or the day before a holiday); the sample must reach the lab within 24 hours; the written report should be ready within 48 hours; payment is due with the sample. It also says some lenders require a third-party sampler. Prices are not posted; call the office. When mailing, use the P.O. Box on its chain-of-custody form.',
       s2=(MM_SCOPE, 'Micro-Methods: MSDH 2026 certificate and scopes (PDF, lab-hosted)')),
  dict(epa='MS00013', name='Bonner Analytical Testing, Inc.', street='2703 Oak Grove Road', cityline='Hattiesburg, MS 39402', city='Hattiesburg',
       phone='(601) 264-2854', printed='Microbiology', group='main', website=None,
       chips=['Microbiology (MSDH list wording)'],
       detail='MSDH EPA ID MS00013; MSDH list wording: "Microbiology".',
       note='We could not load this lab\'s website on 2026-11-17 (the server returned an error), so no prices, sample hours or homeowner services are shown. MSDH lists it among the private labs in its certification program. Call to ask whether it takes private-well samples and which bacteria tests it runs.',
       s2=None),
  dict(epa='MS00008', name='City of Meridian Fresh Water Treatment Plant', street='P.O. Box 1430', cityline='Meridian, MS 39302', city='Meridian',
       phone='(601) 484-6836', printed='Microbiology', group='public', website=None,
       chips=['Microbiology (MSDH list wording)'],
       detail='MSDH EPA ID MS00008; MSDH list wording: "Microbiology". MSDH prints a P.O. Box, not a street address.',
       note='A city water-plant lab. We found no source saying it accepts samples from private-well owners. Call first.', s2=None),
  dict(epa='MS00903', name='NASA Environmental Services', street='Building 8100, Room 112C', cityline='Stennis Space Center, MS 39529', city='Stennis Space Center',
       phone='(228) 688-2053', printed='Chemistry, Microbiology', group='public', website=None,
       chips=['Chemistry, Microbiology (MSDH list wording)'],
       detail='MSDH EPA ID MS00903; MSDH list wording: "Chemistry, Microbiology". MSDH does not say which chemistry tests.',
       note='A lab on a federal site (Stennis Space Center). We found no source saying it accepts samples from the public. Call first.', s2=None),
  dict(epa='MS01000', name='Huntington Ingalls, Inc', street='1000 Access Rd, Mail Station 2030-02', cityline='Pascagoula, MS 39568-0149', city='Pascagoula',
       phone=None, printed='Microbiology', group='public', website=None,
       chips=['Microbiology (MSDH list wording)'],
       detail='MSDH EPA ID MS01000; MSDH list wording: "Microbiology". MSDH prints no phone number for this lab.',
       note='The Pascagoula shipyard\'s in-house lab. We found no source saying it accepts samples from the public.', s2=None),
]
labs = []
for r in rows:
    pieces = [r['epa'], r['name'].split(',')[0], r['cityline'], r['printed']] + r['street'].split(', ')
    if r['phone']: pieces.append(r['phone'])
    for piece in pieces:
        assert piece in flat, piece
        assert piece in flat2, ('ELCP', piece)
    lab = dict(name=r['name'], address=r['street'] + ', ' + r['cityline'], city=r['city'], phone=r['phone'],
               accredited_for=r['chips'], group=r['group'], detail=r['detail'], note=r['note'],
               source_name=SN, source_url=URL, source_date=SD, last_verified=V)
    if r['website']: lab['website'] = r['website']
    if r['s2']: lab['source_url_2'], lab['source_name_2'] = r['s2']
    labs.append(lab)

# State program: not on the participating-labs list (MSDH runs the program).
labs.insert(0, dict(
    name='MSDH private well bacteria sampling (Division of On-Site Wastewater; tested at the MSDH Public Health Laboratory)',
    address='Statewide: an MSDH environmentalist samples your well; apply online', city='Jackson', phone='(855) 220-0192',
    accredited_for=['Not on the MSDH list (state program). Tests: total coliform; E. coli if coliform is present (per MSU Extension P3813)'],
    group='main', website=APPLY,
    detail='Not on the participating-labs list because MSDH runs the certification program. Phone is MSDH\'s toll-free On-Site Wastewater Call Center, which helps with the application and online payment.',
    note='MSDH tests private wells for bacteria only. Its online Private Well Sample application (one well per application; not for homes on a public water system) says "An Invoice of $10 + a processing fee will be emailed within one(1) business day." An MSDH environmentalist visits and takes the sample. MSU Extension publication P3813 (2025) says the Public Health Laboratory in Jackson tests for total coliform and, if positive, E. coli, reported as present or absent. For nitrate, arsenic, lead or other chemicals, MSDH says to use a private lab. After disinfecting a well, MSDH\'s disinfection page says samples can go to a county health department the same day for overnight shipment, or straight to the Public Health Laboratory within 28 hours of collection (8:00 to 4:00 Monday through Thursday, 8:00 to 2:00 Friday); analysis normally takes about 24 hours.',
    source_name='MSDH: On-Site Wastewater online application, Private Well Sample (page prints no date; fetched 2026-11-17)', source_url=APPLY, source_date='2026-11-17',
    source_url_2=WELL, source_name_2='MSDH: Private Well Water Testing page (updated 2026-10-10)',
    last_verified=V))

c = Counter(l['group'] for l in labs)
assert len(labs) == 6 and c['main'] == 3 and c['public'] == 3, c

write_state('mississippi', 'Mississippi', 'MS', labs,
    {'name': SN, 'page_url': URL, 'program_url': ELCP,
     'report_date': 'web page, last updated October 10, 2026 (per MSDH\'s site data; the page prints no date); fetched November 17, 2026'},
    {
     'title': 'Mississippi certified labs for well water testing (MSDH list, Nov 2026)',
     'description': 'All 5 labs on MSDH\'s in-state drinking-water lab list, what each is certified for, MSDH\'s $10 private-well bacteria sampling, and MSU Extension\'s free well-water screenings.',
     'intro': [
      'The Mississippi State Department of Health (MSDH) certifies labs to test drinking water for public water systems. Its Private Well Water Testing page links one list of "private water testing laboratories participating in MSDH\'s Drinking Water Lab Certification Program." We transcribed it on November 17, 2026. It lists 5 labs, all in Mississippi. Two are certified for chemistry and microbiology (Micro-Methods Laboratory in Ocean Springs and NASA Environmental Services at Stennis Space Center); three for microbiology only. Only two are commercial labs. The others are a city water plant, a federal-site lab and a shipyard lab. MSDH\'s Environmental Laboratory Certification Program page shows the same 5 labs.',
      'For most well owners the simplest option is MSDH itself. Apply online and an MSDH environmentalist comes to take a bacteria sample from your well. The application says you will be invoiced $10 plus a processing fee. MSDH tests private wells for bacteria only (total coliform, and E. coli if coliform is found). For nitrate, arsenic, lead or other chemicals, MSDH says to use a private lab. Call the On-Site Wastewater Call Center at 1-855-220-0192 for help applying.',
      'Mississippi State University Extension\'s Mississippi Well Owner Network (MWON) holds free workshops for well owners, and well owners can have their water screened for E. coli at each program. Check the calendar on the MWON page and register ahead, or call (662) 325-1788. MWON\'s sample instructions say to collect the sample no more than 12 hours before dropping it off. A 2025 MSU Extension news release on a Tate County workshop also offered total coliform/E. coli screening and, for the first 21 well owners, a PFAS test. A screening is not the same as a certified lab result.',
      'Mississippi does not require private well owners to test. MSU Extension (publication P3813, 2025) recommends testing drinking-water wells at least once a year. If E. coli is found, it says not to drink the water without boiling it first. MSDH publishes a well disinfection procedure; retest after disinfecting.',
     ],
     'caveats': [
      'Certification is per test. MSDH\'s list only says "Chemistry" and/or "Microbiology". The detailed test list on Micro-Methods\' card comes from the MSDH certificate the lab posts on its own site. For any other lab, ask which tests it is certified for before you sample.',
      'MSDH\'s list is for labs that test public water systems. It does not say which labs take homeowner samples. Where a lab\'s own page says it does, the listing says so and links that page.',
      'Out-of-state labs: MSDH does not certify labs outside Mississippi directly. It accepts other states\' certification by reciprocity, but it does not publish a list of those labs, so none are shown here. To check a lab\'s status, MSDH\'s certification office is at (601) 576-7582.',
      'Bacteria samples are time-limited: Micro-Methods says 24 hours from sampling to the lab; MSDH\'s Public Health Laboratory takes direct deliveries up to 28 hours after collection.',
      'Prices come only from each lab\'s or agency\'s own page, with the date we checked. MSDH\'s $10 fee is from its online application and does not include the processing fee. Micro-Methods does not post prices.',
      'The grouping is ours. The first group is MSDH\'s own sampling service and the commercial labs. The second is the utility, federal-site and shipyard labs on the same list.',
     ],
     'main_heading': 'State sampling service and commercial labs',
     'public_heading': 'City water-plant, federal-site and shipyard labs on the same list',
     'public_note': 'MSDH lists these 3 labs as certified, but we found no source saying any of them takes samples from private-well owners. Call first.',
     'chips_label': 'MSDH certification (list wording unless noted):',
     'resources': [
      {'label': 'MSDH: Water Supply Certification: In-State Labs (labs for private well testing)', 'url': URL},
      {'label': 'MSDH: Private Well Water Testing', 'url': WELL},
      {'label': 'MSDH: Apply online for private well water sampling (On-Site Wastewater)', 'url': APPLY},
      {'label': 'MSDH: On-Site Wastewater (Call Center 1-855-220-0192)', 'url': ONSITE},
      {'label': 'MSDH: Environmental Laboratory Certification Program', 'url': ELCP},
      {'label': 'MSDH: Private Well Disinfection', 'url': DISINF},
      {'label': 'MSU Extension: Mississippi Well Owner Network', 'url': MWON},
      {'label': 'MSU Extension: MWON well water sample instructions', 'url': MWON_S},
      {'label': 'MSU Extension P3813: Testing Residential Private Well Drinking Water and Understanding Bacteriological Analyses (2025)', 'url': P3813},
      {'label': 'MSU Extension news (2025): free water well testing and training, Tate County', 'url': NEWS25},
      {'label': 'Micro-Methods Laboratory: Total coliform sampling instructions (PDF)', 'url': MM_COL},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('mississippi', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed mississippi from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', l['accredited_for'])
