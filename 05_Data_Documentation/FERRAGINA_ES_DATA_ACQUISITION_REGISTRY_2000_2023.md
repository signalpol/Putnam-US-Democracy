# 2000–2023 Ferragina-Compatible E–S Data Acquisition Registry
Date: 2026-09-25
Status: DATA COLLECTION / NO STATISTICAL MODEL EXECUTED

## Rule
Collect and preserve the full 2000–2023 source universe before any new E–S statistical model is run. Do not interpolate, splice unlike social-capital measures, or redefine canonical S. Raw sources and measurement regimes remain separate.

## E — Ferragina-compatible economic block

### E_F1 Real GDP per capita
Coverage: 50 states, 2000–2023.
Status: COMPLETE in existing Ferragina E master.
Construction: BEA real GDP / Census resident population.

### E_F2 Gini
2000–2005: U.S. Census Bureau, Hisnanick & Rogers, Household Income Inequality Measures Based on ACS Data: 2000–2005. Official state tables report point estimates and 90% MOEs.
2006–2019: ACS 1-year B19083, existing canonical raw file.
2020: ACS 1-year estimates were not released. KEEP MISSING; no interpolation.
2021–2023: ACS 1-year B19083, existing canonical raw file.
Status: SOURCE LOCATED for 2000–2005; extraction/integration pending.
Measurement caveat: 2000–2004 ACS testing program (~800,000 addresses/year); 2005 full implementation (~3 million addresses). Preserve regime flag.

Official early source:
https://www.census.gov/library/working-papers/2006/demo/SEHSD-WP2006-07.html
PDF:
https://www.census.gov/content/dam/Census/library/working-papers/2007/demo/ACS-inequality-report-2000-2005_v2.pdf

### E_F3 Activity rate
Coverage: 50 states, 2000–2023.
Source: BLS LAUS civilian labor force / civilian noninstitutional population age 16+.
Status: COMPLETE in existing Ferragina E master.

### E_F4 Population density
Coverage: 50 states, 2000–2023.
Population: Census intercensal/Vintage population series.
Land area: Census TIGER/Line 2020 state ALAND.
Status: COMPLETE in existing Ferragina E master.

### E_F5 National divergence
Ferragina variable retained conceptually, but no U.S.-state analogue accepted yet.
Status: NOT PORTED. Do not invent a proxy. Requires theoretical equivalence decision before use.

## S — social-capital source architecture

### S1 Canonical Putnam/Hawes/Compton
Hawes/CSPP / Compton replication.
Coverage in research window: 48 contiguous states, 2000–2010; 528 observed state-years.
Status: COMPLETE and frozen. Alaska/Hawaii missing, never zero.

### S2 CPS Volunteer Supplement — continuous comparable source family
U.S. Census Bureau Current Population Survey Volunteer Supplement.
Official microdata/API support exists for state geography beginning 2002.
Verified annual source availability: 2002–2015.
Use as a separate Putnam-compatible civic/volunteering proxy family; never splice into Hawes/Compton index.

Canonical Census dataset/API:
https://www.census.gov/data/developers/data-sets/census-microdata-api.CPS.html
2015 example dataset:
https://www.census.gov/data/datasets/2015/demo/cps/cps-volunteer.html

Status: SOURCE SERIES LOCATED; raw annual files/state estimates still to be ingested.

### S2b CPS Civic Engagement Supplement
Separate CPS civic-engagement source years include 2010, 2011, 2013 and the combined 2017 instrument.
Official dataset:
https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-civic.html
Status: SOURCE LOCATED; preserve separately because questionnaire/instrument differs by wave.

### S3 Combined Volunteering and Civic Life / CEV
Official CPS combined supplement. Verified source years:
2017, 2019, 2021, 2023.
2023 page also exposes CSV microdata.
Official dataset:
https://www.census.gov/data/datasets/time-series/demo/cps/cps-supp_cps-repwgt/cps-volunteer.html
Census confirms the combined survey measures formal volunteering, informal helping, group participation, political/civic engagement, donations, and related civic-health behaviors.
Status: 2017/2019/2021/2023 canonical CEV extraction already partly stored; full raw-source harmonization pending.

### S4 JEC Social Capital Index
U.S. Congress Joint Economic Committee Social Capital Project, state/county index.
Official data/download page:
https://www.jec.senate.gov/public/index.cfm/republicans/sci
Status: LOCATED. Cross-sectional/period index; external validation/bridge only unless measurement-vintage structure supports longitudinal use. Never treat as annual observations.

## Coverage implication
There is no defensible single identical S index observed annually for every year 2000–2023. Therefore the data architecture must retain measurement families:
- S1 Hawes/Compton: 2000–2010
- S2 CPS Volunteer: 2002–2015
- S2b CPS Civic Engagement: selected 2010/2011/2013/2017 waves
- S3 CEV combined: 2017/2019/2021/2023
- S4 JEC: external/bridge index
No automatic splicing or interpolation.

## Next data-only actions before statistics
1. Extract and store 50-state 2000–2005 Census Gini point estimates + 90% MOEs.
2. Ingest raw/state-level CPS Volunteer source data for 2002–2015 with year-specific metadata.
3. Verify exact questionnaire-variable continuity across Volunteer and CEV instruments.
4. Preserve 2010/2011/2013 Civic Engagement raw files separately.
5. Complete CEV 2017/2019/2021/2023 raw-source archive and state-level indicator codebook.
6. Update Ferragina E master to v2 only after early Gini QA.
7. Do not run correlations, regressions, significance tests, or mediation until user approval.
