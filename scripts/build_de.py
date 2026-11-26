"""Delaware: Division of Public Health (DPH) Office of Drinking Water (ODW) "Laboratory Certification Program" web page
(https://dhss.delaware.gov/dph/homepage/about/sections/hsp/licenses-and-permits/odw/laboratory-certification-program/), section
"Approved Laboratories". Fetched 2026-11-25 (HTML md5 64abeeda165ca1351e4370fcdbcedb46); the page prints no revision date.
ODW lists 17 labs approved "to perform SDWA compliance testing on drinking water samples", by name only (most names link to the
lab's website; one row prints a phone). No addresses or analytes are printed. Replaces the thin /labs/delaware/ state-guide
(which said the old dwlabcert.html URL was blocked on 2026-11-02).

Delaware Public Health Laboratory (DPHL) is not on ODW's list (it is the state primacy lab) but is the homeowner route: DPH gives
private well owners free bacteria + chemistry kits. Addresses/phones for listed labs come only from the page ODW links to (or the
lab's own site) where it names one location; where the lab has several sites and ODW does not say which, no address is shown.

SRC_DIR (not committed; all fetched 2026-11-25): odw-labcert.html, pdw.html (DPH Private Drinking Water, "last updated 4/24"),
envlab.html (Environmental Laboratory, "last updated 12/23"), bact.html (Bacteriological Laboratory), odwcontact.html (DPH contact
page), prvtwatertestforms.pdf (private well forms, Rev 8/9/23), watertest.pdf (ODW results brochure, older; $4 kits),
watertestperformed.pdf, ODW_SERV_PUB_ENG_0323.pdf, news2023_webfetch.txt (news.delaware.gov 2023-08-31 release; curl rejected,
read via WebFetch), labs/*.html (lab pages ODW links to), labs/bsc_webfetch.txt (bsclab.com TLS-fails for curl; read via WebFetch)."""
import os, sys, re, html, hashlib, json
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-de')
V = '2026-11-25'
more_lib.V = V
PAGE = 'https://dhss.delaware.gov/dph/homepage/about/sections/hsp/licenses-and-permits/odw/laboratory-certification-program/'
SN = 'Delaware DPH Office of Drinking Water: Laboratory Certification Program, "Approved Laboratories" (web page, no revision date printed)'
PDW = 'https://dhss.delaware.gov/dph/homepage/about/sections/ehdishome/labs/environmental-laboratory/private-drinking-water/'
ENVLAB = 'https://dhss.delaware.gov/dph/homepage/about/sections/ehdishome/labs/environmental-laboratory/'
BACT = 'https://dhss.delaware.gov/dph/homepage/about/sections/ehdishome/labs/environmental-laboratory/bacteriological-laboratory/'
FORMS = 'https://dhss.delaware.gov/wp-content/uploads/sites/12/dph/pdf/prvtwatertestforms.pdf'
WTEST = 'https://dhss.delaware.gov/wp-content/uploads/sites/12/dph/pdf/watertest.pdf'
TESTS = 'https://dhss.delaware.gov/wp-content/uploads/sites/12/dph/pdf/watertestperformed.pdf'
NEWS = 'https://news.delaware.gov/2023/08/31/dph-launches-new-financial-aid-program-for-private-well-owners-offers-free-water-testing-kits-to-delaware-residents/'
SURVEY = 'https://survey123.arcgis.com/share/9c4a230cbb7d4d82bad446fcb4c95f70?portalUrl=https://dnrec.maps.arcgis.com'
ODW = 'https://dhss.delaware.gov/dph/homepage/about/sections/hsp/licenses-and-permits/odw/'

p = os.path.join(SRC_DIR, 'odw-labcert.html')
assert hashlib.md5(open(p, 'rb').read()).hexdigest() == '64abeeda165ca1351e4370fcdbcedb46', 'ODW page changed: re-check rows'
src = open(p, encoding='utf-8', errors='ignore').read()
i = src.find('Approved Laboratories'); sec = src[i:src.find('</ul>', i)]
txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', sec)))
items = re.findall(r'<li[^>]*>(.*?)</li>', sec, flags=re.S)
assert len(items) == 17, len(items)
for f, want in [('pdw.html', 'at no charge'), ('pdw.html', 'last updated 4/24'), ('envlab.html', '$2.00 each'), ('bact.html', 'free private drinking water testing kits')]:
    assert want in html.unescape(open(os.path.join(SRC_DIR, f), errors='ignore').read()), (f, want)

