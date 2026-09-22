# Canonical Research + Work Design

## Central Outcome
Assess whether **American democracy as a national system** shows a gradual long-run decline over 2000-2023 and estimate how that national trajectory relates to changes in Putnam-style social capital and economic conditions. The 50 states are the disaggregated empirical foundation for measuring and testing that national trajectory.

## Design principle
No single-event monocausal assumption. Trump-era and post-2021 periods are secondary break/interaction tests nested inside the long-run analysis.

## Unit and levels
**Substantive unit of inference / research target: the United States as a whole over 2000-2023.**
The central object is the long-run change in the level and quality of American democracy, and its relationship to national change in Putnam-style social capital and economic conditions.

**Empirical observation unit: U.S. states.**
The 50 states x 2000-2023 = 1,200 state-years provide the disaggregated evidence base. State-level observations are not the ultimate research target or a state-ranking exercise. They are used to construct, validate, and explain the national trajectory with much stronger evidence than a 24-observation national time series alone.

The national series is therefore a principal outcome of the measurement design, not merely a descriptive supplement. State-level heterogeneity and panel estimates serve as micro-level validation and mechanism tests for the U.S.-wide inference.

Aggregation must not assume that an unweighted arithmetic sum of states literally equals the national population. National measures will report transparent aggregation alternatives (population-weighted and equal-state where theoretically relevant), with sensitivity checks.

## Variable blocks
Y — Democracy:
- Berkeley State Democracy Index 2.0 (primary state-year DV)
- V-Dem only as external/national validation where measurement permits

S — Social capital:
- Canonical Putnam variables only when the original construct, behavior/question, and statistic can be faithfully updated
- Non-equivalent modern proxies excluded from canonical index and retained only for robustness
- No interpolation

E — Economic conditions, minimum core:
E1 Real economic performance: real GDP per capita / real GDP growth (BEA)
E2 Material living standard: real per-capita personal income (BEA)
E3 Labor-market insecurity: annual unemployment rate and employment-population ratio (BLS LAUS)
E4 Distribution: state income inequality/Gini where a comparable annual series exists
E5 Structural economic change: industry composition / manufacturing-employment or value-added share, subject to consistent 2000-2023 state coverage

Do not collapse the economic block into one index before estimating separate effects and checking collinearity.

## Core empirical sequence
M0: describe Democracy(t), SocialCapital(t), Economy(t) nationally and by state.
M1: Democracy_it = state FE + year/trend structure + SocialCapital_it.
M2: Democracy_it = state FE + year/trend structure + EconomicBlock_it.
M3: Democracy_it = state FE + year/trend structure + SocialCapital_it + EconomicBlock_it.
M4: SocialCapital_it = state FE + year/trend structure + EconomicBlock_it.
M5: interaction/mediation specifications only after M1-M4 establish temporal and statistical relationships.
M6: secondary pre-specified break tests around Trump-era onset and post-2021 period; these do not replace the long-run trend model.

## Key tests
A. Is the democracy trend negative over 2000-2023?
B. Is the social-capital trend negative?
C. Are economic deterioration/insecurity/distributional change associated with democracy?
D. Does adding E materially change the magnitude/significance of S?
E. Is E associated with S, consistent with an economic -> social-capital pathway?
F. Are post-2016/post-2021 deviations distinguishable from the pre-existing trajectory?

## Identification discipline
Association is not causation. Fixed effects, lag structures, trend controls, robustness checks, and temporal ordering strengthen inference but do not by themselves establish causal effects. Any causal claim requires a design supporting identification.

## Work order
1. Re-audit P01-P14 against Putnam original operational definitions.
2. Remove non-equivalent proxies from canonical social-capital index; retain them in robustness layer.
3. Complete canonical social-capital data collection and coverage matrix.
4. Acquire economic block E1-E5 from official sources with 50-state 2000-2023 coverage where possible.
5. Merge Y/S/E into master state-year panel.
6. Build national longitudinal series using transparent population/equal-state weighting alternatives.
7. Run descriptive trend/change-point diagnostics without assuming decline.
8. Estimate M1-M6.
9. External validation and sensitivity analysis.
10. Draft tables, figures, abstract, methods, results, limitations.

## Canonical rule
All subsequent collection, code, analysis, and manuscript text must follow this document and 00_RESEARCH_OBJECTIVE_CANONICAL.md unless explicitly revised.
