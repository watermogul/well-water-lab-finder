"""Builds src/_data/labs/new-york.json from county health department lab lists + the NYS DOH PFAS-method lab table.
All sources fetched 2026-11-13 (copies in $SRC_DIR, default /workspace/src-ny). Hand-entered from the county lists
(each is 3-10 labs); the PFAS table is parsed from the saved NYS DOH HTML (check.png / x.png per method column).
Nothing here is inferred: every field is as printed by the cited source; differences between sources are stated in the card."""
import json, os, re, html
V = '2026-11-13'
SRC = os.environ.get('SRC_DIR', '/workspace/src-ny')

S = {
 'wc': dict(name='Westchester County Dept. of Health, "Private Well-Water Testing Law" registered lab list',
            url='https://health.westchestercountyny.gov/images/stories/PDF/List_of_Labs_for_Private_Well_2025.pdf',
            date='No printed date (file named 2025; PDF last modified 2026-04-07)', chip='Westchester County PWT-law list'),
 'rc': dict(name='Rockland County Dept. of Health, Private Well Testing Law registered laboratories',
            url='https://ny.rocklandcountyny.gov/home/showpublisheddocument/924/639184073142130000',
            date='Rev 6/2026', chip='Rockland County PWT-law list'),
 'du': dict(name='Dutchess County Behavioral & Community Health, "Local Laboratories for Water Testing"',
            url='https://www.dutchessny.gov/Departments/DBCH/Local-Laboratories-for-Water-Testing.htm',
            date='Web page with no printed date', chip='Dutchess County list'),
 'sa': dict(name='Saratoga County Dept. of Health, "NYSDOH ELAP Certified Laboratories for Drinking Water Analysis"',
            url='https://www.saratogacountyny.gov/wp/wp-content/uploads/2026/06/DoH-WaterSuppliers-LabList-20260618.pdf',
            date='Revised 2026 (PDF dated 2026-06-18)', chip='Saratoga County list'),
 'on': dict(name='Onondaga County Health Dept., Environmental Health "Laboratory Information" (labs for Onondaga, Cortland and Cayuga counties)',
            url='https://onondaga.gov/health-env/laboratory/',
            date='Web page, last modified 2025-06-26', chip='Onondaga County list (also covers Cortland, Cayuga)'),
 'tc': dict(name='Tompkins County Environmental Health Division, "Water Testing Labs"',
            url='https://www.tompkinscountyny.gov/files/assets/county/v/1/whole-health-environmental-health/documents/water-testing-labs.pdf',
            date='Updated 3/26/2024', chip='Tompkins County list'),
 'pf': dict(name='NYS DOH, Private Well PFAS Pilot "Accredited Post-Treatment Testing Laboratory List"',
            url='https://health.ny.gov/environmental/water/drinking/privatewellspilot/labs.htm',
            date='Revised August 2026', chip=None),
}
MENU = 'NYS ELAP search tool\'s lab-name menu (fetched 2026-11-13; the search itself needs a reCAPTCHA check, so we could not pull each lab\'s scope)'

def lab(name, address, city, phone, srcs, detail, elap=None, website=None, extra_chips=(), note=None):
    first = S[srcs[0]]
    d = dict(name=name, address=address, city=city, phone=phone, group='main',
             accredited_for=[S[k]['chip'] for k in srcs if S[k]['chip']] + list(extra_chips),
             detail=detail, source_name=first['name'], source_url=first['url'], source_date=first['date'], last_verified=V)
    if elap: d['elap_id'] = elap
    if website: d['website'] = website
    if len(srcs) > 1:
        d['source_name_2'] = S[srcs[1]]['name'] + ' [' + S[srcs[1]]['date'] + ']'
        d['source_url_2'] = S[srcs[1]]['url']
    if len(srcs) > 2:
        d['detail'] += ' Also listed by: ' + '; '.join(S[k]['name'] + ' (' + S[k]['date'] + ', ' + S[k]['url'] + ')' for k in srcs[2:]) + '.'
    if note: d['note'] = note
    return d