NOHOME = 'ODW\'s list does not say whether this lab takes homeowner samples, and we found no page from the lab saying so. Call first and ask about bottles, shipping and hold times.'
NOADDR = 'ODW prints the name only; location not stated'
# (name as printed, display name, address, city, phone, website ODW links to, group, note, source2)
ROWS = [
 ('Aerobiology Lab Associates', None, NOADDR, '', None, None, 'limited',
  'ODW links this name to aerobiology.net, but on 2026-11-25 that address served only a redirect to a "/lander" page, not a lab site, so we do not link it. ' + NOHOME, None),
 ('Alloway', None, 'Ohio (Alloway\'s contact page lists offices in Lima, Mansfield, Marion and Columbus; ODW does not say which)', 'Ohio', None,
  'https://www.alloway.com/sampling-analysis/drinking-water', 'limited', NOHOME, ('https://www.alloway.com/contact', 'Alloway: Contact page (fetched 2026-11-25)')),
 ('ALS Environmental – Middletown', 'ALS Environmental (Middletown)', 'Middletown, PA (per the ALS link on ODW\'s list; street address not confirmed)', 'Middletown', None, None, 'limited',
  'ODW links this name to an ALS page for a Middletown, Pennsylvania environmental lab, but that link returned an error (HTTP 500) on 2026-11-25, so we show no street address. ' + NOHOME, None),
 ('Alpha Analytical, LLC', None, NOADDR, '', '800-624-9220', 'https://alphalab.com/', 'limited',
  'Phone is the number on Alpha\'s home page. ' + NOHOME, ('https://alphalab.com/', 'Alpha Analytical home page (fetched 2026-11-25)')),
 ('Analytical Services, Inc.', None, '130 Allen Brook Lane, Williston, VT 05495', 'Williston', '800-723-4432',
  'https://analyticalservices.com/water.html', 'limited',
  'The page ODW links to describes ASI as a water microbiology lab (Cryptosporidium/Giardia, Legionella, viruses, microscopic particulate analysis); address and phone are from ASI\'s contact page. ' + NOHOME,
  ('https://analyticalservices.com/contact-asi.html', 'Analytical Services, Inc.: Contact page (fetched 2026-11-25)')),
 ('Brandywine Science Center, Inc.', None, '204 Line Rd, Kennett Square, PA 19348', 'Kennett Square', '610-444-9850', 'https://bsclab.com/', 'main',
  'BSC\'s home page says it offers testing to "industry, municipalities, real estate and private sector water supplies," and prints "Pennsylvania DEP # 1500301 Delaware DCNR# PA 152". No prices posted.',
  ('https://bsclab.com/', 'Brandywine Science Center home page (read 2026-11-25)')),
 ('Chesapeake Environmental Lab', None, '302 Love Point Road, Stevensville, MD 21666', 'Stevensville', None,
  'https://chesapeakeenvironmentallab.com/', 'main',
  'The lab\'s site says it does water analysis "for homeowners, businesses, municipalities" and "well & septic inspections for the real estate industry," and that "CEL is also certified in Delaware." It prints its phone as 1-800-300-TEST. No prices posted.',
  ('https://chesapeakeenvironmentallab.com/contact/', 'Chesapeake Environmental Lab: home and contact pages (fetched 2026-11-25)')),
 ('EMSL Analytical', None, NOADDR, '', None, None, 'limited',
  'ODW links this name to fdaimportdetention.com, which returned an error (HTTP 500) on 2026-11-25. EMSL runs labs in several states and ODW does not say which one is approved. ' + NOHOME, None),
 ('Eurofins Eaton Analytical', None, NOADDR, '', None, None, 'limited',
  'ODW links this name to a Eurofins page that returned 404 on 2026-11-25 (redirected to eurofins.com), so we do not link it or show a location. ' + NOHOME, None),
 ('Eurofins Eaton Analytical – South Bend', 'Eurofins Eaton Analytical (South Bend)', 'South Bend (per ODW\'s list; street address not printed)', 'South Bend', None, None, 'limited',
  'ODW links this name to Eurofins\' South Bend lab page, which returned 404 on 2026-11-25. ' + NOHOME, None),
 ('Florida Radiochemistry Services, Inc.', None, NOADDR, '', '407-382-7733', None, 'limited',
  'ODW prints "Call 407-382-7733" and no website. A radiochemistry lab (radioactivity tests). ' + NOHOME, None),
 ('Pace Analytical Services – Melville NY', 'Pace Analytical Services (Melville, NY)', '575 Broad Hollow Rd, Melville, NY 11747-5076', 'Melville', '516-370-6000',
  'https://www.pacelabs.com/company/lab-results/melville-laboratory/', 'limited', NOHOME,
  ('https://www.pacelabs.com/company/lab-results/melville-laboratory/', 'Pace: Melville laboratory page (ODW\'s link redirects here; fetched 2026-11-25)')),
 ('Pace Analytical Services – Ormond Beach FL', 'Pace Analytical Services (Ormond Beach, FL)', '8 East Tower Circle, Ormond Beach, FL 32174', 'Ormond Beach', '386-672-5668',
  'https://www.pacelabs.com/company/lab-results/ormond-beach-laboratory/', 'limited', NOHOME,
  ('https://www.pacelabs.com/company/lab-results/ormond-beach-laboratory/', 'Pace: Ormond Beach laboratory page (ODW\'s link redirects here; fetched 2026-11-25)')),
 ('Pace Analytical Services – Williamsport PA', 'Pace Analytical Services (Williamsport, PA)', '2829 Reach Rd, Williamsport, PA 17701', 'Williamsport', '570-326-4001',
  'https://www.pacelabs.com/company/lab-results/williamsport-laboratory/', 'limited', NOHOME,
  ('https://www.pacelabs.com/company/lab-results/williamsport-laboratory/', 'Pace: Williamsport laboratory page (ODW\'s link redirects here; fetched 2026-11-25)')),
 ('PFAS Solutions', None, 'New Castle, DE 19720', 'New Castle', '302-715-3180', 'https://www.pfasolutions.org/', 'limited',
  'A Delaware lab focused on PFAS ("forever chemicals") analysis and treatment; its site names the Stroud Water Research Center and the University of Delaware as partners. City and phone are from its contact page (no street address printed). ' + NOHOME,
  ('https://www.pfasolutions.org/contact', 'PFAS Solutions: Contact page (fetched 2026-11-25)')),
 ('Suburban Testing Labs', None, NOADDR, '', None, 'https://spllabs.com/environmental-laboratories/', 'limited',
  'ODW\'s link (a suburbantestinglabs.com page about environmental labs in Reading, Pennsylvania) now redirects to SPL\'s environmental-laboratories page; we did not confirm the current name or address. ' + NOHOME, None),
 ('Water Testing Laboratories of MD, Salisbury/Stevensville', 'Water Testing Laboratories of Maryland', 'Salisbury / Stevensville (per ODW\'s list; street address not printed)', 'Stevensville', '410-643-7711',
  'https://wtlmd.com/', 'main',
  'ODW\'s link (a wastewater-pricing page) returned 404 on 2026-11-25; the lab\'s home page offers "Drinking Water Testing for Real Estate Transfers" and testing of "tap water or well water," says it has served "Maryland, Delaware, Northern Virginia and Washington DC" since 1975 together with Chesapeake Labs, and prints a Maryland phone of 410-643-7711 (Virginia 703-250-7711). No prices checked.',
  ('https://wtlmd.com/', 'Water Testing Labs of Maryland home page (fetched 2026-11-25)')),
]
assert len(ROWS) == 17
for r in ROWS:
    assert r[0] in txt, r[0]

