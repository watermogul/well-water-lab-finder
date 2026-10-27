"""West Virginia: WV DHHR Office of Laboratory Services, "Laboratory Certified Parameter List" (Environmental Drinking Water Laboratory Certification Program), printed Aug. 20, 2026, fetched 2026-10-27."""
import os, sys, re, collections
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
exec(open(os.path.join(os.path.dirname(__file__), 'wv_parse.py')).read())
URL = 'https://dhhr.wv.gov/ols/labs/Documents/Environmental%20Chemistry/waterqualitylabs%20%282026%29%20-%20Updated%20List%20%288-20-26%29.pdf'
PAGE = 'https://dhhr.wv.gov/ols/regulatory/Pages/WaterLabCertification.aspx'
SN = 'West Virginia DHHR Office of Laboratory Services, "Laboratory Certified Parameter List" (drinking water, printed 8/20/2026)'
SRC_URL = os.environ.get('WV_URL', URL)
merged = collections.OrderedDict()
for k, v in out.items():
    base = re.sub(r'[A-Za-z]$', '', k)
    m = merged.setdefault(base if base == '00003' else k, dict(v, keys=[], params=[]))
    m['keys'].append(k)
    if m is not v: m['params'] = m['params'] + v['params']
    else: pass
labs = []; oos = 0
for k, v in merged.items():
    v['params'] = list({(a, b, c) for a, b, c in v['params']}) if False else v['params']
for k, v in merged.items():
    cert = [p for p in v['params'] if p[2] == 'Certified']
    names = [p[1] + ' ' + p[0] for p in cert]
    chips = key_chips(names + ['polyfluoroalkyl PFAS' if any('Polyfluoro' in p[0] for p in cert) else ''])
    secs = list(dict.fromkeys(p[0] for p in cert))
    street = ', '.join(v['addr'][:-1]); cs = re.sub(r'\s+,', ',', v['addr'][-1])
    m = re.match(r'(.*?),\s*([A-Za-z]{2})\s+(\d{5}(-\d{4})?)', cs)
    city, st, zp = m.group(1), m.group(2).upper(), m.group(3)
    inwv = st == 'WV'
    micro = any(p[0].startswith('Microbiology') for p in cert)
    pub = looks_public(v['name']) and not v['name'].startswith('West Virginia Dept. of Health - Office')
    if not inwv: grp = 'limited'
    elif pub or v['name'].startswith('WVAW'): grp = 'public'
    elif micro or any(k2.endswith('C') and v['name'].startswith('West Virginia Dept. of Health') for k2 in v['keys']): grp = 'main'
    else: grp = 'limited'
    if not inwv and grp != 'limited': pass
    if not inwv: oos += 1
    det = 'WV certificate no. %s · issued %s · expires %s · %d certified parameter entries on the WV list.' % (' and '.join(v['keys']), v['issue'], v['exp'], len(cert))
    if not inwv: det += ' This lab is located outside West Virginia (%s).' % st
    labs.append(dict(name=v['name'], address='%s, %s, %s %s' % (street, city, st, zp), city=city, lab_id=' / '.join(v['keys']),
        accredited_for=chips or [re.sub(r'^Organics, ', '', s) for s in secs] or ['(no certified parameters)'], detail=det,
        group=grp, source_name=SN, source_url=SRC_URL, source_date='2026-08-20'))
order = {'main': 0, 'public': 1, 'limited': 2}
labs.sort(key=lambda l: (order[l['group']], l['name'].lower()))
write_state('west-virginia', 'West Virginia', 'WV', labs,
 {'name': SN, 'page_url': SRC_URL, 'program_url': PAGE, 'report_date': 'Printed August 20, 2026; certificates expire Jan. 31, 2027'},
 {
 'title': 'West Virginia certified drinking-water labs (Office of Laboratory Services list)',
 'description': 'Labs on West Virginia Office of Laboratory Services certified-parameter list for drinking water (printed Aug. 20, 2026): in-state coliform labs, the state chemistry lab, and out-of-state chemistry labs, with the source on every listing.',
 'intro': [
  "West Virginia's Office of Laboratory Services (part of DHHR) certifies drinking-water labs under 64CSR3 and publishes a \"Laboratory Certified Parameter List\": one certificate per lab, with address, issue and expiration dates, and every analyte and method the lab is certified for. The copy used here was printed August 20, 2026; every certificate on it expires January 31, 2027.",
  "Almost every in-state lab on the list is certified for coliform bacteria only (certificate numbers ending in M). The only in-state lab certified for chemistry on the list is the state's own Office of Laboratory Services in Charleston. The chemistry labs the list shows are mostly out-of-state commercial labs (certificate numbers ending in C), so we show those too, with their location in the address.",
 ],
 'caveats': [
  "This is a compliance-certification list. It does not say which labs accept samples from homeowners and does not list prices. Call the lab first, and ask about shipping if it is out of state.",
  "In-state labs whose names look like a water company, utility or agency are shown in the utility/agency group. That is our judgment from the name. They usually test for their own system.",
  "The list has no phone numbers, so none are shown. Check the lab's own website or call directory information.",
  "For out-of-state labs, 'Certified' is as printed on the WV list for drinking water compliance. Several of them are certified only for narrow groups (for example PFAS, radionuclides or disinfection byproducts); the analyte chips show what the WV list shows. Entries printed as 'Not Certified' were left out.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'West Virginia coliform-bacteria labs and the state chemistry lab',
 'public_heading': 'Water-company, utility and agency labs on the same list',
 'public_note': 'These labs look from their names like they belong to a water company, utility or state agency and test mainly for their own system. Call first.',
 'limited_heading': 'Out-of-state labs certified by West Virginia (mostly chemistry)',
 'limited_note': 'These labs are located outside West Virginia (two in Virginia are certified for coliform bacteria; the rest for chemistry) but hold a West Virginia drinking-water certification for the analyte groups shown. Many cover only specialty groups. Ask each lab which test packages and shipping options it has for homeowners.',
 'chips_label': 'Certified analytes shown on the WV list for this lab:',
 'resources': [
  {'label': 'WV Office of Laboratory Services: Laboratory Certified Parameter List (PDF, printed 8/20/2026)', 'url': SRC_URL},
  {'label': 'WV Office of Laboratory Services: drinking-water laboratory certification program', 'url': PAGE},
 ]})
