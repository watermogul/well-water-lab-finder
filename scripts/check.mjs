// Post-build checks: (1) internal links/assets resolve, (2) every listing has source URL + dates, (3) sitemap URLs exist, (4) unique anchors.
import fs from "node:fs"; import path from "node:path";
const site = "_site"; let errors = 0; const err = (m) => { console.error("ERROR:", m); errors++; };
const walk = (d) => fs.readdirSync(d, { withFileTypes: true }).flatMap((e) => e.isDirectory() ? walk(path.join(d, e.name)) : [path.join(d, e.name)]);
const files = walk(site); const htmls = files.filter((f) => f.endsWith(".html"));
const exists = (u) => { u = u.split("#")[0].split("?")[0]; if (!u) return true; const p = path.join(site, u); return fs.existsSync(p) && (fs.statSync(p).isFile() || fs.existsSync(path.join(p, "index.html"))); };
let internal = 0;
for (const f of htmls) {
  const h = fs.readFileSync(f, "utf8");
  for (const m of h.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const u = m[1]; if (/^(https?:|mailto:|tel:|#|data:)/.test(u)) continue;
    internal++; if (!u.startsWith("/")) { err(`${f}: relative link ${u}`); continue; }
    if (!exists(u)) err(`${f}: broken internal link ${u}`);
  }
  const ids = [...h.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]); const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
  if (dup.length) err(`${f}: duplicate ids ${[...new Set(dup)].join(", ")}`);
  if (!/<title>.+<\/title>/.test(h) || !/name="description" content=".+"/.test(h)) err(`${f}: missing title/description`);
}
const dir = "src/_data/labs"; let listings = 0;
for (const f of fs.readdirSync(dir)) {
  const d = JSON.parse(fs.readFileSync(path.join(dir, f)));
  for (const l of d.labs) { listings++;
    for (const k of ["name", "address", "source_url", "source_date", "last_verified"]) if (!l[k]) err(`${f}: ${l.name} missing ${k}`);
    if (!/^https:\/\//.test(l.source_url || "")) err(`${f}: ${l.name} bad source_url`);
    if (!/^\d{4}-\d\d-\d\d$/.test(l.last_verified || "")) err(`${f}: ${l.name} bad last_verified`);
  }
}
const sm = fs.readFileSync(path.join(site, "sitemap.xml"), "utf8"); const locs = [...sm.matchAll(/<loc>https?:\/\/[^\/<]+(\/[^<]*)<\/loc>/g)].map((m) => m[1]);
for (const u of locs) if (!exists(u)) err(`sitemap URL missing: ${u}`);
if (/CHANGE-ME/.test(sm)) console.warn("WARN: sitemap uses placeholder domain (set SITE_URL before deploy)");
console.log(`pages: ${htmls.length}, internal refs checked: ${internal}, listings with source+dates: ${listings}, sitemap urls: ${locs.length}`);
process.exit(errors ? 1 : 0);
