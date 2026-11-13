"""Montana: DPHHS Water Laboratory Certification Program page (HTML list of certified labs), fetched 2026-11-12.
Replaces the thin /labs/montana/ state-guide with a full listing.
SRC_DIR must contain dphhs_wlcp_2026-11-12.html (saved copy of the program page; the page prints no date,
server Last-Modified header was Fri, 05 Jun 2026 14:26:03 GMT; md5 ce360c9124d4aab359abf0f0f2519d04)."""
import os, sys, re, json
from collections import OrderedDict, Counter
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state, clean_phone
from parse_mt import parse_mt

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-mt')
V = '2026-11-12'
more_lib.V = V
URL = 'https://dphhs.mt.gov/publichealth/LaboratoryServices/WaterLaboratoryCertificationProgram'
SN = 'Montana DPHHS Water Laboratory Certification Program: Certified Laboratories (web page)'
SOURCE_DATE = '2026-06-05'  # HTTP Last-Modified of the page; no date is printed on it
MSU = 'https://waterquality.montana.edu/well-ed/testing/certifiedlabs.html'
MSU_N = 'MSU Extension Water Quality: Certified Montana Drinking Water Labs (updated 23.02.15)'
MSU_WE = 'https://waterquality.montana.edu/well-ed/testing/index.html'
ENVLAB = 'https://dphhs.mt.gov/publichealth/LaboratoryServices/EnvironmentalLaboratory/'
CHEM_FORM = 'https://dphhs.mt.gov/assets/publichealth/Lab/EnvironmentalLabtesting/PrivateWellScreenBlueSheet1.pdf'
BACT_FORM = 'https://dphhs.mt.gov/assets/publichealth/Lab/EnvironmentalLabtesting/PrivateBacteria.pdf'
FEES = 'https://dphhs.mt.gov/assets/publichealth/Lab/EnvironmentalLabtesting/EnvironmentalLaboratoryTestingFeeSchedule.pdf'
LHD = 'https://dphhs.mt.gov/publichealth/EHFS/countytribalhealthdepts'

CHIP = {
    'Asbestos': 'Asbestos (chemistry)',
    'Inorganic and Organic': 'Chemistry: inorganic and organic',
    'Inorganic only': 'Chemistry: inorganic only',
    'Radiologic': 'Radiologic (radioactivity) only',
    'Microbiology': 'Microbiology (bacteria)',
}
def chip(cat, region):
    if 'Radiologic' in region: return CHIP['Radiologic']
    for k in ('Asbestos', 'Inorganic and Organic', 'Inorganic only', 'Microbiology'):
        if k in cat: return CHIP[k]
    raise ValueError(cat)

rows = parse_mt(os.path.join(SRC_DIR, 'dphhs_wlcp_2026-11-12.html'))
assert len(rows) == 45, len(rows)

def split_csz(csz):
    m = re.match(r'^(.*?),?\s+([A-Za-z]{2}|New Jersey)\s+(\d{5}(-\d{4})?)$', csz)
    assert m, csz
    st = {'New Jersey': 'NJ'}.get(m.group(2), m.group(2).upper())
    return m.group(1).strip(), st, m.group(3)

def key(name, city):
    n = re.sub(r'[^a-z0-9]', '', name.lower().replace(', inc.', '').replace(' inc.', ''))
    return (n, city.lower())

labs = OrderedDict()
for r in rows:
    city, st, z = split_csz(r['csz'])
    k = key(r['name'], city)
    addr = '%s, %s, %s %s' % (', '.join(r['street']), city, st, z)
    e = labs.setdefault(k, dict(name=r['name'], city=city, st=st, addrs=[], phones=[], chips=[], montana=r['region'].startswith('Montana')))
    if addr not in e['addrs']: e['addrs'].append(addr)
    p = clean_phone(r['phone'])
    if p and p not in e['phones']: e['phones'].append(p)
    c = chip(r['category'], r['region'])
    if c not in e['chips']: e['chips'].append(c)

