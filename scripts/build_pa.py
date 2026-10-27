"""Builds src/_data/labs/pennsylvania.json from two PA DEP accreditation reports (PDF -> text via pdftotext -layout).
Inputs (downloaded 2026-10-26 from the URLs in SRC_*): /workspace/src/pa_chem.txt, pa_micro.txt
Only labs with a Pennsylvania street address are listed; analyte flags come straight from the report rows."""
import re,json
def parse(fn):
    labs={};cur=None
    for ln in open(fn).read().split('\n'):
        s=ln.strip()
        if re.fullmatch(r'\d\d-\d{5}',s):
            cur={'id':s,'hdr':[],'an':set(),'done':False};labs[s]=cur;continue
        if cur is None or not s or s.startswith(('SSRS_LABS','Accredited Labs Report','TYPE')) or re.match(r'^\d+/\d+/\d{4} \d',s): continue
        if not cur['done']:
            cur['hdr'].append(s)
            if re.match(r'^\(?\d{3}\)?[\s-]\d{3}-\d{4}$',s): cur['done']=True
            continue
        parts=re.split(r'\s{2,}',s)
        di=[i for i,p in enumerate(parts) if re.fullmatch(r'\d\d/\d\d/\d{4}',p)]
        if di and len(parts)>di[0]+3:
            assert parts[di[0]+1]=='Drinking Water',parts
            cur['an'].add(parts[di[0]+2])
    return labs
chem=parse('/workspace/src/pa_chem.txt');mic=parse('/workspace/src/pa_micro.txt')
ids=set(chem)|set(mic)
def hdr_info(l):
    h=l['hdr']
    phone=h[-1];h=h[:-1]
    city=h[-1];h=h[:-1]
    # name = first line; extra lines before the first digit-leading line are name continuation
    name=h[0];i=1
    while i<len(h) and not re.match(r'^(\d|P\.?O\.? Box|Route)',h[i],re.I) and not (i==len(h)-1 and False):
        name+=' '+h[i];i+=1
    addr=', '.join(h[i:])
    return name,addr,city,phone
CAP=[('Total coliform / E. coli',r'coliform|E\. coli'),
     ('Nitrate',r'^(Nitrate|Total nitrate-nitrite)'),
     ('pH',r'^pH$'),
     ('Total dissolved solids',r'\(TDS\)'),
     ('Lead',r'^Lead$'),('Arsenic',r'^Arsenic$'),('Radon',r'^Radon-222'),('Uranium',r'^Uranium'),
     ('Iron',r'^Iron$'),('Manganese',r'^Manganese$'),('Chloride',r'^Chloride$'),('Hardness',r'hardness')]
out=[]
for i in sorted(ids):
    an=set()
    for d in (chem,mic):
        if i in d: an|=d[i]['an']
    src=chem.get(i) or mic.get(i)
    name,addr,city,phone=hdr_info(src)
    m=re.match(r'^(.*), ([A-Z]{2}) (\d{5}(?:-\d{4})?)$',city)
    if not m or m.group(2)!='PA': continue
    caps=[c for c,rx in CAP if any(re.search(rx,a,re.I) for a in an)]
    core=[c for c in caps if c in('Total coliform / E. coli','Nitrate','pH','Total dissolved solids')]
    if not core and not any(c in caps for c in('Lead','Arsenic','Radon')): continue
    out.append({'name':name,'address':addr,'city':m.group(1),'state':'PA','zip':m.group(3),'phone':phone,'dep_lab_id':i,
        'accredited_for':caps,'in_chem_report':i in chem,'in_micro_report':i in mic})
out.sort(key=lambda r:(r['city'].lower(),r['name'].lower()))
print(len(out))
json.dump(out,open('/tmp/pa_labs.json','w'),indent=1)