main = [
 lab('Advanced Analytical Technologies, Inc.', '37 Ramland Rd, Orangeburg, NY 10962', 'Orangeburg', '(800) 259-9532', ['wc','rc'],
     'Registered for private-well testing-law work in both Westchester and Rockland counties. Rockland prints a second number, (845) 494-2938, and the website aatec.com. Name in the ' + MENU + ': "Advanced Analytical Technologies".',
     elap='11713', website='https://aatec.com'),
 lab('Analytical Laboratory Service (ALS)', '34 Dogwood Lane, Middletown, PA 17057', 'Middletown, PA', '(800) 794-7709', ['wc','pf'],
     'Westchester prints ELAP 11759 and "Ext. 3135". The NYS DOH PFAS lab table (August 2026) lists ELAP 11759 as "ALS Environmental - Middletown", 301 Fulling Mill Rd., Middletown, PA 17057, 717-944-5541, accredited for EPA Methods 533 and 537.1 v2. The two sources print different street addresses; confirm with the lab.',
     elap='11759', extra_chips=['PFAS: EPA 533 + 537.1 v2 (NYS DOH table)']),
 lab('York Analytical Lab, dba Aqua Environmental Lab', '56 Church Hill Rd, Newtown, CT 06470', 'Newtown, CT', '(203) 270-9973', ['wc'],
     'Name as printed by Westchester. Rockland\'s June 2026 list shows "ALS USA" at the same phone number, (203) 270-9973, and the ELAP search menu has "ALS Environmental - Newtown" but no Aqua or York entry. That suggests a name change, but no source we read says so; ask the lab which name it reports under.',
     elap='11706'),
 lab('ALS USA (Rockland County listing)', 'Street address not printed on the Rockland list', 'Rockland County list', '(203) 270-9973', ['rc'],
     'Rockland lists this lab with website alsglobal.com/usaenviro and a local sampling contact: Master Home Inspection, Brian Kiernan, (914) 589-9949. Same phone as the Newtown, CT lab Westchester lists as Aqua Environmental Lab (above). Name in the ' + MENU + ': "ALS Environmental - Newtown" (match by phone and town, not confirmed by Rockland).',
     website='https://www.alsglobal.com/usaenviro'),
 lab('Carnell Environmental Inspections, Inc.', '26 Legion Dr, Valhalla, NY 10595', 'Valhalla', '(914) 946-4300', ['wc'],
     'On Westchester\'s list with ELAP 11588. We did not find this name in the ' + MENU + '. Confirm its current ELAP status before you hire it.',
     elap='11588'),
 lab('Environmental Labworks, Inc.', 'PO Box 733, Marlboro, NY 12542 (Dutchess prints 1348 Route 9W, Marlboro, NY 12542)', 'Marlboro', '(845) 236-7823', ['wc','du'],
     'Westchester prints ELAP 10824 and a PO box; Dutchess County prints the street address 1348 Route 9W and says the labs it lists "accept water samples from the public for a fee". Name in the ' + MENU + ': "Environmental Labworks Inc".',
     elap='10824'),
 lab('Pace Analytical Services, LLC – Newburgh (Westchester lists it as EnviroTest Laboratories, Inc.)', '315 Fullerton Ave, Newburgh, NY 12550', 'Newburgh', '(845) 562-0890', ['du','wc','rc'],
     'Dutchess lists "Pace Analytical Services, LLC – Newburgh – ELAP ID 10142" at 315 Fullerton Avenue, Newburgh 12550. Westchester lists the same ELAP number, street and phone as "EnviroTest Laboratories, Inc." (its PDF prints ZIP 12250). Rockland lists "Pace Analytical" at the same phone, with website pacelabs.com and a local sampling contact, SEBI Environmental Services, Inc., (845) 789-1307. Name in the ' + MENU + ': "Pace Analytical Services, LLC-Newburgh".',
     elap='10142', website='https://www.pacelabs.com'),
 lab('Phoenix Environmental Laboratories, Inc.', '587 East Middle Turnpike, Manchester, CT 06040', 'Manchester, CT', '(860) 645-1102 or (860) 645-3513', ['wc'],
     'Name in the ' + MENU + ': "Phoenix Environmental Labs".', elap='11715', website='https://www.phoenixlabs.com'),
 lab('Yorktown Medical Laboratories, Inc.', '321 Kear Street, Yorktown Heights, NY 10598', 'Yorktown Heights', '(914) 245-3203', ['wc'],
     'Name in the ' + MENU + ': "Yorktown Medical Laboratory Inc".', elap='10323'),
 lab('Westchester County Laboratories and Research', '10 Dana Road, Valhalla, NY 10595', 'Valhalla', '(914) 231-1781', ['wc','pf'],
     'County-run lab. The NYS DOH PFAS lab table (August 2026) lists it (ELAP 10108, 914-231-1768) as accredited for EPA Method 537.1 v2, not 533, and links its well-water testing page: https://labs.westchestercountyny.gov/environmental-services/well-water-testing (Westchester\'s PDF prints the older address labs.westchestergov.com).',
     elap='10108', website='https://labs.westchestercountyny.gov/environmental-services/well-water-testing', extra_chips=['PFAS: EPA 537.1 v2 (NYS DOH table)']),
 lab('Aquatek Labs', '3 Research Drive, Woodbridge, CT 06525', 'Woodbridge, CT', '(203) 623-9804', ['wc'],
     'Name in the ' + MENU + ': "Aquatek Labs".', elap='12170'),
 lab('AG Environmental', 'Street address not printed on the Rockland list', 'Rockland County list', '(845) 704-8151', ['rc'],
     'Rockland lists website agerny.com and four local sampling contacts: AG Environmental, (845) 704-8151 x416; Joel Lang Associates, (914) 419-3103; Magnificent Pump Service, Inc., (845) 371-7288; SEBI Environmental Services, Inc., (845) 789-1307. Closest name in the ' + MENU + ': "AG Environmental RSC LLC dba Sullivan County Labs" (not confirmed by Rockland).',
     website='https://agerny.com'),
 lab('Kingston Water Department Lab', '1442 Sawkill Road, Kingston, NY 12401', 'Kingston', '(845) 679-2216', ['du'],
     'Dutchess prints ELAP ID 10160 and says the labs it lists accept water samples from the public for a fee. Name in the ' + MENU + ': "Kingston Water Department Lab".', elap='10160'),
 lab('Pace Analytical (Ballston Spa)', '27 Kent Street, Ballston Spa, NY 12020', 'Ballston Spa', '(518) 884-0800', ['sa'],
     'Saratoga County says it has no preference among labs as long as they are ELAP certified. The ' + MENU + ' has many Pace locations but none named for Ballston Spa; ask the lab which ELAP ID it reports under.', website='https://www.pacelabs.com/'),
 lab('Capital Region Environmental Lab (satellite laboratory)', '7 Hemphill Place, Suite 231, Malta, NY 12020', 'Malta', '(518) 400-8014', ['sa'],
     'Name in the ' + MENU + ': "Capital Region Environmental Laboratory".', website='https://crenvlab.com/'),
 lab('Capital Region Environmental Lab (main laboratory)', '137 Columbia Turnpike, Rensselaer, NY 12144', 'Rensselaer', '(518) 949-2020', ['sa'],
     'Main lab of the same company as the Malta satellite above.', website='https://crenvlab.com/'),
 lab('Queensbury Laboratory', '823 Corinth Rd., Queensbury, NY 12804', 'Queensbury', '(518) 793-8866', ['sa'],
     'Saratoga gives the Town of Queensbury water department\'s web page as its website; call to ask whether it takes homeowner samples. Name in the ' + MENU + ': "Queensbury Laboratory".', website='https://www.queensburyny.gov/departments/water/'),
 lab('Adirondack Environmental Services, Inc.', '314 North Pearl Street, Albany, NY 12207', 'Albany', '(518) 434-4546', ['sa','pf'],
     'Also on the NYS DOH PFAS lab table (August 2026) as ELAP 10709, accredited for EPA Method 533 (not 537.1 v2).', website='https://www.adirondackenvironmental.com/', extra_chips=['PFAS: EPA 533 (NYS DOH table)']),
 lab('JH Consulting Group, Inc.', '15 Lynwood Drive, Loudonville, NY 12211', 'Loudonville', '(518) 785-9839', ['sa'],
     'Saratoga prints no website. Name in the ' + MENU + ': "JH Consulting Group, Inc".'),
 lab('Certified Environmental Services', '7280 Caswell Street, North Syracuse, NY 13212', 'North Syracuse', '(315) 478-2374', ['on'],
     'Onondaga calls these "approved laboratories for drinking water bacteriology and nitrates" and recommends private-well owners test at least once a year for total coliform and nitrate. Name in the ' + MENU + ': "Certified Environmental Services Inc".',
     extra_chips=['Bacteria + nitrate (Onondaga)']),
 lab('Microbac New York – Cortland', '3821 Buck Drive, Cortland, NY 13045', 'Cortland', '(607) 753-3403', ['on','tc'],
     'Onondaga lists it for drinking-water bacteriology and nitrates; Tompkins lists it for microbiological, inorganic and organic analyses. Name in the ' + MENU + ': "Microbac New York-Cortland".',
     extra_chips=['Bacteria + nitrate (Onondaga)', 'Microbiological, inorganic, organic (Tompkins)']),
 lab('Panek Laboratory LLC dba JLI Environmental Laboratories', '42 Washington Street (#6 per Tompkins), Auburn, NY 13021', 'Auburn', '(315) 253-4433', ['on','tc'],
     'Onondaga lists it for drinking-water bacteriology and nitrates; Tompkins lists it as "JLI Environmental Laboratories" for microbiological and inorganic analyses. Name in the ' + MENU + ': "Panek Laboratory LLC dba JLI Environmental Laboratories".',
     extra_chips=['Bacteria + nitrate (Onondaga)', 'Microbiological, inorganic (Tompkins)']),
 lab('Community Science Institute (CSI)', '95 Brown Rd, Rm 283 Langmuir Lab, Ithaca, NY 14850', 'Ithaca', '(607) 257-6606', ['tc'],
     'Tompkins lists it for microbiological, inorganic and organic analyses. Name in the ' + MENU + ': "Community Science Institute, Inc.".',
     extra_chips=['Microbiological, inorganic, organic (Tompkins)']),
]

