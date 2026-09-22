# P03 / P05 / P07 Strict Canonical Audit — 2026-09-23

## P07 Public Meeting Attendance
Putnam exact measure: percent attending a public meeting on **town or school affairs** in the last year.
2008 CPS Civic Engagement Q4(b) asks whether respondent attended **a meeting where political issues are discussed**. This is broader/different.
Later VCL/local-government meeting wording is also not identical to Putnam's town-or-school-affairs item.
Disposition: legacy CPS P07 is NON_EQUIVALENT for strict canonical replication unless a wave-specific item with the original town/school wording is verified. Preserve as robustness.

## P03 Civic & Social Organization Density
Putnam exact measure: number of civic and social organizations per 1,000 population.
Census NAICS 813410 is explicitly "Civic and Social Organizations": establishments primarily engaged in promoting the civic and social interests of their members, including alumni associations, booster clubs, ethnic associations, fraternal lodges, granges, PTAs, scouting organizations, social clubs, veterans' membership organizations, etc.
Disposition: CONSTRUCT_COMPATIBLE and strongest modern administrative continuation. Remaining issue is unit continuity: Putnam's original Commerce source may count organizations whereas CBP counts employer establishments. Therefore retain as CANONICAL_CANDIDATE, not EXACT, until original Putnam denominator/numerator definition is matched to Commerce historical source.

## P05 Group Memberships
Putnam exact measure: average number of group memberships.
Binary VLMEMBER ("belonged to any") is not equivalent.
A count variable may be canonical only where CPS/VCL directly records number of groups/organizations, not by summing participation categories unless Putnam's original group-membership construction used the same category-count method.
Disposition: REBUILD_REQUIRED; legacy rate excluded from canonical index pending exact count-item/source verification.

## Canonical impact
P06 turnout and P08 501(c)(3) density remain the clearest currently compatible series.
P03 remains a high-priority compatibility candidate.
P05 and P07 legacy series move to robustness until exact-statistic/wording equivalence is demonstrated.
No legacy data are deleted.
