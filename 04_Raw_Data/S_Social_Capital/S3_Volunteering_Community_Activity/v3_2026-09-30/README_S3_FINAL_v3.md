# S3 Volunteering / Community Activity — ANALYTICAL FINAL v3 (2026-09-30)

## Files
- `S3_Volunteering_Community_Activity_CANONICAL_RAW_v2.csv` — observed-only panel (unchanged; 900 observed / 300 MISSING).
- `S3_Volunteering_Community_Activity_ANALYTICAL_FINAL_v3.csv` — 1,200 rows (50 states × 2000–2023).
  - `value_observed` = original observed value (900 cells, byte-for-byte equal to v2), `value_observed_se` + method.
  - `S3_latent`, `S3_latent_se`, 95% bounds = model-smoothed latent S3 for **all** 1,200 cells (series-A scale). `S3_analytic` = `S3_latent`.
  - `observation_class`: DIRECT_OBSERVED (900) / MODEL_ESTIMATED_BETWEEN_WAVES (2016, 2018, 2020, 2022; 200) / MODEL_ESTIMATED_BACKCAST_NO_DATA (2000–2001; 100).
  - `survey_regime`: A_CPS_VOLUNTEER_2002_2015 / B_CPS_CEV_2017_2023 / A_B_TRANSITION (2016) / NONE_PRE_SURVEY.
- Coverage, measurement-break analysis, model diagnostics, provenance log, raw-source manifest (CPS zips with SHA256 + URLs), code, environment.

## Missing-year re-search (result: no new direct observations)
- 2000–2001: CPS Volunteer Supplement first fielded Sept 2002; SCCBS 2000 covers a national sample + 41 communities in 29 states (not 50-state comparable); other surveys national only.
- 2016, 2018, 2020, 2022: no supplement (CEV is biennial from 2017; no 2016 vintage).

## Measurement break 2015 → 2017
Regime B (CEV) merged the Volunteer and Civic Engagement supplements and changed content; BLS attributes the national jump 24.9% → 30.3% to the redesign.
No overlap year and no external bridge exists (bridge option B rejected). Adopted: series-specific measurement parameters (S1 v34.1 design):
series A anchor (α=0, λ=1); series B α_B = +0.058 (SE 0.025), λ_B = 1.003 (SE 0.052). **Observed values are never rescaled.**
Caveat: the national level change 2015→2017 is not separately identified from α_B (absorbed by the break, subject to the random-walk prior). Cross-state differences and within-regime change are identified.

## Model
Selected M2: latent S_st = μ_t + u_st (national random walk + state random walks), Kalman filter/RTS smoother, MLE (τ_A fixed at 0 — boundary, LR≈0, as in S1 v34.1).
Convergence: max gradient 7e-5, Hessian positive definite. Beats M1 (independent state RW) by ΔAIC = 216.
Uncertainty = smoother variance + parameter uncertainty (300 draws from N(θ̂, H⁻¹)). Bayesian NUTS (M3): NOT EXECUTED.
Holdout 95% coverage (M2): 2013 1.00, 2009 1.00, 2002–03 backcast 0.99, 2017 0.98, **2019 0.84** (under-coverage inside regime B — treat B-era gap-year intervals as optimistic).

## Standard errors of observed values
- 2011–2015: design-based, 160 successive-difference replicate weights (official).
- 2002–2010: official GVF (b = 4,687; no state factor table located) — GVF runs ~9% below replicate SE (2011–2015 check).
- 2017–2023: **not official** — imputed from each state's 2011–2015 replicate SE; τ_B absorbs residual error. OPEN ITEM.

## Not done / open
CEV official SEs; Bayesian NUTS robustness; 2007–2008 BLS benchmark not re-retrieved; raw CPS files (~15–60 MB each) not in the package (manifest + URLs + SHA256 provided).
