# Ferragina-Style E → S Cross-Sectional Replication — U.S. States
Date: 2026-09-25

## Purpose
Run the U.S. analogue alongside the longitudinal lagged panel. Ferragina (2013) first tested socioeconomic determinants of social capital across 85 European regions, then used regression residuals for comparative historical case analysis.

## U.S. specification
State-level cross-sectional OLS, 48 contiguous states.
Variables are state means over the common 2006–2010 window:
S_HAWES_COMPTON ~ Gini + ln(real GDP per capita) + Activity rate + ln(Population density).

National divergence is omitted because no theoretically equivalent U.S. state measure has yet been established. This is therefore Ferragina-style, not an exact replication.

## Results
N = 48 states; R2 = 0.472427.

| Variable | beta | conventional OLS SE | t |
|---|---:|---:|---:|
| Gini | -30.985214 | 7.895453 | -3.9244 |
| ln(real GDP pc) | +1.282138 | 0.802100 | +1.5985 |
| Activity rate (%) | +0.013589 | 0.040406 | +0.3363 |
| ln(pop density) | +0.126967 | 0.095657 | +1.3273 |

## Interpretation guard
The strongest association is Gini: states with higher income inequality have lower measured social capital, conditional on the other included socioeconomic variables. This direction is consistent with Ferragina's reported conclusion that inequitable income distribution negatively affects social capital. The other three coefficients are not strong in this U.S. specification.

This is an observational cross-sectional association, not a causal estimate. The 2006–2010 averaging window is dictated by the currently integrated canonical Gini series and should be rerun after the 2000–2005 Census Gini extraction is integrated. Do not replace the longitudinal panel with this model; report both.

Source paper: Ferragina, E. (2013), International Journal of Comparative Sociology 54(1):48–73, DOI 10.1177/0020715213481788.
