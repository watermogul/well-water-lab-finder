"""Parses the "Out of State Labs" section of MDE's Maryland-Certified-DW-Labs.pdf (pdftotext -layout output)
into $SRC_DIR/oos.json. Source text: $SRC_DIR/labs.txt (default /workspace/src-md). Column split is by
character position (name/address < col 45, head/phone 45-100, tests > 100); each record keeps its raw lines."""
import re, json, os
SRC = os.environ.get('SRC_DIR', '/workspace/src-md')
lines = open(f'{SRC}/labs.txt').read().split('\n')
start = next(i for i, l in enumerate(lines) if 'Out of State Labs' in l)
SKIP = re.compile(r"Latest Revisions|Maryland's Certified|by MDE-LCP|Approved Tests|Head of Laboratory|Name and Address|Telephone Number|accessable|Certification\s*$|Out of State Labs")
blocks, cur = [], []
for l in lines[start + 1:]:
    if not l.strip() or SKIP.search(l) or '\f' in l:
        if cur: blocks.append(cur); cur = []
        continue
    cur.append(l)
if cur: blocks.append(cur)
# second printed line is part of the lab name for these certification numbers
NAME_CONT = {'184', '100', '300'}
out = []
for b in blocks:
    left, mid, right, st, cert = [], [], [], None, None
    for l in b:
        for m in re.finditer(r'\S+(?: \S+)*', l):
            s, pos = m.group(), m.start()
            if pos < 45: left.append(s)
            elif pos < 100: mid.append(s)
            else:
                mm = re.match(r'([A-Z]{2})\s+(\d{3})\s*(.*)$', s)
                if mm and cert is None: st, cert, s = mm.groups()
                if s: right.append(s)
        # state + cert may share one segment with the head's name column
    if cert is None:
        for l in b:
            mm = re.search(r'\s{2,}([A-Z]{2})\s{2,}(\d{3})(?:\s{2,}|$)', l)
            if mm: st, cert = mm.groups(); break
    # rebuild the mid column without the state/cert fields
    mid2 = []
    for s in mid:
        mm = re.match(r'(.*?)\s+([A-Z]{2})\s+(\d{3})\s*(.*)$', s)
        if mm and mm.group(3) == cert: s = mm.group(1); right.insert(0, mm.group(4)) if mm.group(4) else None
        mid2.append(s)
    name = left[0]
    rest = left[1:]
    if cert in NAME_CONT: name = f'{name} {rest.pop(0)}'
    former = [x for x in rest if x.lower().startswith('(formerly')]
    rest = [x for x in rest if x not in former]
    fm = re.search(r'\s*\((formerly [^)]*)\)', name)
    if fm: former.append('(' + fm.group(1) + ')'); name = name[:fm.start()].strip()
    phone = next((x for x in mid2 if re.match(r'\(\d{3}\)', x)), None)
    out.append(dict(name=name, former=[f.strip('()') for f in former], addr_lines=rest, state_col=st, cert=cert,
                    phone=phone, tests=re.sub(rf'^(?:{st}\s+)?{cert}\s*', '', ' '.join(x for x in right if x).strip()), raw=b))
json.dump(out, open(f'{SRC}/oos.json', 'w'), indent=1)
print('out-of-state records:', len(out), 'missing cert:', [r['name'] for r in out if not r['cert']])
