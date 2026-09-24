# Putnam U.S. Democracy — Acquisition Readiness Canonical v1.0
Date: 2026-09-24

This file records execution readiness, not substantive findings.
No item is marked acquired unless a validated numeric artifact exists.

## D — Democracy
- D / Berkeley SDI 2.0: collector present; official endpoint corrected to 2025/01/SDI_2.0.csv.
- Required output: 50 states x 2000-2023 = 1,200 rows.
- Status: COLLECTOR_READY / RAW_NOT_YET_VERIFIED_IN_REPO.

## E — Economic block
- E1 Real GDP: BEA SAGDP9N line 2; collector + canonical builder present.
- E2 PC Personal Income: BEA SAINC1 line 3; nominal PCPI retained pending documented deflation.
- E3 LAUS: unemployment/employment/labor force collector present.
- E4 Gini: ACS1 B19083; 2006-2019 and 2021-2023 canonical; 2020 structural missing.
- E5 Manufacturing VA share: BEA SAGDP2N same-table current-dollar numerator/denominator.
- Status: COLLECTORS_READY / RAW EXECUTION INCOMPLETE.

## S — Social capital strict layer
- P01 Committee service: BLOCKED_SOURCE.
- P02 Officer service: BLOCKED_SOURCE.
- P03 Civic/social organization density: COLLECTORS_READY. CBP numerator plus official Census 2000-2010/2010-2020 intercensal and Vintage 2023 July-1 population collector implemented; numeric execution still required.
- P04 Club meetings: MISSING_STRICT; binary proxy prohibited.
- P05 Group memberships: PENDING_SOURCE.
- P06 Presidential turnout: COLLECTOR_READY; election waves only (2000, 2004, 2008, 2012, 2016, 2020); never annualize.
- P07 Public meeting attendance: PENDING_EQUIVALENCE.
- P08 501(c)(3) density: COLLECTOR_READY. NCCS harmonized/transformed monthly BMF is streamed and aggregated by state for subsection 03 unique EINs; 2017-09, 2017-12, 2018-12 known-bad vintages excluded; numeric execution still required.
- P09 Community project: MISSING_STRICT; rate proxy prohibited.
- P10 Volunteer work: PENDING_EQUIVALENCE.
- P11 Visiting friends: BLOCKED_SOURCE (DDB post-1998 exact microdata not acquired).
- P12 Entertain at home: BLOCKED_SOURCE.
- P13 Generalized trust: BLOCKED_GEOCODE; GSS exact construct but state identifiers restricted.
- P14 Perceived honesty: BLOCKED_SOURCE.

## Pipeline semantics
- Structural missingness is permitted.
- S2/S3 never fill S1.
- No interpolation.
- A written master panel does not imply complete acquisition.
- Pipeline PASS requires executable acquisition/validation gates; otherwise PARTIAL.
\n## Credential/runtime gates\n- BEA API: registered 36-character UserID required by current BEA API guide; E1/E2/E5 correctly fail without BEA_API_KEY.\n- Census population/CBP: public official files/API; no BEA-style credential requirement introduced.\n- NCCS P08: public S3 monthly harmonized/transformed products; large files require streaming and sufficient runtime/network.\n