"""Assembles src/_data/labs/{pennsylvania,ohio,new-hampshire,new-york}.json.
PA: /tmp/pa_labs.json from scripts/build_pa.py. OH: parsed from Ohio EPA list text (oh_all.json, cleaned below).
NH and NY: hand-entered from the primary sources named in each file. Every listing carries source_url + last_verified."""
import json,re
V='2026-10-26'
V_PA='2026-10-30'  # PA re-verified 2026-10-30: DEP page still links the same two June 2024 reports; re-downloaded PDFs are byte-identical (md5) to the 2026-10-26 copies; Penn State AASL page re-checked
def fmt_phone(p):
    d=re.sub(r'\D','',p)
    return f'({d[:3]}) {d[3:6]}-{d[6:10]}' if len(d)>=10 else p
PUB=re.compile(r'(?<!Presque Isle )\b(Water (Authority|Works|Treatment|Plant|Department|Quality|Company|Resources)|Water Pollution|WTP|Filter Plant|Treatment (Plant|Facility)|Municipal|Borough|Sanitary|Health|PAW|Pennsylvania American|PA American|Aqua Pennsylvania|Capital Region Water|DEP|Bureau|Wastewater|Water Lab|MAWC|Pittsburgh Water|Chester Water|Erie Water|Laurel Creek|Hulton|LBCJMA|Sanitary Engineering|Sebring|Water Plant)',re.I)
CORE={'Total coliform / E. coli':'bacteria','Nitrate':'nitrate','pH':'ph','Total dissolved solids':'tds','Lead':'lead','Arsenic':'arsenic','Radon':'radon','Uranium':'radon'}
# ---------- PA
PA_SRC=['https://files.dep.state.pa.us/Water/BSDW/DrinkingWaterManagement/PrivateWaterWells/DW_Lab_Certification_06-11-2024%20Lab%20Accreditation%20Report.pdf',
        'https://files.dep.state.pa.us/Water/BSDW/DrinkingWaterManagement/PrivateWaterWells/DW_Micro_Lab_Certification_06-13-2024%20Accreditation%20Report.pdf']
pa=json.load(open('/tmp/pa_labs.json'))
out=[]
for l in pa:
    cats={CORE[c] for c in l['accredited_for'] if c in CORE}
    if PUB.search(l['name']) and 'Water Testing' not in l['name'] and 'Water Controls' not in l['name']: g='public'
    elif len(cats)>=2: g='main'
    else: g='limited'
    # Penn State AASL: the only lab on this page whose fees I verified
    l2=dict(name=l['name'],address=f"{l['address']}, {l['city']}, PA {l['zip']}",city=l['city'],phone=fmt_phone(l['phone']),
        lab_id=l['dep_lab_id'],accredited_for=l['accredited_for'],group=g,
        source_name='PA DEP drinking water lab accreditation reports (chemistry dated 2024-06-11; microbiology dated 2024-06-13)',
        source_url=PA_SRC[0] if l['in_chem_report'] else PA_SRC[1],
        source_url_2=PA_SRC[1] if (l['in_chem_report'] and l['in_micro_report']) else None,
        source_date='2024-06-11 / 2024-06-13',last_verified=V_PA)
    if l['dep_lab_id']=='14-00588':
        l2['name']='Penn State Agricultural Analytical Services Laboratory'
        l2['address']='720 Tower Rd, University Park, PA 16802'
        l2['website']='https://agsci.psu.edu/aasl/water-testing/drinking-water-testing'
        l2['note']='Mail-in kit (cooler, bottles, form) from many county extension offices; overnight shipping; bacteria sample must arrive within 30 hours and cannot be accepted on a Friday; results typically 10–14 business days. Fee table on the lab page (retrieved 2026-10-26, re-checked 2026-10-30). The PA DEP report lists this lab at a different address string; the street address shown here is from the lab\'s own page.'
        l2['group']='main'
    if l['dep_lab_id'] in ('39-04427','33-00325'): l2['group']='limited'   # bottler / coal-analysis lab: not a typical homeowner lab
    if l['dep_lab_id']=='08-05636':
        l2['name']='LEAP Testing Service'; l2['address']='One Guthrie Square, Sayre, PA'
    out.append(l2)
out.sort(key=lambda r:({'main':0,'public':1,'limited':2}[r['group']],r['city'].lower(),r['name'].lower()))
json.dump(dict(state='Pennsylvania',slug='pennsylvania',abbr='PA',
  list_source=dict(name='Pennsylvania DEP — Laboratory Accreditation, drinking water reports',page_url='https://www.pa.gov/agencies/dep/residents/my-water/private-wells/water-testing',
     report_urls=PA_SRC,report_date='June 2024 (reports dated 2024-06-11 and 2024-06-13)'),
  last_verified=V_PA,labs=out),open('src/_data/labs/pennsylvania.json','w'),indent=1)
