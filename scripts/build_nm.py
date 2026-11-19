"""New Mexico: NMED Drinking Water Bureau "Laboratories Certified by NMED-DWB to Analyze Drinking Water Samples for Water Systems
in New Mexico" (Last Updated: 10/26/2026), linked as "Certified Laboratories" from NMED's Private Wells page. Fetched 2026-11-18.
Replaces the thin /labs/new-mexico/ state-guide with a full listing.
SRC_DIR must contain (all fetched 2026-11-18; not committed):
  certlabs.pdf  - https://service.web.env.nm.gov/urls/CbGsmFug (redirects to cloud.env.nm.gov; md5 b2441dc5d2969b7f1b8d6b9c2024b859;
                  PDF created 2026-10-26; the Water Fairs page's "Certified Laboratories" link returns the identical file)
  certlabs.txt  - pdftotext -layout certlabs.pdf
  pw.html       - NMED Private Wells page; freetest.html - NMED Free Well Water Testing; fairs.html - NMED GWQB Water Fairs
  labcert.html  - NMED Drinking Water Lab Certification page
  assist.txt    - NMED GWQB "Laboratories Providing Assistance..." (PDF created 2022-11-21), used only for one phone cross-check
  indepth_webfetch.txt, ets_webfetch.txt, cardinal.html - lab websites (curl TLS failed for the first two; read with WebFetch)
Row highlighting (renewal in progress / provisional) was read from a rendering of the PDF: only NELAnalytical is highlighted
(blue = renewal in progress); no row is yellow (provisional). The builder asserts 44 rows, so a changed list fails loudly."""
import os, sys, re, json, html
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-nm')
V = '2026-11-18'
more_lib.V = V
URL = 'https://service.web.env.nm.gov/urls/CbGsmFug'
SN = 'NMED Drinking Water Bureau: Laboratories Certified by NMED-DWB to Analyze Drinking Water Samples (PDF, last updated 10/26/2026)'
SD = '2026-10-26'
PW = 'https://www.env.nm.gov/drinking_water/private-wells-2/'
CERT = 'https://www.env.nm.gov/drinking_water/lab-certification/'
FREE = 'https://www.env.nm.gov/septic/free-well-water-testing-2/'
FAIRS = 'https://www.env.nm.gov/gwqb/water-fairs/'
CAL = 'https://www.env.nm.gov/events-calendar/'
INDEPTH = 'https://indepthtest.com/'
ETS = 'https://etsnewmexico.com/'
CARD = 'https://cardinallabsnm.com/'
ASSIST = 'https://cloud.env.nm.gov/resources/_translator.php/OGNiZmMzZmNlODBjZDM5MWFlZmNiNTM0ZF82NDM2Mg~~.pdf'

def flat(fn):
    t = open(os.path.join(SRC_DIR, fn), errors='ignore').read()
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))

txt = open(os.path.join(SRC_DIR, 'certlabs.txt'), errors='ignore').read()
assert 'Last Updated: 10/26/2026' in txt
pw, free, fairs, lc = flat('pw.html'), flat('freetest.html'), flat('fairs.html'), flat('labcert.html')
assert 'many of these labs also offer services to private well owners' in pw
assert 'Test your water every spring' in pw and 'Periodic Testing (Every 5 Years) Uranium' in pw
assert 'NMED provides free testing of private domestic wells only for Nitrate, Iron and Fluoride' in free
assert 'NMED will test for arsenic, electrical conductivity, fluoride, iron, nitrate, pH, and sulfate and mail your results in 2-4 weeks' in fairs
assert 'hosts eight water fairs annually' in pw
assert 'Currently, the DWB only certifies microbiological laboratories located in New Mexico' in lc
assert 'DWB is not currently accepting new reciprocity certification applications' in lc
ind = open(os.path.join(SRC_DIR, 'indepth_webfetch.txt')).read()
ets = open(os.path.join(SRC_DIR, 'ets_webfetch.txt')).read()
card = flat('cardinal.html')
assist = open(os.path.join(SRC_DIR, 'assist.txt')).read()
assert 'Diagnostic & Technology Center' in assist and '(575) 434-4944' in assist

