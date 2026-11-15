"""Builds src/_data/labs/maryland.json from MDE's "Maryland's Certified Drinking Water Laboratories" PDF
("Latest Revisions: 10/1/2026"), hand-transcribed from `pdftotext -layout` output of
https://mde.maryland.gov/programs/water/water_supply/Documents/Maryland-Certified-DW-Labs.pdf (fetched 2026-10-26).
In-state labs are hand-entered below. Out-of-state labs (added 2026-11-14) come from
scripts/parse_md_oos.py -> $SRC_DIR/oos.json (default /workspace/src-md), parsed from the same PDF.
Re-verified 2026-11-14: the PDF fetched that day is byte-identical to the 2026-10-26 copy (md5 eb55267c433d8b6e26e485de60ceb609). Test codes are expanded using MDE's approved-contaminant list
(MD Approved Parameter List.pdf, "Revised 10/10/2024"). Self-check: every name, phone and cert number must appear in the source text."""
import json, re, os, sys
V = '2026-11-14'
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-md')
SRC = 'https://mde.maryland.gov/programs/water/water_supply/Documents/Maryland-Certified-DW-Labs.pdf'
PARAMS = 'https://mde.maryland.gov/programs/water/water_supply/Documents/MD%20Approved%20Parameter%20List.pdf'
UMD = 'https://www.extension.umd.edu/programs/environment-natural-resources/program-areas/wells-septic-systems-and-water-quality/water-quality-and-testing/certified-water-testing-labs'
CODES = {
 'Micro 1': 'Micro 1: total coliform / E. coli (multi-tube fermentation)',
 'Micro 2': 'Micro 2: total coliform (membrane filtration)',
 'Micro 3': 'Micro 3: heterotrophic plate count',
 'Micro 4': 'Micro 4: enzyme substrate test (coliform bacteria)',
 'Micro 5': 'Micro 5: E. coli enumeration',
 'Metals 1': 'Metals 1: lead, copper',
 'Metals 2': 'Metals 2: antimony, arsenic, barium, beryllium, cadmium, chromium, mercury, selenium, thallium',
 'Arsenic': 'Arsenic',
 'Uranium': 'Uranium',
 'Inorganics 1': 'Inorganics 1: nitrate',
 'Inorganics 2': 'Inorganics 2: nitrite',
 'Inorganics 3': 'Inorganics 3: fluoride',
 'Inorganics 4': 'Inorganics 4: asbestos',
 'Inorganics 5': 'Inorganics 5: cyanide',
 'Inorganics 6': 'Inorganics 6: chlorite',
 'Asbestos': 'Asbestos',
 'VOCs': 'VOCs (volatile organic chemicals, e.g. benzene, TCE, vinyl chloride)',
 'THMs': 'THMs (trihalomethanes)',
 'HAA5': 'HAA5 (haloacetic acids)',
 'SOC 1': 'SOC 1: synthetic organics (e.g. benzo(a)pyrene, atrazine, PCBs, pentachlorophenol)',
 'SOC 2': 'SOC 2: dioxin (2,3,7,8-TCDD)',
 'SOC 3': 'SOC 3: EDB, DBCP',
 'Pesticides 1': 'Pesticides 1: endrin, lindane, methoxychlor, toxaphene, chlordane, heptachlor and others',
 'Pesticides 2': 'Pesticides 2: alachlor, atrazine, simazine',
 'Pesticides 3': 'Pesticides 3: aldicarb, carbofuran, oxamyl',
 'Pesticides 4': 'Pesticides 4: PCBs',
 'Pesticides 5': 'Pesticides 5: diquat',
 'Pesticides 6': 'Pesticides 6: endothall',
 'Pesticides 7': 'Pesticides 7: glyphosate',
 'Herbicides': 'Herbicides (2,4-D, silvex, pentachlorophenol, dinoseb, dalapon, picloram)',
 'Radiologicals': 'Radiologicals (gross alpha/beta, radium 226/228, uranium and others)',
 'PFAS': 'PFAS (PFOA, PFOS, PFHxS, PFNA, HFPO-DA, PFBS)',
}
# name, street, city, zip, county code, phone(s), cert no., approved tests (as printed), group, note
L = [
 ('Aberdeen Advanced Wastewater Treatment Plant Laboratory','361 Michael Lane','Aberdeen','21001','HA','(410) 272-2650','G-1002','Micro 3, 4','public',None),
 ('Abingdon Water Treatment Plant Laboratory','3340 Abingdon Road','Abingdon','21009','HA','(410) 638-3939','G-1058','Micro 4, 5; PFAS','public',None),
 ('Advanced Environmental Concepts, Inc','5201 Holniker Drive','Sykesville','21784','CL','(410) 939-5550','333','VOCs; THMs','limited',None),
 ('AMA Analytical Services, Inc','4475 Forbes Boulevard','Lanham','20706','PG','(301) 450-3346','262','Metals 1; Inorganics 4','limited',None),
 ('American Water Laboratory - Fort Meade','3220 Laurel Fort Meade Road','Laurel','20724','AA','(301) 289-7027','342','Micro 4','public',None),
 ('Anne Arundel County Utilities Central Lab','437 Maxwell Frye Road','Millersville','21108','AA','(410) 222-8420','G-1005','Micro 3, 4','public',None),
 ('Ashburton Water Quality Laboratory','3001 Druid Park Drive','Baltimore','21215','BC','(410) 396-0150','G-1006','Micro 1, 3, 4, 5; Inorganics 1, 2, 3','public',None),
 ('Baltimore County Bureau of Utilities Engineering & Regulation Lab','4419 Bucks School House Road','Baltimore','21237','BA','(410) 887-5489','G-1050','Inorganics 1, 2, 3; Metals 1, 2; VOCs; THMs','public',None),
 ('Caliber Analytical Services, LLC','8851 Orchard Tree Lane','Towson','21286','BA','(410) 220-5212','320','Metals 1, 2; THMs; VOCs','limited',None),
 ('Certified Water Testing, LLC','15009 North Franklinville Road','Thurmont','21788','FR','(301) 663-5323','135','Micro 4, 5; Inorganics 1, 2','main','umd'),
 ('Chesapeake Environmental Laboratory, Inc','302 Love Point Road','Stevensville','21666','QA','(410) 643-0800','181','Micro 3, 4, 5; Inorganics 1, 2, 3; Metals 1; Arsenic','main','umd;MDE also prints (800) 300-TEST for this lab.'),
 ('City of Frederick Water Quality Laboratory','100 Treatment Plant Road','Frederick','21701','FR','(301) 600-1473','G-1016','Micro 3, 4, 5','public',None),
 ('City of Hagerstown DW Laboratory','1 Clean Water Circle','Hagerstown','21740','WA','(301) 739-8577','G-1053','Micro 3, 4, 5','public',None),
 ('Community Environmental Laboratories, Inc','1202 Technology Drive, Suite F','Aberdeen','21001','HA','(410) 273-7600','255','Micro 4; Inorganics 1, 2; Metals 1','main','umd'),
 ('Deep Creek Lake Laboratory','762 Mayhew Inn Road','Oakland','21550','GA','(301) 387-6162','G-1035','Micro 4, 5','public',None),
 ('EMSL Analytical, Inc - Beltsville','10752 Baltimore Avenue','Beltsville','20705','PG','(301) 937-5700','305','Micro 3, 4, 5','limited',None),
 ('Fountain Valley Analytical Laboratory, Inc','1413 Old Taneytown Road','Westminster','21158','CL','(410) 848-1014','133','Micro 4, 5; Inorganics 1, 2, 3, 5','main','umd'),
 ('Frederick County Division of Water & Sewer Utilities Laboratory','7400 Marcies Choice Lane','Frederick','21704','FR','(301) 600-1597','G-1044','Micro 3, 4, 5; Metals 1, 2; Inorganics 1, 2; HAA5, THMs','public',None),
 ('Fredericktowne Labs, Inc','3020 Ventrie Court','Myersville','21773','FR','(301) 293-3340','116','Micro 3, 4, 5; Metals 1, 2; Inorganics 1, 2, 3','main','umd'),
 ('Geoscope Environmental Laboratories, Inc','1019 North Division Street','Salisbury','21801','WI','(410) 334-6496','326','Micro 3, 4','limited',None),
 ('Home Land Labs - Annapolis','108 Old Solomons Island Road, #L2','Annapolis','21401','AA','(410) 224-4304','106','Micro 3, 4, 5','limited',None),
 ('Home Land Labs - Forest Hill','2216 Commerce Road, Suite 2A','Forest Hill','21050','HA','(443) 969-1649','370','Micro 4, 5','limited',None),
 ('Home Land Labs - Towson','1220 East Joppa Road, Building C, Suite #505','Towson','21285','BC','(443) 969-1649','365','Micro 3, 4, 5; Metals 1, 2; Inorganics 1, 2, 3','main',None),
 ('Home Land Labs - Waldorf','3430 Rockefeller Court','Waldorf','20602','CH','(240) 448-5600','139','Micro 3, 4, 5; Inorganics 1, 2','main',None),
 ('Howard County Government - Little Patuxent Water Reclamation Plant','8900 Greenwood Place','Savage','20763','HO','(410) 313-1210','G-1045','Micro 4','public',None),
 ('Maryland Spectral Services, Inc','1500 Caton Center Drive, Suite G','Baltimore','21227','BA','(410) 247-7600','153','THMs; VOCs; SOC 3; HAA5; Metals 1, 2; Inorganics 1, 2, 3','limited',None),
 ('Mattawoman Water Quality Lab (Charles County Dept of Utilities)','5310 Hawthorne Road','LaPlata','20646','CH','(301) 609-5612','G-1033','Micro 3, 4; Inorganics 1, 2','public',None),
 ('Microbac Laboratories, Inc - Baltimore','2101 Van Deman Street','Baltimore','21224','BC','(410) 633-1800','109','Micro 3, 4, 5; Metals 1, 2; Inorganics 1, 2','main',None),
 ('Montebello Water Quality Laboratory','3901 Hillen Road','Baltimore','21218','BC','(410) 396-6040','G-1017','Micro 1, 3, 4, 5; Inorganics 1, 2, 3; VOCs, HAA5; THMs','public',None),
 ('NAN Technologies, Inc','1550 Caton Center Drive, Suite #K (Front)','Halethorpe','21227','BA','(410) 800-4263','360','Metals 1, 2','limited',None),
 ('Phase Separation Science, Inc','6630 Baltimore National Pike','Baltimore','21228','BA','(410) 747-8770','179','Metals 1, 2; Inorganics 1, 2, 3, 5; THMs; VOCs','limited',None),
 ("St. Mary's MetCom DW Lab - Lexington Park",'48020 Pine Hill Run Road','Lexington Park','20653','SM','(301) 737-7400','G-1055','Micro 4','public',None),
 ('Town of Ocean City Laboratory Services','6405 Seabay Drive','Ocean City','21842','WO','(410) 723-5090','G-1027','Micro 1, 4, 5; Inorganics 1','public',None),
 ('Washington County Division of Environmental Management Laboratory','16232 Elliott Parkway','Williamsport','21795','WA','(240) 313-2626','G-1025','Micro 4, 5; Metals 1; Inorganics 1, 2, 3','public',None),
 ('Washington Suburban Sanitary Commission Laboratory Division (WSSC)','12245 Tech Road','Silver Spring','20904','MO','(301) 206-7575','G-1049','Micro 3, 4, 5; Metals 1, 2; THMs; VOCs; HAA5; Inorganics 1, 2, 3; SOC 1, 3; Pesticides 1, 2; Herbicides','public','The MDE PDF\'s approved-tests text for this lab ends with "Herbicides;" and may be cut off; check the PDF.'),
 ('Water Testing Labs of MD - Annapolis','1993 Moreland Parkway, Suite 201','Annapolis','21401','AA','(410) 643-7711','134','Micro 4','limited','umd'),
 ('Water Testing Labs of MD - Salisbury','113 High Street','Salisbury','21801','WI','(410) 546-1318','104','Micro 3, 4, 5','limited','umd'),
 ('Water Testing Labs of MD - Stevensville','1000 Butterworth Court','Stevensville','21666','QA','(410) 643-7711','214','Micro 1, 3, 4, 5; Metals 1, 2; Inorganics 1, 2, 3','main','umd'),
]
# Evitts Creek Water Company is in MDE's in-state section but has a Bedford, PA address.
L.append(('Evitts Creek Water Company (City of Cumberland)','1032 Lake Gordon Road','Bedford','15522','PA','(814) 767-9552','G-1014','Micro 4','public','Listed in MDE\'s in-state section with a Pennsylvania address; it is the City of Cumberland\'s water company.'))

