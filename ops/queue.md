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
   - 2026-10-31 nightly run: passed over again (page update). Shipped #14 (how to collect a well water sample) instead.
   - 2026-11-01 nightly run: passed over again (page update). Shipped #15 (reading your results / MCLs) instead.
   - 2026-11-02 nightly run: passed over again (page update). Shipped #16 (shock chlorination) instead.
   - 2026-11-04 nightly run: passed over again (page update). Shipped 'what your bacteria result means' guide (New ideas) instead.
   - 2026-11-03 nightly run: passed over again (page update). Shipped #17 (buying a house with a well) instead. No evergreen new-page items remain; next nightly should take a 'New ideas' item or do #9 as a page update.
   - 2026-11-06 nightly run: passed over again (page update). Skipped Illinois (stale/expired IDPH list), shipped Indiana full listing instead.
   - 2026-11-05 nightly run: passed over again (page update, not a new page). Expanded Georgia microbiological lab list into a full /labs/georgia/ listing instead. Continuous-disinfection evergreen and other New ideas remain for later runs.
   - 2026-11-07 nightly run: passed over again (page update). Shipped Iowa full listing (next item in the 2026-11-02 transcription list) instead.
   - 2026-11-08 nightly run: passed over again (page update). Skipped Kentucky (no current official full list), shipped Missouri full listing instead.
   - 2026-11-09 nightly run: passed over again (page update). Shipped Alabama full listing (next item in the 2026-11-02 transcription list) instead.

