"""Builds src/_data/labs/ohio.json from Ohio EPA's Combined-Lab-List.pdf (November 2026 edition, file created 2026-10-30,
md5 ab2501bd707e83d86ac0071798af02a8). Steps: curl the PDF, pdftotext -layout, python3 scripts/parse_oh.py <txt> <json>, then this.
Set OH_JSON to the parsed file. Every row on the list is published (75 rows); grouping is ours."""
import json,os,re
SRC=os.environ.get('OH_JSON','/workspace/src/oh2611/oh_nov2026.json')
V='2026-11-11'
OH_SRC='https://dam.assets.ohio.gov/image/upload/epa.ohio.gov/Portals/28/documents/labcert/Combined-Lab-List.pdf'
PROG='https://epa.ohio.gov/divisions-and-offices/drinking-and-ground-waters/ddgw-programs/laboratory-certification'
SN="Ohio EPA, Laboratories Certified/Accepted to Perform Analyses on Public Drinking Water (November 2026)"
# Plain-English hints are copied from the category key on page 1 of the same PDF (abridged).
HINT={'Standard Chemistry':'Standard Chemistry (Ohio EPA key includes nitrate, nitrite, fluoride, chloride, sulfate, hardness, pH, TDS)',
 'Volatile Organic Compounds':'Volatile organic compounds (regulated VOCs, vinyl chloride, TTHM, HAAs)',
 'Pesticide - SOC':'Pesticides / SOCs (key includes atrazine, glyphosate, 2,4-D, EDB, 1,2,3-TCP, PCBs)',
 'Radiochemistry':'Radiochemistry (key includes gross alpha, gross beta, radium-226/228, uranium)',
 'Limited Chemistry':'Limited Chemistry (as printed; not defined in the key)',
 'Nitrate':'Nitrate only','Nitrate, Nitrite':'Nitrate and nitrite only','2,3,7,8-TCDD (Dioxin)':'Dioxin (2,3,7,8-TCDD) only'}
HINT['Trace Metals']='Trace Metals (key includes arsenic, lead, copper, iron, manganese, sodium, barium, mercury)'
OTH={'PFAS':'PFAS (regulated compounds)','Asbestos':'Asbestos','Cryptosporidium':'Cryptosporidium'}
PUB=re.compile(r'WTP|Water Plant|Water Department|Water Laboratory|Water Company|Water Resources|Water Works|Sanitary|NEORSD|Health|Department of|Water Compliance|Water Quality|Aqua Pennsylvania')
raw=json.load(open(SRC))
assert len(raw)==75, len(raw)
out=[]
for r in raw:
    addr=r['address']; m=re.search(r',\s*([^,]+),\s*([A-Z]{2}) \d{5}',addr)
    city,st=m.group(1),m.group(2)
    acc=[]
    if r['micro']: acc.append('Bacteria: total coliform / E. coli ('+', '.join(r['micro'])+')')
    acc+= [HINT[c] for c in r['chem']]
    acc+= [OTH[c] for c in r['other']]
    if r['habs']: acc.append('Algal toxins / cyanobacteria ('+', '.join(r['habs'])+'; for surface water)')
    pub=bool(PUB.search(r['name'])) and 'Kleinfelder' not in r['name']
    core=bool(r['micro'] or r['chem'])
    if st!='OH' or not core: g='limited'
    elif pub: g='public'
    else: g='main'
    printed='; '.join(f'{k}: {", ".join(r[c])}' for k,c in (('HABs','habs'),('Microbiological','micro'),('Chemistry','chem'),('Other','other')) if r[c])
    d=dict(name=r['name'],address=addr,city=city,phone=r['phone'],accredited_for=acc,group=g,
        detail='Columns as printed on the Ohio EPA list: '+printed+'.',
        habs=r['habs'],micro=r['micro'],chemistry=r['chem'],other=r['other'],
        source_name=SN,source_url=OH_SRC,source_date='2026-11 (file created 2026-10-30)',last_verified=V)
    if not r['phone']: d['note']='No phone number is printed on the Ohio EPA list for this lab.'
    if st!='OH': d['note']=(d.get('note','')+' Out-of-state lab accepted by Ohio EPA. Ask about shipping and hold times before you collect.').strip()
    out.append(d)
out.sort(key=lambda r:({'main':0,'public':1,'limited':2}[r['group']],r['city'].lower(),r['name'].lower()))
json.dump(dict(state='Ohio',slug='ohio',abbr='OH',
  list_source=dict(name='Ohio EPA Division of Drinking and Ground Waters — Laboratories Certified/Accepted to Perform Analyses on Public Drinking Water',
    page_url=OH_SRC,program_url=PROG,report_date='November 2026 (PDF created 2026-10-30)'),
  last_verified=V,labs=out),open('src/_data/labs/ohio.json','w'),indent=1,ensure_ascii=False)
print('OH',len(out),{g:sum(1 for x in out if x['group']==g) for g in('main','public','limited')})
for g in ('main','public','limited'):
    print('==',g); [print('  ',x['name'],'|',x['city']) for x in out if x['group']==g]