def expand(tests):
    out = []
    for part in re.split(r'[;,]\s*(?=[A-Z])', tests):
        part = part.strip().rstrip(';,')
        m = re.match(r'([A-Za-z]+(?: \d)?)(.*)', part)
        base = re.match(r'(Micro|Metals|Inorganics|SOC|Pesticides)\s+([\d,\s]+)$', part)
        if base:
            for n in re.findall(r'\d', base.group(2)):
                out.append(CODES[f'{base.group(1)} {n}'])
        else:
            out.append(CODES[part])
    return out

txt = open(f'{SRC_DIR}/labs.txt').read() if os.path.exists(f'{SRC_DIR}/labs.txt') else open('/workspace/src/md/labs.txt').read() if os.path.exists('/workspace/src/md/labs.txt') else None
labs = []
for name, street, city, z, cty, phone, cert, tests, grp, note in L:
    if txt:
        for needle in (phone, cert, street.split(',')[0]):
            if needle not in txt: sys.exit(f'not in source: {needle} ({name})')
    st = 'PA' if cty == 'PA' else 'MD'
    acc = expand(tests)
    notes = []
    if note:
        for n in note.split(';', 1) if note.startswith('umd') else [note]:
            if n == 'umd':
                notes.append('Also on University of Maryland Extension\'s list of certified labs that serve homeowners (UMD says that list was last updated in 2019).')
            elif n: notes.append(n)
    d = dict(name=name, address=f'{street}, {city}, {st} {z}', city=city, phone=phone, lab_id=cert, county_code=cty,
             tests_as_printed=tests, accredited_for=acc, group=grp,
             source_name='MDE Laboratory Certification Program, "Maryland\'s Certified Drinking Water Laboratories" (latest revisions 10/1/2026)',
             source_url=SRC, source_date='2026-10-01', last_verified=V)
    if any('umd' == n.split(';')[0] for n in [note or '']): d['source_url_umd'] = UMD
    if notes: d['note'] = ' '.join(notes)
    labs.append(d)

