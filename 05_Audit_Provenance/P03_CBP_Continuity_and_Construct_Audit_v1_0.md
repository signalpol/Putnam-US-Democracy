# P03 — CBP Continuity and Construct Audit v1.0
Date: 2026-09-23

## Target
Putnam P03: Civic & Social Organization Density.

## Modern source verified
U.S. Census Bureau County Business Patterns (CBP):
- annual consistent program;
- downloadable datasets from 1986 through current reference years;
- state geography available;
- detailed NAICS industry;
- establishment counts available.

For study period 2000-2023, annual state data are therefore structurally available.

## Industry construct
NAICS 813410 = Civic and Social Organizations.
Official Census industry description identifies establishments primarily engaged in promoting the civic and social interests of their members.

This is substantively close to the P03 civic/social organization construct.

## Canonical candidate formula
P03_CBP_it = establishments in NAICS 813410 for state i, year t / state population_it * 1000.

Expected canonical grid after collection:
50 states x 24 years = 1,200 state-years.

## Critical unresolved equivalence gate
Do NOT label this EXACT Putnam replication yet.
Need documentary confirmation that Putnam's original P03 numerator/source operationalization corresponds to employer establishments (or a demonstrably equivalent Commerce/Census count), rather than a broader organization count that includes nonemployer entities.

CBP covers establishments with paid employees and excludes most government employees. This scope limitation must be explicitly compared with the original Putnam source.

## Continuity checks required
- confirm NAICS 813410 availability/coding in every 2000-2023 CBP vintage;
- inspect effects of NAICS revisions;
- record Census disclosure/noise procedures (noise infusion from 2007 noted in CBP documentation);
- verify state establishment counts are not suppressed for this industry;
- use one documented annual state population denominator;
- preserve raw annual files and hashes.

## Status
MODERN CONSTRUCT: STRONG / ANNUAL / STATE-LEVEL.
STRICT PUTNAM EQUIVALENCE: PENDING ORIGINAL-NUMERATOR LINEAGE CONFIRMATION.
NUMERIC PANEL: NOT YET INGESTED.