print('PA',len(out),{g:sum(1 for x in out if x['group']==g) for g in('main','public','limited')})
# ---------- OH
OH_SRC='https://dam.assets.ohio.gov/image/upload/epa.ohio.gov/Portals/28/documents/labcert/Combined-Lab-List.pdf'
raw=json.load(open('/workspace/src/oh_all.json'))
oh=[]
for r in raw:
    addr=re.sub(r'\s+qPCR\s*$','',r['address']).strip()
    name=r['name'];
    if name.startswith('Eurofins Environment Testing North Central'):
        name='Eurofins Environment Testing North Central (formerly Metiri Analytical Group, Inc.)'
        addr='4450 Johnston Parkway, Suite B, Cleveland, OH 44128'
    if name.startswith('Kleinfelder'):
        name='Kleinfelder Water Technologies Laboratory (formerly Industrial Fluid Management, Inc.)'
        addr='2926 U.S. Highway 6, McClure, OH 43534'
    if not re.search(r', OH \d{5}',addr) or not (r['micro'] or r['chem']): continue
    if 'Metiri' in name and '|' in name: continue
    m=re.search(r',\s*([^,]+),\s*OH',addr); city=m.group(1) if m else ''
    chem=r['chem'];micro=r['micro']
    acc=[]
    if micro: acc.append('Total coliform / E. coli ('+', '.join(micro)+')')
    if chem: acc.append('Chemistry: '+', '.join(chem))
    pub=bool(re.search(r'WTP|Water Plant|Water Department|Water Laboratory|Water Company|Water Resources|Sanitary|NEORSD|Health|Department of|Water Compliance|Water Quality|Water Technologies' ,name)) and 'Kleinfelder' not in name
    oh.append(dict(name=name,address=addr,city=city,phone=r['phone'],micro=micro,chemistry=chem,accredited_for=acc,
        group='public' if pub else 'main',source_name='Ohio EPA, Laboratories Certified/Accepted to Perform Analyses on Public Drinking Water (dated October 2026)',
        source_url=OH_SRC,source_date='2026-10',last_verified=V))
oh.sort(key=lambda r:({'main':0,'public':1}[r['group']],r['city'].lower(),r['name'].lower()))
json.dump(dict(state='Ohio',slug='ohio',abbr='OH',list_source=dict(name='Ohio EPA Division of Drinking and Ground Waters — Combined Lab List (public drinking water)',page_url=OH_SRC,report_date='October 2026'),last_verified=V,labs=oh),open('src/_data/labs/ohio.json','w'),indent=1)
print('OH',len(oh),sum(1 for x in oh if x['group']=='public'))
# ---------- NH
NH_SRC='https://www.des.nh.gov/sites/g/files/ehbemt341/files/documents/labs-private-wells.pdf'
def nh(name,addr,city,phone,drop,web,extra=None):
    d=dict(name=name,address=addr,city=city,phone=phone,drop_off=drop,website=web,group='main',
       accredited_for=['NHELAP-accredited; NHDES lists it as serving NH private-well users (specific analytes: use the NHDES search linked above)'],
       source_name='NHDES, Water Testing Guidance for Private Well Users (April 2026; lab list updated 2024-09-20)',source_url=NH_SRC,source_date='2024-09-20 (lab list)',last_verified=V)
    if extra: d.update(extra)
    return d
