"""Tennessee: TDEC Division of Water Resources, "Laboratories Certified for Drinking Water Analyses - Commercial Laboratories" (list dated 10/06/2026), fetched 2026-10-27."""
import os, sys, re, subprocess, datetime
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src2')
URL = 'https://www.tn.gov/content/dam/tn/environment/water/drinking-water-unit/wr_wq_dw_certified-commercial-labs.pdf'
PAGE = 'https://www.tn.gov/environment/program-areas/wr-water-resources/water-quality/drinking-water-redirect/lab-certification-program.html'
SN = 'Tennessee TDEC, "Laboratories Certified for Drinking Water Analyses: Commercial Laboratories" (list dated 10/06/2026)'
txt = open(os.path.join(SRC_DIR, 'tn_certified-commercial-labs.txt')).read()
txt = txt.split('Out of State Laboratories')[0] if False else txt
lines = txt.split('\n')
instate = True; labs = []; cur = None
def mdy(s):
    m, d, y = s.split('/'); return datetime.date(int(y), int(m), int(d))
i = 0
blocks = []; cur = None
for ln in [x.replace('\f', '') for x in lines]:
    if 'Out of State Laboratories' in ln: instate = False; continue
    if re.search(r'Certified Contaminant Groups|Page \d+ of 12|Certified for Drinking Water Analysis$|A laboratory may not be approved|TDEC Division', ln) or not ln.strip(): continue
    if re.match(r'^\S', ln) and not ln.startswith(' ') and not re.match(r'^(Section|regarding|certified by|The Department|designated|from those|Any questions|Laboratories Certified)', ln):
        cur = dict(name=ln.strip(), lines=[], instate=instate); blocks.append(cur); continue
    if cur is not None: cur['lines'].append(ln)
today = datetime.date(2026, 10, 27)
out = []; oos = 0; expired = 0
for b in blocks:
    ls = b['lines']
    addr = []; phone = None; chem = bact = None; labid = None; groups = []
    for ln in ls:
        s = ln.strip()
        m = re.search(r'Chem\. Cert\. Expire:\s*(\d+/\d+/\d{4})?', ln)
        if m: chem = m.group(1); 
        m = re.search(r'Lab ID#:\s*(\S+)', ln)
        if m: labid = m.group(1)
        m = re.search(r'Bact\. Cert\. Expire:\s*(\d+/\d+/\d{4})?', ln)
        if m: bact = m.group(1)
        if 'Cert. Expire' in ln or 'Lab ID#' in ln: continue
        if re.match(r'^\d{3}-\d{3}-\d{4}', s): phone = s; continue
        if ln.startswith('                         '): groups.append(s); continue
        addr.append(s)
    # addr = [contact person, street..., city st zip]
    assert len(addr) >= 3, (b['name'], addr)
    street = ', '.join(addr[1:-1]); citystate = addr[-1]
    cm = re.match(r'(.*?),\s*([A-Z]{2})\s+(\d{5}(-\d{4})?)', citystate)
    assert cm, (b['name'], citystate)
    if not b['instate'] or cm.group(2) != 'TN': oos += 1; continue
    cx = mdy(chem) if chem else None; bx = mdy(bact) if bact else None
    live_c = cx and cx >= today; live_b = bx and bx >= today
    if not (live_c or live_b): expired += 1; continue
    gs = [g for g in groups if g]
    inorg = any('Inorganics' in g for g in gs); bacg = any(re.match(r'(Enzyme|Membrane)', g) for g in gs)
    grp = 'main' if (inorg and bacg and live_c and live_b) else 'limited'
    def fmt(kind, s, x):
        if not s: return 'no %s certification listed' % kind
        return '%s certification expires %s%s' % (kind, s, '' if x >= today else ' (already expired as of Oct. 27, 2026)')
    det = 'TDEC lab ID %s · %s · %s.' % (labid, fmt('chemistry', chem, cx or today), fmt('bacteriology', bact, bx or today))
    out.append(dict(name=b['name'], address='%s, %s, TN %s' % (street, cm.group(1), cm.group(3)), city=cm.group(1), phone=clean_phone(phone),
        lab_id=labid, accredited_for=gs, detail=det, group=grp, source_name=SN, source_url=URL, source_date='2026-10-06'))
order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))
write_state('tennessee', 'Tennessee', 'TN', out,
 {'name': SN, 'page_url': URL, 'program_url': PAGE, 'report_date': 'List dated October 6, 2026'},
 {
 'title': 'Tennessee state-certified drinking-water labs (TDEC commercial lab list)',
 'description': 'Tennessee-based commercial labs certified by TDEC for drinking-water chemistry and bacteria (list dated Oct. 6, 2026), with certified analysis groups, expiration dates and the source on every listing.',
 'intro': [
  "The Tennessee Department of Environment and Conservation (TDEC) certifies labs for drinking-water analysis and publishes a list of commercial laboratories. The list in use here is dated October 6, 2026, and splits labs into \"In State\" and \"Out of State\". Each entry shows the lab's address, phone number, lab ID, the expiration dates of its chemistry and bacteriology certifications, and the contaminant groups it is certified for.",
  "This page shows the in-state labs whose certifications were still unexpired on October 27, 2026. A lab with both a current chemistry certification (including inorganics and trace metals) and a current bacteriology certification (enzyme-substrate or membrane-filter coliform testing) is shown first.",
 ],
 'caveats': [
  "TDEC states that this list is for determining whether samples count for compliance with maximum contaminant levels. It does not say which labs accept samples from homeowners and does not list prices. Call the lab first.",
  "TDEC notes that a lab may not be approved for every parameter within a group. For example, \"Inorganics/Trace Metals\" does not mean every metal. Ask the lab for the exact analytes.",
  "The PDF prints two dates: 10/2/2026 in the header of page 1 and 10/06/2026 in each page footer. We use the footer date (10/06/2026) as the list date.",
  "We used only TDEC's commercial-laboratories list. Labs on that list that are located outside Tennessee (%d) and labs whose certifications had all expired as of Oct. 27, 2026 (%d) are left out." % (oos, expired),
  "The TDEC contact-person names printed on the list are not reproduced here.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Tennessee labs certified for both chemistry and bacteria',
 'limited_heading': 'Labs certified for bacteria only, chemistry only, or specialty tests',
 'limited_note': 'Each of these is certified for only part of a basic well test (for example bacteria only, or radiochemistry only) or has one certification that has expired. You may need a second lab for a full panel.',
 'chips_label': 'TDEC-certified groups for this lab:',
 'resources': [
  {'label': 'TDEC: Laboratories certified for drinking-water analyses, commercial labs (PDF, 10/06/2026)', 'url': URL},
  {'label': 'TDEC: Drinking-water laboratory certification program', 'url': PAGE},
 ]})
