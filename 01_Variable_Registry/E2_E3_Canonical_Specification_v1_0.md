# E2/E3 Canonical Specification v1.0
Date: 2026-09-23

## E2 — Income / material living standard

### Measurement problem discovered
BEA's regionally price-adjusted Real Personal Income is conceptually attractive because it adjusts current-dollar personal income by Regional Price Parities (RPPs) and the national PCE price index. However, the current BEA release states that the annual state real-personal-income estimates revised with the release cover 2008-2023. It must therefore NOT be represented as a seamless canonical 2000-2023 series without further historical-source verification.

### Canonical split
E2a_RPP_real_income:
- BEA Real Personal Income / Real Per Capita Personal Income.
- Regionally price-adjusted.
- Use for the verified available period (currently 2008-2023 pending raw-table readback).
- Stronger cross-state purchasing-power interpretation.

E2b_longrun_real_pcpi:
- construct a 2000-2023 long-run state per-capita personal-income series from one consistent BEA current-dollar PCPI vintage and one common national price deflator.
- This adjusts intertemporal inflation but does NOT claim to adjust cross-state cost-of-living differences.
- Use as the full-period income measure if raw-source validation succeeds.

Report E2a and E2b separately. Do not splice them into one undocumented series.

## E3 — Labor market

Official source:
U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics / Geographic Profile of Employment and Unemployment.

Canonical variables:
E3a_unemployment_rate = annual average state unemployment rate.
E3b_employment_population_ratio = annual average employed persons as percent of civilian noninstitutional population.

BLS Geographic Profile annual publications contain state annual-average employment-status tables. The canonical study period is 2000-2023.

Validation:
1. retain 50 states only;
2. annual averages only;
3. verify denominator/population concept and any age threshold;
4. 1,200 state-year keys expected for each complete series;
5. preserve BLS revisions/vintage metadata;
6. no interpolation.

## Interpretation
E2 and E3 are not interchangeable:
- E2 measures material income/resources.
- E3a measures labor-market slack.
- E3b measures employment attachment to the working-age/civilian noninstitutional population.
Estimate separately before any economic composite.

## Status
E2a: VERIFIED CONCEPT; FULL 2000-2023 CONTINUITY NOT ESTABLISHED; current official release documents 2008-2023 revision window.
E2b: SPECIFIED; RAW SERIES/DEFLATOR ACQUISITION PENDING.
E3a/E3b: OFFICIAL ANNUAL STATE SOURCE VERIFIED; RAW 2000-2023 PANEL ACQUISITION PENDING.
