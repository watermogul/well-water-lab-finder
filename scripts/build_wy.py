"""Wyoming: EPA Region 8 "EPA Region 8 Certified Drinking Water Laboratories in Wyoming" (one-page PDF matrix, "Current as of
February 2026", footer 2/17/2026; PDF created 2026-02-17, Last-Modified 2026-02-18; md5 d59b28952307cb2261a8bd773f6b159a),
linked from https://www.epa.gov/region8-waterops/certified-drinking-water-laboratories-systems-wyoming-and-tribal-lands-epa-region
(page "Last updated on February 18, 2026"). Wyoming has no state drinking-water lab certification program; EPA Region 8 certifies
Wyoming labs analyte by analyte. Fetched 2026-11-20. Replaces the thin /labs/wyoming/ state-guide with a full listing.

The PDF is a wide analyte matrix. The rows below were transcribed by hand from a 220-dpi render and cross-checked against
`pdftotext -bbox` mark positions (62 marks: X / D / C / Fl). The builder asserts the PDF md5 and 12 labs, so a new list fails loudly.
Contact names and e-mail addresses printed on the EPA list are not published here (site convention); phone numbers are.

SRC_DIR (not committed; all fetched 2026-11-20) holds: wy_lablist.pdf, epa_r8_wy.html, wdh_water.html (WDH Water Testing page),
factsheet_p1.png (WPHL Water Fact Sheet, MediaLab render), kyw.html (WDEQ Know Your Well), wda_*.html / wda_*.pdf (WDA Analytical
Services Laboratory pages, fee list effective March 1, 2021), teton.html (Teton County Water Lab), tcd.html (Teton Conservation
District well test kits), sw_fee.html / sw_lab.html (Sweetwater County Environmental Health), pinedale.html (Town of Pinedale lab)."""
import os, sys, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-wy')
V = '2026-11-20'
more_lib.V = V
PDF = 'https://www.epa.gov/system/files/documents/2026-02/20260211_wy_r8ic_lablist.pdf'
PAGE = 'https://www.epa.gov/region8-waterops/certified-drinking-water-laboratories-systems-wyoming-and-tribal-lands-epa-region'
SN = 'EPA Region 8: Certified Drinking Water Laboratories in Wyoming (PDF, current as of February 2026)'
SD = '2026-02-17'  # footer date printed on the PDF ("Current as of February 2026")
WDH = 'https://health.wyo.gov/publichealth/lab/microbiology-lab/water/'
WDH_FACT = 'https://www.medialab.com/dv/dl.aspx?d=1591644&dh=2aedd10d1e6e&u=44411&uh=c221d4d5a48f'
KYW = 'https://deq.wyoming.gov/water-quality/groundwater/know-your-well/'
WDA_WT = 'https://agriculture.wy.gov/index.php?section=water-testing'
WDA_FAQ = 'https://agriculture.wy.gov/index.php?section=asl-faqs'
WDA_FEES = 'https://agriculture.wy.gov/corecode/uploads/document6/uploaded_pdfs/corecode/labpricelist3121_1269.pdf'
TETON = 'https://tetoncountywy.gov/1079/Water-Lab'
TCD = 'https://www.tetonconservation.org/well-test-kits'
SW_FEE = 'https://www.sweetwatercountywy.gov/boards/district_board_of_health/environmental_health/fee_schedule.php'
SW_LAB = 'https://www.sweetwatercountywy.gov/boards/district_board_of_health/environmental_health/lab_schedule.php'
PINE = 'https://www.townofpinedale.us/laboratory'
ENERGY = 'https://www.energylab.com/'
PACE = 'https://www.pacelabs.com/'

pdf = os.path.join(SRC_DIR, 'wy_lablist.pdf')
assert hashlib.md5(open(pdf, 'rb').read()).hexdigest() == 'd59b28952307cb2261a8bd773f6b159a', 'EPA R8 Wyoming PDF changed: re-transcribe'

# Matrix columns as printed. Microbiology: D = detect (qualitative), C = count (quantitative).
def micro(ec=None, tc=None, fc=None, hpc=False):
    out = []
    lab = {'D': 'detect', 'C': 'count', 'DC': 'detect + count'}
    if tc: out.append('Total coliform (%s)' % lab[tc])
    if ec: out.append('E. coli (%s)' % lab[ec])
    if fc: out.append('Fecal coliform (%s)' % lab[fc])
    if hpc: out.append('Heterotrophic plate count')
    return out

