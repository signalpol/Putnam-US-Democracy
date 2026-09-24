# S Social Capital Master — Canonical Observed Panel v1

Date: 2026-09-25
Unit: U.S. state-year
Canonical grid: 50 states x 2000–2023 = 1,200 rows
Rule: NO INTERPOLATION / NO IMPUTATION / NO SILENT SPLICING

## Purpose
This file organizes the social-capital evidence currently acquired for the Putnam U.S. Democracy Project on one canonical state-year grid. It does not force conceptually or methodologically distinct series into a single synthetic index.

## Series A — Hawes/Compton
Variable: `S_HAWES_COMPTON_socap_ma`
Source artifact: `SPPQ-15-0108_replication.dta`
Definition in replication codebook: Social Capital, 3-year moving average.
Observed in project window: 2000–2010.
Geography: contiguous 48 states; Alaska and Hawaii remain NA.
Observed project-window cells: 48 x 11 = 528.
Important: this is the Hawes-family longitudinal index used in Compton's replication data. It is not decomposed into the original proprietary component items.

## Series B — CPS Civic Engagement and Volunteering (CEV)
Source artifact: `2017-23_CEV_StateRates_AllMeasures.xlsx`
Observed waves: 2017, 2019, 2021, 2023.
Geography used: 50 states; District of Columbia excluded from the canonical 50-state grid.
Observed state-year rows: 50 x 4 = 200.
Indicators retained separately: 17 observed state rates, including formal volunteering, organizational membership, charitable giving, informal helping, social interaction, issue learning/discussion, online expression, local voting, contacting officials, political donations, public meeting attendance, neighborhood collective action, buycotting/boycotting, and employer promotion of volunteering (available only in later waves).

## Connection rule
Hawes/Compton and CEV are placed on the same state-year grid but are NOT numerically spliced. `S_source_hawes_compton` and `S_source_cev` identify provenance. `S_observed_any` marks rows with at least one observed S source.

The project therefore preserves two empirically observed social-capital regimes:
1. historical longitudinal Hawes-family index for 2000–2010;
2. modern CPS/CEV behavioral indicators for 2017, 2019, 2021, and 2023.

Years without an observed compatible source remain missing. No value is created for 2011–2016, 2018, 2020, or 2022 in v1.

## Adoption rule
No new composite CEV index is designated as the study's final S variable in v1. Construction/adoption of a modern composite is a substantive model decision reserved for the principal investigator. The stored panel preserves all observed components needed for that decision.