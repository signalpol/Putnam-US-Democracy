# Core Economic Raw Acquisition Status — 2026-09-23

## E1 / E5 — BEA
Verified:
- BEA publishes downloadable CSV archives for Regional Economic Accounts.
- Official API Regional example specifies real GDP for all states/all years as TableName=SAGDP9N, LineCode=2, GeoFips=STATE, Year=ALL.
- BEA GDP-by-state source includes industry contributions and downloadable data.
- 2026 BEA update documentation states the Regional Economic Accounts provide state GDP and state personal income in a consistent national/regional accounting framework.

Execution attempt:
- Attempted direct retrieval of the BEA Regional SAGDP ZIP from the current execution container.
- Failed before HTTP retrieval because the container could not resolve apps.bea.gov (DNS temporary failure).
- Therefore no BEA numeric raw file has been ingested and no E1/E5 panel is claimed complete.

Disposition:
NETWORK-BLOCKED-IN-CURRENT-CONTAINER, NOT DATA-UNAVAILABLE.
Keep official API/ZIP route as primary acquisition route in a network-enabled runtime.

## E3 — BLS
Verified from official annual releases:
- BLS annual state release contains both state unemployment rates and employment-population ratios.
- Population concept: civilian noninstitutional population age 16+.
- 2023 official release provides 2022-2023 state values.
- Historical official releases located for 2010, 2015, and 2020, confirming the same annual state architecture across the study period.
- 2020 release states all state employment-population-ratio series begin in 1976.

Important provenance note:
BLS annual releases state that subnational data reflect revised population controls/model re-estimation. Therefore a single current/revised historical series is preferable to mechanically concatenating publication-vintage annual news-release tables. News-release tables are validation anchors, not the preferred final raw panel if a consistent current series is available.

## Next acquisition order
1. Obtain current BLS historical state series for E3a/E3b and validate 1,200 keys.
2. Retry BEA Regional ZIP/API in network-enabled runtime for E1/E5.
3. Acquire E2b BEA PCPI using the same vintage as other BEA regional data where possible.
4. Preserve all raw files and hashes before transformation.