RAD = ['Gross alpha', 'Gross beta', 'Radium-226', 'Radium-228', 'Uranium']
ROWS = [
 # name, address, city, phone printed (contact line), cert end date(s), chips, group
 dict(name='Wyoming Public Health Laboratory', listed='Wyoming Public Health Lab', address='208 S. College Drive, Cheyenne, WY 82009', city='Cheyenne',
      phone='307-777-7431', end='12/31/2026', chips=micro(ec='D', tc='D'), group='main', order=-1),
 dict(name='Wyoming Department of Agriculture Analytical Services Laboratory', listed='Wyoming Dept of Agriculture Analytical Services Laboratory',
      address='1174 Snowy Range Road, Laramie, WY 82070', city='Laramie', phone='307-742-2984', end='6/30/2027',
      chips=['Copper & lead', 'Fluoride (only, of the cyanide/fluoride column)', 'Metals (one column; analytes not itemized)', 'Nitrate & nitrite'] + micro(ec='DC', tc='D', hpc=True),
      group='main', order=0),
 dict(name='Teton County Water Laboratory', address='460 East Pearl St, Jackson, WY 83001', city='Jackson', phone='307-733-6401',
      end='12/31/2028', chips=micro(ec='D', tc='D', hpc=True), group='main', order=1),
 dict(name='Sweetwater County Health Department', address='333 Broadway, Suite 010, Rock Springs, WY 82901', city='Rock Springs', phone='307-872-3930',
      end='12/31/2026', chips=micro(ec='DC', tc='DC'), group='main', order=1),
 dict(name='Town of Pinedale Microbiology Lab', address='69 Pinedale South Road, PO Box 709, Pinedale, WY 82941', city='Pinedale', phone='307-367-2348',
      end='12/10/2028', chips=micro(ec='DC', tc='DC', fc='C'), group='main', order=1),
 dict(name='Energy Laboratories Inc (Casper)', listed='Energy Laboratories Inc', address='2393 Salt Creek Highway, PO Box 247, Casper, WY 82601', city='Casper',
      phone='307-235-0515', end='6/30/2026 (chemistry and radionuclides) and 3/31/2026 (microbiology)',
      chips=['Fluoride (only, of the cyanide/fluoride column)', 'Nitrate & nitrite'] + RAD + ['Carbofuran', 'Diquat', 'Glyphosate', 'Oxamyl (Vydate)'] + micro(ec='DC', tc='DC', hpc=True),
      group='main', order=2),
 dict(name='Energy Laboratories Inc (Gillette)', listed='Energy Laboratories Inc', address='400 W. Boxelder Rd., Gillette, WY 82718', city='Gillette',
      phone='307-686-7175', end='12/31/2026', chips=micro(ec='D', tc='D'), group='main', order=2),
 dict(name='Pace Analytical Services LLC WY', address='1673 Terra Avenue, Sheridan, WY 82801', city='Sheridan', phone='307-461-4938',
      end='12/31/2026', chips=['Copper & lead', 'Cyanide & fluoride', 'Metals (one column; analytes not itemized)', 'Nitrate & nitrite', 'Uranium'] + micro(ec='DC', tc='DC', hpc=True),
      group='main', order=2),
 dict(name='Cheyenne Board of Public Utilities', address='1821 Happy Jack Road, Cheyenne, WY 82009', city='Cheyenne', phone='(307) 635-7693',
      end='12/15/2027', chips=micro(ec='D', tc='D'), group='public'),
 dict(name='Lincoln Water Quality Lab', address='416 South Washington St, PO Box 310, Afton, WY 83110-0310', city='Afton', phone='307-885-9698',
      end='10/13/2027', chips=micro(ec='D', tc='D'), group='public'),
 dict(name='National Park Service Mammoth Water Quality Control Lab', address='PO Box 168, Mammoth Hot Springs, WY 82190', city='Mammoth Hot Springs',
      phone='307-699-3675', end='12/31/2028', chips=micro(ec='DC', tc='DC'), group='public'),
 dict(name='Sage West Healthcare - Lander', listed='Sage West Healthcare - Lander (formerly Lander Regional Hospital)', address='1320 Bishop Randall Dr, Lander, WY 82520',
      city='Lander', phone='307-335-6246', end='12/31/2026', chips=micro(ec='D', tc='D'), group='public'),
]
assert len(ROWS) == 12

