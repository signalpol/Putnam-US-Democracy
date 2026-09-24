# Ferragina-Compatible E Block — Canonical Specification v1

Date: 2026-09-25
Project: Putnam U.S. Democracy Project
Unit: U.S. state-year
Target: 50 states × 2000–2023 = 1,200 rows
Missing-data rule: no interpolation / no imputation.

## Primary E variables
E_F1_REAL_GDP_PC — real GDP per capita. Numerator: BEA SAGDP9N real GDP by state. Denominator: BEA SAINC1 population. Unit: chained-dollar GDP per resident. Formula: SAGDP9N real GDP (millions) * 1,000,000 / SAINC1 population.

E_F2_GINI — Gini coefficient of household income. Existing canonical ACS1 B19083 series retained as observed. Pre-ACS1 unavailable years remain missing; no backfill unless a separately justified, source-compatible series is approved.

E_F3_ACTIVITY_RATE — labor-force participation/activity rate. Source: BLS LAUS annual-average state series. Definition: civilian labor force / civilian noninstitutional population age 16+ × 100. This replaces unemployment rate in the Ferragina-compatible primary specification; unemployment remains archived for robustness.

E_F4_POP_DENSITY — resident population per square mile of land area. Population: annual official state population series; land area: Census state land area. Formula: resident population / land square miles. Land-area vintage and boundary changes must be documented; do not interpolate density.

## Ferragina variable not mechanically ported
NATIONAL_DIVERGENCE — Ferragina's multi-country regional variable. No U.S. state analogue is assigned until the original operational definition is verified and a theoretically equivalent U.S. state measure is justified. No ad-hoc proxy.

## Relationship to legacy E block
Legacy E1 Real GDP, E2 PCPI, E3 unemployment are preserved, not deleted, and moved to robustness/exploratory status.
Legacy E4 Gini maps to E_F2.

## Primary model family
Ferragina-compatible E -> S:
S_it = f(E_F1_REAL_GDP_PC, E_F2_GINI, E_F3_ACTIVITY_RATE, E_F4_POP_DENSITY)
with cross-sectional Ferragina-style replication and longitudinal panel specifications reported separately.

Full project:
E_(t-2) -> S_(t-1) -> D_t

## Source anchors
Ferragina (2013), International Journal of Comparative Sociology 54(1):48–73, DOI 10.1177/0020715213481788.
BEA Regional: SAGDP9N and SAINC1.
BLS LAUS: statewide annual-average employment-status series, 1976-present.
U.S. Census Bureau: population density / land-area documentation and population estimates.

## Integrity guards
1. Do not modify S or D to improve results.
2. Do not substitute unemployment for activity rate.
3. Do not substitute total GDP for GDP per capita in the Ferragina-compatible specification.
4. Do not fill missing Gini years by interpolation.
5. Keep raw source files immutable and record source/vintage/hash.
6. Ferragina cross-sectional replication and the project's longitudinal causal/mediation tests are distinct analyses.
