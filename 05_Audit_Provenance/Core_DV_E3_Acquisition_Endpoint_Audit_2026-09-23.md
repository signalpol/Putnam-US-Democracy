# Core DV / E3 Acquisition Endpoint Audit — 2026-09-23

## D1 — Berkeley State Democracy Index 2.0
Official Democracy Policy Lab page verified:
- coverage: all 50 states, 2000-2023;
- main variable: democracy_mcmc;
- uncertainty: democracy_mcmc_sd, democracy_mcmc_se;
- robustness: democracy_additive;
- official Download the Data link resolves to:
  https://democracypolicylab.berkeley.edu/wp-content/uploads/2025/01/SDI_2.0.csv

Current execution result:
- official CSV endpoint exists and returns text/csv;
- web parser refuses unsupported CSV content type;
- container direct download also failed in current environment;
- bytes NOT acquired;
- 1,200-key validation NOT yet executed.

Status: OFFICIAL ENDPOINT RESOLVED / RAW BYTES NOT YET ACQUIRED.

## E3a — BLS state unemployment
Official BLS LAUS time-series directory verified.
Current directory includes:
- la.data.2.AllStatesU (all-state unadjusted data);
- la.series metadata;
- state-specific files;
- current update timestamps in 2026.

Current execution result:
- directory and filenames readable;
- direct flat-file fetch is rejected by web parser as non-HTML/octet-stream and container download failed;
- numeric bytes NOT acquired.

Status: OFFICIAL FLAT-FILE ENDPOINT RESOLVED / RAW BYTES NOT YET ACQUIRED.

## E3b — Employment-population ratio
Official BLS CNP16+ page verified:
- 50 states + DC;
- monthly January 1976 forward;
- annual-average ZIP explicitly provided;
- current revised historical series is canonical for this project.

Status: OFFICIAL ANNUAL-AVERAGE ROUTE VERIFIED / RAW ZIP NOT YET ACQUIRED.

## Fail-closed rule
No D1/E3 numeric values may be labeled acquired until bytes are read and:
- 50 states;
- 2000-2023;
- 24 years;
- exactly 1,200 unique state-year keys per variable;
- zero duplicates;
- missingness audit;
- SHA-256 raw provenance
all pass.

## Next acquisition fallback
Use an execution environment with ordinary HTTPS file download (e.g. project Colab) against these now-resolved official endpoints. No further source discovery is required.
