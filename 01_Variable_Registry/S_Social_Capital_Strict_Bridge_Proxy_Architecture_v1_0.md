# Social-Capital Strict vs Bridge Data Architecture v1.0
Date: 2026-09-24

## Purpose
Prevent unavailable Putnam-original state series from being silently replaced by similar modern measures.

## Layer S0 — Historical Putnam baseline
Source: original StateMeasures.txt and its exact 14 components.
Role: historical 50-state benchmark / construct anchor.
Never rewrite or impute original missing cells.

## Layer S1 — Strict continuation
Only observations satisfying the canonical equivalence audit:
same construct + same question/behavior + same statistic, with state geography and documented weighting/sample rules.

Current difficult variables:
- P01 committee service: Roper exact lineage; public Roper SPT ends 1994. Post-1994 RoperASW/GfK continuation is proprietary unless lawfully acquired.
- P02 officer service: same rule.
- P11 visiting friends: DDB Needham exact lineage.
- P12 entertained at home: DDB Needham exact lineage.
- P13 generalized trust: GSS TRUST is exact/near-exact national lineage; state geography requires sensitive/geocoded access and must not be inferred from public region.
- P14 most people honest: DDB Needham exact lineage.

Unavailable strict state-years remain missing. No interpolation.

## Layer S2 — Measurement bridge / validation
2000 and 2006 Social Capital Community Benchmark Surveys (SCCBS) are stored separately from S1.
They are NOT a 50-state panel and must never be merged as if they represent all states.

Permitted roles:
1. national measurement bridge;
2. repeated-community/state validation where geography genuinely supports it;
3. item-equivalence and measurement-invariance tests;
4. comparison of strict Putnam constructs with later civic-engagement measures.

Verified bridge examples from official codebooks:
- P07-like public meeting attendance: CPUBMEET / PUBMEET / PUBMEET2 family.
- P10-like volunteer frequency: CVOLTIME / VOLTIMES / VOLTIME2 family.
- informal sociability items exist, but must not be relabeled P11/P12 without wording/statistic equivalence.
- trust batteries exist, but must not be relabeled canonical P13 unless the exact generalized-trust wording/statistic passes audit.

2000 SCCBS design:
national sample ~3,000 plus ~26,700 respondents in 42 communities across 29 states.
Geographically sensitive fields such as FIPS are restricted.

2006 SCCBS design:
national sample 2,741 plus 9,359 respondents in 22 community samples (total 12,100).
No restricted dataset is listed by Roper for 2006; free registration is required for data download.

## Layer S3 — Modern continuation/proxy
Modern civic, volunteering, sociability, trust, nonprofit, or association measures that fail strict equivalence belong here.
They may support robustness or construct validation but cannot be promoted into P01-P14 canonical series.

## Storage
- raw strict-source files: 04_Raw_Data/S_Social_Capital/STRICT/
- raw bridge files: 04_Raw_Data/S_Social_Capital/BRIDGE_SCCBS/
- raw modern/proxy files: 04_Raw_Data/S_Social_Capital/MODERN_PROXY/
- all acquisition/equivalence manifests: 05_Audit_Provenance/
- processed outputs retain S1_/S2_/S3_ prefixes.

## Merge rule
Only S1 variables can populate canonical P01-P14 state-year fields.
S2 and S3 must remain separately named columns/tables and cannot fill S1 missing values.

## Research consequence
The empirical study can use an unbalanced strict Putnam panel, separate dimensional indicators, and bridge/proxy robustness without fabricating annual continuity. Missingness is a property of the evidence, not a value to be repaired silently.
