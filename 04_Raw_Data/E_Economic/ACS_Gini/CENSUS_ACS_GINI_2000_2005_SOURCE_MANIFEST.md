# Census ACS Gini 2000–2005 — Source Manifest

## Canonical source
Hisnanick, John J. and Annette L. Rogers. *Household Income Inequality Measures Based on the ACS Data: 2000–2005*. U.S. Census Bureau working paper, 2007.

Official source URL:
https://www.census.gov/content/dam/Census/library/working-papers/2007/demo/ACS-inequality-report-2000-2005_v2.pdf

## Why retained
This source reports state-level Gini coefficients for each year 2000–2005 and closes the pre-2006 gap in the Ferragina-compatible E_F2_GINI series.

## Source facts / cautions
- Inequality measures were computed nationally and for each state using ACS data for 2000–2005.
- Measures include Gini coefficient, mean logarithmic deviation, Theil index, and Atkinson index.
- ACS was fully implemented in 2005 with about 3 million housing-unit addresses.
- During the 2000–2004 testing program, ACS used about 800,000 addresses per year.
- Census explicitly cautions that comparisons between 2005 and prior years can reflect geographic sample expansion, sampling error, and actual change.
- 2000 table source is Census 2000 Supplementary Survey; subsequent tables identify the corresponding Supplementary Survey / ACS source.
- Preserve reported 90% margins of error when extracting the historical Gini values.

## Canonical integration rule
Do not interpolate or smooth. Preserve original reported values and MOEs in raw/extracted files. Integrate point estimates into E_F2_GINI with a source-period flag. Treat the 2000–2004 test-program period as a documented measurement-regime caveat and test robustness excluding it.

## Existing later series
2006–2019 and 2021–2023: ACS 1-year B19083 canonical file already in repository.
2020 remains missing because ACS 1-year estimates were not released; do not impute.

## Analysis implication
Once 2000–2005 values are extracted and integrated, the main E(t-2) -> S(t-1) window (E years 2000–2008; S years 2002–2010) can use GDPpc, Gini, activity rate, and density on the same 48-state / 9-year panel rather than shrinking to 2008–2010.
