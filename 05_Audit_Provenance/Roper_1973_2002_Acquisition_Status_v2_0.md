# Roper 1973–2002 Acquisition Status v2.0
Date: 2026-09-23

## Verified archive facts
Official openICPSR project E100391V1, The Unheavenly Chorus replication archive:
- contains Roper.sav;
- file type SPSS SAV;
- size 117.4 MB;
- deposited by Sidney Verba, Kay Lehman Schlozman, and Henry E. Brady;
- project documentation explicitly says it is an updated cumulative Roper file covering 1973–2002.

## Access test in current research environment
The project landing page and metadata are readable.
Direct file-view/download endpoint for Roper.sav returned a cache-miss/internal fetch error in the current web execution route.
The project-level download-terms endpoint also returned a cache-miss/internal fetch error.

Therefore:
- archive existence = VERIFIED;
- 1973–2002 coverage claim = VERIFIED FROM OFFICIAL ARCHIVE METADATA;
- binary Roper.sav acquired = NO;
- internal variables inspected = NO;
- 2000–2002 P01/P02/P07 observations = NOT VERIFIED;
- state identifier/weights/sample size = NOT VERIFIED.

## Strict anchor gate
Do not use any 2000–2002 Roper values until the SAV bytes are actually obtained and inspected.

Required inspection immediately after acquisition:
1. variable dictionary / labels;
2. survey-year/date variables and exact 2000–2002 cases;
3. P01 committee-service item;
4. P02 officer-service item;
5. P07 town/school public-meeting item;
6. state identifier and valid state coverage;
7. survey weights;
8. state-year unweighted n and effective n where calculable;
9. wording/coding continuity with Putnam source years;
10. missing/refusal codes.

## Next lawful acquisition routes
- openICPSR browser/manual project download;
- ICPSR/openICPSR authenticated download if required by interface;
- depositor-provided project archive.
No third-party copy should replace the official archive unless hash/provenance equivalence can be demonstrated.