ROW = re.compile(r'^(?P<name>\S.*?)\s+(?P<cert>[A-Z]{2}\d{2,5}(?:/NM00)?)\s+(?P<grp>.+?)\s{2,}(?P<loc>[A-Z][A-Za-z .]+, [A-Z]{2})\s{2,}(?P<exp>\d{1,2}/\d{1,2}/\d{4}(?: & \d{1,2}/\d{1,2}/\d{4} \(M, E\))?)\s{2,}(?P<ph>\(\d{3}\) ?\d{3}[- ]\d{4})\s+(?P<k>[YN])\s*$')
rows = []
for line in txt.splitlines():
    m = ROW.match(line)
    if m: rows.append({k: v.strip() for k, v in m.groupdict().items()})
assert len(rows) == 44, len(rows)

LEG = {'M': 'Microbiological (M)', 'E': 'E. coli enumeration (E)', 'IO': 'Inorganics: nitrate, fluoride, cyanide (IO)',
       'HM': 'Heavy metals (HM)', 'Pb/Cu': 'Lead and copper (Pb/Cu)', 'RAD': 'Radiologicals (RAD)',
       'VOC': 'Volatile organic chemicals (VOC)', 'SOC': 'Synthetic organic chemicals (SOC)', 'PFAS': 'PFAS',
       'PFAS (537.1 only)': 'PFAS (EPA 537.1 only)', 'SD': 'Secondaries (SD)', 'DBP': 'Disinfection byproducts (DBP)',
       'DBPs': 'Disinfection byproducts (DBP)', 'A': 'Asbestos (A)', 'DI': 'Dioxin (DI)', 'SUR': 'Cryptosporidium, Giardia, MPA (SUR)',
       'TOC': 'Total organic carbon (TOC)', 'DOC': 'Dissolved organic carbon (DOC)', 'SUVA': 'Specific UV absorbance (SUVA)'}
ORDER = list(LEG.values())
def chips(grp):
    out = []
    for g in [x.strip() for x in grp.split(',')]:
        c = LEG[g]
        if c not in out: out.append(c)
    return sorted(out, key=ORDER.index)

def phone(p):
    return more_lib.clean_phone(p)

