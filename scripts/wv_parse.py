import re, json
import os
SRC_DIR=os.environ.get('SRC_DIR','/workspace/src2')
t=open(os.path.join(SRC_DIR,'wv.txt')).read()
pages=t.split('\f')
labs={}
for p in pages:
    m=re.search(r'^(\S.*?)\s{3,}Certificate:\s+(\S+(?: \S)?)\s*$',p,re.M)
    if not m: continue
    key=m.group(2).replace(' ','')
    d=labs.setdefault(key,dict(name=m.group(1).strip(),pages=[]))
    d['pages'].append(p)
out={}
for k,d in labs.items():
    lines=d['pages'][0].split('\n')
    i=[j for j,l in enumerate(lines) if 'Certificate:' in l][0]
    iss=exp=None
    for l in lines[i:i+5]:
        mm=re.search(r'Issue Date:\s+(\S+)',l)
        if mm: iss=mm.group(1)
        mm=re.search(r'Expiration Date:\s+(\S+)',l)
        if mm: exp=mm.group(1)
    a=[re.sub(r'\s{3,}.*','',l).strip() for l in lines[i+1:i+4] if l.strip()]
    cur=None; params=[]
    for p in d['pages']:
        for l in p.split('\n'):
            m2=re.match(r'^(\S.*?)\s{2,}Method\s+Status',l)
            if m2: cur=m2.group(1).strip(); continue
            if cur and re.match(r'^\s{2,}\S',l) and re.search(r'\s{2,}(Certified|Provisional|Not Certified|Suspended)\b',l):
                an=re.split(r'\s{2,}',l.strip())[0]
                st=re.search(r'\s{2,}(Certified|Provisional|Not Certified|Suspended)\b',l).group(1)
                params.append((cur,an,st))
    out[k]=dict(name=d['name'],addr=a[:3],issue=iss,exp=exp,params=params)

