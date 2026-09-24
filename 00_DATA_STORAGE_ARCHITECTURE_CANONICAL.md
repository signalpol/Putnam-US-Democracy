# DATA STORAGE ARCHITECTURE — CANONICAL
Date: 2026-09-24

## Purpose
Prevent mixing, accidental overwrite, silent transformation, and loss of data used in the Putnam U.S. Democracy Project.

## Separation rule
The project uses three distinct data layers. A file may never silently move between layers.

### 1. RAW — immutable source data
Path: `04_Raw_Data/`
Store source files exactly as acquired. Never edit values in place.
Organize by substantive block and source:
- `04_Raw_Data/S_Social_Capital/`
- `04_Raw_Data/E_Economic/`
- `04_Raw_Data/D_Democracy/`
Existing historical Putnam raw files remain valid in their existing provenance-preserving location; new acquisitions follow this structure.

Each acquisition must have: source institution, source URL/identifier, acquisition date, original filename, coverage, SHA-256 where bytes are available, and access/processing notes.

### 2. PROCESSED — reproducible transformations only
Path: `02_Putnam_14_Variables/` for canonical Putnam-variable products and source-specific processed outputs; economic and democracy processed products must be clearly prefixed E_ and D_ or placed in dedicated subdirectories as the repository evolves.
No manual undocumented value changes.
Every processed dataset must identify its raw parent(s) and transformation script/version.

### 3. ANALYTIC — merged analysis-ready products
Path: `03_Master_Panel/`
Only validated, explicitly versioned merged datasets belong here.
Never use this directory as raw-data storage.
Every master-panel release must record input file versions/hashes, builder script, row/state/year validation, missingness, and creation date.

## Provenance and audit
Path: `05_Audit_Provenance/`
Maintain acquisition manifests, equivalence audits, coverage audits, hashes, and validation reports.

## Code
Path: `06_Analysis/`
Collectors, validators, builders, and analysis scripts only. Code must not contain hand-entered replacement observations masquerading as acquired data.

## Literature
Path: `07_Literature/`
References, literature maps, full-text notes where legally stored, and manuscript-use evidence tables. Never mix literature-derived numbers with empirical datasets.

## Non-loss rules
1. RAW files are immutable.
2. No interpolation of canonical missing observations.
3. No proxy is promoted to a canonical Putnam variable without explicit equivalence approval.
4. Never overwrite a released master panel; increment version.
5. Preserve source identifiers and hashes so every analytic observation can be traced backward.
6. Failed or incomplete acquisitions remain documented but do not enter the analytic panel as observed data.
7. GitHub is the canonical version/provenance/code store; large/raw archival copies may also be retained in Google Drive. A Drive copy is not claimed unless upload and readback are verified.
8. Periodically mirror critical canonical files and manifests to the project Drive archive; user may additionally retain PC/USB backups.

## Variable-block naming
- `S_` = social capital
- `E_` = economic conditions
- `D_` = democracy
- `T_` = Trump-era/break/interaction variables constructed for analysis
Prefixes must be retained through processed and analytic layers to prevent semantic mixing.

## Merge gate
A dataset may enter `03_Master_Panel/` only after:
- source/provenance recorded;
- coverage checked;
- state/year keys validated;
- duplicates checked;
- missingness reported;
- transformations reproducible;
- variable block (S/E/D/T) explicit.

This file is the canonical storage rule for all subsequent data collection unless explicitly revised.
