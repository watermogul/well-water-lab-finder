"""Parse Ohio EPA Combined-Lab-List.pdf text (pdftotext -layout) into /workspace/src/oh2611/oh_nov2026.json.
Columns are assigned by token content (the vocabulary below is the PDF's own column vocabulary); any unknown token aborts."""
import json,re,sys
SRC=sys.argv[1] if len(sys.argv)>1 else '/workspace/src/oh2611/new.txt'
OUT=sys.argv[2] if len(sys.argv)>2 else '/workspace/src/oh2611/oh_nov2026.json'
VOC={'ELISA':'habs','qPCR':'habs','MMO-MUG':'micro','Quanti-Tray':'micro','Membrane Filtration':'micro',
 'Standard Chemistry':'chem','Trace Metals':'chem','Volatile Organic Compounds':'chem','Pesticide - SOC':'chem','Pesticide – SOC':'chem',
 'Radiochemistry':'chem','Limited Chemistry':'chem','Nitrate':'chem','Nitrate, Nitrite':'chem','2,3,7,8-TCDD (Dioxin)':'chem',
 'PFAS':'other','Asbestos':'other','Cryptosporidium':'other'}
lines=open(SRC).read().split('\n')
start=next(i for i,l in enumerate(lines) if re.match(r'\s+Laboratory\s+HABs',l))
blocks=[];cur=[]
for l in lines[start:]:
    if re.search(r'Page \d+ of \d+|Laboratories Certified/Accepted|^\s+Laboratory\s+HABs',l) or not l.strip():
        if cur and not l.strip(): blocks.append(cur);cur=[]
        continue
    cur.append(l)
if cur: blocks.append(cur)
labs=[]
for b in blocks:
    text=[];cols=dict(habs=[],micro=[],chem=[],other=[])
    for l in b:
        for m in re.finditer(r'\S+(?: \S+)*',l):
            t=m.group(0)
            if m.start()<10: text.append(t)
            elif t in VOC: cols[VOC[t]].append(t.replace('–','-'))
            else: raise SystemExit(f'unknown token {t!r} in {b}')
    name=text[0];rest=text[1:]
    phone=rest.pop() if rest and re.match(r'\(\d{3}\)',rest[-1]) else ''
    former=[x for x in rest if x.startswith('(formerly')]
    rest=[x for x in rest if not x.startswith('(formerly')]
    if former: name+=' '+former[0]
    addr=', '.join(rest)
    labs.append(dict(name=name,address=addr,phone=phone,**cols))
json.dump(labs,open(OUT,'w'),indent=1,ensure_ascii=False)
print(len(labs))