# ---- out-of-state labs (MDE "Out of State Labs" section), added 2026-11-14 ----
ALIAS = {'Metal': 'Metals', 'Inorganic': 'Inorganics', 'SOCs': 'SOC', 'Radiologics': 'Radiologicals'}
def expand2(tests):
    t = re.sub(r'\s*\(Dioxin\)', '', tests).replace(':', ';')
    out = []
    for part in re.findall(r'([A-Za-z]+[A-Za-z0-9]*)((?:\s*\d\s*,?)*)', t):
        word, nums = part
        word = ALIAS.get(word, word)
        ns = re.findall(r'\d', nums) if word in ('Micro', 'Metals', 'Inorganics', 'SOC', 'Pesticides') else []
        if ns:
            out += [CODES[f'{word} {n}'] for n in ns]
        elif word in ('HAA', 'HAA5'):
            out.append(CODES['HAA5'])
        else:
            out.append(CODES[word])
    seen = []
    for o in out:
        if o not in seen: seen.append(o)
    return seen
KEEP = {'LLC', 'ALS', 'EMSL', 'NSF', 'GEL', 'SGS', 'HP', 'KNL', 'H2O', 'II', 'SE', 'NC', 'M.', 'J.'}
FIX = {'Spl-Reading': 'SPL-Reading', 'Testamerica': 'TestAmerica', ' And ': ' and ', '(labs Inc)': '(LABS Inc)'}
def tc(n):
    out = ' '.join(w if w.strip('(),.-') in KEEP else '-'.join(x[:1].upper() + x[1:].lower() for x in w.split('-')) for w in n.split(' '))
    for a, b in FIX.items(): out = out.replace(a, b)
    return out