PUBLIC = {'Billings Public Utilities Department', 'Great Falls Water Plant Lab', 'Missoula CCHD Water Lab', 'Montana Bureau of Mines and Geology'}
ON_MSU = {
    'DPHHS State of Montana Environmental Laboratory': 'Department of Public Health and Human Services Environmental Laboratory',
    'Energy Laboratories, Inc.|Billings': 'Energy Laboratories - Billings',
    'Energy Laboratories, Inc.|Helena': 'Energy Laboratories - Helena',
    'Alpine Analytical': 'Alpine Analytical',
    'Bridger Analytical Laboratory': 'Bridger Analytical Lab',
    'Montana Environmental Laboratory': 'Montana Environmental Laboratory',
    'Aqua Tech Laboratory': 'Aqua Tech Laboratory',
    'Mission Mountain Laboratories': 'Mission Mountain Laboratories',
    'RD Water Lab, LLC': 'RD Water Lab',
    'Water Technologies Laboratory': 'Crisp Water Technologies',
    'Great Falls Water Plant Lab': 'Great Falls Water Treatment Plant Water Testing Lab',
    'Missoula CCHD Water Lab': 'Missoula City/County Health Department Water Lab',
    'Montana Bureau of Mines and Geology': 'Montana Bureau of Mines and Geology',
}
IRON_SULFUR = {'DPHHS State of Montana Environmental Laboratory', 'Energy Laboratories, Inc.|Billings', 'Energy Laboratories, Inc.|Helena', 'Bridger Analytical Laboratory', 'Montana Environmental Laboratory'}
EXTRA = {
    'DPHHS State of Montana Environmental Laboratory': 'This is the state lab, and it tests private wells. Its private-well chemistry form (dated July 2025, "prices subject to change") lists a Basic Screen (coliform/E. coli presence-absence, nitrate + nitrite, specific conductivity) for $55, a Metals Screen (calcium, magnesium, hardness, sodium, lead, arsenic, copper, uranium) for $135, an Anion Screen for $75, VOCs for $148, pesticides for $285 and herbicides for $206. Its private-well bacteria form (dated January 2024) lists total coliform presence/absence for $25 and a coliform count, iron bacteria or sulfur bacteria for $42 each. Both forms say samples must be paid for in advance, and bacteria samples must reach the lab within 48 hours. Mailing address on the forms: P.O. Box 4369, Helena, MT 59604; toll-free (800) 821-7284.',
    'Montana Bureau of Mines and Geology': 'MSU Extension\'s list says this lab "is not able to test samples from homeowners."',
    'Missoula CCHD Water Lab': 'MSU Extension\'s list (Feb 2023) names it "Missoula City/County Health Department Water Lab" and prints the phone as (406) 258-3386; the DPHHS page prints (406) 523-4755. Try both.',
    'Mission Mountain Laboratories': 'MSU Extension\'s list (Feb 2023) prints PO Box 606, Arlee, MT 59821, (406) 745-5227; the DPHHS page prints 82892 US 93 with the town spelled "Ravali" (as printed) and (406) 370-1089. Call to confirm.',
    'Water Technologies Laboratory': 'MSU Extension\'s list (Feb 2023) shows "Crisp Water Technologies" at the same street address (1709 S Avenue W, Missoula) and the same phone number.',
    'Great Falls Water Plant Lab': 'MSU Extension\'s list (Feb 2023) names it "Great Falls Water Treatment Plant Water Testing Lab" and gives the mailing address PO Box 5021, Great Falls, MT 59403.',
    'Billings Public Utilities Department': 'The DPHHS page prints a second name line for the chemistry listing: "City of Billings Public Works- Water Quality". This lab is not on MSU Extension\'s list for well owners.',
    'MSM Laboratory': 'Not on MSU Extension\'s Feb 2023 list for well owners. The DPHHS page does not say whether it takes homeowner samples.',
}

