# S3 v4 FROZEN — Formal Volunteering / Community Activity (Putnam U.S. Democracy Project, 2026-10-01)

## 1. Purpose
Canonical, frozen S3 state-year series for 50 states × 2000–2023. RUN_ID `S3_v4_20261001T090728Z`.

## 2. Canonical definition
Formal volunteering: share of persons 16+ who did unpaid volunteer work through or for an organization in the past ~12 months (primary question + follow-up prompt).

## 3. Data coverage
1,200 state-years (`data/S3_FINAL_v4.csv`). DC and territories excluded.

## 4. Direct vs model-estimated
- DIRECT_OBSERVED: 900 (2002–2015, 2017, 2019, 2021, 2023), values identical to `data/S3_Volunteering_Community_Activity_CANONICAL_RAW_v2.csv`.
- MODEL_ESTIMATED_BETWEEN_WAVES: 200 (2016, 2018, 2020, 2022). MODEL_ESTIMATED_BACKCAST_NO_DATA: 100 (2000–2001).
- Analysis variable: `S3_latent` / `S3_analytic` (series-A scale) with `S3_latent_se`, 95% bounds, for all 1,200 cells. Observed values are kept in `value_observed`.

## 5. Raw sources
2002–2015 CPS September Volunteer Supplement public-use microdata (Census; 2002–2009 via NBER mirror of Census files); 2017–2023 CPS Civic Engagement & Volunteering (CEV) `sep17pub/sep17rep`, `sep19pub/sep19rep`, `sep21pub/sep21nrrep`, `sep23pub/sep23nrrep`. URLs, retrieval timestamps and SHA256 in `provenance/S3_SOURCE_MANIFEST_v4.csv` and `logs/download_log_CEV.txt`. Raw files are not in the package (size); re-download and check SHA256.

## 6. CEV definition
Volunteer = PES16 = 1 OR PES16A = 1; universe PRPERTYP = 2, age 16+, PRSUPINT = 1; weight PWNRWGT. (PES16-only definition rejected: ~4 pp off published rates — `provenance/S3_CEV_DEFINITION_CHECK_v4.csv`.)

## 7. Official SE methodology
2011–2015 and 2017–2023: 160 successive-difference replicate weights, Var = 4/160 × Σ(θ_r − θ_0)². 2002–2010: official GVF (b = 4,687, Total 16+; no state factor table located). Official SE coverage: 900/900.

## 8. AmeriCorps reproduction QA
200/200 published CEV state rates reproduced; max |difference| = 4.9e-8. 2002–2015 national rates reproduce BLS within ±0.05 pp (`data/S3_CPS_NATIONAL_BENCHMARK_v2.csv`).

## 9. Measurement break 2015→2017
CEV merged the Volunteer and Civic Engagement supplements (content and universe changes). Handled by series-specific measurement parameters; observed values never rescaled. There is no overlap year; the national level change 2015→2017 is not separately identified from the break intercept α_B.

## 10. M2 specification
S_st = μ_t + u_st; μ_t national random walk, u_st state random walks. Series A: y = S + e (α = 0, λ = 1, τ_A = 0 fixed at boundary); series B: y = α_B + λ_B·S + e. e variance = official SE² (+ τ²). Kalman filter + RTS smoother, MLE.

## 11. Fitting and convergence
Re-fitted from scratch with official SEs; exit code 0 (`logs/run_v4.log`). Optimizer convergence flag = False; Newton polishing then met the pre-set criterion: max gradient 2.0e-4, Hessian PD (min eigenvalue 7.6). AIC −4,186 (M1 −3,962). α_B = 0.0528 (SE 0.0253), λ_B = 1.023 (SE 0.052). Uncertainty = smoother variance + parameter uncertainty (300 draws from N(θ̂, H⁻¹)).

## 12. M2b robustness test
M2 + transitory national shock. First run failed (NameError, kept in log); rerun: shock variance → 0, fit identical to M2 → M2 retained (parsimony). Not canonical.

## 13. Holdout tests
`qa/S3_HOLDOUT_VALIDATION_v4.csv`: 95% coverage 2013 1.00, 2009 1.00, 2002–03 backcast 0.99, 2017 0.98, 2019 0.82.

## 14. 2019 limitation
2019 holdout coverage = 0.82 (below criterion), mean error +0.031 (common national bias), unchanged under official SEs and under M2b. Not corrected ex post.

## 15. Affected cells
The uncertainty intervals for the 150 model-estimated state-years in 2018, 2020 and 2022 may be too narrow, based on the 2019 holdout coverage of 0.82. Flag: `interval_undercoverage_risk = 1` (150 cells).

## 16. No interpolation
No linear interpolation, forward fill or backward fill. All non-observed cells are Kalman-smoothed model estimates with uncertainty.

## 17. Reproducibility
`code/`: extract.py (2002–15 rates) → se.py (2002–15 SE) → cev_se.py (2017–23 SE) → model_v4.py + final_v4.py (M1/M2, holdouts, final M2) → model_v4b.py (M2b) → build_v4.py (outputs) → freeze_v4.py (flag, final QA, packaging). Environment: `code/ENVIRONMENT_v4.txt`; seed 20260930.

## 18. File inventory
See `SHA256SUMS.txt` (all files except itself).

## 19. Hash verification
`sha256sum -c SHA256SUMS.txt` must return OK for every file.

## 20. Known limitations
2019 holdout under-coverage (§14–15); break level not identified (§9); 2002–2010 SEs use GVF without state factors; 2007–2008 BLS benchmark not re-retrieved; Bayesian NUTS not run; v3-era logs retained for history.

## 21. Freeze declaration
S3 v4 is frozen as the canonical S3 dataset for the Putnam U.S. Democracy Project as of 2026-10-01. The 2019 holdout coverage limitation is retained and documented rather than corrected ex post. Future modification requires a new version and must not overwrite v4. FROZEN ≠ PERFECT.