nhl=[
 nh('Endyne Inc.','56 Etna Rd, Suite F, Lebanon, NH','Lebanon','(603) 678-4891','Lebanon NH; Brattleboro VT; St. Johnsbury VT','https://endynelabs.com'),
 nh('Eurofins Environmental Testing Eastern Analytical','51 Antrim Avenue, Concord, NH','Concord','(603) 228-0525','Concord','https://easternanalytical.com',{'note':'The state PDF\'s table text is garbled around this row; the name shown is our best reading of "Environmental Testing Eastern Analytical / Eurofins". Confirm on the lab website.'}),
 nh('Eurofins Portsmouth','124 Heritage Ave., Portsmouth, NH','Portsmouth','(603) 436-2001','Portsmouth','https://eurofins.com'),
 nh('Granite State Analytical','22 Manchester Road, Derry, NH','Derry','(603) 432-3044','10 NH locations including North Conway, Amherst, Tilton, Hampstead','https://granitestateanalytical.com'),
 nh('Nelson Analytical LLC (Manchester)','490 E. Industrial Park Dr., Manchester, NH','Manchester','(603) 622-0200','Manchester; Canterbury','https://nelsonanalytical.com'),
 nh('Nelson Analytical (Keene)','103 Monadnock Highway, North Swanzey, NH','North Swanzey','(603) 357-2577','Swanzey','https://nelsonanalytical.com'),
 nh('New England Radon Ltd.','11A Industrial Way, Unit 3, Salem, NH','Salem','(603) 893-4260','Salem','https://newenglandradon.com'),
 nh('NHDHHS Public Health Laboratories (Water Analysis Laboratory)','29 Hazen Drive, Concord, NH 03301','Concord','(603) 271-3445','Concord','https://www.dhhs.nh.gov/programs-services/environmental-health-and-you/water-analysis-laboratory-program',
    {'note':'State lab; offers homeowner well-water testing on a fee-for-service basis. Fee table: see the cost guide. Fee form: https://nhphl.qualtraxcloud.com/ShowDocument.aspx?ID=7907 (retrieved 2026-10-26; the form itself prints no date).',
     'fee_source_url':'https://nhphl.qualtraxcloud.com/ShowDocument.aspx?ID=7907'}),
 nh('Seacoast Analytical Services LLC','72 Pinkham Road, Lee, NH','Lee','(603) 868-1457','Lee; Epping','https://seacoastanalytical.com'),
]
nhl.sort(key=lambda r:r['city'])
json.dump(dict(state='New Hampshire',slug='new-hampshire',abbr='NH',list_source=dict(name='NHDES private-well testing guidance',page_url=NH_SRC,report_date='April 2026 document; lab list "updated 9/20/2024"',
  search_url='https://www4.des.state.nh.us/certifiedlabs/certified-method.aspx'),last_verified=V,labs=nhl),open('src/_data/labs/new-hampshire.json','w'),indent=1)
# ---------- NY (Westchester County registered labs only)
WC='https://health.westchestercountyny.gov/images/stories/PDF/List_of_Labs_for_Private_Well_2025.pdf'
def ny(name,addr,city,st,phone,elap,web=None):
    d=dict(name=name,address=addr,city=city,phone=phone,elap_id=elap,group='main',accredited_for=['NYS ELAP-certified; registered with Westchester County Dept. of Health for private-well testing results'],
      source_name='Westchester County Dept. of Health, "Private Well-Water Testing Law" lab list (file named 2025; the PDF prints no date)',source_url=WC,source_date='2025 (per file name)',last_verified=V)
    if web: d['website']=web
    return d
nyl=[
 ny('Advanced Analytical Technologies, Inc.','37 Ramland Rd, Orangeburg, NY 10962','Orangeburg','NY','(800) 259-9532','11713'),
 ny('Analytical Laboratory Service (ALS)','34 Dogwood Lane, Middletown, PA 17057','Middletown, PA','PA','(800) 794-7709','11759'),
 ny('York Analytical Lab, dba Aqua Environmental Lab','56 Church Hill Rd, Newtown, CT 06470','Newtown, CT','CT','(203) 270-9973','11706'),
 ny('Carnell Environmental Inspections, Inc.','26 Legion Dr, Valhalla, NY 10595','Valhalla','NY','(914) 946-4300','11588'),
 ny('Environmental Labworks, Inc.','PO Box 733, Marlboro, NY 12542','Marlboro','NY','(845) 236-7823','10824'),
 ny('EnviroTest Laboratories, Inc.','315 Fullerton Ave, Newburgh, NY 12250','Newburgh','NY','(845) 562-0890','10142'),
 ny('Phoenix Environmental Laboratories, Inc.','587 East Middle Turnpike, Manchester, CT 06040','Manchester, CT','CT','(860) 645-1102 or (860) 645-3513','11715','https://www.phoenixlabs.com'),
 ny('Yorktown Medical Laboratories, Inc.','321 Kear Street, Yorktown Heights, NY 10598','Yorktown Heights','NY','(914) 245-3203','10323'),
 ny('Westchester County Laboratories and Research','10 Dana Road, Valhalla, NY 10595','Valhalla','NY','(914) 231-1781','10108','http://labs.westchestergov.com/'),
 ny('Aquatek Labs','3 Research Drive, Woodbridge, CT 06525','Woodbridge, CT','CT','(203) 623-9804','12170'),
]
json.dump(dict(state='New York',slug='new-york',abbr='NY',list_source=dict(name='Westchester County Dept. of Health lab list; NYS ELAP search',page_url=WC,report_date='2025 (file name; no printed date)',
  search_url='https://healthapps.health.ny.gov/pubdoh/applinks/wc/elappublicweb/'),last_verified=V,labs=nyl),open('src/_data/labs/new-york.json','w'),indent=1)
print('done')
