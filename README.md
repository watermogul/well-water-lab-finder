# Well Water Lab Finder

Static directory (Eleventy 3, Node 20) of state-accredited drinking-water labs for private-well owners.

```
npm install
npm run build     # -> _site/
npm run check     # internal links, listing source/date fields, sitemap
npm run serve     # dev server
SITE_URL=https://your-domain.example npm run build   # sets canonical, OG, sitemap, robots
```

## Data
`src/_data/labs/{state}.json` — one file per state. Every listing has `source_url`, `source_date`, `last_verified`.
`npm run data` regenerates PA/OH/NH/NY JSON from the source files in `/workspace/src` (PDF text extracted with `pdftotext -layout`); NH and NY are hand-entered in `scripts/build_data.py` from the sources cited in each record.
Narrative copy per state: `src/_data/states.json`.

## Ops
`ops/page-log.csv`, `ops/traffic.csv`, `ops/affiliate-ledger.csv`, `ops/queue.md`.

## Rules
Primary sources only. No invented data. No affiliate links until approved and disclosed (`/affiliate-disclosure/`).
