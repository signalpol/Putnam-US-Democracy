# P03 Population Denominator — Canonical Specification v1.0

## Construct
Annual state resident population used only as the denominator for:
P03 = CBP NAICS 813410 employer establishments / resident population * 1,000.

## Canonical source sequence
1. 2000-2009: Census 2000-2010 Intercensal State Population Estimates, July 1 annual estimates.
2. 2010-2020: Census 2010-2020 Intercensal State Population Totals (NST-EST2020INT-POP), July 1 annual estimates where available; the official intercensal series reconciles the decade to the 2020 Census.
3. 2021-2023: Census Population Estimates Program Vintage 2023 state population estimates.

## Boundary rule
Use one observation per calendar year. At decennial boundaries, prefer the official intercensal July 1 estimate for the relevant year rather than mixing April 1 Census counts with July 1 annual estimates.

## Why this sequence
Intercensal estimates provide a consistent series between decennial censuses. Census states that each PEP vintage revises the series since the latest census and that the latest vintage supersedes earlier estimates for those dates. Therefore Vintage 2023 is used for 2021-2023, while completed intercensal series are preferred for closed decades.

## Validation
- 50 states only; exclude DC, PR, territories.
- years 2000-2023.
- 1,200 unique state-year keys.
- population > 0.
- no interpolation.
- retain source-period/vintage field for every observation.
- preserve raw file/API SHA256 and retrieval date.

## Sensitivity
Because P03 is a density, denominator revisions are expected to be small relative to numerator differences but will be checked at 2010 and 2020 boundaries. If material discontinuities appear, report them and test alternative boundary treatment.

## Status
SOURCE ARCHITECTURE: CANONICAL.
RAW NUMERIC PANEL: NOT YET ACQUIRED/VALIDATED.
