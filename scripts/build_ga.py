"""Georgia: EPD "Commercial Laboratories Certified by Georgia for Microbiological Monitoring" (January 9, 2025), fetched 2026-11-05.
Expands the thin /labs/georgia/ state-guide into a full listing. Contact-person names from the PDF are not published.
SRC_DIR should contain ga_micro_2025.txt (pdftotext -layout of the official PDF)."""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import write_state, clean_phone, COMMON_CAVEAT_PRICES, looks_public

SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src-ga')
URL = 'https://epd.georgia.gov/document/pdf/laboratoriescertifiedbygeorgiamicrobiologicalmonitoring2025/download'
PROGRAM = 'https://epd.georgia.gov/watershed-protection-branch/drinking-water'
SN = 'Georgia EPD, "Commercial Laboratories Certified by Georgia for Microbiological Monitoring" (January 9, 2025)'
V = '2026-11-05'
SOURCE_DATE = '2025-01-09'

txt = open(os.path.join(SRC_DIR, 'ga_micro_2025.txt')).read().replace('\f', '')
# Drop repeating page headers
lines = []
for ln in txt.split('\n'):
    if re.search(r'Commercial Laboratories Certified by Georgia|Microbiological Monitoring|January 9, 2025', ln):
        continue
    lines.append(ln)

# Split into blocks starting at a lab-name line (non-indented content that is not Contact:/phone/city line)
raw = '\n'.join(lines)
# Names either end with (GA Lab #...) or (EPA Certified), or are the known UGA line without an ID.
name_re = re.compile(
    r'^(?P<name>.+?)\s*\((?P<id>GA Lab #[A-Za-z0-9]+|EPA Certified)\)\s*$|^(?P<uga>UGA Feed and Environmental Water)\s*$',
    re.M,
)

matches = list(name_re.finditer(raw))
assert len(matches) == 16, 'expected 16 labs, got %d' % len(matches)

blocks = []
for i, m in enumerate(matches):
    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
    body = raw[start:end].strip()
    name = (m.group('name') or m.group('uga')).strip()
    lab_id = m.group('id')
    if lab_id == 'EPA Certified':
        lab_id_out = None
        detail_id = 'Listed as EPA Certified (no GA Lab # printed).'
    elif lab_id:
        lab_id_out = lab_id.replace('GA Lab #', '')
        detail_id = 'Georgia lab ID %s (as printed).' % lab_id_out
    else:
        lab_id_out = None
        detail_id = 'No Georgia lab ID printed on the January 9, 2025 list.'
    blocks.append(dict(name=name, lab_id=lab_id_out, detail_id=detail_id, body=body))

out = []
for b in blocks:
    blines = [ln.strip() for ln in b['body'].split('\n') if ln.strip()]
    # Drop Contact: lines (do not publish contact names)
    blines = [ln for ln in blines if not ln.lower().startswith('contact:')]
    phone = None
    addr_lines = []
    for ln in blines:
        if re.match(r'^\d{3}-\d{3}-\d{4}$', ln):
            phone = clean_phone(ln)
            continue
        # Skip a duplicate name line used as a second street-ish line (Piedmont)
        if ln == b['name']:
            continue
        addr_lines.append(ln)
    assert addr_lines, b['name']
    # Last line should be "City, ST ZIP"
    citystate = addr_lines[-1]
    cm = re.match(r'^(.*?),\s*([A-Z]{2})\s+(\d{5}(-\d{4})?)$', citystate)
    assert cm, (b['name'], citystate, addr_lines)
    city, st, zipc = cm.group(1), cm.group(2), cm.group(3)
    street = ', '.join(addr_lines[:-1])
    # Waypoint: PDF literally prints "Avenue103" with no break; keep as printed and note it.
    note = None
    if 'Avenue103' in street:
        note = 'The EPD PDF prints the street line as "202 Hamilton Avenue103 Carroll Circle" with no break between Avenue and 103; shown as printed. Confirm the street address with the lab.'
    address = '%s, %s, %s %s' % (street, city, st, zipc)

    # Grouping
    if st != 'GA':
        group = 'limited'
        where = 'Out-of-state lab on Georgia\'s commercial microbiological list (%s).' % st
    elif looks_public(b['name']) or b['name'] == 'GA Environmental Protection Division':
        group = 'public'
        where = 'Name reads as a water utility, government or agency lab.'
    elif re.search(r'\bFoods?\b|\bDairy\b', b['name']) and 'Research' not in b['name']:
        # Tyson Foods
        group = 'limited'
        where = 'Industrial / food-plant lab on the commercial list; homeowner acceptance is unverified.'
    elif b['name'] == 'Tyson Foods':
        group = 'limited'
        where = 'Industrial / food-plant lab on the commercial list; homeowner acceptance is unverified.'
    else:
        group = 'main'
        where = None

    detail_parts = [b['detail_id'], 'Certified on this list for microbiological monitoring only (bacteria).']
    if where:
        detail_parts.append(where)
    detail = ' '.join(detail_parts)

    lab = dict(
        name=b['name'],
        address=address,
        city=city,
        phone=phone,
        accredited_for=['Microbiological monitoring (bacteria)'],
        detail=detail,
        group=group,
        source_name=SN,
        source_url=URL,
        source_date=SOURCE_DATE,
        last_verified=V,
    )
    if b['lab_id']:
        lab['lab_id'] = b['lab_id']
    if note:
        lab['note'] = note
    out.append(lab)

