"""Query MassDEP LabCert (https://eeaonline.eea.state.ma.us/DEP/Labcert/Labcert.aspx), Matrix = Potable (DrinkingWater), one analyte at a time.
Saves labcert_potable.json: {analyte: [rows]}; rows = [id, name, address, phone, homeowner]."""
import re,html,requests,json,time
U='https://eeaonline.eea.state.ma.us/DEP/Labcert/Labcert.aspx'
A=['ALL','TOTAL COLIFORM','E. COLI','NITRATE-N','NITRITE-N','ARSENIC','LEAD','COPPER','FLUORIDE','IRON','MANGANESE','SODIUM','CHLORIDE','SULFATE','HARDNESS (CACO3), TOTAL','PH','TOTAL DISSOLVED SOLIDS','URANIUM','GROSS ALPHA','RADIUM-226','RADIUM-228','VOLATILE ORGANIC COMPOUNDS','ATRAZINE','2,4-D','SIMAZINE','ALACHLOR','PFAS','1,4-DIOXANE','PERCHLORATE','TURBIDITY']
def hid(h): return dict(re.findall(r'<input type="hidden" name="([^"]+)" id="[^"]+" value="([^"]*)"',h))
def rows(h):
    t=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','\x01',h)))
    cells=[c.strip() for c in t.split('\x01') if c.strip()]
    out=[]
    for i,c in enumerate(cells):
        if re.fullmatch(r'M-[A-Z0-9]+',c) and i+5<len(cells) and cells[i+5] in ('Y','N'):
            out.append(cells[i:i+6])
    return out
res={}
for a in A:
    s=requests.Session(); h=s.get(U,timeout=60).text
    d=hid(h); d.update(drpLabId='ALL',DrpMassid='ALL',drpstate='ALL',drpregion='ALL',drpRuleCode='ALL',DDpot='Potable (DrinkingWater)',btnSearch='Search',lstAnalyte=[a])
    h=s.post(U,data=d,timeout=120).text
    allr=rows(h); pages=sorted(set(int(p) for p in re.findall(r"__doPostBack\('UG2','Page:(\d+)'\)",h)))
    mx=max(pages) if pages else 1
    p=2
    while p<=mx:
        d=hid(h); d.update(drpLabId='ALL',DrpMassid='ALL',drpstate='ALL',drpregion='ALL',drpRuleCode='ALL',DDpot='Potable (DrinkingWater)',lstAnalyte=[a],__EVENTTARGET='UG2',__EVENTARGUMENT='Page:%d'%p)
        h=s.post(U,data=d,timeout=120).text
        allr+=rows(h)
        mx=max([mx]+[int(x) for x in re.findall(r"__doPostBack\('UG2','Page:(\d+)'\)",h)])
        p+=1
    ids=[r[0] for r in allr]
    res[a]=allr
    print(a,len(allr),len(set(ids)),'pages',mx,flush=True)
    time.sleep(1)
json.dump(res,open('labcert_potable.json','w'),indent=1)
