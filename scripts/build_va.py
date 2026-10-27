"""Virginia: DCLS "Drinking Water Laboratories with certification detail [excel]" (current as of 8/1/2026), fetched 2026-10-27."""
import openpyxl, collections, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src2')
URL = 'https://dgs.virginia.gov/content/dam/site-assets/dcls/Lab%20Certification/VELAP/Q3%202026%20VELAP/DW_Certified_Labs_20260801.xlsx'
PAGE = 'https://dgs.virginia.gov/division-of-consolidated-laboratory-services/certification-accreditation/find-a-lab/'
SN = 'Virginia DCLS, "Drinking Water Laboratories with certification detail" (Excel, current as of 8/1/2026)'
ws = openpyxl.load_workbook(os.path.join(SRC_DIR, 'va_dw.xlsx')).active
rows = [r for r in ws.iter_rows(values_only=True)][1:]
labs = collections.OrderedDict()
for r in rows:
    if r[0] is None: continue
    d = labs.setdefault(r[0], dict(name=r[1].strip(), exp=r[5], street=str(r[7]).strip(), city=str(r[8]).strip(), st=r[9], zip=str(r[10]), ph=[], an=set(), n=0))
    if r[18] and r[18] not in d['ph']: d['ph'].append(r[18])
    d['an'].add(str(r[17])); d['n'] += 1
CHEM = {'Nitrate','Nitrite','Arsenic','Lead','Copper','Fluoride','Manganese','Iron','Uranium','Sodium','Chloride','Sulfate'}
out = []; skipped_oos = 0
for k, d in labs.items():
    if d['st'] != 'VA':
        skipped_oos += 1; continue
    chips = key_chips(d['an'])
    bact = 'Total coliform' in chips or 'E. coli' in chips
    chem = bool(CHEM & set(chips))
    pub = looks_public(d['name'])
    grp = 'public' if pub else ('main' if bact and chem else 'limited')
    ph = clean_phone(d['ph'][0]) if d['ph'] else None
    l = dict(name=d['name'], address='%s, %s, VA %s' % (d['street'], d['city'], d['zip'][:5]), city=d['city'], phone=ph, lab_id=str(k),
             accredited_for=chips if chips else ['No well-test analytes (coliform, nitrate, metals, etc.) on the DCLS list for this lab'],
             detail='DCLS lab ID %s · certification expires %s · %d analyte/method entries on the DCLS list.' % (k, d['exp'].strftime('%B %-d, %Y') if d['exp'] else 'not printed', d['n']),
             group=grp, source_name=SN, source_url=URL, source_date='2026-08-01')
    out.append(l)
order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))
n_main = sum(1 for l in out if l['group'] == 'main')
write_state('virginia', 'Virginia', 'VA', out,
 {'name': SN, 'page_url': URL, 'program_url': PAGE, 'report_date': 'Current as of August 1, 2026 (DCLS quarterly list)'},
 {
 'title': 'Virginia state-certified drinking-water labs for private wells (DCLS list)',
 'description': 'Virginia-based labs on the Division of Consolidated Laboratory Services list of certified/accredited drinking-water labs (current as of Aug. 1, 2026), with the well-test analytes each is certified for and the source on every listing.',
 'intro': [
  "Virginia's Division of Consolidated Laboratory Services (DCLS) accredits and certifies the labs that may run drinking-water compliance tests. DCLS publishes the list as an Excel file with each lab's address, phone number (where printed), certificate expiration date and every analyte and method it is approved for. The version used here is marked \"Current as of 8/1/2026\".",
  "This page shows the labs located in Virginia (%d of the %d labs on the file) and pulls out the analytes a private-well owner usually cares about: coliform bacteria and E. coli, nitrate and nitrite, arsenic, lead and copper, and so on. Labs located outside Virginia are on DCLS's file too; we left them out to keep the page about in-state labs." % (len(out), len(labs)),
  "Labs approved for both bacteria and at least one chemistry analyte, and not run by a water utility or government agency, are listed first. That is the combination a basic well test needs.",
 ],
 'caveats': [
  "This is the certification list for public water system compliance testing. It does not say which labs accept samples from homeowners, and it does not list prices. Call the lab first.",
  "We sorted labs into groups by name: a lab whose name looks like a water authority, utility, city, town, county or agency is shown in the utility/agency group. That is our judgment from the name, not a field in the DCLS file.",
  "Only the analytes we recognised as common well tests are shown on each card. Many labs are approved for dozens more; the DCLS file is the full record.",
  "A phone number is shown only where the DCLS file prints one. Some labs have none listed.",
  "%d labs located outside Virginia (mostly large commercial labs in neighbouring and distant states) are on the DCLS file but not shown here." % skipped_oos,
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Virginia labs certified for bacteria and well-water chemistry',
 'public_heading': 'Water-authority, utility, city, county and agency labs on the same list',
 'public_note': 'These labs look from their names like they are run by a water system or agency for its own sampling. DCLS does not say whether they take homeowner samples. Call first.',
 'limited_heading': 'Labs approved for bacteria only, chemistry only, or specialty tests',
 'limited_note': 'Each of these is approved for only one kind of well test (for example bacteria only, or lead only) or for specialty analytes. You may need a second lab for a full panel.',
 'chips_label': 'Well-test analytes on the DCLS list for this lab:',
 'resources': [
  {'label': 'DCLS: Drinking Water Laboratories with certification detail (Excel, current as of 8/1/2026)', 'url': URL},
  {'label': 'DCLS: Find a Lab (accredited and certified laboratory lists)', 'url': PAGE},
  {'label': 'Virginia Department of Health: private well program', 'url': 'https://www.vdh.virginia.gov/environmental-health/onsite-water-programs/private-well-program/'},
 ]})
