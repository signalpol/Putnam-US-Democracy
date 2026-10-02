# S2 model validation

Run S2_FINAL_20261002T002743Z. Model engine exit code 0; 27/27 structural/method-status QA checks PASS.

| Model | Holdout RMSE (proportion) | MAE | Mean bias | Coverage |
|---|---|---|---|---|
|M0|0.04980276828327666|0.03809820718060522|0.004490263080946013|0.884|
|M1|0.04072322557470654|0.03245718030873597|-0.013199764652191855|0.924|
|M2|0.040160097699742554|0.03293169157475155|-0.007304016126186326|0.932|

All five wave holdouts (2009, 2011, 2013, 2019, 2021) and both optimizer starts were actually executed. Coverage concerns prediction of withheld observed rates. Holdout intervals add the known delta-method sampling variance for 2011/2013, and the estimated nuisance sampling variance for other waves. Earlier review coverage used a shared nuisance variance for all holdouts; this final run corrects that distinction. These are not validation of backcast truth.

Selected covariance profile Hessian minimum eigenvalue: 13.869862168328114; condition number: 20.297063857345336; two-start NLL difference: 8.355982572538778e-12. The coefficient covariance is the inverse GLS information matrix. Positive Hessian is local conditional identification, not empirical identification of the bridge without temporal assumptions.

M2_L6 is selected because the independent official wording audit establishes a participation/membership break and the PI explicitly chose a common latent analytical series. Its small RMSE advantage is not the selection rationale. M0, M1 and M2 are bounded alternatives; AIC weakly favors M2, BIC favors M1. M1/M2 lengths 3, 6 and 12 all enter sensitivity uncertainty; no unrestricted specification search was used.

Primary CEV intercept shift -0.38713387814642863 with conditional GLS SE 0.2061617054703487. The near-zero lower-information bridge is conditional on fixed unit loadings and a common exponential time covariance. No concurrent cross-question anchor exists. Posterior scale correction sets the CEV observation-design offset to zero in latent predictions, rather than leaving the observed-scale offset in annual output.

Profile-Hessian covariance propagation uses 32 bounded multivariate-normal parameter draws, seed 20261002. For each, GLS coefficients are reestimated. The model SE adds conditional latent variance, variance of drawn posterior means, and mean squared deviation across six sensitivity predictions around the primary mean. This is a conservative model-uncertainty measure, not a survey design SE or a Bayesian model probability mixture. CI fields envelope both the resulting mean ±1.96 SE and the six conditional intervals; nominal 95% frequentist coverage is not asserted. The 2013 anchor is held fixed, so anchor uncertainty is not fully integrated.

Holdout coefficient/offset stability is retained for every state and wave in S2_HOLDOUT_VALIDATION.csv. State residual patterns are in S2_STATE_HOLDOUT_RESIDUALS.csv. Backcast and gap values have explicit flags; all rows retain bridge assumptions and incomplete early design calibration.
