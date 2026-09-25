# Ferragina E → S Stage 1 — Joint TWFE Results
Date: 2026-09-25

Specification:
S_(i,t-1) ~ ln(real GDP pc)_(i,t-2) + activity rate_(i,t-2) + ln(pop density)_(i,t-2) + state FE + year FE.

Sample: 48 contiguous states × 9 S years (2002–2010), N=432. Economic years 2000–2008. No interpolation/imputation.

| Variable | beta | State-cluster SE | t | Two-way SE | t |
|---|---:|---:|---:|---:|---:|
| ln(real GDP pc) | -1.170071 | 0.789497 | -1.4820 | 0.749562 | -1.5610 |
| Activity rate (%) | -0.030163 | 0.037284 | -0.8090 | 0.043925 | -0.6867 |
| ln(pop density) | +1.478085 | 1.032188 | +1.4320 | 1.009096 | +1.4648 |

Within R2 = 0.035697.

Interpretation guard:
No coefficient is conventionally significant at the 5% level under either state-cluster or conservative two-way clustered inference. Signs match the corresponding individual TWFE models: GDPpc negative, activity negative, density positive. This is a within-state longitudinal association and is not a replication of Ferragina's cross-sectional regional regression. No mediation or causal conclusion is warranted from this stage.
