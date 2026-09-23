# E3 — BLS Current Historical Series Acquisition v1.0
Date: 2026-09-23

## Canonical decision
Use CURRENT REVISED HISTORICAL SERIES, not concatenated archived annual news releases.

## E3b Employment-Population Ratio
Official BLS LAUS page "Civilian Noninstitutional Population and Associated Rate and Ratio Measures for Model-Based Areas" provides:
- 50 states + District of Columbia;
- monthly data from January 1976 forward;
- Annual Average Series ZIP;
- CNP16+, labor-force participation rates, and employment-population ratios.

Canonical extraction:
- annual average employment-population ratio;
- 50 states only;
- 2000-2023;
- civilian noninstitutional population age 16+.

## E3a Unemployment Rate
Official BLS LAUS data system provides state annual-average labor-force estimates.
The documented state series begin in 1976 and include:
- civilian labor force;
- employed;
- unemployed;
- unemployment rate.

Canonical extraction:
- current revised annual-average state unemployment rate;
- 50 states only;
- 2000-2023.

## Why archived news releases are not canonical raw data
BLS explicitly cautions that archived news-release data may have been revised subsequently and directs users to current program databases for latest revised values.

Archived annual releases remain validation anchors only.

## Revision provenance
The CNP16+/ratio documentation states that revisions can reflect:
- model-based re-estimation;
- revised Census population controls.
Therefore record retrieval date/vintage and raw hashes.

## Validation gates
For each E3a/E3b:
1. 50 states.
2. 24 years (2000-2023).
3. 1,200 unique state-year keys.
4. zero duplicate keys.
5. inspect missing values.
6. exclude DC/Puerto Rico/other areas.
7. preserve raw BLS files unchanged.
8. record raw SHA-256.
9. cross-check selected 2023 values against official 2023 annual release.

## Status
OFFICIAL CURRENT-HISTORICAL ACQUISITION ROUTE VERIFIED.
NUMERIC 1,200-ROW PANELS NOT YET INGESTED/READ-BACK.
