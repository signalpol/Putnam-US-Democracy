# S -> D Temporal Link Test — Putnam U.S. Democracy Project
Date: 2026-09-25

## Question
Does variation in social capital precede and predict variation in state democracy, completing the proposed E -> S -> D chain?

## Canonical input
03_Master_Panel/Putnam_US_Democracy_ESD_FERRAGINA_MASTER_v1.csv
Git blob: f68f77aa1fe0102e66bdbb7f05e1a4d3c6349926

## Test 1: Within-state lagged panel
Model: D_it = beta*S_i,t-1 + state FE + year FE.
S: Hawes/Compton 3-year moving-average social-capital index.
D: Berkeley State Democracy Index 2.0 (democracy_mcmc).
Sample: 48 contiguous states, 11 S years, N=528.
Result: beta = +0.060926; state-clustered SE = 0.063293; t = 0.963; p ≈ 0.336.
Interpretation: positive sign, but no statistically reliable evidence that within-state year-to-year changes in S precede changes in D.

## Test 2: Ferragina-compatible cross-sectional temporal bridge
Predictor: each state's mean S over 2006-2010.
Outcome: each state's mean D over 2011-2023.
Sample: 48 contiguous states.
Bivariate OLS: beta = +0.767858; SE = 0.137417; t = 5.588; p < 0.000001.
Interpretation: states with higher pre-2011 social capital have substantially higher subsequent democracy levels.

## Test 3: Future D controlling Ferragina E block
Outcome: mean D, 2011-2023.
Predictors measured as 2006-2010 state means: S, Gini, ln(real GDP per capita), activity rate, ln(population density).
N=48.
S coefficient = +0.955624; SE = 0.162326; t = 5.887.
Thus the cross-state S -> subsequent D association remains strong after controlling the Ferragina-compatible socioeconomic variables.

Other coefficients:
Gini +23.9623 (t=2.447)
ln GDPpc +2.0584 (t=2.342)
Activity -0.02740 (t=-0.636)
ln density -0.37958 (t=-3.654)

## Test 4: Does baseline S predict democratic change?
Predictor: mean S 2006-2010.
Outcome: D_2023 - D_2011.
N=48.
beta = +0.222048; SE = 0.145871; t = 1.522; p ≈ 0.128.
Interpretation: positive but not statistically reliable.

## Link to Ferragina E -> S result
Ferragina-style E -> S cross-section:
Gini -> S coefficient = -30.985214; SE = 7.895453; t=-3.924.

The product of the Gini->S coefficient and the controlled S->future-D coefficient is negative (-29.610), with a Sobel-style delta-method z ≈ -3.265. However, this must NOT be called causal mediation: E and S are averaged over the same 2006-2010 window, and the total Gini->future-D coefficient controlling the other E variables is not significant (beta=-5.648, t=-0.503), while adding S reverses the conditional Gini coefficient. This is an inconsistent-mediation/suppression pattern, not a clean causal chain.

## Bottom line
Cross-sectional temporal evidence strongly supports the proposition that states with higher social capital subsequently exhibit higher democracy levels. The stronger causal/dynamic proposition — that a decline in S within a state causes a later decline in D — is NOT supported by the current lagged TWFE test, and S does not significantly predict 2011-2023 change in D.

Therefore the full causal E -> S -> D hypothesis is not yet established. The E->S inequality association and the cross-state S->future-D association are both strong, but the within-state temporal transmission link remains unverified.

No S, E, or D values were altered. No interpolation or imputation was used.