EXTRA = {
 'Wyoming Public Health Laboratory': dict(website=WDH, s2=(WDH, 'Wyoming Department of Health: Water Testing page and WPHL Water Fact Sheet (fetched 2026-11-20)'),
   pre='EPA lists the lab contact\'s line, 307-777-6066; the phone shown is the lab\'s main number from the Wyoming Department of Health page. ',
   note='This is the state public health lab, and it tests private wells. The Wyoming Department of Health page says WPHL "is accepting samples from both private individuals and private businesses," including "rural homeowners that would like to test their domestic wells." It tests total coliform and E. coli only. Its undated Water Fact Sheet says: open an account with the customer information sheet; "Cost is $8.00 per sample"; the lab provides the bottle, mailing container and request form (samples in any other container are rejected); samples are accepted until 4:00 PM Monday-Thursday, not on Fridays or before a holiday, and must arrive within 30 hours of collection; results are Satisfactory or Unsatisfactory after 24 hours, and the lab phones you if the result is unsatisfactory. For nitrate or metals, the fact sheet says WPHL refers you to other EPA-certified labs. Address on the WDH page: Combined Laboratories Facility, 208 South College Drive, Cheyenne, WY 82002; new accounts and testing: (307) 777-7544.'),
 'Wyoming Department of Agriculture Analytical Services Laboratory': dict(website=WDA_WT, s2=(WDA_FEES, 'WDA Analytical Services Laboratory FAQ, Water Testing page and price list (effective March 1, 2021; fetched 2026-11-20)'),
   pre='EPA prints the street as "Snowy Ridge Road"; the Wyoming Department of Agriculture and Wyoming DEQ both give 1174 Snowy Range Road (shown). ',
   note='The lab\'s FAQ says it will "analyze most sample types for the general public on a fee basis," and asks first-time submitters to call (307) 742-2984 for a price quote, bottles and sampling instructions before collecting. The fee list linked from its Fees page is headed "WDA ASL 2021 Price List" (effective March 1, 2021): Property Transfer Package $40 ($55 with total coliform), Rural Health Package $70 ($85 with total coliform), Development Package $100 ($115), Comprehensive Water Package $225 ($240; its metals list includes arsenic, lead and uranium), total coliform presence/absence alone $15. The lab\'s FAQ calls this the "most up to date fee schedule," but it is over five years old, so confirm the price when you call. EPA\'s list gives it one "METALS" tick and does not say which metals; ask whether it is certified for the specific metal you need (for example arsenic).'),
 'Teton County Water Laboratory': dict(website=TETON, s2=(TETON, 'Teton County Water Lab page (fetched 2026-11-20)'),
   pre='EPA lists the lab contact\'s line, 307-732-8463; the phone shown is the number Wyoming DEQ and Teton Conservation District give for the lab. Wyoming DEQ gives 460 East Pearl Ave., PO Box 937, Jackson. ',
   note='Teton County\'s Water Lab page says it tests "public/private drinking water" for harmful bacteria. Drinking-water samples are taken every Monday and Tuesday (not county holidays) and must arrive before 2 p.m.; no drinking-water testing in weeks when a county holiday falls on a Monday, Tuesday or Wednesday. Fee: "$25 - Drinking Water Testing." (Teton Conservation District\'s page says the bacteria test is $20; the county\'s own fee schedule says $25.)'),
 'Sweetwater County Health Department': dict(website=SW_LAB, s2=(SW_FEE, 'Sweetwater County Environmental Health: Water Lab Schedule and Fee Schedule pages (fetched 2026-11-20)'),
   note='Sweetwater County Environmental Health\'s fee schedule lists "In-County Bacteriological Water Sample Analysis" at $30 and out-of-county at $40. Its Water Lab Schedule says the lab is open Monday and Tuesday 8 am-5 pm and Wednesday 8 am-3 pm (closed Thursday and Friday); samples must be collected in its bottles; the test takes 24 hours and is started at 3 pm Monday-Wednesday. Fax (307) 872-3981. The pages do not say "private well" in so many words, so mention it when you call.'),
 'Town of Pinedale Microbiology Lab': dict(website=PINE, s2=(PINE, 'Town of Pinedale: Microbiology Testing Laboratory page (fetched 2026-11-20)'),
   pre='EPA prints 69 Pinedale South Road; the town\'s own page and Wyoming DEQ give 55 Pinedale South Road. ',
   note='The town\'s lab page says it is EPA certified for SM9223B and SM9222D (coliforms, E. coli, fecal coliforms) and posts fees: total coliform and E. coli presence/absence $35, enumeration $50. Payment is due before testing unless you have an account (cash, check, most cards). Receiving hours: Tuesday and Wednesday 9 AM-1 PM. Results within one work week by e-mail; the lab calls only if bacteria are detected. Its page has advice for private well owners on E. coli-positive results.'),
 'Energy Laboratories Inc (Casper)': dict(website=ENERGY,
   pre='Both certification end dates printed on EPA\'s February 2026 list (March 31, 2026 for microbiology and June 30, 2026 for the rest) have passed, and EPA has not posted a newer list. We could not confirm from EPA whether this lab\'s Wyoming certifications were renewed; ask the lab for its current certificate before relying on it for a regulatory or real-estate sample. Wyoming DEQ\'s Know Your Well lab list (for homeowners) includes Energy Labs Casper with a toll-free number, (888) 235-0515. ',
   note=None),
 'Energy Laboratories Inc (Gillette)': dict(website=ENERGY,
   pre='Wyoming DEQ\'s Know Your Well lab list includes Energy Labs Gillette with ZIP 82714 and toll-free (866) 686-7175. ', note=None),
 'Pace Analytical Services LLC WY': dict(website=PACE,
   pre='The Wyoming Department of Health water page lists "Pace Labs (Gillette and Sheridan)" as an additional water testing lab. Wyoming DEQ\'s homeowner list names Pace\'s Billings, Montana lab and, separately, "Intermountain Laboratory" at 1633 Terra Ave, Sheridan; we found no primary source tying the two Sheridan names together. EPA\'s list gives one "METALS" tick and does not say which metals. ', note=None),
 'Lincoln Water Quality Lab': dict(pre='The contact e-mail EPA prints is a Town of Afton (aftonwyoming.gov) address. ', note=None),
}
PUB_NOTE = 'We found no page from this lab saying it takes samples from private-well owners. Call first.'

