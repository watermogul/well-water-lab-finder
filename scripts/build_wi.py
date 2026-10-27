"""Wisconsin: (1) DNR 'Drinking water certified labs - chemistry - NR 809 and NR 812' Excel dated 092826 (Sept 28, 2026),
(2) DNR Drinking Water System Portal 'Bacti Labs' page (live page, fetched 2026-10-27). Joined on the DNR facility ID."""
import openpyxl, collections, os, sys, re, html
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src2')
X_URL = 'https://dnr.wisconsin.gov/sites/default/files/topic/LabCert/DWLabs092826.xlsx'
B_URL = 'https://apps.dnr.wi.gov/dwsportalpub/BactiLab'
PAGE = 'https://dnr.wisconsin.gov/topic/labCert/certified-lab-lists'
SN = 'Wisconsin DNR, "Drinking water certified labs - chemistry - NR 809 and NR 812" (Excel, Sept. 28, 2026)'
SNB = 'Wisconsin DNR Drinking Water System Portal, "Drinking Water Bacti Labs" (live page, retrieved 2026-10-27)'
ws = openpyxl.load_workbook(os.path.join(SRC_DIR, 'wi_dw.xlsx')).active
chem = collections.OrderedDict()
for fid, name, typ, par, st, cty, city, ph in list(ws.iter_rows(values_only=True))[1:]:
    d = chem.setdefault(str(fid), dict(name=name.strip(), typ=typ, st=st, cty=cty, city=city, ph=ph, par=[]))
    d['par'].append(par)
