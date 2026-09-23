# E1 — BEA Real GDP by State: Canonical Specification v1.0
Date: 2026-09-23

## Canonical source
U.S. Bureau of Economic Analysis (BEA), Regional data.

## Official API specification
BEA API documentation provides the all-state/all-year real-GDP example using:
- DatasetName: Regional
- TableName: SAGDP9N
- LineCode: 2
- Year: ALL
- GeoFips: STATE

## Study-period extraction
Retain 50 states only.
Study years: 2000-2023.
Exclude District of Columbia and non-state territories from the canonical 50-state panel.

## Canonical E1 measures
E1a_real_gdp = state real GDP level from BEA.
E1b_real_gdp_growth = annual percent change calculated from the canonical real-GDP series or retained from a documented BEA growth table where definition is identical.
E1c_real_gdp_per_capita = E1a_real_gdp divided by a documented annual state population denominator, with units harmonized.

The level, growth rate, and per-capita level are analytically distinct and must not be silently substituted for one another.

## Validation gates
1. 50 states x 24 years expected = 1,200 keys.
2. unique state-year keys.
3. no DC/territory contamination.
4. document BEA units and chained-dollar reference.
5. inspect missingness.
6. archive retrieval date and raw-source hash.
7. document revision vintage.
8. review BEA's annual GDP-by-state discontinuity caution before final longitudinal interpretation.

## Revision rule
Use one internally consistent BEA vintage for the full 2000-2023 extraction. Do not splice values from different historical releases unless a formal vintage analysis is being conducted.

## Status
SOURCE / TABLE / API PARAMETERS VERIFIED.
NUMERIC 2000-2023 PANEL NOT YET INGESTED AND READ-BACK.