labs = []
for r in ROWS:
    ex = EXTRA.get(r['name'], {})
    listed = r.get('listed', r['name'])
    parts = []
    if listed != r['name']: parts.append('Listed by EPA as "%s".' % listed)
    parts.append('EPA certification end date printed on the list: %s.' % r['end'])
    detail = ' '.join(parts) + (' ' + ex['pre'].strip() if ex.get('pre') else '')
    lab = dict(name=r['name'], address=r['address'], city=r['city'], phone=clean_phone(r['phone']), accredited_for=r['chips'],
               detail=detail, group=r['group'], source_name=SN, source_url=PDF, source_date=SD, last_verified=V)
    if ex.get('website'): lab['website'] = ex['website']
    if ex.get('note'): lab['note'] = ex['note']
    elif r['group'] == 'public': lab['note'] = PUB_NOTE
    if ex.get('s2'): lab['source_url_2'], lab['source_name_2'] = ex['s2']
    if r['name'] in ('Energy Laboratories Inc (Casper)', 'Energy Laboratories Inc (Gillette)'):
        lab['source_url_2'], lab['source_name_2'] = KYW, 'Wyoming DEQ Know Your Well: Find a Laboratory (fetched 2026-11-20)'
    if r['name'] == 'Pace Analytical Services LLC WY':
        lab['source_url_2'], lab['source_name_2'] = WDH, 'Wyoming Department of Health: Water Testing page (fetched 2026-11-20)'
    lab['_o'] = r.get('order', 9)
    labs.append(lab)
labs.sort(key=lambda l: ({'main': 0, 'public': 1}[l['group']], l['_o'], l['name']))
for l in labs: del l['_o']
n_main = sum(1 for l in labs if l['group'] == 'main'); n_pub = len(labs) - n_main
assert (n_main, n_pub) == (8, 4)
N_NO3 = [l['name'] for l in labs if 'Nitrate & nitrite' in l['accredited_for']]
assert len(N_NO3) == 3

