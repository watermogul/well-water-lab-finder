"""Vermont: Vermont Department of Health, "Laboratories Certified for Drinking Water Analysis" (September 28, 2026), fetched 2026-10-27.
The PDF highlights in green the labs that "accept private samples"; only those 26 of the 46 certified labs are listed.
Input: vt_cols.json = per-lab text block, green-highlight flag and the analyte-column marks, extracted with pdfplumber and checked against page images."""
import os, sys, re, json
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src2')
URL = 'https://www.healthvermont.gov/sites/default/files/document/lsid-phl-DW-certified-laboratory-list.pdf'
PAGE = 'https://www.healthvermont.gov/environment/drinking-water'
SN = 'Vermont Department of Health, "Laboratories Certified for Drinking Water Analysis" (September 28, 2026)'
raw = json.load(open(os.path.join(SRC_DIR, 'vt_cols.json')))
CH = [('BACT (qualitative coliform/E. coli)', 'Bacteria: total coliform / E. coli (presence-absence)'),
      ('BACT quant', 'Bacteria: quantitative coliform, E. coli, Cryptosporidium, Giardia'),
      ('IOC', 'Inorganic chemicals (metals, nitrate, nitrite)'), ('ASB', 'Asbestos'), ('HAA5', 'Haloacetic acids'),
      ('THMs', 'Trihalomethanes'), ('VOC', 'Volatile organic compounds (VOCs)'),
      ('SOC A', 'Synthetic organics A (EDB and DCBP)'), ('SOC B', 'Synthetic organics B (carbamates)'),
      ('SOC C', 'Synthetic organics C (herbicides)'), ('SOC D', 'Synthetic organics D (pesticides, phthalates, PCBs)'),
      ('PFAS', 'PFAS'), ('RAD', 'RAD column (radionuclides)'), ('WSR', 'Table WSR (non-community water system contaminants)')]
def mdy(s):
    m, d, y = s.split('/'); return '%s/%s/%s' % (int(m), int(d), y)
labs = []; nongreen = 0
for l in raw:
    if not l['green']: nongreen += 1; continue
    t = l['text']
    i0 = next(i for i, x in enumerate(t) if re.match(r'\d', x))
    name = ' '.join(t[:i0])
    street = t[i0]
    cityline = next(x for x in t if re.search(r',\s*[A-Z]{2}\s+\d{5}', x))
    cm = re.match(r'(.*?)\s*,\s*([A-Z]{2})\s+(\d{5}(-\d{4})?)', cityline)
    phone = next(x for x in t if x.startswith('PHONE:'))[6:].strip()
    labid = next(x for x in t if x.startswith('LAB ID:'))[7:].strip()
    web = None
    for x in t:
        if re.match(r'^[a-z0-9.\-]+\.(com|org|gov)(/[a-z0-9\-/]*)?$', x) and not x.endswith('-'):
            web = 'https://' + x
    c = l['cols']; chips = []; kinds = set()
    for k, label in CH:
        v = c.get(k)
        if not v: continue
        kinds.add(k)
        extra = ''
        if 'artial' in v: extra = ' (marked Partial)'
        meth = re.findall(r'EPA [\d.]+(?: v\d)?', v)
        if k in ('PFAS',) or (k == 'BACT quant' and meth): extra = ' (' + ', '.join(meth) + ')'
        chips.append(label + extra)
    exp = mdy(c['EXP'])
    qual = 'BACT (qualitative coliform/E. coli)' in kinds or 'BACT quant' in kinds
    grp = 'main' if (qual and 'IOC' in kinds) else 'limited'
    labs.append(dict(name=name, address='%s, %s, %s %s' % (street, cm.group(1), cm.group(2), cm.group(3)), city=cm.group(1), phone=clean_phone(phone),
        website=web, lab_id='VT ' + labid.replace('VT ', ''), accredited_for=chips,
        detail='Vermont lab ID %s · Vermont certification expires %s.' % (labid, exp), group=grp,
        source_name=SN, source_url=URL, source_date='2026-09-28'))
order = {'main': 0, 'limited': 1}
labs.sort(key=lambda l: (order[l['group']], l['name'].lower(), l['address']))
assert len(labs) == 26 and nongreen == 20
write_state('vermont', 'Vermont', 'VT', labs,
 {'name': SN, 'page_url': URL, 'program_url': PAGE, 'report_date': 'List dated September 28, 2026'},
 {
 'title': 'Vermont certified labs that accept private well samples (Vermont Dept. of Health list)',
 'description': 'The 26 labs on the Vermont Department of Health drinking-water certification list (Sept. 28, 2026) that Vermont marks as accepting private samples, with certified test groups, expiration dates and the source on every listing.',
 'intro': [
  "The Vermont Department of Health publishes the list \"Laboratories Certified for Drinking Water Analysis\" (dated September 28, 2026). It has 46 certified labs, and the Department highlights in green the labs that accept private samples. This page lists those 26 green-highlighted labs, which is what a private well owner needs.",
  "Many of the labs are outside Vermont, in New Hampshire, New York, Massachusetts and elsewhere. The state certifies them to test Vermont drinking-water samples, and several (like the Endyne, Eurofins and Nelson Analytical locations) are near the border. The address of each lab is printed on its listing.",
 ],
 'caveats': [
  "The Department notes that some labs that generally accept private samples may specifically not accept private PFAS samples, or may analyze them by a method that is not certified. Call the lab before you send a sample.",
  "The list marks each test group \"X\" for certified or \"Partial\" for some but not all analytes in a group. We carry \"Partial\" through as printed. The list links each lab's detailed scope sheet, which is the place to check a specific analyte such as arsenic or uranium.",
  "The %d labs on the Vermont list that are not highlighted green (for example utility labs and out-of-state specialty labs) are left out because the Department does not mark them as accepting private samples. Laboratories may be added to or deleted from the list at any time." % nongreen,
  "A lab with both a bacteria group and the inorganic-chemicals group (metals, nitrate, nitrite) is shown first. Labs with only bacteria, only PFAS, only asbestos or only radionuclides are shown under the second heading.",
  "The list does not define the \"RAD\" column. We show it as printed, with the radionuclides label added by us. Fax numbers on the list are not reproduced.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Vermont labs that accept private samples: bacteria and inorganic chemistry',
 'limited_heading': 'Labs that accept private samples for bacteria, PFAS or other single test groups',
 'limited_note': 'Vermont marks each of these as accepting private samples, but its certification list shows only bacteria, or only specialty groups (such as PFAS, asbestos or radionuclides). Pair one with a lab above for a fuller panel.',
 'chips_label': 'Test groups certified in Vermont for this lab:',
 'resources': [
  {'label': 'Vermont Department of Health: Laboratories Certified for Drinking Water Analysis (PDF, 9/28/2026)', 'url': URL},
  {'label': 'Vermont Department of Health: drinking water', 'url': PAGE},
 ]})
