"""Connecticut: CT DPH Environmental Lab Certification, "In-State Approved Commercial Laboratories Certified to Test Drinking Water" (10/09/2026)
plus street addresses from the same program's "A List of Approved In-State Commercial Environmental Laboratories" (updated 07/02/2026), matched on license number. Fetched 2026-10-27.
Analyte marks were read from the PDF with pdfplumber by column position and checked against the page image (17 labs)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
URL = 'https://portal.ct.gov/dph/-/media/dph/dph-2025/environmental-lab-certification/lab-lists/in-state-laboratories-certified-to-test-drinking-water_20261009.pdf'
URL2 = 'https://portal.ct.gov/dph/-/media/dph/dph-2025/environmental-lab-certification/lab-lists/in-state-approved-commercial-environmental-labs_072026.pdf'
PAGE = 'https://portal.ct.gov/dph/environmental-health/environmental-laboratory-certification/environmental-laboratory-certification'
SN = 'Connecticut DPH Environmental Lab Certification, "In-State Approved Commercial Laboratories Certified to Test Drinking Water" (10/09/2026)'
SN2 = 'Connecticut DPH Environmental Lab Certification, "A List of Approved In-State Commercial Environmental Laboratories" (updated 07/02/2026), used for the street address'
COL = {'PWT': 'Accepts private well samples (Connecticut DPH marking)', 'Asb': 'Asbestos', 'As': 'Arsenic', 'Bact': 'Bacteriological (total coliform and/or E. coli)',
       'Inorg': 'Inorganics (inorganic chemicals, physical, sanitary chemicals, nitrate, metals: some or all)',
       'Org': 'Organic chemicals (semi-volatiles, haloacetic acids, VOCs, pesticides, PCBs, synthetic organics: some or all)',
       'PFAS': 'PFAS', 'Rad': 'Radiological (gross alpha/beta, radium, radon, uranium: some or all)', 'U': 'Uranium by EPA Method 200.8'}
# town, name, license, phone (drinking-water list), street (address list), zip, marks
R = [
 ('Dayville','Microbac Laboratories, INC. - Dayville','PH-0465','(860) 774-6814','61 Louisa Viens Drive','06241','PWT As Bact Inorg Org U'),
 ('Greenwich','Greenwich Health Department Laboratory','PH-0703','(203) 622-7843','101 Field Point Road','06830','PWT As Bact Inorg Rad'),
 ('Madison','Environmental Consulting Lab','PH-0535','(203) 245-0568','1005 Boston Post Road','06443','PWT As Bact Inorg U'),
 ('Manchester','Phoenix Environmental Laboratories, Inc.','PH-0618','(860) 645-1102','587 East Middle Turnpike','06040','As Bact Inorg Org U'),
 ('Meriden','EMSL Analytical, Inc. - CT','PH-0322','(203) 284-5948','165 Gracey Avenue','06451','PWT Asb Bact'),
 ('New Haven','Regional Water Authority','PH-0411','(203) 401-2700','90 Sargent Drive','06511','PWT As Bact Inorg Org PFAS'),
 ('Newtown','ALS Environmental - Newtown','PH-0843','(203) 270-9973','56 Church Hill Road #2','06470','PWT As Bact Inorg Org Rad U'),
 ('Old Saybrook','Eastern Analytical Laboratory, Inc.','PH-0448','(860) 388-2378','134 Boston Post Road','06475','PWT Bact Inorg'),
 ('Rocky Hill','Northeast Laboratories, Inc','PH-0404','(860) 828-9787','30 Cold Spring Road','06067','PWT Bact Inorg'),
 ('Stamford','Stamford Health Department Laboratory','PH-0710','(203) 977-4378','888 Washington Blvd.','06901','PWT Bact Inorg'),
 ('Stratford','Complete Environmental Testing, Inc.','PH-0116','(203) 377-9984','80 Lupes Drive','06615','As Bact Inorg Org PFAS U'),
 ('Stratford','ALS Environmental - Stratford','PH-0840','(203) 325-1371','120 Research Drive','06615','As Inorg Org U'),
 ('Wallingford','Environmental Monitoring Lab','PH-0509','(203) 284-0555','59 North Plains Industrial Road, Suite A','06492','PWT As Bact Inorg Org'),
 ('Waterbury','Northwest Environmental Water Labs','PH-0537','(203) 437-4110','450 Meriden Road','06705','PWT As Bact Inorg'),
 ('Wilton','South Norwalk Electric & Water Laboratory','PH-0461','(203) 762-7884','164 Old Boston Road','06897','Bact Inorg'),
 ('Windsor','Envirotech Laboratory','PH-0464','(860) 688-7249','77 Cook Hill Road','06095','PWT Bact Inorg Rad'),
 ('Woodbridge','Aquatek Labs, Inc.','PH-0466','(203) 389-1824','3 Research Drive','06525','PWT As Bact Inorg Org Rad U'),
]
labs = []
for town, name, ph, phone, street, zp, marks in R:
    m = marks.split()
    pwt = 'PWT' in m
    grp = 'main' if (pwt and 'Bact' in m and 'Inorg' in m) else 'limited' if pwt else 'public'
    labs.append(dict(name=name, address='%s, %s, CT %s' % (street, town, zp), city=town, phone=phone, lab_id=ph,
        accredited_for=[COL[k] for k in m if k != 'PWT'], group=grp,
        detail='Connecticut DPH license %s.%s' % (ph, ' Connecticut DPH marks this lab as accepting private well samples.' if pwt else ' Not marked by Connecticut DPH as accepting private well samples.'),
        source_name=SN, source_url=URL, source_date='2026-10-09', source_name_2=SN2, source_url_2=URL2, source_date_2='2026-07-02'))
order = {'main': 0, 'limited': 1, 'public': 2}
labs.sort(key=lambda l: (order[l['group']], l['name'].lower()))
write_state('connecticut', 'Connecticut', 'CT', labs,
 {'name': SN, 'page_url': URL, 'program_url': PAGE, 'report_date': 'List dated October 9, 2026'},
 {
 'title': 'Connecticut state-approved drinking-water labs (CT DPH list)',
 'description': 'The 17 in-state commercial labs approved by Connecticut DPH to test drinking water (list dated Oct. 9, 2026), with which ones accept private well samples, certified test groups and the source on every listing.',
 'intro': [
  "Connecticut's Department of Public Health (DPH) approves commercial labs to test drinking water and publishes a list of the in-state ones. The list dated October 9, 2026 has 17 labs. Connecticut says all of them are approved to test drinking water, but only some offer testing for private wells, and the list marks those.",
  "For each lab the list marks which groups of tests it is approved for: arsenic, bacteriological, inorganics, organic chemicals, PFAS, radiological, uranium and asbestos. Street addresses come from DPH's separate approved in-state commercial environmental laboratories list (updated July 2, 2026), matched on the DPH license number.",
 ],
 'caveats': [
  "The list covers Connecticut labs only. DPH says information on out-of-state approved labs is available from its approval program at (860) 509-7389.",
  "DPH defines its groups loosely: \"Inorganics\", \"Organic Chemicals\" and \"Radiological\" each mean some or all of a set of tests, not every test in the set. DPH suggests calling (860) 509-7389 to verify the parameters a lab is certified for within a group.",
  "Labs marked as accepting private well samples and certified for both bacteriological and inorganics tests are shown first. The heading for the last group says which labs the list does not mark for private wells.",
  "The phone number is from the October 9 drinking-water list. For South Norwalk Electric & Water Laboratory the July address list shows a different number, (203) 866-3366 ext. 259. Check which one works before you drive over.",
  "Lab director names on the address list are not reproduced.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Connecticut labs that accept private well samples: bacteria and inorganics',
 'limited_heading': 'Accept private well samples for a narrower set of tests',
 'limited_note': 'Connecticut marks these as accepting private well samples, but its list shows approval for only part of a basic well test (for example bacteria and asbestos only).',
 'public_heading': 'Approved for drinking water but not marked as accepting private well samples',
 'public_note': 'These labs are on the same Connecticut DPH list, but DPH does not mark them for private well testing. Some serve water systems or other commercial clients. Call first to ask whether they would take a homeowner sample.',
 'chips_label': 'Test groups the Connecticut list marks for this lab:',
 'resources': [
  {'label': 'CT DPH: In-State Approved Commercial Laboratories Certified to Test Drinking Water (PDF, 10/09/2026)', 'url': URL},
  {'label': 'CT DPH: Approved In-State Commercial Environmental Laboratories (PDF, updated 07/02/2026)', 'url': URL2},
 ]})
