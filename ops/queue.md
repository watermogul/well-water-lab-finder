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
   - 2026-10-27 nightly run: passed over (not skipped for sourcing). It expands the existing /labs/new-york/ page rather than shipping a new page, and the statewide ELAP part needs a user action. Do it as a page-update run.
   - 2026-10-28 nightly run: passed over again for the same reason (page update, not a new page). Shipped #11 (NH arsenic/radon/uranium guide) instead.
   - 2026-10-29 nightly run: passed over again (page update). Shipped #12 (Ohio where-to-test guide) instead. Suggest scheduling a dedicated page-update run for this.
   - 2026-10-30 nightly run: passed over again (page update). Shipped #13 (NY flood/drought guide) instead. All new-page queue items in "State guides" are now used; next nightly should take an evergreen guide (#14-#17) or do #9 as a page update.

## State guides (free / low-cost programs and local risks, from state sources only)
(#13 NY flood/drought guide shipped 2026-10-30.)

## Evergreen guides
14. **How to collect a well water sample (bacteria vs chemistry)** — from lab instructions (Penn State, NH PHL already fetched) and EPA.
15. **Reading your results: maximum contaminant levels in plain English** — EPA MCL list (PA DEP also links PA_MCLs_06.pdf — check date).
16. **Shock chlorination: when and how** — state extension/DEP source only.
17. **Buying a house with a well: what to test and when** — NHDES home-buyer test plus EPA.

## Kits and money pages (blocked until affiliate approval)
18. **Tap Score review/comparison** — blocked: affiliate not applied for; need verified kit price and lab accreditation from their own pages (the product URL I tried returned 404).
19. **Mail-in kit comparison** (Tap Score, WaterTestingKits.com, others) — verify who runs the lab and its accreditation in your state before publishing. Apply to programs only after the user provides a live domain and payee details.

## Maintenance
20. **Re-verification pass** — re-fetch PA DEP reports (DEP may publish a newer one), Ohio EPA list (monthly updates likely), NHDES lab list, Westchester list; bump `last_verified` only when re-compared. **Done for PA on 2026-10-30** (reports unchanged, byte-identical). Next oldest: NH (list dated 2024-09-20), Westchester, Ohio. Consider moving NH to NHDES's live search once a scripted export is possible.

## New ideas (found while building Maryland, 2026-10-26)
- **Maryland: out-of-state certified labs** near the PA/VA/DE lines — MDE's 10/1/2026 PDF lists 53 out-of-state labs (e.g. PA and VA labs with Micro + Inorganics). Could be a second section on /labs/maryland/; verify each from the same PDF.
- **Maryland: county health department well-testing help** — MDE's Be Well Wise page points to local health departments and UMD Extension; verify each county's own page before listing.
- **Maryland: certified water samplers** — MDE recommends a certified sampler for private/real-estate testing and publishes Current-Certified-Water-Samplers.pdf; check whether it's usable as a listing source.
- **UMD Extension's 2019 homeowner lab list** includes Caswell Testing, Enviro-Chem, Martel and Environmental Testing Lab, which are not on MDE's 10/1/2026 in-state list. Do not list them unless re-verified.

## New ideas (found while building the PA free/low-cost testing guide, 2026-10-27)
- **PA free-testing guide: re-check for a 2026-27 Penn State / PA DOH session schedule.** None was published on 2026-10-27 (Safe Drinking Water Clinic page said "check back for future occurrences"). Add dates only from extension.psu.edu event pages.
- **PA county programs not yet verified:** Chester County Health Dept (chesco.org/957 lists well-testing info and a lab list at chesco.org/978, but no county kit service was confirmed), Montgomery County, Erie County Dept of Health. Add each only from its own page. ACHD's own web pages return 403 to curl; the kit fee isn't printed on ACHD's May 2026 instructions PDF.
- **PA DOH "How to Interpret Water Test Results" guide + "Private Well Water Testing Checklist" PDFs** (pa.gov, both return 200). Good primary sources for evergreen guide #15 (reading results).
- **Penn State county test summaries** (agsci.psu.edu/.../drinking-water-test-summaries), possibly a "what's common in your PA county" page. Check the data format and date first.
- **Bucks County's own accredited-lab PDF** (buckscounty.gov/DocumentCenter/View/27708). Cross-check against the PA DEP list on /labs/pennsylvania/.
- **PA DOH PFAS and private wells fact sheet (Sept 2025)**, possibly a "PFAS in Pennsylvania wells" guide. It cites treatment cost ranges, which must be quoted with attribution only.

## New ideas (found while building the Ohio where-to-test guide, 2026-10-29)
- **Re-verify /labs/ohio/ against Ohio EPA's October 2026 Combined-Lab-List.pdf.** That page was built from the 2026-10-26 pull. Several labs on OSU's 2021 list are no longer on it: Brookside, Advanced Analytics, Archbold, Con-Test, Perry, Heidelberg NCWQR and Alloway Mansfield (now Eurofins).
- **CWM Environmental lineage:** its old address and phone now appear under "Eurofins Environment Testing North Central (formerly Metiri)". Confirm this from Eurofins' or Ohio EPA's own page before listing it as CWM.
- **More Ohio county health districts:** add rows to the guide's fee table one at a time, each from the district's own page or fee schedule. So far it has Wayne, Mercer, Logan and Highland.
- **Highland County adopted 2026 fees:** the guide cites a PDF titled "Proposed 2026". Re-check for the adopted schedule.
- **ODH nitrate and arsenic fact sheets + OSU water-test interpretation resources:** could become an Ohio "reading your results" guide (ties to evergreen #15).
- **Heidelberg University NCWQR well-testing program:** it was on OSU's 2021 list but not on the Ohio EPA list. Check its own site for a current homeowner program before mentioning it.

## Known gaps to close
- Contact/corrections channel (needs an email or form from the owner).
- Per-lab analyte detail for NH and NY.
- A `/kits/` hub (nothing verified yet).
- Individual lab pages (`/labs/{state}/{lab}/`): held back to avoid thin pages; add only with fee or service details from the lab's own page.

## New ideas (found while building the NH arsenic/radon/uranium guide, 2026-10-28)
- **NH page re-verification:** NHDES PDFs and pages return 403 to curl but load via the WebFetch tool. The NH lab list (/labs/new-hampshire/) can be re-checked that way. The April 2026 guidance still says "Lab list updated 9/20/2024".
- **NH PFAS in private wells:** NHDES samples private wells for PFAS, with a Sampling Dashboard and a Private Well Testing Request Form on the NH PFAS Response page (per the April 2026 guidance). This could become a guide on free NHDES PFAS sampling. Verify on the PFAS Response page itself.
- **NH PHL fee drift:** the 2021 arsenic fact sheet printed $15 for arsenic; the current PHL submittal form shows $17. When re-verifying /guides/how-much-does-well-water-testing-cost/, compare all NH PHL fees against the current form.
- **Rock blasting and wells (NH):** the NHDES brochure says to test before blasting and several months to a year after. Look for an NHDES blasting/well fact sheet for a short guide.
- **NHDES fact sheet URLs:** dwgb-2-1.pdf (Suggested Water Testing) now returns 404 to WebFetch, so it is not cited. Find its current location before citing it anywhere.

## New ideas (found while building the NY flood/drought guide, 2026-10-30)
- **NY certified bulk water haulers by county** — NYS DOH publishes the certified hauler list (health.ny.gov/environmental/water/drinking/bulkwater/bulkwter.htm). A page sorted by county, from that list only, with its date. The list does not say who delivers to private homes; state that.
- **NY Private Well Risk Mapper / PFAS testing rebate pilot** — mentioned in the NYS DOH 2024-03-22 press release (Dutchess, Orange, Putnam, Suffolk, Ulster, Westchester). Verify current status on a DOH page before writing.
- **NYS DOH Fact Sheet #3 (water quality testing)** — good primary source for evergreen #14 / #15 (condition-based test list).
- **NYS DOH pub 6562 (printed 2/17) prints old Wadsworth/DEC URLs that have moved.** Don't cite those printed URLs; use current pages.
- **PA live accredited-lab report** — DEP's Laboratory Reports page links an SSRS "Accredited Labs" report (cedatareporting.pa.gov/Reportserver/...Lab_Certification). If it can be exported (CSV/PDF) it may be newer than the June 2024 PDFs that /labs/pennsylvania/ uses. Check its date and the drinking-water filter before switching.