PUBLIC = {'NM9402', 'NM9405', 'NM9411', 'NM9415', 'NM1301', 'NM9422', 'NM9429', 'NM9901', 'NM9424/NM00', 'NM9454', 'NM9420', 'NM9427'}
EXTRA = {
 'NM9412': dict(address='290 Dinosaur Trail, Santa Fe, NM 87508', website=INDEPTH,
   note='Indepth\'s own site says it has tested water "for public water systems and well owners in Santa Fe and northern New Mexico since 1986" and lists "Homeowner Wells". Posted prices (tax not included): coliform and E. coli $80; bacteria and nitrate $130 (2-3 business days); bacteria, nitrate and lead (FHA/VA) $280 (10-14 business days); a 32-element panel that includes arsenic, fluoride, lead, manganese, nitrate and uranium $495 (14-17 business days). Bacteria samples must reach the lab within 24 hours of collection, kept cold; samples dropped off after 3:00 pm Thursday or on Friday add a $100 fee. Payment is due at drop-off; sampling visits are charged by time and mileage. Note NMED certifies this lab for microbiology only, so the chemistry in its panels is not covered by the NMED certification shown here; ask who runs those tests. The site gives (505) 473-7973 and the address above; NMED prints (505) 471-2023.',
   s2=(INDEPTH, 'Indepth Water Testing website (prices, fetched 2026-11-18)')),
 'NM9414': dict(address='4501 Bogan Avenue NE, Suite B3, Albuquerque, NM 87109', website=ETS,
   note='Its own site (ETS New Mexico) offers "Private Water Testing", says it can "assist you with testing for almost any water quality concern", offers sample collection services, and does well inspections for real estate transactions. No prices are posted; call.',
   s2=(ETS, 'Environmental Testing Services (ETS New Mexico) website, fetched 2026-11-18')),
 'NM00036': dict(website=CARD,
   note='Its site says it tests soil and water "for public and private interests", is drinking-water certified in Colorado, New Mexico and Texas, and has a sample receiving office in Farmington. It does not post homeowner prices or say it takes walk-in well samples; call.',
   s2=(CARD, 'Cardinal Laboratories website, fetched 2026-11-18')),
 'NM0301': dict(note='NMED\'s list prints (505) 434-4944. NMED\'s older Ground Water Quality Bureau list of labs (PDF created 2022) gives (575) 434-4944 for this lab, which matches Alamogordo\'s area code. Try 575 first.',
   s2=(ASSIST, 'NMED GWQB: Laboratories Providing Assistance With Water, Wastewater, and Soil Analysis (PDF created 2022-11-21)')),
 'NM1201': dict(note='NMED\'s older Ground Water Quality Bureau list of labs (PDF created 2022) also lists Aqua Environmental Testing Lab offices in Clovis (575) 749-2189 and Ruidoso (575) 336-1107. Only the Las Cruces lab is on the current certified list.',
   s2=(ASSIST, 'NMED GWQB: Laboratories Providing Assistance With Water, Wastewater, and Soil Analysis (PDF created 2022-11-21)')),
 'NM9425': dict(note='Certified for the widest range of groups of any New Mexico lab on the list, including bacteria, inorganics (nitrate and fluoride), heavy metals, radiologicals, VOCs and PFAS. NMED\'s older 2022 lab list showed this phone number for Hall Environmental Analysis Laboratory. We did not verify homeowner prices or services; call.'),
 'NM9424/NM00': dict(note='The state public health lab (NM Department of Health). NMED\'s lab-certification page calls it the Principal State Laboratory. Its own page says it supports "tax-supported agencies and groups or entities administering health and environmental programs"; we found no source saying it tests samples for individual well owners. Call first.'),
 'ME00009': dict(note='Highlighted on NMED\'s list as "Certification renewal is in progress, there will be no lapse in certification." Its expiration date (12/7/2026) is close; confirm status.'),
 'NM9420': dict(note='NMED lists a certification expiration of 11/30/2026 for this lab. Confirm it has been renewed.'),
}
for k, v in EXTRA.items():
    pass
assert 'well owners in Santa Fe and northern New Mexico since 1986' in ind and '$495' in ind and '$100.00 Fee' in ind and '(505) 473-7973' in ind
assert 'Private Water Testing' in ets and '505-881-0243' in ets and 'collection services' in ets
assert 'public and private interests' in card and 'Farmington' in card

labs = []
for r in rows:
    nm = r['loc'].endswith(', NM')
    grp = 'public' if r['cert'] in PUBLIC else ('main' if nm else 'outofstate')
    ex = EXTRA.get(r['cert'], {})
    exp = r['exp']
    detail = 'NMED certification number %s; analyte groups as printed: "%s"; certification expires %s; on contract with NMED-DWB: %s.' % (
        r['cert'], r['grp'], exp, 'yes' if r['k'] == 'Y' else 'no')
    if r['cert'] == 'NM9424/NM00':
        detail = detail.replace('NM9424/NM00', 'NM9424/NM00 (the number is cut off in NMED\'s PDF)', 1)
    lab = dict(name=r['name'], address=ex.get('address', r['loc'] + ' (NMED lists city only)'), city=r['loc'].split(',')[0],
               phone=phone(r['ph']), accredited_for=chips(r['grp']), group=grp, detail=detail,
               source_name=SN, source_url=URL, source_date=SD, last_verified=V)
    if 'website' in ex: lab['website'] = ex['website']
    if 'note' in ex: lab['note'] = ex['note']
    if 's2' in ex: lab['source_url_2'], lab['source_name_2'] = ex['s2']
    labs.append(lab)

