# P01-P02 Roper.sav Binary Acquisition Gate v1.1
Date: 2026-09-24

## Verified public object
Repository: openICPSR project E100391V1, The Unheavenly Chorus (2012)—Replication Archive.
File: Roper.sav
Type: SPSS SAV
Displayed size: 117.4 MB.
Archive description explicitly states that the source includes Roper Social and Political Trends 1973-1994 and an updated cumulative Roper file 1973-2002, and that the cumulative file is in the archive.

## Current execution result
The official project/file page is reachable and the Roper.sav object is enumerated.
Direct binary retrieval from the current web execution environment returns a cache-miss/fetch failure.
This is an acquisition-environment failure, NOT evidence that the file is unavailable.

Status:
- object existence: VERIFIED
- public archive metadata: VERIFIED
- 1973-2002 description: VERIFIED
- raw bytes in project storage: NOT ACQUIRED
- SHA-256: NOT AVAILABLE until bytes acquired
- P01/P02 numeric extraction: NOT EXECUTED

## Next executable route
In an environment capable of ordinary binary download:
1. Download Roper.sav from openICPSR E100391V1.
2. Save immutable raw bytes under:
   04_Raw_Data/S_Social_Capital/STRICT/P01_P02_ROPER/
3. Record original filename, project DOI/ID, acquisition timestamp, byte size and SHA-256.
4. Run 06_Analysis/extract_p01_p02_from_roper_sav.py.
5. Inspect variable labels before accepting any candidate mapping.
6. Verify exact committee/officer wording, YEAR, state identifier, weights, valid-response coding and state-year sample sizes.
7. Produce P01/P02 estimates only for genuinely observed state-years.
8. Never interpolate or extend beyond the archive's actual survey years.

## Public-repository rule
Before committing raw Roper.sav to public GitHub, verify redistribution terms for the deposited file. If uncertain, archive raw bytes in project Drive/private storage and commit only provenance, hashes, code and permitted derived statistics.

## Merge gate
P01/P02 values may enter canonical S1 fields only after the extraction audit passes. Until then all P01/P02 post-baseline cells remain missing.