# ---- NYS DOH PFAS-method table (parsed from saved HTML)
t = open(os.path.join(SRC, 'nys_pfas_labs.html'), encoding='utf-8', errors='replace').read()
i = t.find('<td>10709</td>'); tb = t[t.rfind('<table', 0, i):t.find('</table>', i)]
rows, seen = [], set()
for p in re.split(r'<tr[^>]*>', tb)[1:]:
    c = re.split(r'<td[^>]*>', p)[1:]
    if len(c) < 7: continue
    tx = lambda s: re.sub(r'\s+', ' ', html.unescape(re.sub(r'<br\s*/?>', ' | ', re.sub(r'</?(?!br)[^>]+>', '', s)))).strip(' |')
    m533, m537 = 'check.png' in c[5], 'check.png' in c[6]
    assert ('x.png' in c[5]) != m533 and ('x.png' in c[6]) != m537
    r = dict(name=tx(c[0]), phone=tx(c[1]).strip(' |'), address=tx(c[2]).replace(' | ', ', '), elap=tx(c[3]), type=tx(c[4]), m533=m533, m537=m537)
    h = re.search(r'href="([^"]+)"', c[0]); r['href'] = h.group(1).split('?')[0] if h else None
    if r['elap'] in seen: continue
    seen.add(r['elap']); rows.append(r)
