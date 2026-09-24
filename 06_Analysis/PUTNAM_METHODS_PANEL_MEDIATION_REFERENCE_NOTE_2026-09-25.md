# PUTNAM U.S. DEMOCRACY PROJECT
## Methodology & Panel-Mediation Reference Note
**Date:** 2026-09-25
**Status:** Research-method archive for later paper drafting. Not a final estimator lock.

## Core hypothesis
The project tests a temporally ordered mechanism:

**Economic Conditions E(t-2) -> Social Capital S(t-1) -> Democracy D(t)**

The main test is not a comparison of parallel trends. It asks whether economic change precedes subsequent social-capital change and whether that social-capital change precedes subsequent democratic change in a 50-state, 2000-2023 state-year panel.

## Difference from Putnam's original statistical strategy
Putnam, Leonardi & Nanetti (1993), *Making Democracy Work*, relied primarily on between-region relationships among civic-community and institutional-performance measures, combined with historical and qualitative evidence. It did not estimate a modern longitudinal indirect-effect model E -> S -> D.

The present project changes the empirical question from primarily **between-region S -> institutional performance** to a **within-state longitudinal pathway E(t-2) -> S(t-1) -> D(t)**.

## Basic mediation logic
Path a:
S(i,t-1) = a E(i,t-2) + controls + panel structure + error

Path b/direct path:
D(i,t) = b S(i,t-1) + c' E(i,t-2) + controls + panel structure + error

Indirect effect:
**a x b**

The final specification must evaluate state fixed effects, year fixed effects, panel-appropriate clustered inference, autoregressive terms for persistence, and endogeneity/reverse-causality robustness. These components are not yet locked; estimator choice must fit N=50, T=24 and actual S coverage.

## Principal macro-panel precedent: Delhey & Steckermeier (2020)
Jan Delhey & Leonie C. Steckermeier. 2020. “Social Ills in Rich Countries: New Evidence on Levels, Causes, and Mediators.” *Social Indicators Research* 149:87-125.
DOI: 10.1007/s11205-019-02244-3
Official: https://link.springer.com/article/10.1007/s11205-019-02244-3

This is the closest applied macro-panel precedent found in the discussion. It studies aggregate economic conditions, mediators, and social outcomes. Its panel mediation explicitly delays economic conditions by one year relative to mediators and by two years relative to the outcome; mediators are one year before the outcome. Thus the design is directly analogous to **X(t-2) -> M(t-1) -> Y(t)**. It estimates separate panel equations for mediation paths and reports two-way fixed-effect longitudinal regressions.

**Paper use:** principal applied reference showing an aggregate longitudinal mediation design with the same temporal ordering as our E(t-2) -> S(t-1) -> D(t). Do not imply identical substantive variables.

## Panel-mediation specification precedent: Khan & Kutan (2021)
Habib Hussain Khan & Ali M. Kutan. 2021. “Testing the structure-conduct-performance relationship for ASEAN: Addressing the issues in the panel mediation.” *Journal of Asian Economics* 72:101269.
DOI: 10.1016/j.asieco.2020.101269
Publisher: https://www.sciencedirect.com/science/article/pii/S1049007820301494

The paper argues that longitudinal mediation must account for causal processes unfolding over time and highlights lags of explanatory variables, autoregressive effects, distributed lags, and endogeneity. It uses GMM and PVAR robustness and shows that corrected dynamic panel specifications can materially alter mediation conclusions.

**Paper use:** justification for not estimating E-S-D as contemporaneous mediation and for explicitly considering lag structure, persistence, and endogeneity.

## Method comparison: Becker (2024)
Dominik Becker. 2024. “Many Roads to Mediation: A Methodological and Empirical Comparison of Different Approaches to Statistical Mediation.” *methods, data, analyses* 18(1):7-32.
DOI: 10.12758/mda.2023.02
Official: https://majournals.bib.uni-mannheim.de/mda/article/view/2023.02

