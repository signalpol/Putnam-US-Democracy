# E4/E5 Canonical Specification v1.0
Date: 2026-09-23

## E4 — State income inequality

### Verified source architecture
1. U.S. Census Historical Income Tables: States, Table S4:
   state Gini ratios for 1969, 1979, 1989, 1999.
2. American Community Survey Detailed Table B19083:
   Gini Index of Income Inequality, household universe, modern ACS period.

### Canonical rule
Do NOT manufacture a seamless 2000-2023 Gini series by:
- copying the 1999 decennial value into 2000;
- interpolating 1999 to the first ACS year;
- silently splicing estimates from different survey designs.

### E4 variables
E4a_gini_1999_anchor:
- historical Census state Gini.
- pre-period baseline/context only unless a model explicitly uses baseline inequality.

E4b_acs_gini:
- ACS B19083 state household Gini.
- use only years with verified comparable ACS estimates.
- retain estimate and margin of error when available.

### Analysis use
Primary full-period models may omit E4 where annual comparable data are unavailable.
Use E4a as baseline structural inequality and E4b in ACS-era restricted-period models.
Any bridge model must be separately justified and reported as robustness, never canonical raw data.

## E5 — Structural economic change

### Official source
BEA GDP by State, industry detail.
BEA methodology covers state GDP by industry for 1997-2023 on the NAICS-era framework.
Manufacturing is NAICS 31-33.

### Canonical variables
E5a_manufacturing_share_current:
  current-dollar manufacturing value added / current-dollar total state GDP * 100.
This is the preferred structural-composition share because numerator and denominator are additive current-dollar value-added concepts.

E5b_manufacturing_real_growth:
  growth of real manufacturing value added, analyzed separately.
Do not compute a 'real GDP share' by dividing chain-dollar components unless BEA additivity guidance supports that operation.

Optional later extensions:
- goods-producing share;
- finance/professional-services share;
- industry concentration/diversification index,
only after the manufacturing-share core measure is validated.

### Study-period continuity
Because the canonical period begins in 2000, the 1997 SIC-to-NAICS discontinuity precedes the study window. Use a single current BEA vintage covering 2000-2023 and document later NAICS revisions/BEA revisions.

## Validation gates
E4:
- identify first comparable ACS annual year;
- verify all 50 states;
- preserve MOE;
- document survey/design changes.

E5:
- verify total GDP and manufacturing industry line codes/table;
- 50 states x 24 years = 1,200 expected keys;
- confirm units;
- calculate current-dollar manufacturing share;
- inspect missingness;
- archive raw vintage and hash.

## Status
E4: DUAL-SERIES DESIGN FIXED; annual 2000-2023 seamless series REJECTED unless future evidence establishes comparability.
E5: SOURCE / INDUSTRY CONCEPT / PERIOD CONTINUITY VERIFIED; numeric panel acquisition pending.
