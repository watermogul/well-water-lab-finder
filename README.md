# Well Water Lab Finder

Static directory (Eleventy 3, Node 20) of state-accredited drinking-water labs for private-well owners.

```
npm install
npm run build     # -> _site/
npm run check     # internal links, listing source/date fields, sitemap
npm run serve     # dev server
SITE_URL=https://your-domain.example npm run build   # sets canonical, OG, sitemap, robots
```

## Deploy (GitHub Pages)
`.github/workflows/pages.yml` builds on push to `main` and deploys to https://watermogul.github.io/well-water-lab-finder/ using `SITE_URL` and `PATH_PREFIX=/well-water-lab-finder/` (Eleventy `pathPrefix` + HTML Base plugin rewrite internal links). For a custom domain later, change those two env vars in the workflow to `SITE_URL=https://your-domain.example` and `PATH_PREFIX=/`, and set the domain in the repo's Pages settings.

## Data
`src/_data/labs/{state}.json` — one file per state. Every listing has `source_url`, `source_date`, `last_verified`.
`npm run data` regenerates PA/OH/NH/NY JSON from the source files in `/workspace/src` (PDF text extracted with `pdftotext -layout`); NH and NY are hand-entered in `scripts/build_data.py` from the sources cited in each record.
Narrative copy per state: `src/_data/states.json`.

## Ops
`ops/page-log.csv`, `ops/traffic.csv`, `ops/affiliate-ledger.csv`, `ops/queue.md`.

## Rules
Primary sources only. No invented data. No affiliate links until approved and disclosed (`/affiliate-disclosure/`).