labs = [dict(
    name='Delaware Public Health Laboratory (free state kits)', address='30 Sunnyside Rd., Smyrna, DE 19977', city='Smyrna', phone=clean_phone('302-802-5000'),
    accredited_for=['Total coliforms', 'E. coli', 'Nitrate', 'Nitrite', 'Iron', 'Fluoride', 'Alkalinity', 'pH', 'Chloride', 'Sulfate', 'Sodium', 'Hardness'],
    detail='Not on ODW\'s approved list: DPHL is the state lab ("EPA State Primacy Water Laboratory") that tests the free private-well kits. Address and main phone are from the private-well sample forms (Rev 8/9/23) and DPH\'s contact page.',
    note='DPH says test kits "for private drinking water are available for pickup and drop-off for testing at no charge," Monday-Friday 8:00 AM-4:30 PM, "for private well owners." Pick-up points on that page: University Office Plaza-Chopin Building, Suite 105, Newark; the Public Health Laboratory, Smyrna; James W. Williams Building, Suite 105 (302-744-1220); Stockley Center, Georgetown. (The 2023 forms and news release list Thomas Collins Building, Dover, and Thurman Adams State Service Center, Georgetown, instead, so call first.) Do not collect on Friday, Saturday or Sunday; run the cold water five minutes, fill from a bathroom sink or tub (not the kitchen), and return the sample to an EHFS office by 9:00 AM the day you collect it. Forms say bacteria results are mailed in 1-2 weeks and chemical results in 2-3 weeks, and are marked "PRIVATE HOMEOWNER USE ONLY - NOT FOR REAL ESTATE USE." Questions about results: DPH Health Systems Protection, 302-744-4830. DPHL does not test private wells for other contaminants unless ODW submits the sample.',
    group='main', website=PDW, source_name='Delaware DPH: Private Drinking Water page ("last updated 4/24")', source_url=PDW, source_date='2024-04',
    source_url_2=FORMS, source_name_2='DPH private well water sample forms (PDF, Rev 8/9/23)', last_verified=V)]
