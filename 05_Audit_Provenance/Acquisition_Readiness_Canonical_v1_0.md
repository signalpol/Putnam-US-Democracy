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
- P03 Civic/social organization density: PARTIAL_COLLECTOR. CBP numerator ready; canonical July-1 population acquisition not yet wired.
- P04 Club meetings: MISSING_STRICT; binary proxy prohibited.
- P05 Group memberships: PENDING_SOURCE.
- P06 Presidential turnout: COLLECTOR_READY; election waves only (2000, 2004, 2008, 2012, 2016, 2020); never annualize.
- P07 Public meeting attendance: PENDING_EQUIVALENCE.
- P08 501(c)(3) density: ACQUISITION_SCAFFOLD. Snapshot map resolved; actual NCCS download/filter/aggregation not yet wired.
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
