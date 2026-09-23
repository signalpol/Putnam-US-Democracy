# Remaining Six Acquisition Update — Roper / DDB
Date: 2026-09-24

## P01 / P02 — Roper route upgraded to downloadable archive target

Official openICPSR project E100391V1 lists:
- Roper.sav
- SPSS SAV
- 117.4 MB
- updated cumulative Roper file 1973–2002
- file defined by the authors of The Unheavenly Chorus.

Roper Center independently confirms that the canonical 12-item battery separately contains:
- Served as an officer of some club or organization
- Served on a committee of some local organization

The openICPSR web parser currently fails when fetching the binary itself (cache miss), so the bytes have NOT been acquired or inspected in this environment.

Required inspection immediately after acquisition:
1. identify year/survey variables;
2. identify state identifier and weights;
3. identify separate committee and officer variables;
4. enumerate 2000–2002 observations for each item;
5. verify wording/coding continuity;
6. compute state estimates only where sample size/design are defensible.

Status:
P01 = EXACT ITEM + OFFICIAL 1973–2002 FILE LOCATED; BINARY INSPECTION PENDING.
P02 = EXACT ITEM + OFFICIAL 1973–2002 FILE LOCATED; BINARY INSPECTION PENDING.

## P11 / P12 / P14 — DDB public-replication search

Evidence continues to show:
- Putnam public archive exposes the historical DDB release (roughly through 1998/1999).
- Post-1998 DDB Life Style files existed and were used by academic researchers.
- Literature explicitly describes the post-1998 material as proprietary / not publicly released.
- A recent independent research effort reports inability to obtain 1999–2005 DDB files.

No lawful public replication copy of the 1999–2005 DDB microdata was located in this search pass.

Decision:
Do not spend repeated cycles searching the same Putnam public archive.
Proceed by (a) targeted author/institutional replication deposits, then (b) direct DDB academic request for only YEAR, STATE, WEIGHT, visfrd, enthome, honesty and design fields, or exact weighted state-year tabulations.

## Important methodological note
Historical DDB state estimates were based on accumulating annual national surveys; individual state samples in a single year can be small/nonrepresentative. Even if annual post-1998 microdata are acquired, do not automatically treat every state-year cell as a reliable observation. Report n/weights and pool years only under a pre-specified defensible rule.
