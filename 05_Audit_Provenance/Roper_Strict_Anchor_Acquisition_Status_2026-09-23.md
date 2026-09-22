# Roper Strict Anchor Acquisition Status — 2026-09-23

## Verified
openICPSR project E100391V1, The Unheavenly Chorus replication archive, contains:
- Roper.sav
- SPSS SAV format
- 117.4 MB
- cumulative Roper file defined by the book authors
- archive description explicitly identifies it as an updated Roper file covering 1973-2002.

The Roper Center documents the original Social and Political Trends battery and explicitly lists:
- served as an officer of some club or organization;
- served on a committee of some local organization;
- attended a public meeting on town or school affairs.

These map directly to strict Putnam P02, P01, and P07 constructs respectively.

## Current acquisition status
The archive's browser file endpoint for Roper.sav was identified, but direct binary retrieval through the current web retrieval path failed (cache/fetch failure). Therefore:
- Roper.sav has NOT yet been downloaded into the working environment.
- variable labels, state identifier, weights, and exact 2000-2002 item availability have NOT yet been inspected.
- no state estimates from Roper 2000-2002 are claimed.

## Next validation gate
Before promoting P01/P02/P07 to canonical 2000-2002 observations, verify inside Roper.sav:
1. survey/year identifiers include 2000, 2001 and/or 2002;
2. exact participation battery variables continue in those waves;
3. state identifier is available and sufficiently populated;
4. survey weights are available and appropriate;
5. sample sizes permit defensible state estimates;
6. wording/coding did not change.

Until all six pass, status remains CANDIDATE_STRICT_ANCHOR, NOT ACQUIRED.
