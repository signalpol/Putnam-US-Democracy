# S DATASET COMPLETION AUDIT — 2000–2023
Date: 2026-09-25
Rule: no interpolation, no synthetic splicing, no statistical test.

## Numerically stored canonical S
- Master: 03_Master_Panel/S_Social_Capital/S_SOCIAL_CAPITAL_MASTER_OBSERVED_50states_2000_2023_v1.csv
- Total state-year skeleton: 1200
- Hawes/Compton observed cells: 528; years 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010
- CEV state formal-volunteering observed cells: 200; years 2017, 2019, 2021, 2023
- CEV master contains 17 separate state-level civic indicators for 2017/2019/2021/2023.

## Verified additional annual S2 source
CPS Volunteer / VCLA contains annual state-level volunteer rates for 50 states + DC for every year 2002–2015: 51 geographies × 14 years = 714 entries.
Definition reported in the published data description: share answering yes to the past-12-month organizational volunteering item.
Primary provenance: Census CPS Volunteer Supplement / AmeriCorps VCLA.
Independent published verification: Ng & Cheung (2023), British Journal of Psychology 114:945–968, DOI 10.1111/bjop.12669.

## Current ingestion status
The 714-value S2 numeric table is NOT yet copied into this repository. The Census microdata API currently requires an API key, and the legacy AmeriCorps VCLA annual table is not exposed as a directly retrievable file through the connected GitHub/Census interfaces in this session. Do not label S2 numeric ingestion complete until the 714 values are actually committed.

## Measurement break
2002–2015 Volunteer and 2017+ CEV cannot be silently concatenated. Published methodological discussion notes wording/sequencing changes beginning in 2017. Preserve as S2 and S3.

## Completion criterion
S is numerically complete for the intended multi-family architecture only after:
1. 714 S2 state/DC-year volunteer rates are committed;
2. state-only 700 rows are mapped to 50-state master;
3. source vintage and definition are attached;
4. no gaps are fabricated for 2000–01, 2016, 2018, 2020, 2022.
