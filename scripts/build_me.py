"""Maine: Maine CDC Drinking Water Program, "Maine In-State Commercial Drinking Water Labs" (last updated 5/16/2026), fetched 2026-10-27.
Transcribed from the PDF text (12 labs); the list prints city only, no street address."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
URL = 'https://www.maine.gov/dhhs/mecdc/sites/maine.gov.dhhs.mecdc/files/CommercialListMaineLabs.pdf'
PAGE = URL
SN = 'Maine CDC Drinking Water Program, "Maine In-State Commercial Drinking Water Labs" (last updated 5/16/2026)'
R = [  # code, name, restriction, website, city, phone
 ('BGL','Bigelow Laboratory for Ocean Sciences','PFAS only','https://www.bigelow.org/','East Boothbay','(207) 315-2567'),
 ('CLWR','ClearWater Laboratory (A Division of Acheron Engineering)',None,'https://www.acheronengineering.com/','Newport','(207) 368-5786'),
 ('LAB-EWA','Eurofins Auburn (Previously A&L)',None,'http://www.allaboratory.com/','Auburn','(207) 784-5354'),
 ('LAB-EEP','Eurofins Portland ME','Bacteria only','https://www.eurofinsus.com/','Portland','(207) 846-6569'),
 ('HETL','Health and Environmental Testing Laboratory',None,'https://www.maine.gov/dhhs/mecdc/services/maine-public-health-laboratory/environmental-chemistry','Augusta','(207) 287-2727'),
 ('KTHDN','Katahdin Analytical Services (SGS Scarborough)',None,'http://www.katahdinlab.com','Scarborough','(207) 874-2400'),
 ('MEC','Maine Coast Laboratory (DBA Water Quality & Compliance Services Inc.)',None,'http://www.waterqualityservicesme.com','Wiscasset','(207) 882-5476'),
 ('MLN','Maine Laboratories, LLC','PFAS only','https://www.mainelaboratories.com/','Norridgewock','(207) 518-8030'),
 ('MNL',"Mi'Kmaq Environmental Laboratory",'Bacteria only','https://watertestlab.com/laboratory/','Presque Isle','(207) 764-4001'),
 ('NLSON','Nelson Analytical Lab',None,'http://www.nelsonanalytical.com','Kennebunk','(207) 467-3478'),
 ('NELAB','NELAnalytical (Previously Northeast Laboratory Services)',None,'http://www.nelabservices.com','Winslow','(207) 873-7711'),
 ('NAP','Nova Analytic Labs (DBA Nova EnviroLabs)','PFAS only','https://www.novaenvirolabs.com/','Portland','(207) 804-7327'),
]
labs = []
for code, name, restr, web, city, ph in R:
    chips = ['PFAS only (as printed by Maine CDC)'] if restr == 'PFAS only' else ['Bacteria only (as printed by Maine CDC)'] if restr else ['Accredited by test: ask the lab which drinking-water tests it is accredited for']
    labs.append(dict(name=name, address='%s, ME (the Maine list prints city only)' % city, city=city, phone=ph, website=web, lab_id=code,
        accredited_for=chips, detail='Maine lab code %s.%s' % (code, ' Maine CDC marks this lab "%s".' % restr if restr else ''),
        group='limited' if restr else 'main', source_name=SN, source_url=URL, source_date='2026-05-16'))
labs.sort(key=lambda l: (l['group'] != 'main', l['name'].lower()))
write_state('maine', 'Maine', 'ME', labs,
 {'name': SN, 'page_url': URL, 'program_url': PAGE, 'report_date': 'Last updated May 16, 2026'},
 {
 'title': 'Maine in-state commercial drinking-water labs (Maine CDC list)',
 'description': 'The 12 in-state commercial labs on the Maine CDC Drinking Water Program list (updated May 16, 2026), with phone numbers, websites and which are bacteria-only or PFAS-only, and the source on every listing.',
 'intro': [
  "The Maine CDC Drinking Water Program publishes a short list of in-state commercial drinking-water labs. The version used here was last updated May 16, 2026 and has 12 labs. For each it prints a lab code, name, website, city and phone number, and marks labs that do only PFAS or only bacteria testing.",
  "Maine's list does not print street addresses or specific tests. It tells you instead that labs are accredited test by test, so you need to ask each lab what it is accredited for. The list links to a separate Excel file of all labs accredited by Maine, including out-of-state labs.",
 ],
 'caveats': [
  "The list gives city only, so each listing shows the city and says so. Use the lab's website or phone for the street address and drop-off options.",
  "Maine CDC warns that labs are accredited by test, that the tests a lab can do change regularly, and that you should confirm with the lab. For help, call the Maine Drinking Water Program at 207-287-2070 and ask for the Laboratory Accreditation Officer.",
  "If you mail a sample, check that the lab can receive bacteria samples within the holding time from your postal area. Many labs offer statewide service.",
  "Labs not marked PFAS-only or bacteria-only are shown first. Maine's list does not say what they test for; it is not a promise they accept homeowner samples.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Maine commercial drinking-water labs (not marked bacteria-only or PFAS-only)',
 'limited_heading': 'Bacteria-only and PFAS-only labs',
 'limited_note': 'Maine CDC marks each of these as doing only one kind of test. You would need a second lab for a full well-water panel.',
 'chips_label': 'What the Maine CDC list says about this lab:',
 'resources': [
  {'label': 'Maine CDC: In-State Commercial Drinking Water Labs (PDF, updated 5/16/2026)', 'url': URL},
 ]})
