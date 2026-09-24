# P08 Historical BMF Source Resolution v1.3
Date: 2026-09-24

## Resolution
The canonical numerator for Putnam P08 should be built from historical IRS Exempt Organizations Business Master File (EO BMF) snapshots, not from annual Form 990 sample/population counts.

NCCS/Urban Institute preserves historical IRS BMF snapshots and documents BMF as the IRS registry of federally tax-exempt organizations. The legacy archive exposes snapshots including:
1999-12; 2000-05; 2001-07; 2002-01/07; 2003-07/11; 2004-04/12; 2005-07/11; 2006-01/05/11; 2007-01/04/09; 2008-01/04/06/10/12; 2009-04/07/10; 2010-01/04/08/11; 2011 multiple; 2012 multiple; 2013 multiple; 2014 multiple; 2015 multiple; 2016 through August in the legacy listing.
Current NCCS Unified BMF describes coverage from 1989 to present.

## Important correction
IRS SOI annual 501(c)(3) "population counts" refer to the population represented by annual Form 990/990-EZ studies/filings. They are not automatically the stock of all IRS-recognized 501(c)(3) organizations.
Example: IRS reports Tax Year 2000 sample count 16,353 and population count 233,816. Do not use 233,816 as P08 organization-stock numerator without a construct-equivalence demonstration.

## Canonical extraction
For each selected historical BMF snapshot:
1. retain one record per EIN;
2. identify IRC subsection 03 / 501(c)(3) using the documented BMF coding;
3. verify exempt status field and any relevant active-status rule;
4. use headquarters STATE field;
5. exclude DC, territories, international records;
6. count unique EINs for each of the 50 states;
7. merge the canonical July 1 resident-population denominator;
8. P08 = count / population * 1,000.

## Snapshot rule
Prefer one consistent annual reference month when available. Because early archive coverage is irregular, do not pretend every calendar year has an identical month.
Store exact snapshot month and conduct a timing sensitivity check where multiple snapshots exist.
Never interpolate missing BMF years.

## Coverage architecture
S1_P08_BMF_STRICT = observed historical BMF snapshots only.
Do not silently fill absent years from Form 990 samples or current BMF backcasts.
If current Unified BMF can reproduce historical snapshots from its 1989-present longitudinal structure, validate its historical state/subsection/status representation against legacy snapshots before using it as the principal extractor.

## Remaining task
Acquire actual NCCS historical/Unified BMF bytes, inspect dictionary/coding, calculate state counts, and compare overlapping legacy vs Unified BMF snapshots. Numeric P08 panel is NOT yet claimed complete.
