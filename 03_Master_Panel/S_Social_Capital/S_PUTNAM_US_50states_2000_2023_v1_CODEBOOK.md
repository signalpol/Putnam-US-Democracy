# Putnam U.S. Social Capital Index v1 — 50 States, 2000–2023

## Scope
50 states × 24 years = 1,200 state-year observations.

## Construction
1. 2000–2010, contiguous 48 states: Hawes/Compton `socap_ma` benchmark observations.
2. Modern behavioral/structural block: P01 public meeting, P02 group membership, P03 volunteering, P04 community activity, P06 nonprofit density. Each component is standardized cross-sectionally within year; the row score is the mean when at least 3 components are observed.
3. Modern score is placed on the Hawes/Compton scale using the 2010 overlap across contiguous states. Calibration: `S = 0.20842116 + 0.59651786 * modern_raw_z`; overlap correlation r=0.590613, R²=0.348824, N=48.
4. 2011–2023 years with ≥3 observed modern components are `HARMONIZED_OBSERVED`.
5. Alaska/Hawaii 2000–2010 lack Hawes observations; values are model-estimated by applying the 48-state Hawes annual mean movement to each state's 2010 calibrated anchor.
6. Remaining unmeasured internal years (principally 2016/2018/2020/2022) are linear temporal bridges between that state's nearest measured anchors and are explicitly `MODEL_ESTIMATED`. They are not raw observations.
7. P05 presidential turnout is preserved but excluded from the annual core index to avoid mechanically imposing a four-year election cycle on annual S. It is available for robustness.

## Status counts
- OBSERVED_BENCHMARK: 528
- HARMONIZED_OBSERVED: 450
- MODEL_ESTIMATED: 222

## Regime counts
- HAWES_COMPTON: 528
- CPS_CEV_PLUS_NONPROFIT: 450
- TEMPORAL_BRIDGE_BETWEEN_MEASURED_ANCHORS: 200
- AK_HI_BACKCAST_NATIONAL_HAWES_TREND: 22

## Integrity rule
`OBSERVED_BENCHMARK`, `HARMONIZED_OBSERVED`, and `MODEL_ESTIMATED` must never be conflated. Primary hypothesis tests should report robustness excluding model-estimated rows. No E or D variable was used to construct S.
