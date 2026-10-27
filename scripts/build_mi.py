"""Michigan: EGLE Remediation & Redevelopment Division, "State of Michigan Certified Laboratories: Microbiological" (165 labs) and "...: Chemistry" (61 labs),
both footed "SOM Certified Labs 3/11/2026", fetched 2026-10-27. The two PDFs are merged on the EGLE lab code (173 distinct labs).
Contact-person names, emails and the contact's direct phone numbers printed on the PDFs are NOT reproduced."""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
from more_lib import *
from mi_parse import parse
SRC_DIR = os.environ.get('SRC_DIR', '/workspace/src2')
U_MICRO = 'https://www.michigan.gov/egle/-/media/Project/Websites/egle/Documents/Programs/RRD/Lab/Microbiological-Laboratory-Certifications.pdf'
U_CHEM = 'https://www.michigan.gov/egle/-/media/Project/Websites/egle/Documents/Programs/RRD/Lab/Chemistry-Laboratories.pdf'
PAGE = 'https://www.michigan.gov/egle/about/organization/remediation-and-redevelopment/laboratory/certifications'
SN_M = 'Michigan EGLE, "State of Michigan Certified Laboratories: Microbiological" (list footed 3/11/2026)'
SN_C = 'Michigan EGLE, "State of Michigan Certified Laboratories: Chemistry" (list footed 3/11/2026)'
a = parse(os.path.join(SRC_DIR, 'mi_micro.txt')); b = parse(os.path.join(SRC_DIR, 'mi_chem.txt'))
MI_PUB = re.compile(r"township|treatment|filt\.|filtration|\bwfp\b|wtp|brd\.|board of water|water auth|auth\.|national park|water lab\b|water plant|water works", re.I)
BOTTLER = re.compile(r"blue triton|bottl", re.I)
PRIVATE = re.compile(r"great lakes water quality laboratory|consultants", re.I)  # names that trip the utility words but read as private firms
labs = []
for k in sorted(set(a) | set(b)):
    d = a.get(k) or b.get(k)
    h = [re.sub(r'^\W+', '', x) for x in d['head']]
    m = re.match(r"(.*),\s*([A-Za-z.' ]+),\s*MI,\s*(\d{5})(-\d{0,4})?\s*$", h[0])
    assert m, (k, h)
    street, city, zp = m.group(1), m.group(2), m.group(3)
    an = sorted(set(a.get(k, {}).get('analytes', [])) | set(b.get(k, {}).get('analytes', [])))
    bact = any(re.search(r'coliform|e\.? ?coli', x, re.I) for x in an)
    chem = any(re.search(r'nitrate|arsenic|\blead\b|copper|fluoride|manganese|\biron\b', x, re.I) for x in an)
    chips = key_chips(an)
    if any(re.search(r'\bvocs\b', x, re.I) for x in an) and 'Volatile organic compounds (VOCs)' not in chips:
        chips.append('Volatile organic compounds (VOCs)')
    pub = (looks_public(d['name']) or bool(MI_PUB.search(d['name']))) and not PRIVATE.search(d['name'])
    if BOTTLER.search(d['name']): grp = 'limited'
    elif pub: grp = 'public'
    elif bact and chem: grp = 'main'
    else: grp = 'limited'
    first, sn, su, sd = (a, SN_M, U_MICRO, None) if k in a else (b, SN_C, U_CHEM, None)
    l = dict(name=d['name'], address='%s, %s, MI %s' % (street, city, zp), city=city, lab_id='EGLE lab code %s' % k,
        accredited_for=chips, group=grp,
        detail='Michigan EGLE lab code %s · %d analytes listed as certified (see the source PDF for the full list).' % (k, len(an)),
        source_name=sn, source_url=su, source_date='2026-03-11')
    if k in a and k in b:
        l.update(source_name_2=SN_C, source_url_2=U_CHEM)
    labs.append(l)
order = {'main': 0, 'public': 1, 'limited': 2}
labs.sort(key=lambda l: (order[l['group']], l['name'].lower()))
write_state('michigan', 'Michigan', 'MI', labs,
 {'name': SN_M + ' and ' + SN_C, 'page_url': U_MICRO, 'program_url': PAGE, 'report_date': 'Lists footed March 11, 2026'},
 {
 'title': 'Michigan state-certified drinking-water labs (EGLE list)',
 'description': 'Michigan labs certified by EGLE for drinking-water microbiology and chemistry (lists footed March 11, 2026): commercial labs shown first, municipal labs separate, with the analytes certified and the source on every listing.',
 'intro': [
  "Michigan's Department of Environment, Great Lakes, and Energy (EGLE) certifies labs for drinking-water analysis and publishes two PDF lists: one for microbiological labs and one for chemistry labs. Both are footed 3/11/2026. Together they name 173 labs, and each entry gives the lab's address and the analytes it is certified for.",
  "We merged the two lists on EGLE's lab code. A lab certified for both coliform bacteria (total coliform or E. coli) and at least one common well chemistry test (nitrate, arsenic, lead, copper, fluoride, manganese or iron) is shown first, unless its name says it is a water system, treatment plant or municipal lab.",
 ],
 'caveats': [
  "These lists are several months old (March 2026). EGLE can add or drop labs at any time, so confirm on EGLE's certification page or by calling the Lab Certification program at (517) 335-9219.",
  "EGLE certifies labs for compliance testing. The lists do not say which labs take homeowner samples and do not give prices. Call the lab first.",
  "The grouping is ours and comes from lab names, not from EGLE. Labs with \"water treatment plant\", \"township\", \"water authority\", \"board of water\" and similar words in the name are shown in the municipal/utility group. Bottlers are shown with the limited labs.",
  "The EGLE lists print a contact person, email and direct phone number for each lab. We do not reproduce those. Use the lab's website or ask EGLE for the main number. The chips show only a short list of common well tests, not every analyte; EGLE's PDFs list all of them.",
  "EGLE's lists send readers to separate PFAS lab lists for PFAS testing. We did not use those.",
  COMMON_CAVEAT_PRICES,
 ],
 'main_heading': 'Michigan commercial and private labs certified for bacteria and well chemistry',
 'public_heading': 'Municipal, utility and other water-system labs on the EGLE lists',
 'public_note': 'These are usually run by a city, township, authority or treatment plant for its own sampling. EGLE does not say whether they take homeowner samples. Call first. The grouping is based on the lab name.',
 'limited_heading': 'Labs certified for only one test category, plus bottlers',
 'limited_note': 'EGLE shows these as certified for bacteria only or chemistry only (or for a narrow set of tests), or they are bottling labs. Most are probably not set up for homeowners.',
 'chips_label': 'Common well tests EGLE lists for this lab:',
 'resources': [
  {'label': 'EGLE: Certified Laboratories, Microbiological (PDF)', 'url': U_MICRO},
  {'label': 'EGLE: Certified Laboratories, Chemistry (PDF)', 'url': U_CHEM},
  {'label': 'EGLE: Laboratory certification program page', 'url': PAGE},
 ]})
