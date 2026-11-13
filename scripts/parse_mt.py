"""Parse Montana DPHHS Water Laboratory Certification Program page (HTML accordion of certified labs).
Usage: parse_mt(path) -> list of (category, region, name, street_lines, citystatezip, phone)."""
import re, html

def _clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).replace('\xa0', ' ').strip()

def parse_mt(path):
    t = open(path, encoding='utf-8', errors='replace').read()
    a = t.find('Certified Laboratories</h1>'); b = t.find('For questions regarding laboratory certification')
    assert a > 0 and b > a, 'lab section not found'
    seg = re.sub(r'(?s)<!--.*?-->', '', t[a:b])
    rows = []
    cards = re.split(r'<div class="card-header"', seg)[1:]
    for card in cards:
        cat = _clean(re.search(r'(?s)<button[^>]*>(.*?)</button>', card).group(1))
        body = card[card.find('card-body'):]
        region = None
        for m in re.finditer(r'(?s)<h3>(.*?)</h3>|<p>(.*?)</p>', body):
            if m.group(1) is not None:
                region = _clean(m.group(1)); continue
            parts = [_clean(x) for x in re.split(r'<br\s*/?>', m.group(2))]
            parts = [p for p in parts if p]
            if not parts: continue
            assert region, ('no region', parts)
            phone = parts[-1] if re.search(r'\(\d{3}\)\s*\d{3}-\d{4}', parts[-1]) else None
            if phone: parts = parts[:-1]
            name, csz = parts[0], parts[-1]
            rows.append(dict(category=cat, region=region, name=name, street=parts[1:-1], csz=csz, phone=phone))
    return rows

if __name__ == '__main__':
    import sys
    for r in parse_mt(sys.argv[1]): print(r)