assert len(rows) == 39, len(rows)
in_main = {'10108', '10709', '11759'}
pf = S['pf']; lim = []
for r in rows:
    if r['elap'] in in_main: continue
    meth = [m for m, ok in (('EPA 533', r['m533']), ('EPA 537.1 v2', r['m537'])) if ok]
    st = re.search(r',\s*([A-Z]{2})\s+[0-9A-Z]', r['address'])
    city = re.search(r',\s*([^,]+),\s*[A-Z]{2}\s+[0-9A-Z]', r['address'])
    d = dict(name=r['name'], address=r['address'], city=(city.group(1) if city else ''), phone=r['phone'], elap_id=r['elap'], elap_src='the NYS DOH PFAS lab table', group='limited',
             accredited_for=['PFAS: ' + ' + '.join(meth), r['type'] + ' lab (as listed)'],
             detail='Listed by NYS DOH as New York State accredited for ' + ' and '.join(meth) + ' (PFAS). ' + ('Out-of-state lab (' + st.group(1) + ').' if st and st.group(1) != 'NY' else 'New York lab.') + ' This table is for PFAS tests only; it does not say the lab takes other well-water tests or homeowner samples.',
             source_name=pf['name'], source_url=pf['url'], source_date=pf['date'], last_verified=V)
    if r['href']: d['website'] = r['href']
    lim.append(d)
lim.sort(key=lambda d: (', NY ' not in d['address'], d['name']))
for d in main:
    assert d['address'] and d['source_url'].startswith('https://')
out = dict(state='New York', slug='new-york', abbr='NY',
           list_source=dict(name='County health department lab lists (Westchester, Rockland, Dutchess, Saratoga, Onondaga, Tompkins) + NYS DOH PFAS lab table; NYS ELAP search',
                            page_url=S['wc']['url'],
                            report_date='County lists dated 2024 to June 2026 (see each listing); NYS DOH PFAS table revised August 2026; all fetched November 13, 2026',
                            search_url='https://healthapps.health.ny.gov/pubdoh/applinks/wc/elappublicweb/'),
           last_verified=V, labs=main + lim)
json.dump(out, open('src/_data/labs/new-york.json', 'w'), indent=1, ensure_ascii=False)
print('main', len(main), 'pfas-only', len(lim), 'total', len(main) + len(lim))
