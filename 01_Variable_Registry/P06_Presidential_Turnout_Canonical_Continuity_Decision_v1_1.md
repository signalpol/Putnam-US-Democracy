# P06 Presidential Turnout — Canonical Continuity Decision v1.1
Date: 2026-09-24

## Construct
P06 is Putnam-style presidential-election turnout at the state level.
It is an election-wave variable, not an annual variable.

Canonical study-period waves:
2000, 2004, 2008, 2012, 2016, 2020.
2024 is outside the canonical 2000-2023 panel.

## Continuity problem
The U.S. Election Assistance Commission's EAVS begins in 2004. Therefore EAVS alone cannot provide a homogeneous 2000-2020 presidential series.
EAVS also reports turnout using denominators such as CVAP; denominator choice must not be silently changed across waves.

## Canonical rule
Select one documented denominator definition that can be applied consistently to all six presidential elections.
Candidate hierarchy:
1. Voting Eligible Population (VEP) turnout if a documented state series covers all six waves consistently.
2. Voting Age Population (VAP) turnout if it better matches the original Putnam statistic and is consistently available.
3. Ballots/votes divided by a Census population denominator only if numerator and denominator definitions are fully documented and invariant.

The final choice must be justified against Putnam's original P06 definition before canonical merge.

## EAVS role
EAVS 2004+ is an official validation/robustness source, not automatically the strict P06 continuation.
Store EAVS-derived turnout separately until denominator equivalence is established.

## Panel representation
Observed presidential-election years only.
No interpolation into 2001-2003, 2005-2007, etc.
For models needing an annual panel, P06 may enter as an observed-wave covariate or election-cycle measure; it must not be forward-filled and relabeled as annual observation.

## Validation
- 50 states; DC excluded.
- six election waves expected.
- exact numerator/denominator metadata.
- state-year uniqueness.
- missingness explicit.
- source vintage and acquisition hash.