write_state('wyoming', 'Wyoming', 'WY', labs,
    {'name': SN, 'page_url': PAGE, 'program_url': PAGE,
     'report_date': 'PDF headed "Current as of February 2026" (footer 2/17/2026); fetched November 20, 2026'},
    {
     'title': 'Wyoming certified labs for well water testing (all 12 on EPA Region 8\'s list, Nov 2026)',
     'description': 'All 12 Wyoming labs EPA Region 8 certifies for drinking water (Feb 2026 list), what each is certified for, and the published private-well prices: $8 state lab bacteria test, county and town labs, and the state agriculture lab\'s chemistry packages.',
     'intro': [
      'Wyoming does not certify drinking-water labs itself. EPA Region 8 staff inspect and certify Wyoming labs for particular analytes and methods, and EPA publishes the list as a one-page PDF. We transcribed that PDF on November 20, 2026. It is headed "Current as of February 2026" and lists 12 labs, all in Wyoming. EPA notes that it also "accepts reciprocal certification for laboratories certified in other states," so out-of-state labs certified elsewhere can be used for Wyoming public water systems, but they are not on this list.',
      'The list is written for public water systems; it does not say which labs take homeowner samples. Wyoming DEQ\'s Know Your Well program keeps a separate "Find a Laboratory" list "to assist homeowners," which includes some of these labs and some that are not on EPA\'s Wyoming list (Wyoming Analytical Laboratories in Laramie and Rock Springs, Intermountain Laboratory in Sheridan and Gillette, and labs in Billings, Montana). DEQ says to check prices with each lab and to get bottles and sampling instructions from the lab you choose.',
      'What to test for: Wyoming DEQ recommends testing a private well "for bacteria (e. coli, total coliform) and nitrates every year," and "for arsenic, lead, copper, iron, manganese, sulfate, and total dissolved solids (TDS) every five years." It adds that uranium, radium, selenium and methane are also common in Wyoming groundwater, and that owners near oil and gas development should test for more. DEQ\'s well-owner helpline is 307-777-WELL (9355).',
      'Cheapest published options we found: the Wyoming Public Health Laboratory in Cheyenne tests well water for total coliform and E. coli for $8 a sample (bacteria only). County and town labs in Jackson ($25), Rock Springs ($30 in county) and Pinedale ($35) also post bacteria-test prices. For chemistry, the Wyoming Department of Agriculture lab in Laramie posts water packages from $40 (2021 price list), and Teton Conservation District sells that lab\'s well kits to Teton County residents for $50 ($130 for non-residents). Only three labs on EPA\'s list are certified for nitrate, and one of those (Energy Laboratories, Casper) shows certification end dates that have passed.',
     ],
     'caveats': [
      'EPA\'s list is dated February 2026. Certification end dates are printed per lab; Energy Laboratories in Casper shows March 31, 2026 (microbiology) and June 30, 2026 (chemistry and radionuclides), both past. EPA\'s page says "it is the responsibility of the water system to ensure that the laboratory certification is current for the analyte of interest." Ask the lab for its current certificate.',
      'Chips show exactly what EPA ticked. For bacteria, "detect" means certified for presence/absence methods and "count" for counting methods. EPA has one "METALS" column and does not say which metals, so ask whether a lab is certified for arsenic, uranium or another specific metal.',
      'No lab on EPA\'s Wyoming list is certified for VOCs, and only two (Energy Laboratories, Casper and Pace in Sheridan) are certified for uranium. For these tests you may need a lab certified in another state; Region 8 accepts reciprocal certification.',
      'Bacteria samples have short hold times. The state lab requires samples within 30 hours of collection and does not accept them on Fridays; county and town labs take samples only on certain weekdays (listed under each lab).',
      'The grouping is ours: the first group is labs with a primary source (their own page, the Wyoming Department of Health, or Wyoming DEQ\'s homeowner list) showing they serve the public; the second is the Cheyenne utility lab, the Lincoln Water Quality Lab in Afton, a National Park Service lab and a hospital lab, which may test only their own water.',
      'Contact names and e-mail addresses on EPA\'s list are not shown. Where EPA prints a staff line and the lab publishes a main number, we show the main number and note both. Where addresses differ between EPA and the lab\'s own page, both are noted.',
      'Prices come only from the labs\' or agencies\' own pages, with dates where printed. We did not verify prices for Energy Laboratories, Pace or the second-group labs, so none are shown.',
     ],
     'main_heading': 'Wyoming labs that serve the public',
     'public_heading': 'Utility, water-quality, park and hospital labs on the same list',
     'public_note': 'These labs are certified for bacteria only. EPA\'s list does not say whether they take homeowner samples, and we found no page saying they do. Call first.',
     'chips_label': 'Certified by EPA Region 8 for:',
     'resources': [
      {'label': 'EPA Region 8: Certified drinking water laboratories for systems in Wyoming and on tribal lands', 'url': PAGE},
      {'label': 'EPA Region 8: Certified drinking water labs in Wyoming (PDF, current as of February 2026)', 'url': PDF},
      {'label': 'Wyoming DEQ: Know Your Well (what to test for, Find a Laboratory, understanding results)', 'url': KYW},
      {'label': 'Wyoming Department of Health: Wyoming Public Health Laboratory water testing', 'url': WDH},
      {'label': 'Wyoming Department of Agriculture: Analytical Services Laboratory water testing', 'url': WDA_WT},
      {'label': 'WDA Analytical Services Laboratory price list (PDF, effective March 1, 2021)', 'url': WDA_FEES},
      {'label': 'Teton Conservation District: well test kits', 'url': TCD},
      {'label': 'Teton County Water Lab', 'url': TETON},
      {'label': 'Sweetwater County Environmental Health: water lab schedule', 'url': SW_LAB},
      {'label': 'Town of Pinedale: Microbiology Testing Laboratory', 'url': PINE},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('wyoming', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed wyoming from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', '; '.join(l['accredited_for']))
