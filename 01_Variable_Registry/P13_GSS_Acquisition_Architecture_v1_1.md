# P13 GSS Acquisition Architecture v1.1
Date: 2026-09-24

## Canonical construct
P13 = generalized trust:
"Generally speaking, would you say that most people can be trusted or that you can't be too careful in dealing with people?"
Canonical statistic: percent selecting "most people can be trusted" among valid responses, using the appropriate GSS weight.

## Public national series — S1-NATIONAL
Official source: NORC General Social Survey cumulative cross-sectional data.
Current official cumulative release: GSS 1972-2024 Cross-Sectional Cumulative Data, Release 3a (July 2026).
Relevant study-period survey years available publicly include 2000, 2002, 2004, 2006, 2008, 2010, 2012, 2014, 2016, 2018, 2021, 2022 (and 2024 outside the canonical 2000-2023 endpoint).

Use exact TRUST trend variable where the current GSS release designates it as the trend-compatible variable.
For 2021/2022 multi-mode variants, preserve mode/version variables and conduct mode-sensitivity analysis; do not silently pool changed wording/modes into the historical series.

National P13 is irregular-wave data. Never interpolate non-survey years in the strict series.

## State series — S1-STATE-RESTRICTED
NORC explicitly states that geocoded data such as states and counties require GSS Sensitive Data access because of deductive-disclosure risk.
Therefore:
- public GSS REGION must NOT be reverse-engineered into states;
- no state-level P13 is claimed from the public cumulative file;
- state estimates require approved sensitive/geocoded access or an independently lawful exact-question state source.

## Empirical roles
1. P13 national GSS trend can enter national social-capital dimensional analysis on observed survey years.
2. P13 state strict panel remains missing until restricted access is obtained.
3. S2/S3 trust proxies may be used only under separate names for robustness/measurement validation.
4. Never fill state P13 with national P13.

## Storage
Public raw GSS file, if redistribution terms permit: 04_Raw_Data/S_Social_Capital/STRICT/P13_GSS/NATIONAL/
Restricted state/geocode file: private controlled storage only; never public GitHub.
Derived national annual-wave estimates: processed S1_P13_GSS_NATIONAL with provenance/weight/mode metadata.
Derived approved state estimates: processed S1_P13_GSS_STATE_RESTRICTED.

## Required validation after bytes acquired
- raw SHA-256
- release/version
- TRUST labels/codes
- valid-response denominator
- weight used
- survey year
- mode variables for 2021/2022+
- weighted N / unweighted N
- estimate and uncertainty
- no interpolation
