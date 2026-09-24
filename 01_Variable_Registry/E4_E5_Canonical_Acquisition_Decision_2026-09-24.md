# E4-E5 Canonical Acquisition Decision — 2026-09-24

## E4 — State income inequality
Primary annual source: U.S. Census Bureau, American Community Survey (ACS), table B19083, Gini Index of Income Inequality.
Canonical annual coverage: 50 states, 2006-2023.
Reason: Census explicitly identifies 2006 as the earliest year the ACS Gini index is available. Therefore 2000-2005 MUST NOT be backfilled, interpolated, or labeled ACS Gini.

Variable:
- B19083_001E = Gini index estimate
- preserve MOE where available

Pre-2006 extension:
- remains a separate acquisition problem.
- any CPS/decennial/other state inequality series must be audited for construct, universe, estimator, and comparability before joining.
- if not comparable, E4 remains missing for 2000-2005 in the canonical annual panel.
- national historical Gini is not a substitute for state-year Gini.

## E5 — Structural economic change
Primary concept: state economic structure, with manufacturing exposure as the principal interpretable measure.
Candidate official sources:
1. BEA Regional GDP by industry — manufacturing value-added share of state GDP.
2. BEA/BLS state employment by industry — manufacturing employment share, if consistent 2000-2023 state coverage is verified.

Canonical rule:
- retain level/share and change measures separately.
- do not combine value-added share and employment share into one index before separate estimation.
- preserve industry classification/version metadata and audit NAICS continuity.

## Storage
E4 raw: 04_Raw_Data/E_Economic/Census_ACS_Gini/
E5 raw: 04_Raw_Data/E_Economic/BEA_Industry/ (or BLS industry subfolder if used)
Processed outputs retain E4_/E5_ prefixes.
No file enters 03_Master_Panel until coverage, duplicates, missingness, and provenance gates pass.

## No-interpolation rule
No canonical missing state-year observation may be interpolated.
