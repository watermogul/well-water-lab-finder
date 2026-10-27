# Page queue (next 20)

Rules for every page: primary sources only; source URL + source date + "last verified" on every listing; no invented data; no affiliate links until a program has approved the account and the disclosure is updated. Log each shipped page in `page-log.csv`.

## State lab pages (new data pulls)

## State lab pages: shipped 2026-10-27 (batch expansion)
Done (each uses only the state's official list, fetched 2026-10-27; builders in `scripts/build_<st>.py`, shared code in `scripts/more_lib.py`; raw source files are not committed, set `SRC_DIR`): **Virginia, Wisconsin, Tennessee, West Virginia, Minnesota, Maine, Vermont, Connecticut, Michigan, Rhode Island.** Run `npm run data:more` after re-downloading sources.

Skipped this run (do not retry without a new route to the data):
- **New Jersey** — official lookup is the interactive NJEMS DataMiner (https://njems.nj.gov/DataMiner/), NJDEP site blocks automated fetch; no downloadable list found. Overview: https://dep.nj.gov/dsr/oqa/certified-laboratories/
- **Massachusetts** — MassDEP lab search is interactive (https://eeaonline.eea.state.ma.us/DEP/Labcert/Labcert.aspx); mass.gov blocks automated fetch. How-to page: https://www.mass.gov/how-to/find-a-certified-laboratory-for-water-testing
- **North Carolina** — certified lab list is an interactive/online search; no downloadable list verified.
- **Illinois** — IEPA/IDPH lists found were stale or too thin to publish.
- **Kentucky, Indiana, Georgia, South Carolina, Colorado, Missouri, Iowa, Washington, Oregon, California, Texas** — program pages fetched but no downloadable official list (interactive search, per-county lists, or lists for compliance labs only). Not published.
- **Nebraska, Delaware, Montana** — seen in search, not evaluated (Montana's only list found is a university directory, not an official state list). NE: https://dhhs.ne.gov/Public%20Health%20Lab%20Documents/certified%20labs.pdf; DE: https://dhss.delaware.gov/dph/homepage/about/sections/hsp/licenses-and-permits/odw/laboratory-certification-program/
- Not-yet-reverified links: tn.gov, NH sites and mass.gov return 403 to automated fetch (TDEC page URL was confirmed by web search; NH links predate this batch).

Known data caveats to revisit: Michigan lists are footed March 2026 (re-pull when EGLE updates); Wisconsin bacteria-portal rows show the zip the portal prints (some do not match the city); the public/limited grouping on VA, WI, WV, MI is name-based.

Still open:
9. **New York: other counties** — Rockland, Chemung and others publish private-well lab lists; fetch each PDF and verify before listing. Also try to get a statewide ELAP drinking-water list another way (call/email Wadsworth ELAP is a user action).

## State guides (free / low-cost programs and local risks, from state sources only)
10. **Pennsylvania: free and low-cost private well testing programs** (county health departments, Penn State Extension). Verify each program on its own page first.
11. **New Hampshire: arsenic, radon and uranium in bedrock wells** — from NHDES/DHHS pages.
12. **Ohio: where to get a private well tested** — find the Ohio Dept. of Health / local health district pages and verify which labs accept homeowner samples (call list).
13. **New York: private-well testing after a flood or drought** — NYS DOH source pages.

## Evergreen guides
14. **How to collect a well water sample (bacteria vs chemistry)** — from lab instructions (Penn State, NH PHL already fetched) and EPA.
15. **Reading your results: maximum contaminant levels in plain English** — EPA MCL list (PA DEP also links PA_MCLs_06.pdf — check date).
16. **Shock chlorination: when and how** — state extension/DEP source only.
17. **Buying a house with a well: what to test and when** — NHDES home-buyer test plus EPA.

## Kits and money pages (blocked until affiliate approval)
18. **Tap Score review/comparison** — blocked: affiliate not applied for; need verified kit price and lab accreditation from their own pages (the product URL I tried returned 404).
19. **Mail-in kit comparison** (Tap Score, WaterTestingKits.com, others) — verify who runs the lab and its accreditation in your state before publishing. Apply to programs only after the user provides a live domain and payee details.

## Maintenance
20. **Re-verification pass** — re-fetch PA DEP reports (DEP may publish a newer one), Ohio EPA list (monthly updates likely), NHDES lab list, Westchester list; bump `last_verified` only when re-compared. Consider moving NH to NHDES's live search once a scripted export is possible.

## New ideas (found while building Maryland, 2026-10-26)
- **Maryland: out-of-state certified labs** near the PA/VA/DE lines — MDE's 10/1/2026 PDF lists 53 out-of-state labs (e.g. PA and VA labs with Micro + Inorganics). Could be a second section on /labs/maryland/; verify each from the same PDF.
- **Maryland: county health department well-testing help** — MDE's Be Well Wise page points to local health departments and UMD Extension; verify each county's own page before listing.
- **Maryland: certified water samplers** — MDE recommends a certified sampler for private/real-estate testing and publishes Current-Certified-Water-Samplers.pdf; check whether it's usable as a listing source.
- **UMD Extension's 2019 homeowner lab list** includes Caswell Testing, Enviro-Chem, Martel and Environmental Testing Lab, which are not on MDE's 10/1/2026 in-state list. Do not list them unless re-verified.

## Known gaps to close
- Contact/corrections channel (needs an email or form from the owner).
- Per-lab analyte detail for NH and NY.
- A `/kits/` hub (nothing verified yet).
- Individual lab pages (`/labs/{state}/{lab}/`): held back to avoid thin pages; add only with fee or service details from the lab's own page.
