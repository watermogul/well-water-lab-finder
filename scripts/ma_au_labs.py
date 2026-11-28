"""Cross-check for /guides/massachusetts-arsenic-uranium-bedrock-wells/.
Joins MassDEP LabCert (Matrix = Potable) results for ARSENIC, URANIUM, GROSS ALPHA, RADIUM-226, RADIUM-228
(harvested with a copy of scripts/ma_labcert_harvest.py restricted to those analytes; JSON in $SRC_DIR,
default /workspace/src-ma-as/labcert_au_2026-11-27.json) with the labs that say "Yes" to residential customers
on MassDEP's private-well spreadsheet (as stored in src/_data/labs/massachusetts.json).
Prints the markdown table used on the guide. Asserts the 2026-11-27 counts so a change fails loudly."""
import json, os, re
SRC = os.environ.get('SRC_DIR', '/workspace/src-ma-as')
lc = json.load(open(os.path.join(SRC, 'labcert_au_2026-11-27.json')))
ma = json.load(open('src/_data/labs/massachusetts.json'))
counts = {a: len(v) for a, v in lc.items()}
assert counts == {'ARSENIC': 24, 'URANIUM': 13, 'GROSS ALPHA': 6, 'RADIUM-226': 5, 'RADIUM-228': 6}, counts
cols = [('ARSENIC', 'Arsenic'), ('URANIUM', 'Uranium'), ('GROSS ALPHA', 'Gross alpha'), ('RADIUM-226', 'Radium-226'), ('RADIUM-228', 'Radium-228')]
rows = []
for l in ma['labs']:
    if 'residential customers: Yes' not in l['detail']:
        continue
    ids = re.findall(r'lab (M-[A-Z0-9]+)', l['detail'])
    have = [k for k, _ in cols if any(r[0] in ids for r in lc[k])]
    if not have:
        continue
    st = l['address'].rsplit(',', 1)[-1].split()[0]
    rows.append((st != 'MA', l['name'], f"{l['city']}, {st}", l.get('phone') or '', ids[0], have))
rows.sort()
assert len(rows) == 10, len(rows)
print('| Lab (MassDEP spreadsheet name) | Location | Phone | LabCert ID | ' + ' | '.join(c for _, c in cols) + ' |')
print('|---|---|---|---|' + '---|' * len(cols))
for _, n, loc, ph, i, have in rows:
    print(f'| {n} | {loc} | {ph} | {i} | ' + ' | '.join('Yes' if k in have else '-' for k, _ in cols) + ' |')