order = {'main': 0, 'public': 1, 'limited': 2}
out.sort(key=lambda l: (order[l['group']], l['name'].lower()))

# Override more_lib's hard-coded V for last_verified on write
import more_lib
more_lib.V = V

write_state(
    'georgia', 'Georgia', 'GA', out,
    {
        'name': SN,
        'page_url': URL,
        'program_url': PROGRAM,
        'report_date': 'List dated January 9, 2025',
    },
    {
        'title': 'Georgia labs certified for drinking-water microbiological monitoring (EPD list)',
        'description': 'The 16 commercial labs on Georgia EPD January 9, 2025 microbiological-monitoring certification list, with address, phone, lab ID and the source on every listing.',
        'intro': [
            'The Georgia Environmental Protection Division (EPD) publishes a PDF of commercial laboratories certified for microbiological monitoring of drinking water. The version transcribed here is dated January 9, 2025. Every lab on that list is certified for bacteria (microbiological monitoring); the PDF does not list chemistry certifications.',
            'UGA\'s Agricultural and Environmental Services Lab (AESL) publishes its own homeowner water-test menu and fees, usually handled through a county Extension office. AESL is a separate UGA page from this EPD list; see the links below for current AESL fees.',
        ],
        'caveats': [
            'The EPD list is dated January 9, 2025. Certification can change after that date. Confirm with EPD or the lab before you send a sample.',
            'This is a microbiological-monitoring list only. It does not say which labs are certified for nitrate, metals, lead, arsenic or other chemistry tests, and it does not say which labs accept samples from private-well owners. Call first.',
            'Contact-person names printed on the PDF are not reproduced here.',
            'Labs whose names read as a water utility, government lab or industrial plant, and labs with an out-of-state address, are listed in separate groups. Out-of-state labs appear on EPD\'s commercial list by reciprocity; confirm they will take a Georgia homeowner sample.',
            'One street address (Waypoint Analytical) is printed in the PDF with no space between "Avenue" and "103"; we show it as printed and note it on that listing.',
            COMMON_CAVEAT_PRICES,
        ],
        'main_heading': 'Georgia-address commercial labs on the microbiological list',
        'public_heading': 'Water-utility and government labs on the same list',
        'public_note': 'These are on EPD\'s commercial microbiological list, but their names read as a water company or the state EPD lab. They may serve their own system or compliance work. Call before sending a private-well sample.',
        'limited_heading': 'Out-of-state labs and industrial labs on the same list',
        'limited_note': 'Out-of-state labs are certified for Georgia microbiological monitoring by reciprocity. The industrial / food-plant lab is on the commercial list but is unlikely to be set up for homeowners. Confirm before you call.',
        'chips_label': 'On the EPD list for:',
        'resources': [
            {'label': 'Georgia EPD: Commercial labs certified for microbiological monitoring (PDF, January 9, 2025)', 'url': URL},
            {'label': 'Georgia EPD: Drinking water (Watershed Protection Branch)', 'url': PROGRAM},
            {'label': 'UGA AESL: water analyses and published fees', 'url': 'https://aesl.ces.uga.edu/water.html'},
            {'label': 'Georgia DPH: Well water', 'url': 'https://dph.georgia.gov/environmental-health/well-water'},
        ],
    },
)

from collections import Counter
print('groups', dict(Counter(l['group'] for l in out)))
for l in out:
    print(l['group'], l['name'], l.get('lab_id'), l['address'], l['phone'])
