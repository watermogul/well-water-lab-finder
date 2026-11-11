"""Idaho: Idaho Bureau of Laboratories (IBL) drinking-water lab certificates, fetched 2026-11-10.
Source: the "Drinking Water Lab Certification" folder (Laserfiche WebLink folder 2940) linked as
"View drinking water lab certificates" from the IDHW Drinking Water Testing and Certification page.
Each lab has one scanned certificate PDF per category (microbiology, inorganics, organics, PFAS,
radiochemistry). Certificates were OCR'd (rapidocr) and every name, address, EPA ID, effective period
and analyte status used below was checked by eye against the certificate image. Raw files are not
committed: /workspace/src-id/pdf/<docid>.pdf, folder listing in /workspace/src-id/tree.json.
In-state phone numbers come from the "Idaho Certified Laboratories" table on IDHW's Drinking Water and
Private Wells page (page last updated 2026-11-02). Certificates do not print phone numbers.
Grouping: main = the 8 labs on IDHW's table (7 commercial + IBL); public = other Idaho certificate
holders (2 city labs, 1 hospital lab); limited = out-of-state labs (certificates granted by reciprocity)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import more_lib
from more_lib import write_state

V = '2026-11-10'
more_lib.V = V
PAGE = 'https://healthandwelfare.idaho.gov/providers/idaho-laboratories-and-testing/drinking-water-testing-and-certification'
FOLDER = 'https://publicdocuments.dhw.idaho.gov/WebLink/Browse.aspx?id=2940&dbid=0&repo=PUBLIC-DOCUMENTS'
PW = 'https://healthandwelfare.idaho.gov/health-wellness/environmental-health/drinking-water-and-private-wells'
FORM = 'https://publicdocuments.dhw.idaho.gov/WebLink/DocView.aspx?id=15082&dbid=0&repo=PUBLIC-DOCUMENTS'
TOOLS = 'https://healthtools.dhw.idaho.gov/collections/other-environmental-health/products/idaho-private-well-water-testing'
PHD = 'https://healthandwelfare.idaho.gov/health-wellness/community-health/public-health-districts'
def doc(i): return 'https://publicdocuments.dhw.idaho.gov/WebLink/DocView.aspx?id=%d&dbid=0&repo=PUBLIC-DOCUMENTS' % i

# (docid, category label, effective period as printed, date the file was last modified in the folder)
# category: Micro, Inorganic, Organic, PFAS, Radiochemical
LABS = [
 # ---- main: IDHW's "Idaho Certified Laboratories" table (8 labs)
 dict(name='Idaho Bureau of Laboratories (state lab)', address='2220 Old Penitentiary Road, Boise, ID 83712', city='Boise', phone='(208) 334-2235', group='main', epa='ID00018',
      chips=['Bacteria (total coliform, E. coli)', 'Nitrate', 'Fluoride', 'Arsenic', 'Lead', 'Uranium', 'Organics (VOCs, pesticides, herbicides)'],
      certs=[(36256, 'Chemistry (EPA Region 10 letter, March 24, 2025; renewal due 2027)', '2026-03-31'), (36257, 'Microbiology (EPA Region 10 letter, May 23, 2025; renewal due 2027)', '2026-03-31')],
      note='The state lab is certified by EPA Region 10, not by its own program. It takes private well samples with its Private Well Owner submission form (see fees in the Idaho section above). EPA lab number ID00018 is printed on that form.'),
 dict(name='Analytical Laboratories, Inc.', address='1804 North 33rd Street, Boise, ID 83703', city='Boise', phone='(208) 342-5515', group='main', epa='ID00020',
      chips=['Bacteria (total coliform, E. coli)', 'Nitrate', 'Fluoride', 'Arsenic', 'Lead', 'Uranium', 'VOCs (EPA 524.2)'],
      certs=[(5125, 'Microbiological, July 1, 2026 to June 30, 2027', '2026-07-09'), (5073, 'Inorganic, 1/1/2026 to 12/31/2026', '2025-12-04'), (5251, 'Organic, 4/1/26 to 3/31/27', '2026-03-30')],
      note='Its organic certificate covers VOCs, trihalomethanes, glyphosate, carbofuran, oxamyl, diquat, endothall and haloacetic acids. The pesticides group (atrazine, alachlor and others) is marked "Certification Not Requested".'),
 dict(name='Anatek Labs, Inc. (Moscow)', address='1282 Alturas Drive, Moscow, ID 83843', city='Moscow', phone='(208) 883-2839', group='main', epa='ID00013',
      chips=['Bacteria (total coliform, E. coli)', 'Nitrate', 'Fluoride', 'Arsenic', 'Lead', 'Uranium', 'Organics (VOCs, pesticides, herbicides)', 'PFAS (EPA 533, 537.1)'],
      certs=[(5126, 'Microbiological, January 1, 2026 to December 31, 2026', '2026-02-12'), (5074, 'Inorganic, 11/1/2026 to 10/31/2027', '2026-10-27'), (22629, 'Organic incl. PFAS, 11/1/26 to 10/31/27', '2026-10-27')]),
 dict(name='IAS EnviroChem', address='3314 Pole Line Road, Pocatello, ID 83201', city='Pocatello', phone='(208) 237-3300', group='main', epa='ID00952',
      chips=['Bacteria (total coliform, E. coli)', 'Nitrate', 'Fluoride', 'Arsenic', 'Lead', 'Uranium'],
      certs=[(5202, 'Microbiological, October 1, 2026 to September 30, 2027', '2026-10-05'), (5112, 'Inorganic, 11/1/2026 to 10/31/2027', '2026-10-30')]),
 dict(name='Magic Valley Labs, Inc.', address='210 Addison Avenue, Twin Falls, ID 83301', city='Twin Falls', phone='(208) 733-4250', group='main', epa='ID00911',
      chips=['Bacteria (total coliform, E. coli)', 'Nitrate', 'Fluoride'],
      certs=[(5209, 'Microbiological, January 1, 2026 to December 31, 2026', '2026-02-12'), (5115, 'Inorganic, 1/1/2026 to 12/31/2026', '2025-12-29')],
      note='Its inorganic certificate covers nitrate, nitrite and fluoride only. Arsenic, lead, uranium and the other metals are marked "Certification Not Requested".'),
 dict(name='Teton Microbiology Laboratory, Inc.', address='300 S. Freeman Ave., Idaho Falls, ID 83401', city='Idaho Falls', phone='(208) 529-0077', group='main', epa='ID00969',
      chips=['Bacteria (total coliform, E. coli)'],
      certs=[(5232, 'Microbiological, October 1, 2026 to September 30, 2027', '2026-10-05')],
      note='Only a microbiological (bacteria) certificate is posted for this lab.'),
 dict(name='SVL Analytical, Inc.', address='One Government Gulch, Kellogg, ID 83837', city='Kellogg', phone='(208) 784-1258', group='main', epa='ID00019',
      chips=['Nitrate', 'Fluoride', 'Arsenic', 'Lead', 'Uranium'],
      certs=[(5122, 'Inorganic, 1/1/2025 to 12/31/2025 (expired as posted)', '2024-12-03')],
      note='The only certificate posted for SVL is its 2025 inorganic certificate, which ran to December 31, 2025. IDHW still lists SVL on its private well page (updated November 2, 2026). Ask the lab for its current Idaho certificate before you rely on it. No bacteria certificate is posted.'),
 dict(name='Accurate Testing Labs, LLC', address="7950 Meadowlark Way, Suite H, Coeur d'Alene, ID 83815", city="Coeur d'Alene", phone='(208) 762-8378', group='main', epa='ID00912',
      chips=['Bacteria (total coliform, E. coli)', 'Nitrate', 'Fluoride', 'Arsenic', 'Lead'],
      certs=[(5124, 'Microbiological, January 1, 2026 to December 31, 2026', '2026-02-12'), (14291, 'Inorganic, 1/1/2026 to 12/31/2026', '2025-12-29')],
      note="Uranium is marked \"Certification Not Requested\" on its inorganic certificate. Its microbiological certificate prints the address as 7950 Meadowlark Way, Coeur d'Alene, ID 83814 (no suite, different ZIP)."),
 # ---- public: other Idaho certificate holders
 dict(name='City of Idaho Falls Wastewater Treatment Laboratory', address='P.O. Box 50220, Idaho Falls, ID 83405', city='Idaho Falls', group='public', epa='ID00908',
      chips=['Bacteria (total coliform, E. coli)'], certs=[(31500, 'Microbiological, October 1, 2026 to September 30, 2027', '2026-10-05')]),
 dict(name='City of Pocatello Water Pollution Control Laboratory', address='P.O. Box 4169, Pocatello, ID 83205', city='Pocatello', group='public', epa='ID00028',
      chips=['Bacteria (total coliform, E. coli)'], certs=[(5223, 'Microbiological, October 1, 2026 to September 30, 2027', '2026-10-05')]),
 dict(name='Steele Memorial Medical Center', address='203 S. Daisy St., Salmon, ID 83467', city='Salmon', group='public', epa='ID00909',
      chips=['Bacteria (total coliform, E. coli)'], certs=[(5229, 'Microbiological, October 1, 2026 to September 30, 2027', '2026-10-05')]),
]
# ---- limited: out-of-state labs (name, address, EPA ID, [(docid, category, period, modified)])
OOS = [
 ('ACZ Laboratories, Inc.', '2773 Downhill Dr., Steamboat Springs, CO 80487', 'CO00028', [(5070, 'Inorganic', '10/1/2026 to 9/30/2027', '2026-10-15'), (5264, 'Radiochemical', '10/1/2026 to 9/30/2027', '2026-10-15')]),
 ('Alliance Technical Group, LLC - Akron', '3310 Win Street, Cuyahoga Falls, OH 44223', 'OH00923', [(32268, 'Inorganic', '6/1/2026 to 5/31/2027', '2026-05-05'), (32311, 'Organic', '6/1/2026 to 5/31/2027', '2026-05-05'), (32372, 'Radiochemical', '6/1/2026 to 5/31/2027', '2026-06-02')]),
 ('ALS Environmental - Cincinnati, OH', '4388 Glendale-Milford Road, Cincinnati, OH 45242', 'OH01323', [(5071, 'Inorganic', '4/1/2026 to 3/31/2027', '2026-03-27')]),
 ('Anatek Labs, Inc. - Spokane', '504 E. Sprague Ave., Suite D, Spokane, WA 99202', 'WA00169', [(5127, 'Microbiological', 'January 1, 2026 to December 31, 2026', '2026-04-16'), (5075, 'Inorganic', '1/1/2026 to 12/31/2026', '2025-11-24'), (5253, 'Organic', '1/1/2026 to 12/31/26', '2025-11-24'), (5267, 'Radiochemical', '1/1/2026 to 12/31/2026', '2025-11-24')]),
 ('Chemtech-Ford, LLC', '9632 S 500 W, Sandy, UT 84070', 'UT00027', [(35645, 'Inorganic', '2/1/2026 to 1/31/2027', '2026-01-23'), (36127, 'Organic', '2/1/26 to 1/31/27', '2026-03-06')]),
 ('EMSL Analytical, Inc.', '200 Route 130 North, Cinnaminson, NJ 08077', 'NJ00337', [(5085, 'Inorganic', '7/1/2026 to 6/30/2027', '2026-07-08'), (36903, 'Organic', '6/1/2026 to 6/30/2027', '2026-07-08'), (26763, 'Radiochemical', '7/1/2026 to 6/30/2027', '2026-07-08')]),
 ('Energy Laboratories, Inc. (Billings)', '1120 South 27th Street, Billings, MT 59101', 'MT00005', [(5106, 'Inorganic', '1/1/2026 to 12/31/2026', '2025-12-12'), (24197, 'Organic', '1/1/2026 to 12/31/2026', '2026-03-06')]),
 ('Energy Laboratories, Inc. (Casper)', '2393 Salt Creek Highway, Casper, WY 82601', 'WY00002', [(5100, 'Inorganic', '8/1/2026 to 7/31/2027', '2026-07-08'), (5255, 'Organic', '8/1/26 to 7/31/2027', '2026-07-08'), (5268, 'Radiochemical', '8/1/2026 to 7/31/2027', '2026-07-08')]),
 ('Eurofins Built Environment Testing East', '730 SE Maynard Road, Cary, NC 27511', 'NC02074', [(35559, 'Inorganic', '2/1/2026 to 1/31/2027', '2026-01-07')]),
 ('Eurofins Eaton Analytical, LLC - Pomona', '941 Corporate Center Dr., Pomona, CA 91768', 'CA00006', [(25741, 'Microbiological', 'April 1, 2026 to March 31, 2027', '2026-04-16'), (25239, 'Inorganic', '2/1/2026 to 1/31/2027', '2026-02-09'), (25240, 'Organic', '2/1/2026 to 1/31/2027', '2026-02-09'), (33945, 'PFAS', '2/1/2025 to 1/31/2026 (expired as posted)', '2025-06-13')]),
 ('Eurofins Edge Analytical', '1620 S. Walnut Street, Burlington, WA 98233', 'WA00097', [(32431, 'Inorganic', '2/1/2025 to 1/31/2026 (expired as posted)', '2025-02-04'), (32433, 'Organic', '2/1/2025 to 1/31/2026 (expired as posted)', '2025-02-04')]),
 ('Eurofins Environment Testing Northwest / Eurofins Environment Testing - Spokane', '11922 East First Avenue, Spokane Valley, WA 99206', 'WA01220', [(36367, 'Microbiological', 'March 2, 2026 to March 1, 2027', '2026-04-16'), (35560, 'Inorganic', '1/1/2026 to 12/31/2026', '2026-01-07')]),
 ('Eurofins South Bend', '110 South Hill Street, South Bend, IN 46617', 'IN00035', [(35582, 'Inorganic', '1/1/2026 to 12/31/2026', '2026-01-12'), (35583, 'Organic', '1/1/2026 to 12/31/2026', '2026-01-12'), (35584, 'Radiochemical', '1/1/2026 to 12/31/2026', '2026-01-12')]),
 ('GEL Laboratories, LLC', '2040 Savage Road, Charleston, SC 29407', 'SC00012', [(5111, 'Inorganic', '4/1/2026 to 3/31/2027', '2026-03-06'), (5259, 'Organic', '4/1/2026 to 3/31/2027', '2026-03-06'), (33115, 'PFAS', '4/1/2025 to 3/31/2026 (expired as posted)', '2025-04-11'), (5274, 'Radiochemical', '4/1/2026 to 3/31/2027', '2026-03-06')]),
 ('National Testing Laboratories, Ltd.', '556 South Mansfield Street, Ypsilanti, MI 48197', 'MI00044', [(5116, 'Inorganic', '1/1/2026 to 12/31/2026', '2026-02-18'), (5260, 'Organic', '1/1/2026 to 12/31/2026', '2026-02-18')]),
 ('Pace Analytical National Center for Testing & Innovation', '12065 Lebanon Road, Mt. Juliet, TN 37122', 'TN00003', [(5119, 'Inorganic', '10/1/2026 to 9/30/2027', '2026-09-22'), (5262, 'Organic', '10/1/2026 to 9/30/2027', '2026-09-22'), (5278, 'Radiochemical', '10/1/2026 to 9/30/2027', '2026-09-22')]),
 ('Pace Analytical Services, LLC (Minneapolis)', '1700 Elm Street SE, Suite 200, Minneapolis, MN 55414', 'MN00064', [(5118, 'Inorganic', '1/1/2026 to 12/31/2026', '2026-01-07'), (5261, 'Organic', '1/1/2026 to 12/31/2026', '2026-01-07')]),
 ('Pace Analytical Services, LLC (Sheridan, WY)', '1673 Terra Avenue, Sheridan, WY 82801', 'WY00005', [(11386, 'Inorganic', '7/1/2026 to 6/30/2027', '2026-06-08')]),
 ('Pace Analytical Services, LLC - Greensburg', '1638 Roseytown Road, Suites 2, 3 & 4, Greensburg, PA 15601', 'PA01457', [(5277, 'Radiochemical', '4/1/2026 to 3/31/2027', '2026-03-18')]),
 ('Teton County Water Laboratory', '460 E. Pearl, Jackson, WY 83001', 'WY00934', [(33813, 'Microbiological', 'April 1, 2026 to December 31, 2027', '2026-06-10')]),
 ('Tshimakain Creek Laboratories, LLC', '5505 E Broadway Ave. #102, Spokane Valley, WA 99212', 'WA01260', [(30366, 'Microbiological', 'May 1, 2026 to November 21, 2026', '2026-06-10'), (29610, 'Inorganic', '5/1/2026 to 4/30/2027', '2026-05-04')]),
 ('Weck Laboratories, Inc.', '14859 Clark Avenue, Industry, CA 91745', 'CA00211', [(36711, 'Inorganic', '6/1/2026 to 5/31/2027', '2026-06-02'), (32446, 'Organic', '6/1/2026 to 5/31/2027', '2026-06-02'), (35615, 'PFAS', '6/1/2026 to 5/31/2027', '2026-06-03'), (36712, 'Radiochemical', '6/1/2026 to 5/31/2027', '2026-06-02')]),
]
CHIP = {'Microbiological': 'Bacteria certificate', 'Inorganic': 'Inorganics certificate', 'Organic': 'Organics certificate', 'PFAS': 'PFAS certificate', 'Radiochemical': 'Radiochemistry certificate'}

out = []
for l in LABS:
    certs = l['certs']
    newest = max(c[2] for c in certs)
    first = certs[0]
    r = {'name': l['name'], 'address': l['address'], 'city': l['city']}
    if l.get('phone'): r['phone'] = l['phone']
    r['accredited_for'] = l['chips']
    r['detail'] = 'EPA lab ID %s. Certificates posted by the Idaho Bureau of Laboratories: %s.' % (l['epa'], '; '.join(c[1] for c in certs))
    r['group'] = l['group']
    r['source_url'] = doc(first[0])
    r['source_name'] = 'IBL certificate folder: %s' % first[1].split(',')[0].split(' (')[0]
    r['source_date'] = newest
    r['last_verified'] = V
    if l['group'] == 'main' and l['name'].startswith('Idaho Bureau') is False:
        r['source_url_2'] = PW
        r['source_name_2'] = "IDHW Drinking Water and Private Wells page, \"Idaho Certified Laboratories\" table (phone; page updated 2026-11-02)"
    elif l['name'].startswith('Idaho Bureau'):
        r['source_url_2'] = FORM
        r['source_name_2'] = 'IBL Private Well Owner Drinking Water Analysis Submission Form (revised 08/21/2024)'
    if l.get('note'): r['note'] = l['note']
    if len(certs) > 1:
        r['note'] = (r.get('note', '') + ' Other certificate files: ' + ', '.join('%s (%s)' % (c[1].split(',')[0], doc(c[0])) for c in certs[1:]) + '.').strip()
    out.append(r)
for name, addr, epa, certs in OOS:
    city = addr.split(', ')[-2]
    newest = max(c[3] for c in certs)
    cats = []
    for c in certs:
        lbl = CHIP[c[1]] + (' (expired)' if 'expired' in c[2] else '')
        if lbl not in cats: cats.append(lbl)
    r = {'name': name, 'address': addr, 'city': city, 'accredited_for': cats,
         'detail': 'EPA lab ID %s. Idaho certificates posted: %s.' % (epa, '; '.join('%s, %s' % (c[1], c[2]) for c in certs)),
         'group': 'limited', 'source_url': doc(certs[0][0]),
         'source_name': 'IBL certificate folder: %s %s certificate' % (name, certs[0][1].lower()),
         'source_date': newest, 'last_verified': V}
    notes = []
    if all('expired' in c[2] for c in certs):
        notes.append('Every certificate posted for this lab had expired before we checked. Ask the lab or IBL whether it is still certified for Idaho.')
    if name.startswith('Eurofins Environment Testing Northwest'):
        notes.append('The bacteria certificate is issued to "Eurofins Environment Testing - Spokane" (filed in the folder as Eurofins Eaton Analytical Spokane) and the inorganic certificate to "Eurofins Environment Testing Northwest"; both print the same address and EPA ID, so they are shown as one lab.')
    if name.startswith('Tshimakain'):
        notes.append('Its bacteria certificate ends November 21, 2026.')
    if 'Billings' in name:
        notes.append('The organics certificate prints the name as "Energy Laboratory, Inc."')
    if len(certs) > 1:
        notes.append('Other certificate files: ' + ', '.join('%s (%s)' % (c[1], doc(c[0])) for c in certs[1:]) + '.')
    if notes: r['note'] = ' '.join(notes)
    out.append(r)

from collections import Counter
c = Counter(l['group'] for l in out)
ncerts = sum(len(l['certs']) for l in LABS) + sum(len(x[3]) for x in OOS)
write_state('idaho', 'Idaho', 'ID', out,
    {'name': 'Idaho Bureau of Laboratories drinking-water lab certificates (folder "Drinking Water Lab Certification")',
     'page_url': FOLDER, 'program_url': PAGE,
     'report_date': 'Certificates posted between December 2024 and October 30, 2026; folder checked November 10, 2026'},
    {
     'title': 'Idaho certified drinking-water labs for private well testing (state certificates, Nov 2026)',
     'description': 'All %d labs with an Idaho drinking-water certificate posted by the Idaho Bureau of Laboratories, what each in-state lab is certified to test (bacteria, nitrate, arsenic, uranium), and state lab fees.' % len(out),
     'intro': [
      'Idaho does not publish a single list of certified drinking-water labs. Instead, the Idaho Bureau of Laboratories (IBL), part of the Idaho Department of Health and Welfare (IDHW), posts each lab\'s certificate in a public document folder linked from its Drinking Water Testing and Certification page ("View Idaho and Out of State Drinking Water Certificates for Inorganics, Organics, Microbiology, and Radiochemistry"). We opened every certificate in that folder on November 10, 2026. Together they cover %d labs, %d in Idaho and %d out of state. Each listing below shows the certificates and effective dates as printed, and links the certificate itself.' % (len(out), c['main'] + c['public'], c['limited']),
      'IDHW says about 30% of Idaho residents use private wells as their main source of drinking water, that private wells are not regulated, and that well owners should test for bacteria and nitrate once a year and for other contaminants, including metals and chemicals, every 3 to 5 years. Its Drinking Water and Private Wells page (updated November 2, 2026) lists eight labs under "Idaho Certified Laboratories"; those eight are the first group below.',
      'Free state testing (currently sold out): IDHW\'s private wells page announces "Free Idaho Private Well Water Testing (Available Fall 2026)" for nitrate, fluoride, arsenic, lead, uranium, manganese, chromium, nickel, copper, zinc, selenium, cadmium and barium. Bacteria are not on that list. Kits are requested through the Idaho Health Tools site, one kit per household every five years, and results are shared on IDHW\'s groundwater map without names or addresses. IDHW warns processing "may take up to two months." When we checked on November 10, 2026 the Idaho Health Tools listing was marked "Sold Out" and said testing is offered "while funding lasts."',
      'Paying the state lab directly: IBL\'s Private Well Owner Drinking Water Analysis Submission Form (revised August 21, 2024, as posted in IBL\'s forms folder) lists these prices: total coliform/E. coli $21, nitrate $20, fluoride $20, arsenic $23, lead $23, uranium $23, copper $13, manganese $13, iron $13, hardness $28, TDS $16, and gross alpha/beta by quote. The form says bacteria samples must reach the lab within 30 hours of collection in a sterile bottle from IBL, nitrate must be tested within 48 hours, and bottles come from IBL or your local public health district. The form is more than two years old, so confirm prices with IBL at (208) 334-2235 before you send a sample.',
     ],
     'caveats': [
      'Certification is not the same as taking homeowner samples. Certificates say what a lab is certified to test for public water systems; they do not say who accepts samples from the public, prices or turnaround. Call first and ask about bottles, fees and drop-off hours.',
      'Chips for Idaho labs come from each certificate: an analyte is shown only if the certificate marks it "C" (certified). Chips for out-of-state labs show only which certificate types are posted, not individual tests.',
      'Some posted certificates had already expired when we checked (for example SVL Analytical\'s 2025 inorganic certificate and Eurofins Edge Analytical\'s certificates). These are flagged on each listing. The folder may lag behind renewals, so ask the lab or IBL for current status.',
      'The grouping is ours: the first group is the eight labs on IDHW\'s private wells page; the second is the other Idaho certificate holders (two city labs and a hospital lab); the third is labs outside Idaho, which hold Idaho certificates by reciprocity.',
      'Phone numbers for the first group are from IDHW\'s private wells page. The certificates do not print phone numbers, so none are shown for the other labs.',
      'We did not verify prices (except IBL\'s published form), turnaround times or websites for any lab, so none are shown.',
     ],
     'main_heading': 'Idaho labs on IDHW\'s private well page (7 commercial labs and the state lab)',
     'public_heading': 'Other Idaho labs with a posted certificate (city and hospital labs)',
     'public_note': 'These hold bacteria certificates only. They are run by a city or a hospital. The certificates do not say whether they take homeowner samples. Call first.',
     'limited_heading': 'Out-of-state labs with Idaho certificates',
     'limited_note': 'These labs are outside Idaho and hold Idaho certificates by reciprocity. Ask about shipping, bottles and hold times before you collect. IBL\'s own form requires bacteria samples to arrive within 30 hours of collection; ask each lab for its limit.',
     'chips_label': 'Certified in Idaho for (from the posted certificates):',
     'resources': [
      {'label': 'IDHW: Drinking Water Testing and Certification (Idaho Bureau of Laboratories)', 'url': PAGE},
      {'label': 'IBL: Drinking Water Lab Certification folder (all certificates)', 'url': FOLDER},
      {'label': 'IDHW: Drinking Water and Private Wells (testing advice, lab table, free testing program)', 'url': PW},
      {'label': 'IBL: Private Well Owner Drinking Water Analysis Submission Form (PDF, revised 08/21/2024, prices)', 'url': FORM},
      {'label': 'Idaho Health Tools: Idaho Private Well Water Testing (free kit; marked Sold Out on 2026-11-10)', 'url': TOOLS},
      {'label': 'IDHW: Public Health Districts (local contacts and sample bottles)', 'url': PHD},
     ],
    })