def rank(l):
    a = l['accredited_for']
    return (-('Microbiological (M)' in a), -('Inorganics: nitrate, fluoride, cyanide (IO)' in a), -len(a), l['name'])
main = [l for l in labs if l['group'] == 'main']
# lab-published homeowner info first, then by breadth
pref = {'BSN dba Indepth Water Testing': 0, 'Environmental Testing Services Co., Inc.': 1}
main.sort(key=lambda l: (pref.get(l['name'], 9),) + rank(l))
pub = sorted([l for l in labs if l['group'] == 'public'], key=lambda l: l['name'])
oos = sorted([l for l in labs if l['group'] == 'outofstate'], key=rank)

screen = dict(
    name='NMED free well-water screening (field offices and water fairs; not a certified lab test)',
    address='Statewide: drop off at an NMED field office, or bring a sample to a water fair', city='Santa Fe', phone='(505) 827-2900',
    accredited_for=['Not on the certified list (NMED screening). Field offices: nitrate, iron, fluoride', 'Water fairs: arsenic, electrical conductivity, fluoride, iron, nitrate, pH, sulfate'],
    group='main', website=FREE,
    detail='Phone is NMED\'s Ground Water Quality Bureau, which runs the water fairs (gwqb.general@env.nm.gov).',
    note='NMED\'s Free Well Water Testing page says it tests private domestic wells free "only for Nitrate, Iron and Fluoride": collect at least one quart from the kitchen cold tap in a clean covered container, fill out the Well Testing Form, and bring both to your nearest NMED field office; results come by mail. NMED\'s Ground Water Quality Bureau also holds water fairs (the Private Wells page says eight a year) that test arsenic, electrical conductivity, fluoride, iron, nitrate, pH and sulfate, with results mailed in 2-4 weeks; dates are on the NMED events calendar. NMED says these are screenings only and do not replace certified lab testing. Neither tests for bacteria.',
    source_name='NMED: Free Well Water Testing (page prints no date; fetched 2026-11-18)', source_url=FREE, source_date='2026-11-18',
    source_url_2=FAIRS, source_name_2='NMED Ground Water Quality Bureau: Water Fairs page (fetched 2026-11-18)', last_verified=V)

labs = [screen] + main + pub + oos
c = Counter(l['group'] for l in labs)
print(c)
assert len(labs) == 45 and c['main'] == 12 and c['public'] == 12 and c['outofstate'] == 21, c

