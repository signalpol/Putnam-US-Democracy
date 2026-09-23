# Democracy DV — SDI 2.0 Canonical Specification v1.0
Date: 2026-09-23

## Official source
UC Berkeley Democracy Policy Lab — State Democracy Index 2.0.
Official page states coverage is all 50 U.S. states, 2000-2023.
Official CSV endpoint identified as SDI_2.0.csv.

## Canonical variables
Primary DV:
- democracy_mcmc — Electoral Democracy Score; official codebook identifies this as the main measure used in the paper.

Uncertainty retained:
- democracy_mcmc_sd — posterior standard deviation.
- democracy_mcmc_se — posterior standard error.

Robustness DV:
- democracy_additive — alternative additive Electoral Democracy Score.

## Required acquisition validation
After binary/CSV acquisition:
1. verify 50 states;
2. verify years 2000-2023;
3. verify 1,200 unique state-year keys;
4. verify zero duplicate state-year keys;
5. inspect missingness in democracy_mcmc;
6. preserve posterior uncertainty fields;
7. inspect scale/direction and codebook;
8. retain additive index for robustness;
9. archive raw file unchanged and record hash.

## National aggregation rule
The SDI is a state-level democracy measure. A national series derived from it is not automatically equivalent to total U.S. democracy.

Construct at minimum:
- equal-state mean of democracy_mcmc by year;
- population-weighted mean by year.

Compare these against an independent national democracy series (planned: V-Dem). Divergence must be reported rather than averaged away.

## Anti-circularity implication
Because the SDI captures electoral democracy, social-capital indicators that directly measure electoral/political participation (especially P06 presidential turnout and P07 public meeting participation) require sensitivity analyses excluding them from the social-capital predictor. This reduces mechanical conceptual overlap between predictor and outcome.

## Status
SOURCE AND COVERAGE VERIFIED.
RAW CSV ENDPOINT VERIFIED.
RAW FILE NOT YET INGESTED/READ-BACK IN REPOSITORY.
No numerical DV results are claimed until acquisition and validation are completed.
