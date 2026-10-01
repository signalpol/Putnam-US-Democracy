# Model comparison and research decision

Only the inherited 400 direct values were used. Source estimates were never replaced. Diagnostic annual predictions are not canonical estimates.

M0: Gaussian logit mixed model, random state intercept, common linear trend, independently estimated error variance for observations without verified SE.
M1: M0 plus state and common temporal Gaussian processes, exponential covariance with fixed six-year length scale.
M2: M1 plus CEV measurement-regime offset. Both model fitting and prediction use GLS, conditional covariance and likelihood maximization from two starts.

Known 2011/2013 SEs enter through the delta-method logit variance. Other wave SEs remain unknown; fitted nuisance error is model-based, not design-based. Intervals condition on estimated covariance parameters, omit full hyperparameter uncertainty, and do not validate nine-year extrapolation. Holdout coverage evaluates withheld direct estimates, not unobserved true participation.

Five complete-wave holdouts (2009/2011/2013/2019/2021), 250 state-wave predictions per candidate, were actually executed. M1 RMSE 0.040723, MAE 0.032457, coverage 94.8%; M2 RMSE 0.040160, MAE 0.032932, coverage 95.6%. M2 improves RMSE by only 0.000563 (0.0563 percentage points). AIC slightly favors M2 (-238.51 versus -237.62); BIC favors M1 (-213.67 versus -210.57). Both optimizations converged; gradients are small. A full numerical Hessian, process length-scale sensitivity and hyperparameter uncertainty have not been verified, so these are not approved final specifications.

Despite similar holdout performance, model annual diagnostic averages differ materially: 2000 M1 46.44%, M2 39.93% (6.52pp); 2015 M1 33.83%, M2 38.22% (4.40pp). The common logit trend per decade is -0.38782 for M1 versus -0.09015 for M2. M2 regime offset is -0.38713 with conditional SE 0.20616. Its nominal interval includes zero. Temporal change and regime offset are weakly separable under these process assumptions and are not nonparametrically identified by these nonoverlapping waves.

M2 predictions include the observed-scale CEV offset after 2017. They are not a silently regime-adjusted latent series. A common-target counterfactual would require choosing an anchor and interpreting or constraining that offset. Keeping every direct value unchanged while calling a mixed-predicate annual series measurement invariant would be misleading.

The user's sole research-decision STOP condition is met: two plausible temporal/regime treatments have similar predictive evidence but produce materially different historical levels and decline. PI decision required: choose a descriptive mixed-regime annual construct with explicit discontinuity, or authorize a common-target calibration with substantive anchoring assumptions. The latter also requires clarifying how unchanged direct values coexist with separately harmonized latent estimates.

No FINAL/FROZEN package or 1200-row canonical panel has been declared. The next authorized work after this decision includes resolved 2008 status, full wave documentation, Hessian/length-scale/offset sensitivity, approved specification, canonical QA and final dual-store verification.
