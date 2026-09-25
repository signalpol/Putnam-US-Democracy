# Ferragina E → S Stage 1 — Individual TWFE Results
Date: 2026-09-25

## Design
Outcome: Hawes/Compton social capital S at S_year.
Exposure: Ferragina-compatible E measured two years earlier (E_year = S_year - 2).
Specification: S_(i,t-1) ~ E_(i,t-2) + state FE + year FE.
Balanced sample: 48 contiguous states × 9 S years (2002–2010) = N 432.
Economic years: 2000–2008.
No interpolation/imputation. Alaska and Hawaii excluded by canonical S availability.

## Individual models
| E variable | beta | State-cluster SE | State-cluster p (df=47) | Two-way SE | Two-way p (conservative df=8) | Within R2 |
|---|---:|---:|---:|---:|---:|---:|
| ln(real GDP per capita) | -1.499037 | 0.781189 | 0.0611 | 0.731300 | 0.0745 | 0.01895 |
| Activity rate (%) | -0.050513 | 0.037363 | 0.1829 | 0.041299 | 0.2561 | 0.01404 |
| ln(population density) | +1.779439 | 0.973463 | 0.0739 | 0.856627 | 0.0714 | 0.01507 |

## Interpretation guard
None of the three individual coefficients reaches conventional two-sided 5% significance under the reported cluster inference.
GDP per capita is negative; activity rate is negative; population density is positive.
These are within-state, over-time TWFE associations and are not equivalent to Ferragina's cross-sectional regional coefficients.
Population density under state FE is identified from within-state population change, not persistent cross-state density differences.
Do not infer mediation or causality from this stage alone.

## Provenance
Analysis sample: 06_Analysis/E_TO_S_FERRAGINA_STAGE1_SAMPLE_v1.csv
Source master blob: f68f77aa1fe0102e66bdbb7f05e1a4d3c6349926
