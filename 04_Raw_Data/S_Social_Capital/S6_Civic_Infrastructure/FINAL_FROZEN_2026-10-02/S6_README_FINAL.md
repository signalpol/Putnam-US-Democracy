# S6 Civic Infrastructure — final analytical series

RUN_ID: S6_CBP_DENSITY_20261002_v1

1,200rows,50states,2000–2023. Unit: NAICS813410 employer establishments per1,000residents. Every row is DIRECT with model_estimated=0. RAW counts are preserved. CanonicalCSV provides count, population, populationvintage, NAICSversion, flags and cellprovenance;XLSX repeats the complete canonical fields plus QA/method tabs.

## Reproduction
Extract the replicationZIP and run `python build_s6.py --inputs inputs --output reproduced`. Python3 standardlibrary only. Locked original population files and inheritedRAW/API responses are embedded. The five deterministic analytical/source CSVs were rerun and hashmatched. Runmetadata timestamps vary legitimately. `audit_sources.py` performs the independent officialZIP countcomparison from the24ZIP inputs documented in CBP_OFFICIAL_ACQUISITION.json; download those sources to inputs/cbp_official first for the independent acquisition audit. It is not needed to reproduce the canonical density from packaged locked inputs.

To regenerate XLSX, install@oai/artifact-tool and run `node build_workbook.mjs <workroot>` after build_s6.py has written workbook_data.json. No surveySE/CI is fabricated for an administrative rate. Statistical/nonsampling limitations and denominator/NAICS boundaries are in the measurementaudit.

SHA256SUMS checks all embedded package members except itself. The outerZIP hash and GitHub/Drive verification are recorded outside the ZIP to avoid self-referential hashes. GitHub stores native CSV/MD/scripts/XLSX and the complete native replicationZIP; source inputs are inside that ZIP. Existing RAW files and S1–S4 were not modified. GitHub Actions were not invoked.
