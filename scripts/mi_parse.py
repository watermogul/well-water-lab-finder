import re
def parse(path):
    t=open(path).read().replace('\f','\n')
    parts=re.split(r'\n(?=\d{4} [^\n]*:\s*\n)',t)
    out={}
    for p in parts[1:]:
        L=p.split('\n')
        m=re.match(r'(\d{4}) (.*):\s*$',L[0])
        lid,name=m.groups()
        i=next(k for k,l in enumerate(L) if 'Certified Analytes' in l)
        body=L[1:i]
        an=[]
        for l in L[i+1:]:
            if 'Michigan.gov/EGLELab' in l: break
            if not l.strip(): continue
            for c in re.split(r'\s{2,}',l.strip()): an.append(c.lstrip('_').strip())
        out[lid]=dict(name=name,head=[b.strip() for b in body if b.strip()],analytes=an)
    return out
if __name__=='__main__':
    a=parse('mi_micro.txt'); b=parse('mi_chem.txt')
    print(len(a),len(b),len(set(a)&set(b)))
    for k in list(a)[:12]: print(k,a[k]['name'],a[k]['head'],len(a[k]['analytes']), len(b[k]['analytes']) if k in b else None)
    ex=[k for k in b if k in a and set(b[k]['analytes'])!=set(a[k]['analytes'])]
    print('differ',len(ex), ex[:5])
