# S5 measurement decision required

Status: PARTIAL — BLOCKED_METHOD_DECISION. RUN_ID: S5_REVIEW_20261002T042315Z. No annual canonical series is selected or frozen.

The actual current RAW is 2,000 individual item observations, not a 200-row single indicator: 10 measures ×50 states ×4 waves. Each is an archived state proportion, reproduced exactly against the archived CEV workbook. Earlier project protocol keeps the ten measures separate and reserves composite construction for a measurement decision. The new finalization instruction allows model construction but does not specify which substantive civic participation construct the one S5 column should represent.

## Concrete competing definitions

Broad10 includes learning about issues; political/societal/local discussions with family/friends and with neighbors; online expression; voting in local elections; contacting officials; political donations; public meetings; collective neighborhood action; political consumption.

Active6 includes voting, contact, donations, meetings, neighborhood action and political consumption. It excludes learning, both discussion items, and online expression. Neither definition is automatically identical to Putnam's original civic involvement variables. Both preserve all original measurements; the distinction is the analytical construct, not a data-cleaning choice.

Fixed2017 scaling: z_j(s,t)=(p_j(s,t)−mean_s[p_j(s,2017)])/SD_s[p_j(s,2017)]. Each basket is its item mean divided by that basket's 2017 state SD. This is an exploratory candidate index, not a percentage and not year-specific standardization. Equal-state 2017 mean is zero by definition. Between2017 and2023, Broad10 mean changes -0.774905 baseline SD; Active6 changes -0.178246 baseline SD; difference 0.596659 baseline SD. A pooled all10 PC1 alternative changes -0.782014, supporting that the large difference is largely basket scope rather than arbitrary equal weighting. All pooled pairwise correlations are positive; PC1 explains50.5%, second eigenvalue1.066. This supports a broad common association but does not prove a single invariant latent construct.

The choice changes the central national civic-decline result and must be made by the research director under the expressly permitted methodological exception. Proposed decision: broad civic orientation/engagement (ten-item latent primary, active6 robustness) OR active civic participation (six-item latent primary, broad10 robustness). A third admissible alternative is no one-number S5 composite and separate civic-information, political-expression and collective-action subscales, which would require modifying the requested single-column architecture.

## Historical evidence

Fresh extraction from official existing Census raw files adds300 direct ITEM observations: contacted public official and bought/boycotted product,50 states in2010/2011/2013. Adult civilian supplement respondents and official PWNRWGT used, negative codes excluded.2011 and2013 item SEs use verified official NR160 replicate weights and4/160 ratio variance, matching each full-weight person record.2010 SE remains unverified. These two items do not supply direct observations of either full basket, and are not used to manufacture a changing-basket score.

Historical monthly discussion asks politics during a typical month, rather than political/societal/local discussion at least once in the year; historical local voting asks habitual always/sometimes/rarely/never, rather than last eligible election; committee/officer service is not collective neighborhood action. These are PARTIAL or NON-EQUIVALENT depending the linkage aim, not direct replacements. Archived project public-meeting rates2010–2015 exist in PUTNAM_01_PublicMeeting.csv but source/weight/denominator lineage is unresolved and excluded from modeling. Public IPUMS volunteer-only meeting variable has a narrower universe; it cannot establish equivalence for all adults.2000/2006 community benchmark samples do not furnish50 independent representative state rates.2008/2009 microdata not acquired for S5 in this bounded review; this is not a claim of source absence.2000–2007 complete ten-item/five-item state-equivalent sources are not established in current evidence.

## Models and validation

M0 Gaussian random-state intercept plus common mean; M1 adds state-specific and common OU temporal covariance with fixed6-year scale. Both fit separately to each candidate score. Two optimizer starts,20 total fits including4 complete-wave holdouts, training-only preprocessing. likelihood/AIC/BIC only compare M0 versusM1 within a basket; cross-basket information criteria have different outcomes and cannot select the construct. Full fit convergence4/4; finite-difference Hessian eigenvalues, fixed-boundary parameters, parameter start results and raw optimizer values preserved. Boundary components indicate weakly estimated covariance dimensions. The predictive intervals include residual noise, not verified survey-design SE. Coverage is exploratory and below nominal for some broad-basket endpoint folds. No holdout can validate the2000–2016 backcast from four recent complete-basket waves. Measurement-regime model between historical and CEV baskets is not empirically identified until a basket and cross-regime loading assumptions are specified. Never treat the conditional model fit as empirical invariance.

## Required decision

Choose the primary substantive basket. Then estimate the separate annual latent analytical series, retain all2,300 direct item rates in observed tables, estimate cross-wave measurement loading/regime sensitivity and flag backcast identification. This review deliberately does not claim journal-ready completeness or emit a purported FINAL/FROZEN canonical panel.
