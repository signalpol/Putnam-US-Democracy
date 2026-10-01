# S4 Model Validation Report
Final model: M2 primary — latent S = national RW + state RW (2011–2023); measurement per indicator × regime (α, λ, τ), official replicate SEs; anchor NB_B; Kalman/RTS smoother, MLE.
Fit: loglik 1211.85, k 14, AIC −2395.70, L-BFGS success True, max |grad| 4.6e-4, Hessian PD (min eig 0.28). Uncertainty = smoother variance + parameter uncertainty (200 draws N(θ̂, H⁻¹)).
DIRECT years carry a single-year GLS composite of the two indicators on the latent scale (no temporal smoothing); MODEL years carry the smoothed latent.

Comparison (rank correlation with M2 direct composite, by year): M0 equal-weight min 0.979 / mean 0.989; M1 SE-weighted min 0.966 / mean 0.979.
Reference-indicator sensitivity (anchor NB_A): identical loglik and latent ranking (rank corr 1.000) — pure reparameterisation.
Loading-equality sensitivity (λ_A = λ_B): loglik 1203.71 (ΔAIC +12.3, LR 16.3, 2 df); L-BFGS reports success but max |grad| 0.037 and Hessian NOT PD (min eig −2.3e-5) → rejected; latent rank corr ≥ 0.995.
Friends/Family sensitivity (+FF, k 20): L-BFGS success False (reported as-is); after Newton step max |grad| 1.4e-5, Hessian PD; latent rank corr min 0.989, trend-slope corr 0.983.
Bridge-period sensitivity (2014–2016): rank corr ≥ 0.9935; mean |level diff| 0.004 (+FF) to 0.008 (equal loadings).

Holdouts (pre-registered): 2011 cov 0.83 / MAE 0.024 / RMSE 0.033 / bias +0.015; 2013 0.94 / 0.025 / 0.032 / −0.018; 2019 0.97 / 0.024 / 0.030 / +0.002; 2021 0.93 / 0.030 / 0.039 / −0.022.
2011 holdout is the only failure; it is an edge extrapolation and its refit Hessian is near-singular (min eig 1.2e-5). Not corrected ex post. Per the pre-written rule, regime-A model cells (2012, 2014–2016; 200) get undercoverage_risk = 1; all 2000–2010 backcast cells (550) also get undercoverage_risk = 1 because they are edge extrapolations of the same kind.

2000–2010 backcast (director-instructed inclusion, 2026-10-02): SE rises monotonically backward (mean 0.020 in 2011 → 0.034 in 2000); state ranking preserved (rank corr 2000 vs 2011 = 1.000); national mean flat by construction (0.746); cross-state SD shrinks from 0.034 (2011) to 0.015 (2000) — backcast values carry no new information and pull states toward the 2011 profile; primary vs +FF backcast rank corr 0.990. Use with backcast_flag = 1.
