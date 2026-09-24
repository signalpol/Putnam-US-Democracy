# P08 501(c)(3) Density — Historical Snapshot Decision v1.1
Date: 2026-09-24

## Construct
P08 = number of 501(c)(3) nonprofit organizations per 1,000 state residents.

## Critical source rule
The current IRS Exempt Organizations Business Master File (EO BMF) is cumulative and contains the most recent information known to IRS. It is NOT a historical panel snapshot.
Therefore the current 2026 EO BMF must not be used to infer organization counts for 2000-2023.

## Canonical numerator
For each year t, use only a contemporaneous/historical IRS/SOI extract or archived EO BMF vintage that supports the number of active/recognized 501(c)(3) organizations in state s at the defined reference date/year.
Acceptable sources must preserve:
- tax-exemption/subsection code sufficient to identify 501(c)(3);
- state/headquarters location;
- historical vintage/reference year;
- inclusion/exclusion rules.

IRS notes that state in EO BMF represents filing/headquarters address and may not represent every state in which an organization operates. This limitation must be stated.

## Denominator
Use the same canonical July 1 state resident population framework adopted for P03 unless the original Putnam P08 definition requires a different denominator after final lineage audit.
Density = historical 501(c)(3) count / state resident population * 1,000.

## Current IRS data role
Current EO BMF may be used for:
- present-day validation;
- code/field mapping;
- endpoint comparison;
but NOT as a substitute for historical annual snapshots.

## Historical acquisition routes
1. IRS Statistics of Income historical exempt-organization population extracts.
2. IRS archived annual extracts / historical BMF vintages.
3. Reputable preserved federal-data archives with exact IRS vintage/provenance.
4. If only selected years exist, retain observed years; do not interpolate.

## Validation
- 50 states, DC/territories excluded.
- explicit reference date/year.
- subsection/501(c)(3) filter verified.
- unique EIN counting rule.
- raw hash/vintage recorded.
- no interpolation.
- no current-snapshot backcasting.
