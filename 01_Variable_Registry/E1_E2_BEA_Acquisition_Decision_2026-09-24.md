# E1-E2 BEA Acquisition Decision — 2026-09-24

## E1 — Real economic performance
Canonical source: U.S. Bureau of Economic Analysis (BEA), Regional accounts.
Coverage target: 50 states x 2000-2023.
Measures:
- real GDP by state
- real GDP per capita constructed only with an explicitly documented population denominator or an official per-capita line where available
- annual real GDP growth derived reproducibly from the real GDP series

BEA state GDP methodology covers all states and DC from 1997, so 2000-2023 is within the official coverage window.

## E2 — Material living standard
Canonical long-panel source: BEA SAINC1 Personal Income Summary.
Coverage target: 50 states x 2000-2023.
SAINC1 supplies personal income, population, and per-capita personal income over the full required period.

### Important comparability decision
BEA's regionally price-adjusted Real Personal Income / real per-capita personal income series is not used as the sole canonical E2 for 2000-2023 because the modern RPP-based state series begins in 2008. It will be retained as a 2008-2023 robustness/validation series.

For the full 2000-2023 E2 panel, nominal per-capita personal income from SAINC1 must be converted to a national constant-price basis with one documented national deflator if a real-dollar level is required. This removes national inflation but does not impose state-specific RPPs before 2008. The manuscript must state this distinction.

## Storage
Raw BEA responses/files -> 04_Raw_Data/E_Economic/BEA/
Processed E1/E2 -> clearly prefixed E1_/E2_ products
Analytic merge -> 03_Master_Panel only after validation

## Validation gates
- exactly 50 states; exclude DC/territories
- years 2000-2023
- 1,200 unique state-year keys per complete measure
- no interpolation
- missingness explicit
- source table/line codes preserved
- raw and processed SHA-256 recorded
