# Methodology Stress Test against Closest Precedents — v0.1
Date: 2026-09-23

## Research target
Substantive inference: change in American democracy as a national system, 2000-2023.
Empirical architecture: disaggregated state evidence (50 states x years), used to construct/validate national trajectories and test mechanisms.
Not a state-ranking project.

## Closest methodological precedents
1. Putnam, Leonardi & Nanetti (1993): subnational Italian regions, multi-indicator civic community and institutional performance; indicators drawn from different periods/sources.
2. Paxton (1999): U.S. social-capital trend using multiple indicators and measurement modeling; warns that conclusions depend on how social capital is measured.
3. Paxton (2002): democracy and social capital treated as potentially interdependent rather than a one-way causal relation.
4. Knack (2002): U.S. states as observational units linking social capital to quality of government.
5. Rice/Sumberg and related U.S.-state civic-culture work: state-level civic culture and government performance.
6. Ferragina (2013): regional European evidence; socioeconomic determinants of social capital, including inequality/labor-market participation; direct precedent for E -> S.
7. Bordandini et al. (2025/26): subnational Italian units used to reassess national social-capital change decades after Putnam; distinguishes civic decline from civic shift.

# Stress-test findings

## 1. MAJOR ISSUE: 50 states do not by themselves identify a national time trend
A state-year panel increases observations and permits heterogeneity/mechanism tests, but it does not magically turn 24 calendar years into 1,200 independent observations of national change. Common national shocks are shared across states.
Required fix:
- separate national time-series/descriptive inference from state-panel mechanism inference;
- use state/year fixed effects as appropriate for within-state mechanisms;
- cluster/robust SE design must respect common shocks and serial correlation;
- do not claim N=1,200 as the effective sample size for the national trend.

## 2. MAJOR ISSUE: aggregation must match the construct
"American democracy" is not necessarily the population-weighted mean of state democracy.
Some democratic institutions are state-based; citizens are population-distributed; federal institutions have their own national properties.
Required fix:
- define what the national democracy index means before aggregation;
- report at least equal-state and population-weighted state aggregates;
- compare them with an independent national democracy series (e.g. V-Dem or another defensible national measure);
- treat divergence as substantive evidence, not nuisance.

## 3. MAJOR ISSUE: strict Putnam social capital is not annual
Putnam's original index combined multiple indicators measured over different periods. Exact continuations of many indicators are irregular or unavailable after 2000.
Required fix:
- do NOT create a fake annual strict-Putnam index through interpolation;
- maintain STRICT replication/extension and MODERN longitudinal extension separately;
- use available strict waves as anchors/validation;
- annual national/state trajectory must use a transparently defined modern measurement model if annual coverage is required.

## 4. MAJOR ISSUE: measurement invariance over 24 years
Declining newspaper readership, traditional memberships, meetings, and changing online/hybrid participation can make a fixed indicator set look like civic decline when participation has shifted form.
Bordandini's "decline vs shift" problem is directly relevant.
Required fix:
- test indicator-level trends before index construction;
- distinguish bonding/bridging, formal/informal, offline/modern participation where data permit;
- conduct sensitivity tests excluding indicators whose social meaning changed materially;
- never interpret a falling legacy indicator automatically as falling latent social capital.

## 5. MAJOR ISSUE: social-capital index construction cannot simply average whatever is observed
Missing indicators and changing source composition can generate artificial trend breaks.
Required fix:
- pre-specify index construction;
- compare z-score/composite approach with a latent-variable approach where feasible;
- hold measurement composition constant within each trend comparison or explicitly model changing composition;
- report indicator coverage by state-year.

## 6. MAJOR ISSUE: democracy and social capital may be jointly endogenous
Paxton/McLaren-Baird/Rothstein-type arguments imply D -> S as well as S -> D.
Required fix:
- avoid causal wording from contemporaneous FE regressions;
- estimate lagged competing pathways;
- test D_(t-1) -> S_t alongside S_(t-1) -> D_t;
- economic variables may themselves be endogenous to democracy;
- mediation claims require stronger temporal/identification assumptions than ordinary panel regression.

