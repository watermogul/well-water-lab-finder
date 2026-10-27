"""Rhode Island: RIDOH "Certified Drinking Water Testing Labs" page (page last updated 2026-09-03; lists 5 RI-area labs by city, plus one nearby CT lab)
and RIDOH "Nearby Out-of-state Laboratories" PDF dated March 18, 2026 (full contact details and certification categories), fetched 2026-10-27."""
import os, sys, re, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src2')
PAGE = 'https://health.ri.gov/drinking-water-quality/certified-drinking-water-testing-labs'
PDF = 'https://health.ri.gov/sites/g/files/xkgbur1006/files/2025-01/OutOfState.pdf'
SN_P = 'Rhode Island Department of Health, "Certified Drinking Water Testing Labs" (page last updated Sept. 3, 2026)'
SN_F = 'Rhode Island Department of Health, "Certified Drinking Water Testing Labs: Nearby Out-of-state Laboratories" (PDF dated March 18, 2026)'
# RI-area labs exactly as the page prints them: (city, name, link printed on the page)
RI = [('North Kingstown', 'Eurofins North Kingstown', 'https://www.eurofins.com/en-us/'),
      ('Providence', 'Rhode Island Department of Health, State Health Lab', 'https://health.ri.gov/laboratory-testing/drinking-water-quality-testing'),
      ('Warwick', 'Eurofins Warwick', 'https://www.eurofins.com/en-us/'),
      ('Warwick', 'Rhode Island Analytical Laboratories', 'https://www.rianalytical.com/chemical-biological'),
      ('West Warwick', 'New England Testing Laboratory', 'https://www.newenglandtesting.com/DrinkingWater.php')]
labs = []
for city, name, web in RI:
    l = dict(name=name, address='%s, RI (RIDOH prints city only)' % city, city=city, website=web, group='main',
        accredited_for=['RIDOH certified for drinking water (specific tests not shown on the RIDOH page; ask the lab)'],
        detail='Listed by RIDOH as certified to test drinking water in Rhode Island and the surrounding area.',
        source_name=SN_P, source_url=PAGE, source_date='2026-09-03')
    if 'State Health Lab' in name:
        l.update(address='150 Richmond Street, Suite 100, Providence, RI 02903', phone='(401) 222-5600',
                 detail='Listed by RIDOH as certified to test drinking water. Address and phone are the State Health Laboratories location printed in the footer of the RIDOH page.')
    labs.append(l)
txt = subprocess.run(['pdftotext', '-layout', os.path.join(SRC_DIR, 'ri_oos.pdf'), '-'], capture_output=True, text=True).stdout.replace('\f', '\n')
CAT = re.compile(r'\s{2,}((?:Non-)?[Pp]otable water.*|Radiochemistry|PFAS|Environmental Lead|Asbestos)\s*$')
blocks = []; cur = None
for ln in txt.split('\n'):
    if not ln.strip() or re.match(r'\s*(Page \d of 5|March 18, 2026|LABORATORY CONTACT|INFORMATION|\(Contact the Certification|analytes/methods)', ln) or 'CERTIFICATION CATEGORIES' in ln: continue
    cm = CAT.search(ln)
    left = ln[:cm.start()] if cm else ln
    cats = [cm.group(1).strip()] if cm else []
    left = left.strip()
    if left and (cur is None or cur.get('phone')):
        cur = dict(left=[], cats=[], phone=None); blocks.append(cur)
    if cur is None: continue
    cur['cats'] += cats
    if not left: continue
    if re.match(r'(Certification|License)\s*#', left):
        cur['cert'] = re.sub(r'\s+', '', re.sub(r'^(Certification|License)\s*#\s*', '', left)); cur['seen_cert'] = True
    elif cur.get('seen_cert'):
        cur['phone'] = re.sub(r'^Phone:\s*', '', left)
    else:
        cur['left'].append(left)