out = []
for k, e in labs.items():
    nm = e['name']; nk = nm + '|' + e['city']
    msu = ON_MSU.get(nk) or ON_MSU.get(nm)
    if not e['montana']:
        group = 'limited'
    elif nm in PUBLIC:
        group = 'public'
    else:
        group = 'main'
    parts = ['Listed on the DPHHS page under: ' + '; '.join(e['chips']) + '.']
    if len(e['addrs']) > 1:
        parts.append('The DPHHS page prints a different address in different categories: ' + ' / '.join(e['addrs']) + '.')
    if not e['montana']:
        parts.append('Out-of-state lab (%s) on the DPHHS list.' % e['st'])
    if msu and nm not in ('Montana Bureau of Mines and Geology',):
        parts.append('Also on MSU Extension\'s list of certified labs for Montana well owners.')
    if (nk in IRON_SULFUR) or (nm in IRON_SULFUR):
        parts.append('MSU Extension says this lab can test for iron bacteria and sulfur-reducing bacteria.')
    lab = dict(
        name=nm + ('' if e['st'] != 'MT' or nm.endswith(e['city']) or nm not in ('Energy Laboratories, Inc.',) else ' (%s)' % e['city']),
        address=e['addrs'][0], city=e['city'], phone=' / '.join(e['phones']) if len(e['phones']) > 1 else (e['phones'][0] if e['phones'] else None),
        accredited_for=e['chips'], detail=' '.join(parts), group=group,
        source_name=SN, source_url=URL, source_date=SOURCE_DATE, last_verified=V,
    )
    if msu:
        lab['source_url_2'] = MSU; lab['source_name_2'] = MSU_N
    ex = EXTRA.get(nm)
    if ex: lab['note'] = ex
    if nm.startswith('DPHHS'):
        lab['source_url_2'] = CHEM_FORM; lab['source_name_2'] = 'DPHHS private-well chemistry form (July 2025)'
    out.append(lab)

order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], 0 if l['name'].startswith('DPHHS') else 1, l['name'].lower(), l['city']))
c = Counter(l['group'] for l in out)
assert len(out) == 36 and c['main'] == 11 and c['public'] == 4 and c['limited'] == 21, (len(out), c)

