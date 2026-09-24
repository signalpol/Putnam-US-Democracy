# Social Capital Acquisition Status — v1.0

Date: 2026-09-24

This is an execution-status ledger, not a claim of completed data.

| ID | Putnam construct | Strict S1 status | Canonical treatment |
|---|---|---|---|
| P01 | Committee Service | Roper source identified; raw not acquired | missing until raw microdata validated |
| P02 | Officer Service | Roper source identified; raw not acquired | missing until raw microdata validated |
| P03 | Civic & Social Organization Density | CBP collector exists; population denominator collector remains scaffold | do not claim 2000-2023 density yet |
| P04 | Club Meetings | strict continuation unresolved | missing |
| P05 | Group Membership | strict continuation unresolved | missing; legacy/proxy quarantined |
| P06 | Presidential Turnout | UF Election Lab collector exists for 2000/04/08/12/16/20 | election-wave only; equivalence to original Putnam denominator remains a gate |
| P07 | Public Meeting Attendance | strict continuation unresolved | missing; exclusion sensitivity required |
| P08 | Nonprofit Organization Density | observed NCCS/IRS BMF snapshot collector exists; 2017/2021 unresolved | observed snapshots only; no interpolation |
| P09 | Community Project | strict continuation unresolved | missing |
| P10 | Volunteer Work | strict continuation unresolved | missing |
| P11 | Visiting Friends | DDB post-1998 public microdata unresolved | missing |
| P12 | Entertain at Home | DDB post-1998 public microdata unresolved | missing |
| P13 | Generalized Trust | GSS TRUST available nationally; state geocode restricted | do not infer state from public region |
| P14 | Perceived Honesty | DDB post-1998 public microdata unresolved | missing |

## Non-negotiable rules

1. S0 historical Putnam baseline is retained as historical baseline, not annual 2000-2023 data.
2. Only S1 strict continuation can populate canonical P01-P14 fields.
3. S2 bridge and S3 modern proxy variables remain separately named and cannot fill S1 gaps.
4. No interpolation.
5. P06 remains election-wave data; no annual interpolation.
6. P08 uses only observed BMF snapshots; unresolved years remain missing.
7. A script existing is not evidence that its numeric output has been acquired.
