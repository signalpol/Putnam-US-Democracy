# CANONICAL METHODOLOGY — U.S. Democracy, Putnam Social Capital, and Political Economy
Version 1.0 — 2026-09-23

## 1. Substantive research target
The primary object of study is **the long-run change in American democracy as a national system over 2000-2023**.

The 50 U.S. states are not the ultimate research target and the project is not a state-ranking exercise. States are the disaggregated empirical observation units used to measure, decompose, validate, and explain the national trajectory.

Thus:
- Unit of substantive inference: United States.
- Unit of disaggregated observation: state-year.
- Main period: 2000-2023.
- State panel architecture: 50 states x 24 years = 1,200 state-years where data exist.
- Important qualification: 1,200 state-years are not 1,200 independent observations of national democratic change. National temporal inference still has only 24 annual periods.

## 2. Theoretical framework
The project follows Putnam's core research logic: use subnational variation to understand the performance and evolution of democracy at the larger political-system level.

The project extends this framework by explicitly modeling economic conditions rather than treating social capital as historically autonomous.

Core relationships:
E -> S
S -> D
E -> D
E x S -> D

Competing/reverse pathway:
D(t-1) -> S(t)

Where:
E = economic conditions
S = social capital
D = democratic performance

No causal direction is assumed in advance. The empirical analysis tests competing relationships subject to identification limits.

## 3. Five-layer empirical architecture

### Layer 1 — National trajectory: PRIMARY substantive result
Construct annual U.S. trajectories for:
- D_US(t): American democratic performance
- S_US(t): social capital
- E_US(t): economic conditions

Central descriptive question:
Did American democracy undergo gradual long-run deterioration, stability, improvement, or non-linear change between 2000 and 2023?

Social-capital and economic trajectories are then compared with the democracy trajectory.

Because T=24, national time-series models will remain parsimonious. Descriptive trajectories, uncertainty, and pre-specified tests take priority over data-mined breakpoints.

Trump-era onset and post-2021 tests are secondary structural-break/interaction tests, not the primary causal explanation.

### Layer 2 — State decomposition: MICRO EVIDENCE FOR THE NATIONAL TRAJECTORY
Use state data to determine whether national movement is:
- broad-based across states;
- concentrated in particular states or regions;
- driven by population-heavy states;
- visible under equal-state institutional weighting;
- heterogeneous across economic/social conditions.

This layer provides micro-level empirical support for national inference without pretending that state-years are independent national observations.

### Layer 3 — State-panel mechanism analysis
Separate three estimands:

A. National change:
How did American democracy change over time?

B. Between-state relationship:
Do states with higher/lower social capital and different economic conditions systematically differ in democratic performance?

C. Within-state relationship:
When social capital or economic conditions change within a state, does democratic performance also change?

Fixed-effects models identify within-state relationships and are not treated as direct replications of Putnam's between-region historical comparison.

Where appropriate, between-within decomposition / correlated random effects (Mundlak-type specifications) will bridge the two estimands.

### Layer 4 — Strict Putnam replication/validation
Maintain a STRICT PUTNAM layer based only on:
- exact original variables; or
- measures with demonstrated construct, wording/behavior, statistic, and source continuity.

Rules:
- no interpolation;
- no silent proxy substitution;
- irregular waves remain irregular;
- missing observations remain missing;
- exact/compatible Putnam measures serve as replication and measurement-validation anchors.

A separate MODERN LONGITUDINAL EXTENSION may use contemporary equivalent/proxy measures for annual analysis, but it must never be represented as identical to Putnam's original 14-variable operationalization.

### Layer 5 — Robustness and external validation
Required robustness:
- equal-state vs population-weighted national aggregation;
- state-derived democracy trajectory vs independent national democracy measures;
- strict Putnam vs modern social-capital measurement;
- alternative economic specifications;
- between-state vs within-state estimates;
- lagged competing pathways;
- common national shock/serial-correlation diagnostics;
- spatial-dependence diagnostics;
- demographic composition/migration sensitivity where feasible;
- indicator-composition and measurement-invariance tests.

## 4. Democracy measurement
Primary subnational DV:
Berkeley State Democracy Index 2.0.

The state-derived national series is not automatically equated with total U.S. democracy because federal democratic institutions may change independently of state-level democracy.

Therefore:
1. construct state-derived national trajectories;
2. report population-weighted aggregation;
3. report equal-state aggregation where theoretically relevant;
4. validate against independent national democracy measures, including V-Dem where appropriate;
5. interpret divergence between state-derived and national measures substantively.

## 5. Social-capital measurement
Putnam's original indicators were collected from multiple sources and periods; they were not a complete annual 50-state panel.

Therefore:
- do not manufacture an annual strict-Putnam series through interpolation;
- preserve exact historical/modern continuation waves as strict anchors;
- build any annual modern series separately and transparently;
- examine individual indicator trends before index construction;
- do not automatically interpret decline in traditional participation as decline in latent social capital.