Becker compares OLS, fixed-effects mediation, GMM, causal mediation with/without FE, and fixed-effects cross-lagged panel models. The study emphasizes the consecutive predictor -> mediator -> outcome order, unobserved heterogeneity, reverse causality, and matching the lag structure to the theoretical data-generating process. GMM and FE-CLPM perform particularly well in its simulations when lag structure is correctly specified.

**Paper use:** methodological reference for estimator choice and causal-order/lag specification.

## Ferragina (2013): substantive bridge to Putnam
Emanuele Ferragina. 2013. “The socio-economic determinants of social capital and the mediating effect of history: Making Democracy Work revisited.” *International Journal of Comparative Sociology* 54(1):48-73.
DOI: 10.1177/0020715213481788
Publisher: https://journals.sagepub.com/doi/10.1177/0020715213481788

Ferragina is primarily the substantive bridge for **E -> S**: contemporary socioeconomic conditions can be investigated as determinants of social capital rather than social capital being treated only as historical inheritance. It is not the main statistical template for our panel mediation.

## Three-wave/time-lagged empirical precedents
Three-wave studies establish the generic empirical sequence **X(T1) -> M(T2) -> Y(T3)**. They are secondary methodological support because most are individual-level rather than macro state panels.

Haider et al. (2020): three-wave longitudinal mediation with temporally separated predictor, mediator and outcome and autoregressive controls.
https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2020.00792/full

Quintelier, Stolle & Harell (2012), *Political Research Quarterly*: longitudinal/cross-lagged analysis relevant to directionality between social/network variables and political participation.
https://journals.sagepub.com/doi/10.1177/1065912911411099

Political/political-communication three-wave studies discussed in the project are supporting precedents for temporal mediation in political outcomes, but must not be represented as macro state-panel equivalents.

## Current methodological position
Simple E/S/D trend plots and contemporaneous correlations are descriptive only. The principal empirical design under consideration is:

**longitudinal/dynamic panel mediation with explicit consecutive temporal order**
**E(i,t-2) -> S(i,t-1) -> D(i,t)**

State/year panel structure, persistence and endogeneity must be handled with a specification appropriate to the final data. A lagged observational panel strengthens evidence about temporal order and mechanism but does not by itself prove experimental causation.

## Reference hierarchy for manuscript
**Tier A — direct macro-panel precedent**
1. Delhey & Steckermeier (2020): aggregate economic conditions -> lagged mediator -> lagged outcome; two-way FE panel mediation.

**Tier A — panel mediation method/specification**
2. Khan & Kutan (2021): lagged/autoregressive/endogeneity-aware panel mediation.
3. Becker (2024): FE/GMM/CMFE/FE-CLPM comparison and causal-order/lag issues.

**Tier B — substantive bridge**
4. Ferragina (2013): socioeconomic determinants of social capital; Putnam revisited.

**Tier B — three-wave/cross-lagged empirical support**
5. Haider et al. (2020) and related three-wave mediation studies.
6. Quintelier, Stolle & Harell (2012) and related political longitudinal studies.

## Items not locked without PI/user approval
- Exact estimator: TWFE mediation vs dynamic FE vs GMM vs FE-CLPM or a layered robustness set.
- Exact autoregressive terms.
- Lag sensitivity windows beyond the core t-2/t-1/t hypothesis.
- Exact construction of S in the mediation equation.

Final variable/model adoption remains the principal investigator/user's decision.

## Working paper-ready methodology sentence
The study evaluates a temporally ordered mediation mechanism in which state economic conditions at t-2 predict social capital at t-1, which in turn predicts democratic performance at t. This design follows the logic of longitudinal panel mediation, with a macro-panel precedent in Delhey and Steckermeier (2020), while panel-specific concerns regarding autoregressive persistence, distributed lags, endogeneity, and unobserved heterogeneity are addressed with reference to Khan and Kutan (2021) and Becker (2024).

## Verification note
Core bibliographic details and methodological claims for Delhey & Steckermeier (2020), Khan & Kutan (2021), and Becker (2024) were rechecked against publisher/official journal pages on 2026-09-25 before archiving. Supporting references from the conversation should be bibliographically rechecked before final manuscript citation.
