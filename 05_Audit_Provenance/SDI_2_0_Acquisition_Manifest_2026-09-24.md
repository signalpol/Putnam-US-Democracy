# SDI 2.0 Acquisition Manifest — 2026-09-24

## Dataset
State Democracy Index 2.0 (SDI 2.0)

## Canonical publisher
UC Berkeley Democracy Policy Lab.
Official landing page states coverage is all 50 U.S. states, 2000–2023, and defines:
- democracy_mcmc: main Electoral Democracy Score
- democracy_mcmc_sd: posterior SD
- democracy_mcmc_se: posterior SE
- democracy_additive: alternative additive score

Official CSV endpoint identified:
https://democracypolicylab.berkeley.edu/wp-content/uploads/2025/01/SDI_2.0.csv

The current tool environment could identify but not directly ingest the official CSV because of CSV MIME/download restrictions.

## Acquired bytes
Public GitHub mirror:
haomeng797-ship-it/dem-crime-equity/data/raw/SDI_2.0.csv
Source blob SHA: 9235fa971c908996819896fa8848541df0c310c1

Local canonical-project path:
04_Raw_Data/Democracy/SDI_2.0_public_mirror.csv

## Structural validation
- rows: 1,200
- states: 50
- years: 24
- year range: 2000–2023
- unique state-year keys: 1,200
- duplicate state-year keys: 0
- rows with missing fields: 0
- schema: st, state, year, democracy_mcmc, democracy_mcmc_sd, democracy_mcmc_se, democracy_additive

## Provenance status
ACQUIRED_FROM_PUBLIC_MIRROR; STRUCTURALLY_VALIDATED.
The mirror schema and coverage match the official Berkeley SDI 2.0 codebook/landing page. It must remain labeled as a public mirror until byte-level identity with the official Berkeley CSV is verified.

## Analysis rule
Use democracy_mcmc as primary state-year democracy DV; preserve SD/SE; democracy_additive is robustness measure.