## State guides (free / low-cost programs and local risks, from state sources only)
(#13 NY flood/drought guide shipped 2026-10-30.)

## Evergreen guides
(#14 how-to-collect-a-sample guide shipped 2026-10-31. #15 reading-results/MCL guide shipped 2026-11-01. #16 shock chlorination guide shipped 2026-11-02. #17 buying-a-house-with-a-well guide shipped 2026-11-03.)

## Kits and money pages (blocked until affiliate approval)
18. **Tap Score review/comparison** — blocked: affiliate not applied for; need verified kit price and lab accreditation from their own pages (the product URL I tried returned 404).
19. **Mail-in kit comparison** (Tap Score, WaterTestingKits.com, others) — verify who runs the lab and its accreditation in your state before publishing. Apply to programs only after the user provides a live domain and payee details.

## Maintenance
20. **Re-verification pass** — re-fetch PA DEP reports (DEP may publish a newer one), Ohio EPA list (monthly updates likely), NHDES lab list, Westchester list; bump `last_verified` only when re-compared. **Done for PA on 2026-10-30** (reports unchanged, byte-identical). **Done for NH on 2026-11-05** (labs-private-wells.pdf still April 2026 / lab list updated 9/20/2024; existing 9 rows unchanged; added missing Nelson Analytical Maine/Kennebunk row from same PDF). Next oldest: Westchester, Ohio. **Ohio list has changed:** on 2026-11-09 the Combined-Lab-List.pdf at the OH_SRC URL was a new file (created 2026-10-30, md5 ab2501bd...; our copy in /workspace/src is the 2026-09-30 file, md5 2f93046e...). /labs/ohio/ says "Oct 2026" and was built from the 2026-09-30 file. Re-parse and diff row by row on the next re-verification run (not done 2026-11-09: not cheap). Consider moving NH to NHDES's live search once a scripted export is possible.

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

## New ideas (found while building the sampling guide, 2026-10-31)
- **NH PHL submittal form changed (file created 2026-07-29):** the bacteria-sample flush step is now "run the water for 1 minute" after cleaning the rim (older form said 5 minutes); fees match /guides/how-much-does-well-water-testing-cost/ ($95 standard, $120 with radon, $17 bacteria, $35 basic). Radon and nitrate/nitrite hold time is 48 hours. Re-check the NH arsenic guide's PHL wording on its next re-verification.
- **Colorado CDPHE "Collecting water samples" page** (cdphe.colorado.gov/laboratory-services/4-collecting-water-samples) has detailed state-lab rules (fill between 100 and 120 mL, alcohol not bleach on the faucet, 24-hour receipt) but returned 403 to curl and WebFetch on 2026-10-31. Not used. Try again or via browser before citing.
- **TCEQ GI-433 points to a Texas accredited-lab list** (www.tceq.texas.gov/goto/certified_labs). Texas was skipped on 2026-10-27 for no downloadable list; re-check where this link lands.

## New ideas (found while building the reading-results/MCL guide, 2026-11-01)
- **Watch EPA's PFAS rulemaking.** On 2026-05-18 EPA proposed keeping the PFOA/PFOS MCLs (4.0 ppt) with an option to extend compliance to 2031, and rescinding the PFHxS/PFNA/HFPO-DA/Hazard Index MCLs. /guides/reading-well-water-test-results-mcls/ describes these as proposals. Update that section when EPA finalizes either rule (check https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas).
- **Lead action level change on 2027-11-01** (LCRI): EPA's table says the public-system lead action level becomes 0.010 mg/L. Update the MCL guide's lead row after that date.
- **PA DEP MCL sheet (pa-mcls_06.pdf) is dated April 2006.** It is still linked from PA DOH's Sept 2024 guide. Not used. Look for a current PA DEP MCL list (PA adopted its own PFOA/PFOS MCLs) before citing any PA-specific numbers.
- **Penn State Drinking Water Interpretation Tool (DWIT)**: named on extension.psu.edu (best-management-practices page). Not fetched tonight. Verify its current URL before linking it from the MCL guide.
- **State-specific "reading your results" pages**: NH (NHDES standards, 5 ppb arsenic), Ohio (ODH nitrate/arsenic sheets, see Ohio ideas), and a "what your bacteria result means" page (see 2026-10-31 ideas) can each link back to the MCL guide.
- **Penn State video transcript typo:** it says arsenic's standard is "0.10 milligrams per liter" (EPA MCL is 0.010). Noted on the page; not reported to Penn State (that would be a user action).


## Added 2026-11-02: transcribe downloadable state lab lists into full listings
- Illinois: https://epa.illinois.gov/topics/labs/lab-accreditation/accredited-labs.html — **skipped 2026-11-06**: page links IDPH "Certified Water Microbiology Laboratories" (revision date 2025-12-04, 70 labs: 26 commercial, 40 municipal, 4 health dept) but 37 of the 70 printed expiration dates (Dec 2025-Oct 2026) are already past, so current status can't be verified from it; the IEPA "Primary/Secondary Labs - Chemical" PDF (created 2025-12-09, modified 2026-03-16) is a general NELAP list (wastewater/industrial labs included) with no drinking-water fields. Retry when IDPH posts a newer micro list, or list only unexpired rows with a clear caveat.
- **Georgia: SHIPPED 2026-11-05** as full /labs/georgia/ listing (16 labs from Jan 9, 2025 microbiological PDF; bacteria only; out-of-state + industrial grouped as limited; Waypoint address noted as printed with glued Avenue103). PDF: https://epd.georgia.gov/document/pdf/laboratoriescertifiedbygeorgiamicrobiologicalmonitoring2025/download
- **Indiana: SHIPPED 2026-11-06** as full /labs/indiana/ listing (49 in-state labs from the "accept samples from the public" section of the 11/7/2025 PDF; builder scripts/build_in.py + scripts/extract_in_tables.py, needs pdfplumber; IDOH kit fees on page). PDF: https://www.in.gov/idem/cleanwater/files/dw_cert_lab_in-state.pdf
- **Iowa: SHIPPED 2026-11-07** as full /labs/iowa/ listing (58 labs with the Drinking Water program from Iowa DNR LabCert "List of Certified Labs", generated 11/7/2026; main 11 commercial in-state, public 27, out-of-state 20; cert period/status from each DNR Lab Details record; six-test chips from DNR public search with Program = Drinking Water; builder scripts/build_ia.py, raw files in /workspace/src-ia). List: https://programs.iowadnr.gov/labcert/Home/LabListing
- Kentucky: https://eec.ky.gov/Environmental-Protection/Water/PermitCert/LabCert/Pages/Drinking-Water-Lab-Certification-Program.aspx — **skipped 2026-11-08**: the program page links no lab list (it only mentions "the Drinking Water Laboratory List"); .../LabCert/Documents/KYCertifiedDWLaboratoryList.pdf returns 404. The only full list found is a "2025 KY Certified Drinking Water Laboratory List" re-hosted by Greenup County Health Dept (greenupchdky.gov), not a current state copy. EEC does host current narrow lists: Lead-Certified DW Labs (revised 05/04/2026, .../DWProfessionals/ComplianceDocuments/LeadCertifiedLabs.pdf) and 2026 Certified DW PFAS Lab List (revised 1/23/2026, .../Water/Protection/Documents/KYCertifiedDWPFASLabList.pdf). Retry when EEC re-posts the full list, or ask DOWLabCertification@ky.gov for it (user action).
- **Missouri: SHIPPED 2026-11-08** as full /labs/missouri/ listing (87 labs from DNR micro 68 + chem 26 live lists, merged on street+ZIP; builder scripts/build_mo.py, raw files in /workspace/src-mo). Lists: https://dnr.mo.gov/water/business-industry-other-entities/certified-laboratories
- **Alabama: SHIPPED 2026-11-09** as full /labs/alabama/ listing (66 labs from ADEM's four PDFs: bacteriological + in-state chemical revised 2026-04-07, out-of-state chemical + PFAS revised 2025-10-03; main 13 commercial-by-name + 2 ADPH state labs, public 19, limited 34 out-of-state; builder scripts/build_al.py, tables via pdfplumber in /workspace/src-al/al_tables.json; ADPH BCL fee waived per form CL-27). Program page: https://adem.alabama.gov/water/drinking-water-branch/information-public-water-systems/adem-drinking-water-laboratory-certification-program
- Colorado: https://cdphe.colorado.gov/dwlabs
- Idaho: https://healthandwelfare.idaho.gov/providers/idaho-laboratories-and-testing/drinking-water-testing-and-certification
- Montana: https://waterquality.montana.edu/well-ed/testing/certifiedlabs.html
- Nebraska: https://dhhs.ne.gov/Public%20Health%20Lab%20Documents/certified%20labs.pdf
- Louisiana: https://ldh.la.gov/page/laboratory-certification
- Mississippi: https://msdh.ms.gov/safe-food-water-and-housing/water-supply/private-well-water-testing/water-supply-certification-labs
- New Mexico: https://www.env.nm.gov/drinking_water/lab-certification/
- Utah: https://deq.utah.gov/ddw/lab-sampling-resources
- Wyoming: https://www.epa.gov/region8-waterops/certified-drinking-water-laboratories-systems-wyoming-and-tribal-lands-epa-region
- South Dakota: https://danr.sd.gov/OfficeOfWater/DrinkingWater/LaboratoryCert.aspx
- Hawaii: https://health.hawaii.gov/sdwb/files/2025/12/Certified_Labs_202512.pdf
- Massachusetts: MassDEP private-well lab XLSX (mass.gov blocks curl; try browser)
- Kentucky: certified-lab PDF link 404 on 2026-11-02 and again 2026-11-08 (see above)

## New ideas (found while building the shock chlorination guide, 2026-11-02)
- **TCEQ approved-bleach list** (www.tceq.texas.gov/goto/bleach, cited in GI-432). Not fetched. Check before naming any brands.
- **"Bacteria came back after chlorinating" guide**: CSU covers biofilm, well cap/casing/seal repair and septic causes. Pair it with a state well-inspection or contractor-licensing page.
- **Iron bacteria in wells**: CSU covers detection and prevention. Could be a short evergreen guide; it needs a second extension source.
- **Re-verification**: NH done 2026-11-05. Still due: Ohio, NY/Westchester, MD (pages built 2026-10-26).

## New ideas (found while building the home-buyer guide, 2026-11-03)
- **State sale-testing rules page**: Oregon (ORS 448.271, verified 2026-11-03) requires seller testing for arsenic, nitrate, coliform; NJ PWTA (dep.nj.gov/privatewells/pwta/ blocked WebFetch with Incapsula tonight; try browser); Rhode Island reportedly requires testing at sale (unverified). Build a per-state table only from each state's own page.
- **Oregon domestic well guide**: OHA RET page links accredited labs and Well Report Query; could become an Oregon page from OHA sources.
- **VDH 'Buying a Home with a Well' video** linked from the VDH private well page; VDH real-estate FAQ metadata says modified 2017. Look for a newer VDH page before relying on it further.
- **Well yield/flow tests for buyers**: need a state or extension source with a method before writing.
- **NH re-verification done 2026-11-05**: NHDES April 2026 guidance still says "Lab list updated 9/20/2024"; row-by-row compare complete; Nelson Maine row added.

## New ideas (found while building the bacteria-result guide, 2026-11-04)
- **NH lab-list re-verification done 2026-11-05** (was due by 2026-11-06). PDF footnote still 9/20/2024; added Nelson Maine row.
- **Continuous disinfection guide (UV vs chlorination)**: Penn State Coliform Bacteria (2025-09-08) covers both with limits (UV not for >1,000 TC or >100 fecal coliform per 100 mL). Needs a second extension or state source; no equipment prices.
- **Sanitary well caps / well-cap inspection**: Penn State and CSU both point to caps and casing; find a state or extension how-to with photos/specs.
- **NYS DOH bacteria fact sheet**: health.ny.gov/.../bacteria_fact_sheet.htm returned 404 on 2026-11-04. Find the current NYS DOH coliform page before citing NY.
- **Penn State 2006 survey (coliform ~35%, E. coli ~15% of 450 PA wells)**: possible PA-specific context; quote with its date only.

## New ideas (found while expanding Georgia labs, 2026-11-05)
- **Georgia chemistry lab list:** the EPD PDF used tonight is microbiological monitoring only. Look for a separate EPD certified-chemistry / inorganic labs list before claiming full well panels for Georgia labs.
- ~~Indiana next~~ shipped 2026-11-06.
- **Nebraska / Hawaii PDFs** also fetched 200 tonight (NE short coliform/nitrate list; HI Nov 20, 2025 directory with in-state private-sample labs + many out-of-state). Iowa LabCert listing HTML also loaded.
- **UGA AESL vs EPD "UGA Feed and Environmental Water":** AESL publishes homeowner fees (W1 $20*, W6 $12*, W33B $90*, W35 coliform $40) at aesl.ces.uga.edu/water.html; EPD list names "UGA Feed and Environmental Water" at 2300 College Station Road without a GA Lab #. Do not merge fee rows onto the EPD listing without confirming they are the same lab on a primary source.
- **Continuous disinfection guide** still open (Penn State Coliform Bacteria 2025-09-08 + second extension/state source); no equipment prices.

## New ideas (found while building Indiana labs, 2026-11-06)
- **Indiana out-of-state labs:** the IDOH certification page (https://www.in.gov/health/laboratories/drinking-water-laboratory-certification) has a live HTML table of out-of-state labs approved for Indiana drinking water (chemistry by state, plus a radiological table incl. uranium/radium labs). Could be a second section on /labs/indiana/; note American Water Central Lab (Belleville IL) is marked "does not accept samples from the public". The table repeats some rows (Pace Madisonville KY, Element Lafayette LA) — de-duplicate and say so.
- **Indiana radiological labs:** IDOH lists Eurofins South Bend (gross alpha/beta, radium, uranium) and IDOH (uranium by mass) as in-state radiological labs. Not on the 11/7/2025 PDF; add only from the IDOH page.
- **Indiana arsenic/methane guide:** IDOH EPH page says glacial arsenic deposits and naturally occurring methane exist throughout Indiana. Pair with IDOH/IDEM or Purdue Extension sources for a short guide; no treatment prices.
- **IDOH kit fees on the cost guide:** /guides/how-much-does-well-water-testing-cost/ could add the IDOH private-citizen fees ($10 bacteria, $10 nitrate, $10 fluoride, $20 arsenic/lead/copper, plus shipping), quoted with the page URL and check date.
- **Illinois retry:** see the 2026-11-02 list entry (IDPH micro list has many expired rows as printed). Also check IDPH's own private-well testing page for local health department kits.
- **Re-verification due soon:** Ohio, NY/Westchester and MD (built 2026-10-26) have never been re-verified; NH was re-verified 2026-11-05 and PA 2026-10-30. Next run with time should re-verify Ohio (Combined-Lab-List.pdf is monthly).

## New ideas (found while building Iowa labs, 2026-11-07)
- **Iowa Private Well Grants guide:** Iowa DNR Well Testing page (metadata 2026-02-04) lists PWG funding amounts per service ($400 shock chlorination, $600 well assessment, $700 well plugging, $400 cistern plugging, $2,000 well reconstruction/renovation) with DNR forms, plus free county testing for bacteria, nitrate, arsenic, manganese. DNR PWG guidance PDF (updated July 8, 2026, /media/4621) defines qualifying wells/work. Good primary sources for a "free well testing and well grants in Iowa" guide; quote amounts with page date only.
- **Iowa county environmental health contacts:** DNR links a published Google Sheet of county contacts. A per-county table is possible, but verify against each county's own page before listing phone numbers.
- **SHL Well Water Quality and Home Treatment Systems Guide** (shl.uiowa.edu, file path 2023-11) has a coliform action-response flowchart. Possible second source for the continuous-disinfection / "bacteria came back" guides.
- **Iowa PFAS:** DNR "Private Wells and PFAS Overview" PDF (/media/4619); DNR says PFAS testing requires DNR pre-approval. Read the PDF before writing.
- **Iowa listing caveats to re-check on next pull:** QC Analytical Services (lab 113) record shows period ending Oct 1, 2026 but status Certified; Eurofins TestAmerica St. Louis (373) period starts Dec 1, 2026; EMSL Cinnaminson (419) ZIP printed as 80779; Des Moines Water Works, Davy, Microbac Northbrook marked Provisional.
- **More Iowa test chips:** LabCert public search (GET /labcert/Home/PublicSearchResults with program=1&analyteName=<id>) can add fluoride, uranium, radium, atrazine etc. Note it filters by program (verified: nitrate under Nonpotable only is excluded).
- **Re-verification due by ~2026-11-12:** NH was re-verified 2026-11-05; Ohio (monthly Combined-Lab-List.pdf), NY/Westchester and MD (built 2026-10-26) still never re-verified. Next night with time should do Ohio.

## New ideas (found while building Missouri labs, 2026-11-08)
- **Missouri State Public Health Laboratory micro certificate shows Jul 31, 2026 expiration** on the DNR list (still listed 2026-11-08). Re-check on the next Missouri pull; DNR CAS lab and St. Louis County R7 MO R01 chem entries also show Jul 31, 2026, Teklab micro and Milk Regulatory Consultants Oct 31, 2026.
- **Missouri private well sampling maps** (health.mo.gov/.../private-well-sampling-maps): DHSS county maps of wells tested and 10 contaminants. Possible "what's common in Missouri wells" guide; check data dates first.
- **Missouri lead-mining areas and wells:** DHSS kit page says lead occurs in groundwater in mining areas and recommends metals testing there; DHSS also posts "Radionuclides in Missouri Groundwater" (PDF dated 2026/03). Short Missouri guide from DHSS sources only.
- **MSPHL forms and instructions (Lab34 sampling instructions, Lab-177 private water form 2026/06, Lab-10H coliform/E. coli explanation 2026/08):** could feed the sampling and bacteria-result guides with a Missouri row (48-hour receipt rule vs 30 hours for public supplies).
- **Kentucky narrow lists:** EEC Lead-Certified labs (05/04/2026) and PFAS labs (1/23/2026) are current; a Kentucky lead/PFAS testing section could be added to /labs/kentucky/ from those two PDFs while the full list is missing.
- **Each Missouri DNR lab entry links a per-lab "parameters" document** (dnr.mo.gov/document/...-parameters-<date>); not used. Could give per-lab micro test detail (coliform vs E. coli) if the documents open as text.


## New ideas (found while building Alabama labs, 2026-11-09)
- **Cost guide: Alabama row.** ADPH form CL-27 (Collection Instructions for Private Water Samples, file modified 2026-09-23, https://www.alabamapublichealth.gov/bcl/assets/private-water-sample-form-ada.pdf) says "The fee is currently waived" for private-well bacteria tests at the ADPH Prattville and Mobile labs. Add to /guides/how-much-does-well-water-testing-cost/ with that date. County collection fees can still apply (Houston County page, updated 2025-08-21: $30 collection, $15 test at the county's own lab).
- **Sampling guide: Alabama row.** ADPH form: run water at least 3 minutes, fill to 100 mL, Mon-Thu 7:30-4:00, reject if over 30 hours old. ACES step-by-step guide (modified 2026-08-19) says 24 hours. Show both, side by side, like the other states.
- **Alabama county health department contacts:** ACES "Where to Get Your Well Water Tested" (modified 2025-06-04) has a county-by-county list of ADPH offices. A county table is possible, but verify each county's own ADPH page before listing phones or fees.
- **Auburn Soil, Forage and Water Testing Lab (W1 Total Water Analysis):** AU Water Resources Center says it is not drinking-water certified but can screen. Check the lab's own page for current tests and fees before mentioning it.
- **Water Well Trust (named on ADEM's consumer page for certain Alabama counties):** verify eligibility and counties on the Trust's own site before writing anything.
- **ADEM out-of-state chemical and PFAS lists are dated 2025-10-03.** Re-check the ADEM page for newer versions on the next Alabama pull.
