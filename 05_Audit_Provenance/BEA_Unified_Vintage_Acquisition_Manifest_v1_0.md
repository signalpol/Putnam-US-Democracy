# BEA Unified-Vintage Acquisition Manifest v1.0
Date: 2026-09-23

## Objective
Acquire E1, E2b, and E5 from one current BEA Regional Economic Accounts vintage wherever possible, using BEA's complete downloadable datasets rather than mixing publication vintages.

## Official routes verified
BEA Regional GDP & Personal Income portal explicitly provides "Download complete data sets".
BEA GDP by State page provides downloadable data and industry contributions.
BEA Personal Income by State page provides downloadable data.
BEA Real Personal Income page provides interactive/downloadable historical time series.

## Blocks
### E1
Real GDP by state:
- canonical real GDP level
- derive/retain real GDP growth
- derive real GDP per capita with documented population denominator
- study years 2000-2023

### E2b
Long-run state PCPI:
- current-dollar BEA per-capita personal income from one consistent vintage
- deflate over time with one documented national price index
- do not claim cross-state purchasing-power adjustment

### E2a
RPP-adjusted real personal income:
- separate BEA series
- current 2026 release explicitly revised 2008-2023
- use 2008-2023 unless older continuity is independently verified
- do not splice into E2b

### E5
Structural economic change:
- current-dollar manufacturing value added (NAICS 31-33)
- current-dollar total state GDP
- manufacturing share = manufacturing VA / total GDP * 100
- real manufacturing growth retained separately

## Vintage rule
E1/E2b/E5 should use the same BEA Regional vintage when raw acquisition is completed.
Record:
- retrieval date
- release/vintage date
- raw filenames
- SHA-256
- table names / line codes
- units
- revision notes

## Current execution status
Official source routes are verified.
The current container previously failed DNS resolution for apps.bea.gov before HTTP retrieval.
Therefore this manifest is READY, but no numeric BEA panel is marked ACQUIRED.

## Completion gates
Each full-period block must pass:
- exactly 50 states
- years 2000-2023
- 1,200 unique state-year keys
- zero duplicate keys
- documented missingness
- DC/territories excluded
- raw hash preserved
- source vintage preserved
