"""Extract the table rows from IDEM/IDOH 'Indiana Certified Drinking Water Laboratories' PDF (Revised 11/7/2025).
Needs pdfplumber (e.g. python3 -m venv /tmp/venv && /tmp/venv/bin/pip install pdfplumber).
Usage: /tmp/venv/bin/python scripts/extract_in_tables.py  ->  $SRC_DIR/in_tables.json"""
import json, os, pdfplumber
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-in')
rows = []
with pdfplumber.open(os.path.join(SRC_DIR, 'dw_cert_lab_in-state.pdf')) as pdf:
    for i, p in enumerate(pdf.pages):
        for t in p.extract_tables():
            for r in t:
                rows.append({'page': i + 1, 'cells': [(c or '').replace('\n', ' ').strip() for c in r]})
json.dump(rows, open(os.path.join(SRC_DIR, 'in_tables.json'), 'w'), indent=1)
print(len(rows), 'rows')