write_state('montana', 'Montana', 'MT', out,
    {'name': SN, 'page_url': URL, 'program_url': URL,
     'report_date': 'Web page with no printed date (server last-modified June 5, 2026); fetched November 12, 2026'},
    {
     'title': 'Montana certified drinking-water labs for private well testing (DPHHS list, Nov 2026)',
     'description': 'All %d labs on Montana DPHHS\'s certified drinking-water lab list (%d in Montana), what each is certified for, which are on MSU Extension\'s well-owner list, and the state lab\'s published private-well prices.' % (len(out), c['main'] + c['public']),
     'intro': [
      'The Montana Department of Public Health and Human Services (DPHHS) runs the Water Laboratory Certification Program. Its web page lists every lab certified to analyze Montana public drinking water, in five categories: asbestos, chemistry (inorganic and organic), chemistry (inorganic only), radiologic only, and microbiology (bacteria). We transcribed that page on November 12, 2026. It lists %d labs: %d in Montana and %d out of state. The page has no printed date; the server reported it was last changed on June 5, 2026.' % (len(out), c['main'] + c['public'], c['limited']),
      'DPHHS says certification "authorizes laboratories to analyze public water supplies in Montana." The list does not say which labs take samples from private-well owners. MSU Extension Water Quality keeps a separate list for well owners (last updated February 2023) and advises calling a lab first "to get the most up to date information on analyses, costs, and hold times." Each listing below says whether the lab is also on MSU\'s list.',
      'The state lab tests private wells. The DPHHS State Environmental Laboratory in Helena says it serves "the general public" and publishes private-well forms with prices. Its chemistry form (July 2025) lists a $55 Basic Screen (coliform/E. coli, nitrate + nitrite, conductivity) and a $135 Metals Screen that includes arsenic, lead and uranium. Its bacteria form (January 2024) lists total coliform presence/absence for $25. Both forms say "prices subject to change" and require payment in advance. Call (406) 444-3444 or (800) 821-7284 to check before you send a sample.',
      'MSU Extension\'s Well Educated program offers test kits through participating county offices, with guidance on what to test for in each county. MSU says the program "is not intended for real estate or legal purposes"; for those, or if you are in a hurry, it points well owners to a certified lab directly. DPHHS also runs free well-water testing for licensed or prospective childcare facilities on wells (request form linked from the State Environmental Laboratory page).',
     ],
     'caveats': [
      'Certification is not the same as taking homeowner samples. The DPHHS list is for labs that test public water supplies. Call first and ask about bottles, fees, hold times and drop-off or shipping.',
      'The chips show only the DPHHS category a lab is listed under. "Inorganic" covers things like nitrate and metals, but the page does not list individual tests, so ask the lab whether it is certified for the specific test you want (for example arsenic or uranium).',
      'Bacteria samples have short hold times. The state lab\'s forms say bacteria samples must reach the lab within 48 hours of collection. Out-of-state labs may be hard to reach in time.',
      'The grouping is ours: the first group is Montana commercial labs and the state lab; the second is a city utility lab, a water plant lab, a county health department lab and the Montana Bureau of Mines and Geology; the third is labs outside Montana. Labs listed in more than one category are shown once with every category.',
      'Where the DPHHS page and MSU Extension\'s 2023 list print different phone numbers or addresses, the listing notes both.',
      'Prices are shown only for the state lab, from its own published forms. We did not verify prices, turnaround times or websites for any other lab.',
     ],
     'main_heading': 'Montana commercial labs and the state lab',
     'public_heading': 'City, county and state-agency labs on the same list',
     'public_note': 'These are run by a city utility, a water plant, the Missoula City-County Health Department or the Montana Bureau of Mines and Geology. MSU Extension lists the Great Falls and Missoula labs for well owners, but says the Bureau of Mines lab does not test homeowner samples. Call first.',
     'limited_heading': 'Out-of-state labs on the Montana list',
     'limited_note': 'These labs are outside Montana and certified for Montana public water supplies. Most are large commercial or compliance labs. Ask about shipping and hold times before you collect a sample.',
     'chips_label': 'Listed by DPHHS under:',
     'resources': [
      {'label': 'Montana DPHHS: Water Laboratory Certification Program (certified lab list)', 'url': URL},
      {'label': 'Montana DPHHS: State Environmental Laboratory (private well testing forms)', 'url': ENVLAB},
      {'label': 'DPHHS: Chemistry testing for private wells, sample form with prices (PDF, July 2025)', 'url': CHEM_FORM},
      {'label': 'DPHHS: Bacteria testing for private wells, sample form with prices (PDF, January 2024)', 'url': BACT_FORM},
      {'label': 'DPHHS: Environmental Laboratory testing fee schedule (PDF, effective January 1, 2024)', 'url': FEES},
      {'label': 'MSU Extension Water Quality: Certified Montana drinking water labs (updated Feb 2023)', 'url': MSU},
      {'label': 'MSU Extension: Well Educated program, testing your well water (county test kits)', 'url': MSU_WE},
      {'label': 'DPHHS: Local (county and tribal) health departments', 'url': LHD},
     ],
    })

# drop thin state-guide entry
gp = os.path.join(os.path.dirname(__file__), '..', 'src/_data/stateGuides.json')
g = json.load(open(gp))
if g.pop('montana', None) is not None:
    with open(gp, 'w') as f:
        json.dump(g, f, indent=2, ensure_ascii=False); f.write('\n')
    print('removed montana from stateGuides.json')
for l in out:
    print(l['group'], '|', l['name'], '|', l['address'], '|', l['phone'], '|', l['accredited_for'])
