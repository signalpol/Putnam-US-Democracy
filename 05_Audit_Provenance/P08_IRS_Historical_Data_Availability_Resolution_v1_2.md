# P08 IRS Historical Data Availability Resolution v1.2
Date: 2026-09-24

## Major finding
IRS SOI currently exposes annual charities/tax-exempt organization microdata pages covering 1985-2022. The annual samples include IRC 501(c)(3) organizations and contain weights for population estimation.
Examples verified directly from IRS include 2000, 2002, 2005 and 2010 microdata pages.

IRS also exposes "population data" derived from the Exempt Organization Master File for all Forms 990, 990-EZ and 990-PF returns filed by active organizations.

## Critical distinction
Putnam P08 is nonprofit organization density, not Form-990 return density.
Therefore:
- annual SOI SAMPLE microdata cannot automatically be counted as organizations;
- sample weights may estimate a filing population, but this must be audited against the P08 construct;
- IRS population/BMF historical files are preferred if they represent active organizations by state and subsection at the relevant historical vintage.

## Acquisition strategy
A. Preferred canonical numerator:
historical IRS population/BMF file for active 501(c)(3) organizations by state and year/vintage.

B. Validation/secondary:
annual SOI Form 990/990-EZ sample microdata with population weights, only after confirming state field, subsection, filing universe, and comparability to active-organization counts.

C. Never:
use current cumulative BMF to backcast prior years;
count sample rows as organizations;
mix filing-return counts with active-organization counts without labeling.

## Verified annual availability
IRS annual SOI charities/tax-exempt microdata index lists:
1985 through 2022, including every study year 2000-2022.
2023 is not listed in the current annual SOI microdata index as of this audit.

## Next extraction gate
For each candidate historical population file:
- verify vintage/reference date;
- locate EIN, subsection/status, state, active/filer universe;
- filter 501(c)(3);
- unique-EIN count by state;
- exclude DC/territories;
- merge canonical July 1 state population denominator;
- compute per-1,000 density;
- retain raw hash and source metadata.

## Coverage status
Historical source infrastructure: VERIFIED.
Canonical 50-state P08 numeric panel: NOT YET EXTRACTED.