write_state('new-mexico', 'New Mexico', 'NM', labs,
    {'name': SN, 'page_url': PW, 'program_url': CERT,
     'report_date': 'PDF "Last Updated: 10/26/2026"; fetched November 18, 2026'},
    {
     'title': 'New Mexico certified labs for well water testing (all 44 on NMED\'s list, Nov 2026)',
     'description': 'All 44 labs on NMED\'s certified drinking-water lab list (updated 10/26/2026), what each is certified for, NMED\'s free nitrate, iron and fluoride screening, free arsenic screening at water fairs, and posted Santa Fe lab prices.',
     'intro': [
      'The New Mexico Environment Department (NMED) Drinking Water Bureau certifies labs to test water for public water systems. Its Private Wells page links one list of "Certified Laboratories" and says that while NMED certifies labs for public water systems, "many of these labs also offer services to private well owners." We transcribed the list on November 18, 2026. It is dated "Last Updated: 10/26/2026" and has 44 labs: 23 in New Mexico and 21 out of state.',
      'NMED certifies labs by groups of tests. For a well owner the key groups are M (microbiological: coliform bacteria), IO (inorganics: nitrate, fluoride and cyanide), HM (heavy metals) and RAD (radiologicals). Most New Mexico labs on the list are certified for bacteria only. Only two in-state commercial labs are also certified for nitrate (IO) and heavy metals (HM): Eurofins Environmental Testing South Central in Albuquerque and Cardinal Laboratories in Hobbs. The state lab (SLD) is too, but we found no source saying it takes homeowner samples.',
      'NMED does not regulate private wells. Its Private Wells page recommends testing every spring for coliform bacteria and nitrate, testing for arsenic every year because it occurs naturally in New Mexico, and testing for uranium every five years. It also says to test after a new well is drilled, when buying a home with a well, after a septic failure, wildfire, flood or prolonged drought, and when someone in the home is pregnant or nursing a baby under 6 months.',
      'NMED offers two free screenings. NMED field offices test well water free for nitrate, iron and fluoride. NMED\'s water fairs test arsenic, conductivity, fluoride, iron, nitrate, pH and sulfate. NMED says both are screenings, not certified lab results, and neither checks for bacteria.',
     ],
     'caveats': [
      'Certification is by test group, and the list is for labs that test public water systems. It does not say which labs take homeowner samples. Where a lab\'s own site says it does, the card says so and links the site. Call the others first.',
      'Bacteria-only labs (group M) cannot give you a certified nitrate, arsenic or uranium result. NMED\'s list does not break heavy metals (HM) or radiologicals (RAD) down by element, so ask whether arsenic and uranium are covered before you sample.',
      'NMED lists city and phone only. Street addresses shown here come from the lab\'s own website, where it has one.',
      '"On contract" (Y/N) on the NMED list is about whether NMED pays the lab for public water system samples. It does not affect a homeowner.',
      'Two expiration dates are close: Red River AWWT Laboratory (11/30/2026) and NELAnalytical Laboratory (12/7/2026; NMED marks its renewal as in progress). NMED\'s lab-certification page also says it is not accepting new reciprocity applications for out-of-state labs until at least January 2027.',
      'Bacteria samples are time-limited: Indepth Water Testing says 24 hours from collection to the lab, kept cold.',
      'Prices come only from each lab\'s own page, with the date we checked. Only Indepth Water Testing posts prices.',
      'The grouping is ours. The first group is NMED\'s free screening and the New Mexico labs whose names do not show a city, utility or state owner (we did not check who owns each one). The second is labs whose names show a city, town, water utility or the state. Out-of-state labs are last, with bacteria and nitrate labs first.',
     ],
     'main_heading': 'Free NMED screening and New Mexico commercial labs',
     'public_heading': 'City, utility and state labs on the same list',
     'public_note': 'These labs test water for a city, water utility or the state. NMED\'s list does not say whether they take samples from private-well owners, and we found no source saying they do. Call first.',
     'oos_heading': 'Out-of-state labs on NMED\'s list',
     'oos_note': [
      'NMED certifies these 21 labs outside New Mexico by reciprocity. Most test for water utilities, and several only do specialty tests such as asbestos, dioxin, PFAS or radiologicals; each card shows NMED\'s groups. Labs certified for bacteria and inorganics (nitrate) are listed first.',
      'Bacteria samples usually must reach a lab within about a day, so out-of-state labs are mostly useful for chemistry. Ask each lab how to ship samples.',
     ],
     'chips_label': 'Certified by NMED for (analyte groups as defined in NMED\'s legend):',
     'resources': [
      {'label': 'NMED: Laboratories Certified by NMED-DWB to Analyze Drinking Water Samples (PDF, last updated 10/26/2026)', 'url': URL},
      {'label': 'NMED Drinking Water Bureau: Private Wells', 'url': PW},
      {'label': 'NMED Drinking Water Bureau: Laboratory Certification', 'url': CERT},
      {'label': 'NMED: Free Well Water Testing (nitrate, iron, fluoride at field offices)', 'url': FREE},
      {'label': 'NMED Ground Water Quality Bureau: Water Fairs', 'url': FAIRS},
      {'label': 'NMED events calendar (water fair dates)', 'url': CAL},
     ],
    })

gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('new-mexico', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed new-mexico from stateGuides.json')
for l in labs:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', '; '.join(l['accredited_for']))