## 7. IMPORTANT: economic variables must not be treated only as controls
Ferragina directly motivates E -> S. Putnam's earlier institutional-performance work also considered socioeconomic development.
Required fix:
- distinguish confounder, antecedent, moderator, mediator, and competing explanation;
- estimate E -> S, E -> D, S -> D, E+S -> D before interaction/mediation;
- do not claim that the project is the first ever to consider economics; contribution is integrated U.S. longitudinal testing and explicit political-economy specification.

## 8. IMPORTANT: national democracy decline cannot be inferred from the Berkeley state index alone
A state democracy index captures state institutions/policies but may omit federal democratic deterioration or improvement.
Required fix:
- Berkeley State Democracy Index = principal subnational DV;
- construct state-derived national trajectory;
- validate against independent national-level democracy measures;
- explicitly discuss federal/state mismatch.

## 9. IMPORTANT: fixed effects can remove the very between-state historical variation Putnam emphasized
Putnam's classic result is largely comparative across regions and historically persistent civic differences. State FE identify within-state change, a different estimand.
Required fix:
- separate estimands:
  A. national trajectory;
  B. between-state Putnam-style association;
  C. within-state longitudinal association;
- do not present FE as a direct replication of Putnam;
- use correlated random effects/Mundlak or between-within decomposition as a useful bridge if appropriate.

## 10. IMPORTANT: spatial dependence
Neighboring states share regional economies, migration, media markets, institutions, and political diffusion.
Required fix:
- inspect spatial autocorrelation of residuals;
- consider region-year shocks or spatially robust specifications if diagnostics warrant;
- do not assume 50 states are independent cross-sectional units.

## 11. IMPORTANT: state composition and migration
A state's social capital can change because people change behavior or because different people move into/out of the state.
Required fix:
- interpret state-level change carefully;
- where feasible, control demographic composition and migration or test sensitivity;
- avoid ecological-to-individual causal claims.

## 12. IMPORTANT: only 24 national annual observations
For national trajectory/change-point analysis, 2000-2023 gives T=24.
Required fix:
- keep national trend models parsimonious;
- avoid data-mined multiple breakpoints;
- pre-specify secondary break tests (e.g. Trump era / post-2021) and label them secondary;
- prioritize descriptive trajectories and uncertainty over elaborate national time-series models.

# Revised empirical architecture

## Layer 1 — National measurement (PRIMARY substantive result)
Construct and display 2000-2023 national trajectories:
D_US(t): American democracy
S_US(t): social capital
E_US(t): economic conditions
Use transparent aggregation and external national validation.

## Layer 2 — State decomposition (EVIDENCE BASE)
Show whether national movement is:
- broad across states;
- concentrated in particular regions/states;
- population-driven;
- equal-state institutional movement.
This prevents a national average from hiding heterogeneity.

## Layer 3 — Mechanism panel
Estimate state panel models to test E/S/D relationships.
Distinguish between-state and within-state effects.
Use lags and competing directions.
Do not equate association with causation.

## Layer 4 — Strict Putnam replication anchors
Use exact/compatible Putnam variables where available.
No interpolation.
Use these anchors to test whether modern social-capital measurement tracks the original construct.

## Layer 5 — Robustness / validation
- equal-state vs population-weighted aggregation;
- alternative democracy measures;
- strict vs modern social-capital measurement;
- alternative economic specifications;
- spatial/common-shock diagnostics;
- measurement-invariance checks.

# Bottom line
The overall research architecture is viable, but the earlier formulation "50 states x 24 years = 1,200 observations, therefore stronger evidence for the national decline" is statistically too simple. The strongest design treats national democratic change as the primary substantive object, the state panel as disaggregated evidence and mechanism identification, and strict Putnam measures as replication anchors rather than forcing them into a complete annual panel.