NEAR = ['PA', 'DE', 'VA', 'WV', 'DC']
oos = json.load(open(f'{SRC_DIR}/oos.json'))
assert len(oos) == 53, len(oos)
for r in oos:
    if txt:
        for needle in (r['phone'], r['addr_lines'][-1]):
            if needle not in txt: sys.exit(f'not in source: {needle} ({r["name"]})')
    city_line = r['addr_lines'][-1]
    m = re.match(r'(.+?),\s*([A-Za-z ]+?)\s+(\d{5})$', city_line)
    city, st_name, z = m.groups()
    st = {'Florida': 'FL'}.get(st_name, st_name)
    acc = expand2(r['tests'])
    phone = r['phone'].replace('- ', '-')
    notes = []
    if r['former']: notes.append('MDE lists it as ' + '; '.join(r['former']) + '.')
    if r['state_col'] != st: notes.append(f'MDE\'s state column says {r["state_col"]}, but the printed address is in {st}.')
    if phone != r['phone']: notes.append(f'MDE prints the phone as "{r["phone"]}".')
    if 'ENVIRONEMT' in r['name']: notes.append('Name spelled as printed by MDE ("Environemt").')
    if city in ('Greenburg', 'Kennet Square'): notes.append(f'City spelled as printed by MDE ("{city}").')
    bact = any(a.startswith(('Micro 1', 'Micro 2', 'Micro 4')) for a in acc)
    nitr = any(a.startswith('Inorganics 1') for a in acc)
    detail = ('Certified on MDE\'s list for both coliform bacteria and nitrate, two of the four yearly tests MDE recommends for private wells.' if bact and nitr
              else 'Certified on MDE\'s list for coliform bacteria but not nitrate.' if bact
              else 'Certified on MDE\'s list for nitrate but not coliform bacteria.' if nitr
              else 'Not certified on MDE\'s list for coliform bacteria or nitrate; specialty tests only.')
    d = dict(name=tc(r['name']), address=', '.join(r['addr_lines']).replace(f'{st_name} {z}', f'{st} {z}'), city=city, state=st,
             phone=phone, lab_id=r['cert'], tests_as_printed=r['tests'].rstrip(';'), accredited_for=acc, group='outofstate',
             basic_well_test=bact and nitr, detail=detail,
             source_name='MDE Laboratory Certification Program, "Maryland\'s Certified Drinking Water Laboratories", Out of State Labs section (latest revisions 10/1/2026)',
             source_url=SRC, source_date='2026-10-01', last_verified=V)
    if notes: d['note'] = ' '.join(notes)
    labs.append(d)
GO = {'main': 0, 'public': 1, 'limited': 2, 'outofstate': 3}
labs.sort(key=lambda r: (GO[r['group']], (0 if r.get('basic_well_test') else 1, 0 if r.get('state') in NEAR else 1, r.get('state', '')) if r['group'] == 'outofstate' else (), r['city'].lower(), r['name'].lower()))
json.dump(dict(state='Maryland', slug='maryland', abbr='MD',
  list_source=dict(name="MDE Laboratory Certification Program — Maryland's Certified Drinking Water Laboratories", page_url=SRC,
    program_url='https://mde.maryland.gov/programs/water/water_supply/pages/wsp-labcert.aspx', parameter_list_url=PARAMS,
    report_date='October 1, 2026 ("Latest Revisions: 10/1/2026")'),
  last_verified=V, labs=labs), open('src/_data/labs/maryland.json', 'w'), indent=1)
print('MD', len(labs), {g: sum(1 for x in labs if x['group'] == g) for g in GO}, 'oos basic:', sum(1 for x in labs if x.get('basic_well_test')))
