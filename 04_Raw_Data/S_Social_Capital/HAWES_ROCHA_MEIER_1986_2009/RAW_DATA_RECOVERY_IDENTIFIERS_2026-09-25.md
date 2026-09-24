# Hawes numeric raw-data recovery — additional exact identifiers (2026-09-25)

## Newly verified
DataCite historical DOI-resolution logs contain both:
- 10.15139/S3/SMKJFZ
- 10.15139/S3/SMKJFZ.DTA

This is strong evidence of a legacy direct Stata-data DOI/identifier in addition to the study-level DOI.

ResearchGate publicly lists three supplementary resources for Hawes (2017):
- HawesSPPQ ReplicationData
- HawesSPPQ ReplicationFile V2
- HawesSPPQ Codebook V2

CauSciBench independently documents a converted dataset named:
- hawes_social_capital.csv
and identifies:
- entity key: statename
- time key: year
- social-capital field: SC8609_ma
- study period: 1986–2009

## Retrieval attempts in current environment
Direct requests to legacy Dataverse datafile endpoint, DOI .DTA endpoint, and Hugging Face file tree are blocked by the current retrieval layer. These are transport/access-path failures, not evidence that the public data are unavailable.

## Rule
Do not reconstruct or fabricate the 1,296 SC8609_ma values from summary statistics. Preserve the authors' or faithful public derivative numeric bytes when retrieved.
