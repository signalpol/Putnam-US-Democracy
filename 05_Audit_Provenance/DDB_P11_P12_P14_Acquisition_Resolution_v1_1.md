# DDB P11/P12/P14 Acquisition Resolution v1.1
Date: 2026-09-24

## What is now verified

### Putnam public original microdata
Robert Putnam's Bowling Alone research distribution explicitly states that the DDB Life Style archive is downloadable for scholarly/academic fair use under DDB Worldwide copyright.
Coverage stated by the distribution: 1975-1998.
Unweighted N: 84,989.
Formats listed: tab-delimited, portable SPSS, SPSS v9 for Windows, plus a data dictionary.
This is the canonical historical S1 microdata source for P11/P12/P14 and must be preserved separately from StateMeasures.txt.

### Exact variables
P11: VISFRD — agreement with "I spend a lot of time visiting friends."
P12: ENTHOME — frequency/number of times entertained people in home in prior 12 months.
P14: MOSTHON / corresponding DDB honesty item — agreement that "Most people are honest"; exact machine variable name must be confirmed from the acquired dictionary/microdata before extraction.

The released DDB dictionary contains YEAR, WEIGHT and STATE among its 389 variables, enabling replication of historical state aggregation after exact coding inspection.

### Evidence of later DDB waves
Published research independently demonstrates that the DDB Life Style survey continued beyond the Putnam public 1975-1998 archive:
- later scholarly work uses DDB Life Style data through 2005;
- published figures based on VISFRD and ENTHOME extend into the 2000s.
This establishes continuation of the survey/items as an evidence lead, but NOT public availability or state-year coverage.

## Strict acquisition split

### S1A — Putnam public historical DDB
Acquire the 1975-1998 public microdata from Putnam's research distribution.
Store immutable raw bytes under:
04_Raw_Data/S_Social_Capital/STRICT/P11_P12_P14_DDB/PUTNAM_1975_1998/
Record copyright/access note, original filename, byte size and SHA-256.
Extract P11/P12/P14 only after dictionary-based code verification.

### S1B — Post-1998 DDB continuation
Treat 1999+ as a separate acquisition object.
Priority:
1. author replication deposits using 1999-2005 DDB;
2. institutional repositories;
3. direct scholarly request to authors/DDB successor/rightsholder;
4. exact state-year tabulations if microdata cannot be released.

Do not merge S1A and S1B until wording, coding, weights, geography, sample design and state variable continuity are audited.

## Important non-claims
- Evidence that an author used data through 2005 does NOT mean those microdata are publicly downloadable.
- A figure extending to 2005 is not a substitute for microdata.
- No 2000-2023 50-state DDB panel is currently claimed.
- No values may be reconstructed from plotted figures or regression coefficients.
- Modern proxy questions cannot fill P11/P12/P14 strict missing cells.

## Extraction requirements
For each strict DDB variable:
- exact item wording
- response codes
- YEAR
- STATE coding
- WEIGHT
- valid/missing codes
- unweighted and weighted state-year N
- aggregation statistic matching Putnam
- observed-year coverage
- raw SHA-256 and extraction-code version

## Research implication
The original historical state index can be replicated from individual DDB microdata once acquired, strengthening measurement validation. Later DDB waves may extend P11/P12/P14 into the early 2000s, but this remains an acquisition task rather than an observed-data claim.