for (nm, disp, addr, city, ph, web, grp, note, s2) in ROWS:
    disp = disp or nm
    d = 'Listed by ODW as "%s".' % nm if disp != nm else 'Listed by ODW by name only.'
    d += ' ODW does not list which tests the lab is approved for; ask for its Delaware approval for the specific test you need.'
    lab = dict(name=disp, address=addr, city=city, phone=clean_phone(ph), accredited_for=[], detail=d, note=note, group=grp,
               source_name=SN, source_url=PAGE, source_date=V, last_verified=V)
    if web: lab['website'] = web
    if s2: lab['source_url_2'], lab['source_name_2'] = s2
    labs.append(lab)
from collections import Counter
assert Counter(l['group'] for l in labs) == Counter({'main': 4, 'limited': 14})

write_state('delaware', 'Delaware', 'DE', labs,
    {'name': SN, 'page_url': PAGE, 'program_url': PDW, 'report_date': 'web page, no revision date printed; fetched November 25, 2026'},
    {
     'title': 'Delaware well water testing: free state kits and all 17 ODW-approved labs (Nov 2026)',
     'description': 'Delaware DPH gives private well owners free bacteria and chemistry test kits (nitrate, fluoride, sodium, iron and more). Plus all 17 labs on the Office of Drinking Water\'s approved list, with which ones serve homeowners.',
     'intro': [
      'The cheapest way to test a Delaware well is the state\'s own kit. The Division of Public Health (DPH) says test kits for private well owners "are available for pickup and drop-off for testing at no charge." One kit has two bottles: a bacteria bottle (total coliforms and E. coli) and a chemistry bottle (nitrate, nitrite, iron, fluoride, alkalinity, pH, chloride, sulfate, sodium and hardness). The Delaware Public Health Laboratory in Smyrna tests them.',
      'For anything else (arsenic, lead, VOCs, pesticides, PFAS, radioactivity), you need a commercial lab. DPH says the state lab "does not test private drinking water wells for non-prescribed chemical or bacterial contaminants unless the DE Office of Drinking Water submits the sample." The Office of Drinking Water (ODW) publishes a list of 17 approved labs. We copied it on November 25, 2026; it prints no revision date, gives names only (no addresses or test lists), and says the labs are approved "to perform SDWA compliance testing" for public water systems. We checked each lab\'s linked website for a location and for any sign that it serves homeowners.',
      'What and when to test: DPH says EPA and CDC both recommend annual sampling, and to test more often if someone in the home is pregnant or nursing, the water is used for infant formula, a neighbor finds a dangerous contaminant, the taste, odor, color or clarity changes, or after repairing or replacing any part of the well or plumbing. The state kit "WILL NOT be analyzed for compounds that may be in your water due to a spill or environmental release"; if you suspect that, DPH says to contact DNREC and consider bottled water for drinking and cooking.',
      'Help with treatment: in August 2023 DPH announced a financial-assistance program for private well owners whose state-lab results show too much total coliform, E. coli, fluoride, nitrite or (for people on severely salt-restricted diets) sodium, with proof of enrollment in SNAP, WIC, SSI, LIHEAP or TANF. It covers a treatment system, installation and the first year of maintenance, and had a $200,000 budget "until funds expire or additional funding is secured." We did not confirm it is still open; DPH lists DHSS_DPH_PrivateWell@delaware.gov and 302-744-4546 option 9.',
     ],
     'caveats': [
      'Price: DPH\'s current Private Drinking Water page (last updated April 2024), its Bacteriological Laboratory page and the August 2023 news release all say the kits are free. Two older DPH documents still show prices: the Environmental Laboratory page (last updated December 2023) says $2.00 each, and ODW\'s results brochure says $4 per kit. We go with "no charge"; confirm when you pick up.',
      'The state kit forms say "PRIVATE HOMEOWNER USE ONLY - NOT FOR REAL ESTATE USE." For a home sale or loan, use a commercial lab.',
      'ODW\'s list gives names only. Where a lab has several locations and ODW does not say which is approved (Alloway, Alpha, EMSL, Eurofins), or the link was dead, we show no street address. Addresses shown come from the page ODW links to or the lab\'s own contact page, not from ODW.',
      'ODW does not list which tests each lab is approved for. Ask the lab for its Delaware approval for the exact test you need (ODW: 302-741-8630).',
      'Several of ODW\'s links were broken on November 25, 2026: both Eurofins pages and the Water Testing Labs of Maryland pricing page returned 404, the ALS and EMSL links returned server errors, aerobiology.net no longer showed a lab site, and the Suburban Testing Labs link redirects to SPL. We did not link the broken ones.',
      'The grouping is ours: the first group is the state lab plus the three listed labs whose own sites say they test well water for homeowners or real estate; the rest are on ODW\'s list with no homeowner page found. No prices are shown for commercial labs; we did not find any posted.',
     ],
     'main_heading': 'Free state kits and ODW-approved labs that serve homeowners',
     'limited_heading': 'Other labs on ODW\'s approved list (no homeowner service found)',
     'limited_note': 'Approved by Delaware ODW for drinking-water compliance testing. Several are large out-of-state labs or specialty labs (microbiology, radiochemistry, PFAS). We found no page saying they take homeowner samples. Call first.',
     'chips_label': 'Tests in the free DPH kit (bacteria bottle + chemistry bottle):',
     'resources': [
      {'label': 'Delaware ODW: Laboratory Certification Program (approved labs list)', 'url': PAGE},
      {'label': 'Delaware DPH: Private Drinking Water (free test kits for well owners)', 'url': PDW},
      {'label': 'Delaware DPH: Private well water sample forms and instructions (PDF, Rev 8/9/23)', 'url': FORMS},
      {'label': 'Delaware DPH: Private Well Water Sampling Request and Consent Form (online)', 'url': SURVEY},
      {'label': 'Delaware DPH: Environmental Laboratory (how to get your water tested, results)', 'url': ENVLAB},
      {'label': 'Delaware DPH: Interpreting your drinking water results (PDF brochure)', 'url': WTEST},
      {'label': 'Delaware DPH: Drinking water tests at the Public Health Laboratory (PDF)', 'url': TESTS},
      {'label': 'State of Delaware News: DPH financial aid program for private well owners, free kits (Aug 31, 2023)', 'url': NEWS},
      {'label': 'Delaware Office of Drinking Water', 'url': ODW},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('delaware', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed delaware from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'])
