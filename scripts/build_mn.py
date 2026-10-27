"""Minnesota: MDH "Accredited Labs in Minnesota Accepting Drinking Water Samples from Private Well Users" (Oct. 2026), fetched 2026-10-27.
Table transcribed from the PDF text and checked against rendered page images (pages 3-4). Flags order: coliform, nitrate, arsenic, lead, manganese.
'X' = lab performs it, '*' = subcontracted (asterisk on the MDH list), '-' = blank on the list. Star = courier / drop-off network marked on the list."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
URL = 'https://www.health.state.mn.us/communities/environment/water/docs/wells/waterquality/labmap.pdf'
PAGE = 'https://www.health.state.mn.us/communities/environment/water/wells/waterquality/index.html'
SN = 'Minnesota Department of Health, "Accredited Labs in Minnesota Accepting Drinking Water Samples from Private Well Users" (October 2026)'
R = [
 (1,'Fillmore SWCD Water Quality Laboratory','Fillmore','900 Washington Street NW','Preston, MN 55965','507-765-3878','X----',False),
 (2,'Southeastern Minnesota Water Analysis Laboratory','Olmsted','2100 Campus Drive SE, Suite 100','Rochester, MN 55904','507-328-7495','XX***',True),
 (3,'UC Laboratory','Waseca','129 North Main Street','Janesville, MN 56048','507-234-5835','XX**X',True),
 (4,'Worthington Public Utilities Laboratory','Nobles','1950 27th Street N','Worthington, MN 56187','507-372-8660','X----',False),
 (5,'Southwest Health and Human Services','Lyon','607 West Main Street, Suite 200','Marshall, MN 56258','507-537-6713','XX---',False),
 (6,'Minnesota Valley Testing Laboratories, Inc.','Brown','1126 North Front Street','New Ulm, MN 56073','507-354-8517','XXXXX',False),
 (7,'Red Wing City Laboratory','Goodhue','1020 East Fifth Street','Red Wing, MN 55066','651-385-5143','X----',False),
 (8,'RMB Environmental Laboratories, Inc. - Burnsville','Hennepin','501 Highway 13 E, Suite 104','Burnsville, MN 55337','952-456-8470','XX***',True),
 (9,'Tri-City/William Lloyd Analytical Lab','Hennepin','9300 Poplar Bridge Road','Bloomington, MN 55437','952-563-4904','XXX-X',True),
 (10,'Twin City Water Clinic, Inc.','Hennepin','617 13th Avenue S','Hopkins, MN 55343','952-935-3556','XXXX*',False),
 (11,'Engel Water Testing, Inc.','Hennepin','9300 County Road 15','Minnetrista, MN 55359','952-955-1800','X***-',False),
 (12,'Pace Analytical Services, LLC - Minneapolis','Hennepin','1700 Elm Street SE, Suite 200','Minneapolis, MN 55414','612-607-1700','XXXXX',False),
 (13,'EMSL Analytical, Inc.','Hennepin','3410 Winnetka Avenue N','New Hope, MN 55427','763-449-4922','XXXXX',False),
 (14,'Instrumental Research, Inc.','Anoka','7800 Main Street NE','Fridley, MN 55432','763-571-3698','XX**-',False),
 (15,'Water Laboratories, Inc.','Sherburne','333 Main Street NW','Elk River, MN 55330','763-441-7509','XXXX-',False),
 (16,'Traut Water Analysis Lab','Stearns','32640 County Road 133','St. Joseph, MN 56374','320-251-5090','XX**-',False),
 (17,'Steven M. Traut Wells, Inc.','Douglas','754 Cross Country Lane SW','Alexandria, MN 56308','320-762-1528','XX**-',True),
 (18,'A.W. Research Laboratories, Inc.','Crow Wing','314 Charles Street','Brainerd, MN 56401','218-829-7974','XXXXX',True),
 (19,'RMB Environmental Laboratories, Inc. - Pequot Lakes','Crow Wing','30968 S. Washington Avenue','Pequot Lakes, MN 56472','218-828-2118','X****',True),
 (20,'RMB Environmental Laboratories, Inc. - Detroit Lakes','Becker','22796 County Highway 6','Detroit Lakes, MN 56501','218-846-1465','XXXXX',True),
 (21,'Pace Analytical Services, LLC - Duluth','St. Louis','4730 Oneota Street','Duluth, MN 55807','218-727-6380','XX***',False),
 (22,'RMB Environmental Laboratories, Inc. - Virginia','St. Louis','110 \u00bd South 15th Avenue W','Virginia, MN 55792','218-440-2043','XX***',True),
 (23,'Pace Analytical Services, LLC - Virginia','St. Louis','315 Chestnut Street','Virginia, MN 55792','218-727-6380','X****',False),
 (24,'AC Analytical & Consulting, LLC','Beltrami','21518 Basset Drive NW','Puposky, MN 56667','218-243-3328','XX**-',False),
 (25,'Koochiching Health Department Water Testing','Koochiching','1000 Fifth Street','International Falls, MN 56649','218-283-7070','X----',False),
]
AN = ['Total coliform bacteria', 'Nitrate (as N)', 'Arsenic', 'Lead', 'Manganese']
labs = []
for no, name, cty, street, cz, ph, fl, star in R:
    assert len(fl) == 5
    chips = []; sub = []
    for a, f in zip(AN, fl):
        if f == 'X': chips.append(a)
        elif f == '*': chips.append(a + ' (subcontracted)'); sub.append(a.lower())
    det = 'MDH map number %d · %s County.' % (no, cty)
    if sub: det += ' Marked with an asterisk on the MDH list (sample is subcontracted to another accredited lab): %s.' % ', '.join(sub)
    if star: det += ' MDH marks this lab with a star: it offers a courier service network or other drop-off locations (contact the lab for sites).'
    labs.append(dict(name=name, address='%s, %s' % (street, cz), city=cz.split(',')[0], phone=clean_phone(ph), lab_id='MDH map #%d' % no,
        accredited_for=chips, detail=det, group='main', source_name=SN, source_url=URL, source_date='2026-10-01'))
write_state('minnesota', 'Minnesota', 'MN', labs,
 {'name': SN, 'page_url': URL, 'program_url': PAGE, 'report_date': 'October 2026'},
 {
 'title': 'Minnesota accredited labs that accept private-well water samples (MDH list)',
 'description': 'The 25 labs on the Minnesota Department of Health list of accredited labs accepting drinking-water samples from private well users (October 2026), with the tests each offers, subcontracting notes and the source on every listing.',
 'intro': [
  "The Minnesota Department of Health (MDH) publishes a map and table of accredited labs that accept drinking-water samples from private well owners. The October 2026 edition lists 25 labs across the state. Unlike most state lists, this one is specifically for homeowners: every lab on it takes samples from private well users.",
  "The table covers five tests MDH recommends for well water: total coliform bacteria, nitrate (as N), arsenic, lead and manganese. An asterisk on the MDH list means the lab subcontracts that test to another accredited lab; we show that as \"(subcontracted)\". A blank on the MDH list means the lab is not listed for that test.",
 ],
 'caveats': [
  "MDH says the list is informational, is not an endorsement, and that other labs may hold accreditation for the same tests but not appear here. MDH points to its accredited-lab search for other analytes (choose the Safe Drinking Water Program and tick \"Accepts samples from private homeowners\").",
  "The list covers only coliform, nitrate, arsenic, lead and manganese. If you want another contaminant, such as PFAS or VOCs, call the lab or use MDH's search.",
  "MDH lists no prices. Fees, hours and sample-bottle pick-up vary by lab, so call first.",
  "Some labs on the list are run by a county, city, utility or conservation district. MDH includes them because they accept private samples.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Minnesota labs that accept private-well samples (MDH list)',
 'chips_label': 'Tests listed by MDH for this lab:',
 'resources': [
  {'label': 'MDH: Accredited Labs in Minnesota Accepting Drinking Water Samples from Private Well Users (PDF, October 2026)', 'url': URL},
  {'label': 'MDH: Search for Accredited Laboratories', 'url': 'https://www.health.state.mn.us/labsearch'},
  {'label': 'MDH: well water testing for private wells', 'url': 'https://www.health.state.mn.us/communities/environment/water/wells/waterquality/index.html'},
 ]})