h = open(os.path.join(SRC_DIR, 'wi_bact.html')).read()
bact = {}
for r in re.findall(r'<tr[^>]*>(.*?)</tr>', h, re.S):
    cells = [re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', ' ', c))).strip() for c in re.findall(r'<td[^>]*>(.*?)</td>', r, re.S)]
    if len(cells) < 6: continue
    ids = [x.strip() for x in cells[1].split(';') if x.strip()]
    fid = ids[-1]
    m = re.match(r'(.*?)\s+WI\s+(\d{5})', cells[4])
    bact[fid] = dict(name=cells[0], phone=cells[3], addr=cells[4])
def tc(s):
    keep = {'A. O. Smith':'A. O. Smith','Llc':'LLC','Inc':'Inc'}
    out = s.title()
    out = re.sub(r"\b(Llc|Lllp|Llp)\b", lambda m: m.group(0).upper(), out)
    out = re.sub(r"\bInc\b\.?", "Inc.", out); out = re.sub(r"\bInc\.\.", "Inc.", out)
    out = re.sub(r"\bWi\b", "WI", out)
    out = re.sub(r"\b(Uw|Uwsp|Cdc|Wwtp|Wtp|Psa|Hd)\b", lambda m: m.group(0).upper(), out)
    out = out.replace("'S", "'s")
    return out
PUBTYPES = {'Municipal Lab', 'Public Water Supply Lab', 'Industrial Lab', 'Treatment, Storage & Disposal Lab'}
CHEM_KEYS = {'Nitrate','Nitrite','Arsenic','Lead','Copper','Fluoride','Manganese','Iron','Uranium','Sodium','Chloride','Sulfate','Hardness'}
fids = list(dict.fromkeys(list(chem) + list(bact)))
out = []; oos = 0
for fid in fids:
    c = chem.get(fid); b = bact.get(fid)
    if c and c['st'] != 'WI': oos += 1; continue
    if not c and b and not re.search(r'\bWI\s+\d{5}', b['addr']): oos += 1; continue
    name = c['name'] if c else tc(b['name'])
    typ = c['typ'] if c else None
    names = c['par'] if c else []
    chips = key_chips(names)
    if b: chips = ['Total coliform (enzyme-substrate method)'] + chips if False else chips
    has_chem = bool(CHEM_KEYS & set(chips)) or bool(c)
    pub = (typ in PUBTYPES) if typ else (looks_public(name) and not re.search(r'health|county|universit|human services', name, re.I))
    if b and c: grp = 'public' if pub else ('main' if has_chem else 'limited')
    else: grp = 'public' if pub else 'limited'
    if grp == 'public': pass
    if b:
        addr = re.sub(r'\s+', ' ', b['addr']).title().replace(' Wi ', ', WI ')
        addr = re.sub(r'^(.*?)\s+([A-Z][A-Za-z.\' ]+?), WI (\d{5})(-\d{4})?$', lambda m: m.group(0), addr)
        street_zip = b['addr']
        m = re.match(r'(.*?)\s+([A-Z][A-Z. \'-]*?)\s+WI\s+(\d{5})', street_zip)
        # source prints "STREET CITY WI ZIP"; keep it verbatim in title case
        address = tc(street_zip).replace(' WI ', ', WI ')
    else:
        address = '%s, WI (street address not given in the DNR chemistry file)' % c['city']
    city = (c['city'] if c else re.sub(r',? WI \d{5}(-\d{4})?$', '', address))  # city field only feeds the anchor id; bacteria-only rows have no separate city
    phone = clean_phone(c['ph'] if c else b['phone']) if (c or b) else None
    if b and b['phone']: phone = clean_phone(b['phone'])
    bits = []
    if c: bits.append('DNR lab type: %s' % typ)
    if c: bits.append('%d analyte/method entries on the DNR chemistry list' % len(c['par']))
    else: bits.append('Not on the DNR chemistry file; listed on the DNR bacteria (coliform) lab page only')
    if b: bits.append('listed on the DNR page of labs certified for coliform bacteria (enzyme-substrate method)')
    else: bits.append('not on the DNR coliform-bacteria lab page')
    chip_list = (['Coliform bacteria (enzyme-substrate method), per DNR bacteria page'] if b else []) + chips
    l = dict(name=name, address=address, city=city, phone=phone, lab_id=fid,
             accredited_for=chip_list or ['Chemistry analytes on the DNR file are specialty or not in our well-test list'],
             detail='DNR facility ID %s. %s.' % (fid, '; '.join(bits)),
             group=grp, source_name=SN, source_url=X_URL, source_date='2026-09-28')
    if b:
        l['source_name_2'] = 'the DNR bacteria-lab page' if c else None
        l['source_url_2'] = B_URL
        if not c:
            l['source_name'] = SNB; l['source_url'] = B_URL; l['source_date'] = '2026-10-27'; l.pop('source_url_2'); l.pop('source_name_2')
    if l.get('source_name_2') is None: l.pop('source_name_2', None)
    out.append(l)
order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))
write_state('wisconsin', 'Wisconsin', 'WI', out,
 {'name': 'Wisconsin DNR certified drinking-water lab lists (chemistry Excel + coliform-bacteria lab page)', 'page_url': PAGE, 'program_url': PAGE,
  'report_date': 'Chemistry list dated Sept. 28, 2026; bacteria lab page retrieved Oct. 27, 2026'},
 {
 'title': 'Wisconsin state-certified drinking-water labs for private wells (DNR lists)',
 'description': 'Wisconsin labs on the DNR lists of certified drinking-water chemistry labs (Sept. 28, 2026) and coliform-bacteria labs, with lab type, phone numbers where printed and the source on every listing.',
 'intro': [
  "Wisconsin's Department of Natural Resources (DNR) certifies drinking-water labs and publishes two lists that matter for well owners: an Excel file of labs certified for drinking-water chemistry (dated Sept. 28, 2026 in the file name), and a web page of labs certified for coliform bacteria testing. DNR labels the chemistry file for homeowners and public water systems alike, and it names each lab's type: commercial, public health, municipal and so on.",
  "We joined the two lists on DNR's facility ID. Labs located in Wisconsin that appear on both lists, and are not municipal, industrial or water-system labs, are shown first. Labs on only one list are in a second group.",
  "The bacteria page prints a street address and phone number; the chemistry file prints only city, county and phone. Where a lab is only on the chemistry file we show the city and say so.",
 ],
 'caveats': [
  "These are the DNR's certification lists for drinking-water compliance and homeowner testing. They do not say which labs will take a sample from a homeowner, and they do not list prices. Call the lab first.",
  "Groups follow DNR's lab-type field where the chemistry file has one. Labs that appear only on the bacteria page have no type field, so we judged those from the name: water utilities, wastewater plants, villages, cities and state agencies go in the municipal group, while county health departments and universities go in the single-list group.",
  "Only the analytes we recognised as common well tests are shown as chips. The DNR file lists every method and analyte; the Excel file is the full record.",
  "Wisconsin's list also names labs in other states (for example Illinois, Michigan, Minnesota and Indiana). We left out the %d out-of-state labs." % oos,
  "The bacteria page is a live DNR web page with no revision date, so its source date is the day we retrieved it.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Wisconsin labs certified for chemistry and coliform bacteria',
 'public_heading': 'Municipal, water-system, industrial and agency labs',
 'public_note': 'DNR types these as municipal, water-system or industrial labs, or they look like one from the name. They usually test for their own system. Call first.',
 'limited_heading': 'Labs on only one DNR list (chemistry only or bacteria only)',
 'limited_note': 'These labs appear on only one of the two DNR lists (most are on the bacteria page only), so you may need a second lab for a full well test. Many are county health departments, which often run just a basic bacteria test.',
 'chips_label': 'Well-test analytes on the DNR lists for this lab:',
 'resources': [
  {'label': 'Wisconsin DNR: certified drinking-water lab lists (chemistry Excel, Sept. 28, 2026)', 'url': X_URL},
  {'label': 'Wisconsin DNR: labs certified for coliform bacteria (Drinking Water System Portal)', 'url': B_URL},
  {'label': 'Wisconsin DNR: certified lab lists page', 'url': PAGE},
  {'label': 'Wisconsin DNR: wells', 'url': 'https://dnr.wisconsin.gov/topic/Wells'},
 ]})
