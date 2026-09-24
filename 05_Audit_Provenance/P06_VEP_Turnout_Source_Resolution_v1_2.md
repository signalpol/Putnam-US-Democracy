# P06 VEP Turnout Source Resolution v1.2
Date: 2026-09-24

## Resolved source
Canonical modern source: University of Florida Election Lab / Michael McDonald.
The Election Lab archive currently provides a 1980-2022 General Election Turnout Rates state time series, superseding the legacy U.S. Elections Project files.

## Canonical denominator
Voting-Eligible Population (VEP).
The Election Lab defines state VEP from voting-age population, subtracting ineligible noncitizens and disenfranchised felons according to state law. Eligible overseas voters are added only to national VEP because they cannot reliably be apportioned to states.

## Canonical P06 waves
Use the state VEP turnout rate for presidential general-election years:
2000, 2004, 2008, 2012, 2016, 2020.
Expected grid: 50 states x 6 waves = 300 observations.
Exclude DC and territories.

## Why this resolves the continuity problem
The current UF Election Lab archive provides one state general-election time-series framework spanning all six required waves. Separate 2016 and 2020 pages document the same VEP concept and components.
Therefore EAVS is no longer needed as the primary P06 source; retain it only as an official robustness/validation source.

## Remaining equivalence gate
Before calling this a strict Putnam continuation, compare the original Putnam P06 denominator/statistic with VEP. If original Putnam used VAP rather than VEP, preserve:
- P06_original_definition replication;
- P06_VEP modern continuity series;
and do not falsely label VEP numerically identical to the historical Putnam statistic.

## Storage
Raw UF Election Lab files:
04_Raw_Data/S_Social_Capital/STRICT/P06_TURNOUT/UF_ELECTION_LAB/
Processed six-wave file:
S1_P06_VEP_50states_2000_2020_presidential_waves.csv
Manifest records dataset version, download date, hashes, state exclusions, and exact source fields.

## No interpolation
P06 exists only in observed presidential-election waves. Never interpolate or forward-fill it into intervening years.