assert len(blocks) == 39, len(blocks)
skipped = 0; out = []
for b in blocks:
    cats = []
    for c in b['cats']:
        for p in c.split('-Asbestos'): pass
        if c.endswith('-Asbestos'): cats += [c[:-9], 'Asbestos']
        else: cats.append(c)
    L = b['left']
    ci = next(i for i, x in enumerate(L) if re.search(r',?\s+[A-Z]{2}\s+\d{5}', x))
    cl = L[ci]; cmm = re.match(r'(.*?),?\s+([A-Z]{2})\s+(\d{5}(-\d{4})?)', cl)
    # name = lines up to the first line that starts with a digit or 'PO Box'
    k = next(i for i, x in enumerate(L) if re.match(r'(\d|PO Box|BLDG)', x))
    name = ' '.join(L[:k]); street = ', '.join(L[k:ci])
    if cmm.group(2) == 'RI': raise SystemExit('unexpected RI in out-of-state list: ' + name)
    well = [c for c in cats if c.startswith('Potable') or c == 'PFAS']
    if not well: skipped += 1; continue
    phone = re.sub(r'\s+', '', b['phone'])
    ph = re.sub(r'\D', '', phone); phone = '(%s) %s-%s' % (ph[:3], ph[3:6], ph[6:]) if len(ph) == 10 else b['phone']
    out.append(dict(name=name.replace('LLC- Cary', 'LLC - Cary'), address='%s, %s, %s %s' % (street, cmm.group(1).strip(), cmm.group(2), cmm.group(3)) if street else '%s, %s %s' % (cmm.group(1).strip(), cmm.group(2), cmm.group(3)),
        city=cmm.group(1).strip(), phone=phone, lab_id='RIDOH ' + b['cert'], group='limited', accredited_for=cats,
        detail='RIDOH certification %s. RIDOH says to contact its Certification Officer at (401) 222-5542 for the specific analytes and methods.' % b['cert'],
        source_name=SN_F, source_url=PDF, source_date='2026-03-18'))
out.sort(key=lambda l: l['name'].lower())
labs += out
n_oos = len(blocks)
write_state('rhode-island', 'Rhode Island', 'RI', labs,
 {'name': SN_P, 'page_url': PAGE, 'program_url': PAGE, 'report_date': 'Page updated Sept. 3, 2026; out-of-state PDF dated March 18, 2026'},
 {
 'title': 'Rhode Island certified drinking-water testing labs (RIDOH list)',
 'description': 'Rhode Island labs certified by RIDOH to test drinking water, plus the out-of-state labs RIDOH certifies, with certification categories, phone numbers and the source on every listing.',
 'intro': [
  "The Rhode Island Department of Health (RIDOH) publishes a short list of labs in Rhode Island and the surrounding area that are certified to test drinking water for a fee. The page (last updated September 3, 2026) names five: Eurofins North Kingstown, the RIDOH State Health Lab in Providence, Eurofins Warwick, Rhode Island Analytical Laboratories in Warwick and New England Testing Laboratory in West Warwick. It also points to one nearby out-of-state lab, Microbac in Dayville, CT.",
  "RIDOH links a second document, a PDF dated March 18, 2026, listing the nearby out-of-state labs it certifies. That PDF gives an address, phone number, RIDOH certification number and certified categories for each lab. We show the %d of its %d labs that are certified for at least one potable-water category or PFAS in a second group below." % (len(out), n_oos),
 ],
 'caveats': [
  "The RIDOH web page gives city and a link only for the five Rhode Island labs, with no street address, phone number or list of tests. The one exception is the State Health Lab, whose address and phone number are the State Health Laboratories location printed in the page footer. Use each lab's own website for the rest.",
  "The out-of-state PDF says to contact RIDOH's Certification Officer at (401) 222-5542 for the specific analytes and methods behind each category. Category names such as \"Potable water inorganic chemistry\" are broad.",
  "RIDOH says it does not endorse or recommend any of the certified labs, and that labs provide analytical services for a fee. Some labs (like Microbac in Dayville, CT) appear on both lists.",
  "We left out %d labs on the out-of-state PDF that are certified only for non-potable water, radiochemistry or environmental lead (paint, dust and soil) testing, since those are not drinking-water tests." % skipped,
  "RIDOH warns it is unlawful to test drinking water without certification, and that some companies offer \"free\" tests in exchange for a sales pitch for treatment systems. Use an independent certified lab before deciding on a treatment system.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Rhode Island labs on the RIDOH certified list',
 'limited_heading': 'Out-of-state labs RIDOH certifies (full details from the March 2026 PDF)',
 'limited_note': 'These labs are outside Rhode Island but are certified by RIDOH. Many take mailed samples. Check whether the lab accepts homeowner samples before you ship, and confirm the analytes with the lab.',
 'chips_label': 'RIDOH certification categories for this lab:',
 'resources': [
  {'label': 'RIDOH: Certified Drinking Water Testing Labs', 'url': PAGE},
  {'label': 'RIDOH: Nearby out-of-state certified laboratories (PDF, March 18, 2026)', 'url': PDF},
 ]})
