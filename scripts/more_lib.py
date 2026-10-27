"""Shared helpers for the state builders added 2026-10-27 (build_<state>.py). Each builder reads an official
state list that was fetched on 2026-10-27, writes src/_data/labs/<slug>.json and merges narrative into src/_data/states.json.
Nothing here invents data: every field comes from the source file; groups are the only editorial step and are explained on each page."""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = '2026-10-27'

# Well-relevant analytes, matched as whole words against the analyte names printed in a state list.
KEY = [
 ('Total coliform', r'total coliform'),
 ('E. coli', r'e\.? ?coli|escherichia'),
 ('Nitrate', r'\bnitrate\b'),
 ('Nitrite', r'\bnitrite\b'),
 ('Arsenic', r'\barsenic\b'),
 ('Lead', r'\blead\b'),
 ('Copper', r'\bcopper\b'),
 ('Fluoride', r'\bfluoride\b'),
 ('Manganese', r'\bmanganese\b'),
 ('Iron', r'\biron\b'),
 ('Uranium', r'\buranium\b'),
 ('Radon', r'\bradon\b'),
 ('Gross alpha', r'gross alpha'),
 ('Radium', r'\bradium\b'),
 ('Sodium', r'\bsodium\b'),
 ('Chloride', r'\bchloride\b'),
 ('Sulfate', r'\bsulfate\b'),
 ('Hardness', r'hardness'),
 ('pH', r'^ph\b|\bph\b'),
 ('Total dissolved solids', r'total dissolved solids|\btds\b'),
 ('Volatile organic compounds (VOCs)', r'\bvoc\b|volatile organic|\bbenzene\b|trichloroethylene'),
 ('Pesticides / herbicides', r'pesticide|herbicide|atrazine|alachlor|simazine|2,4-d'),
 ('PFAS', r'pfas|perfluoro|pfoa|pfos'),
]

def key_chips(names):
    out = []
    for label, rx in KEY:
        r = re.compile(rx, re.I)
        if any(r.search(n) for n in names):
            out.append(label)
    return out

PUB_RX = re.compile(r"(water (treatment|plant|authority|department|dept|works|district|system|production|reclamation|filtration|utilit|supply|resources|commission|board|company)|waterworks|\butilit|public service|service authority|wastewater|waste water|sanitation|sanitary|\bwwtp\b|\bwtp\b|\bcity of\b|\btown of\b|village of|borough|\bcounty\b|\bdepartment\b|\bdept\b|\bauthority\b|\bdistrict\b|virginia american water|wv american water|american water (company|works|central)|fairfax water|loudoun water|prince william water|division of consolidated|water co\b|water company|health (dept|department|division|district|agency)|public health|state laboratory|state lab|\bvdacs\b|\bnavfac\b|\bhrsd\b|aqueduct|municipal|\bboard of\b|filter plant|water plant|water quality lab|environmental services division|commission)", re.I)

def looks_public(name):
    return bool(PUB_RX.search(name))

def write_state(slug, name, abbr, labs, list_source, narrative):
    labs = [dict(l) for l in labs]
    for l in labs:
        l.setdefault('last_verified', V)
    d = {'state': name, 'slug': slug, 'abbr': abbr, 'list_source': list_source, 'last_verified': V, 'labs': labs}
    with open(os.path.join(ROOT, 'src/_data/labs', slug + '.json'), 'w') as f:
        json.dump(d, f, indent=1, ensure_ascii=False); f.write('\n')
    sp = os.path.join(ROOT, 'src/_data/states.json')
    s = json.load(open(sp))
    n = dict(narrative); n.update({'name': name, 'abbr': abbr})
    s[slug] = n
    with open(sp, 'w') as f:
        json.dump(s, f, indent=1, ensure_ascii=False); f.write('\n')
    from collections import Counter
    c = Counter(l['group'] for l in labs)
    print(slug, len(labs), dict(c))

def clean_phone(p):
    if not p: return None
    p = str(p).strip()
    d = re.sub(r'\D', '', p)
    if len(d) == 10:
        return '(%s) %s-%s' % (d[:3], d[3:6], d[6:])
    return p

COMMON_CAVEAT_PRICES = 'We did not verify prices, turnaround times or websites for any lab on this page, so none are shown.'