The analysis must explicitly consider the "civic decline versus civic shift" problem: traditional clubs, newspapers, and face-to-face meetings may change social meaning as online, informal, or hybrid participation develops.

## 6. Social-capital index construction
Before constructing any composite:
- document state-year indicator coverage;
- pre-specify inclusion rules;
- avoid averaging changing baskets of indicators without adjustment;
- compare standardized composite methods with latent-variable methods where feasible;
- test sensitivity to indicators whose meaning changed materially over time.

No composite is canonical until its measurement properties are documented.

## 7. Economic block
Economic conditions are theoretical variables, not merely nuisance controls.

Minimum economic block:
E1 real economic performance — real GDP per capita / growth (BEA)
E2 material living standard — real per-capita personal income (BEA)
E3 labor-market insecurity/participation — unemployment and employment-population ratio (BLS)
E4 distribution — state income inequality/Gini where comparable measurement permits
E5 structural economic change — industry composition/manufacturing share where consistent

Do not collapse E1-E5 into one index before estimating separate effects and diagnosing collinearity.

## 8. Model sequence
M0 — descriptive national trajectories:
D_US(t), S_US(t), E_US(t)

M1 — Putnam relationship:
D_it ~ S_it + appropriate temporal/state structure

M2 — economic explanation:
D_it ~ E_it + appropriate temporal/state structure

M3 — integrated political-economy model:
D_it ~ S_it + E_it + appropriate temporal/state structure

M4 — economic formation of social capital:
S_it ~ E_it + appropriate temporal/state structure

M5 — interaction:
D_it ~ S_it + E_it + S_it x E_it + ...

M6 — temporal/competing pathways:
D_it ~ S_i,t-1 + E_i,t-1 + ...
S_it ~ D_i,t-1 + E_i,t-1 + ...

M7 — secondary pre-specified period/break tests:
Trump-era onset and post-2021, interpreted cautiously.

Mediation analysis is performed only if temporal ordering, measurement coverage, and identification assumptions justify it.

## 9. Dependence and uncertainty
State observations are not assumed independent.

Potential dependence:
- national shocks;
- serial correlation;
- regional economic shocks;
- spatial diffusion;
- common media/political environments.

Standard-error/covariance choices and spatial diagnostics must reflect these structures. The final specification will be chosen after empirical diagnostics rather than mechanically.

## 10. Interpretation rules
- Association is not causation.
- State-level relationships do not establish individual-level behavior.
- National trends are not assigned a single cause without identification.
- State FE results are within-state estimates, not Putnam-style historical between-region replication.
- Economic variables can be antecedents, confounders, moderators, mediators, or competing explanations; these roles must be distinguished empirically.
- A declining legacy civic indicator does not by itself establish declining social capital.
- State-derived national democracy does not by itself measure federal democracy.

## 11. Intended contribution
The project combines four literatures that are usually studied separately:
1. Putnam's civic-community/social-capital thesis;
2. long-run change in American social capital;
3. democratic performance/decline;
4. political-economic determinants of social capital and democracy.

The intended contribution is not simply another 50-state comparison. It is a longitudinal assessment of **American democracy as a national system**, grounded in disaggregated state evidence and a Putnam-derived measurement strategy, while explicitly testing economic conditions and competing causal pathways.

## 12. Canonical workflow
1. Complete exact Putnam source-continuity audit.
2. Separate strict canonical variables from robustness proxies.
3. Acquire democracy DV and E1-E5 official economic series.
4. Construct state-year analytical panel.
5. Build national D/S/E trajectories using transparent aggregation alternatives.
6. Validate national democracy trajectory externally.
7. Diagnose social-capital measurement invariance and indicator composition.
8. Estimate between-state and within-state relationships separately.
9. Estimate M1-M7 with appropriate dependence corrections.
10. Conduct robustness and sensitivity analysis.
11. Only then finalize causal language, results, abstract, and conclusions.


## 13. Dimensionality rule for social capital — added after Paxton/Norris audit
The analysis must not assume that all social-capital indicators form a single declining latent dimension.

Required sequence:
1. estimate and graph indicator-level trajectories;
2. estimate an Associational-Civic dimension separately;
3. estimate a Trust dimension separately where measurement permits;
4. test whether these dimensions covary sufficiently to justify a higher-order/composite Social Capital measure;
5. compare conclusions from dimensions with conclusions from the composite.

A composite index must not conceal divergent trends. A decline in trust alongside stability or increase in associational activity is substantively different from a general decline in social capital.

This rule follows the methodological warning from Paxton's U.S. multiple-indicator assessment and Norris's cross-national tests: conclusions about social capital and democracy are sensitive to operationalization and to the distinction between trust and associational networks.
