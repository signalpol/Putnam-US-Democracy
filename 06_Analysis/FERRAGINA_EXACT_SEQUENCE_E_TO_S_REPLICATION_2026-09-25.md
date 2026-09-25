# Ferragina-Method E -> S Cross-Sectional Replication — U.S. States
Date: 2026-09-25
Project: Putnam U.S. Democracy Project

## Method lock
This analysis follows Ferragina (2013), International Journal of Comparative Sociology 54(1):48–73, DOI 10.1177/0020715213481788, as closely as the currently verified U.S. state data permit.

Ferragina sequence:
1. Regional cross-sectional multiple regression of social capital on socioeconomic conditions.
2. Inspect regression residuals.
3. Select deviant and regular cases from residual patterns for comparative historical analysis.

Ferragina socioeconomic variables:
- Gini coefficient
- GDP per capita
- population density
- activity rate
- national divergence

U.S. mapping:
- Gini = state household-income Gini
- GDP per capita = real state GDP per capita
- density = resident population / land area
- activity rate = state labor-force participation rate
- national divergence = OMITTED; no theoretically equivalent U.S.-state operationalization has been verified. No proxy is invented.

Dependent variable:
- S_HAWES_COMPTON_socap_ma, Social Capital 3-year moving average.

## Cross-sectional construction
Geography: 48 contiguous U.S. states.
Common observed window: 2006–2010.
Each state is one cross-sectional observation, using its 2006–2010 mean for S and each E variable.
This window is used because the current canonical E master has Gini observed from 2006 onward while Hawes/Compton S is observed through 2010.
No interpolation or imputation.

Model:
S_i = alpha + beta1*Gini_i + beta2*ln(RealGDPpc_i) + beta3*ActivityRate_i + beta4*ln(PopDensity_i) + error_i

Estimator: OLS with conventional cross-sectional standard errors, matching the Ferragina-style regional cross-sectional stage.

## Results
N = 48 states
R-squared = 0.472427
Adjusted R-squared = 0.423351

| Variable | Coefficient | OLS SE | t | two-sided p |
|---|---:|---:|---:|---:|
| Intercept | -1.388913 | 7.242576 | -0.1918 | |
| Gini | -30.985214 | 7.895453 | -3.9244 | 0.000309 |
| ln(real GDP per capita) | +1.282138 | 0.802100 | +1.5985 | 0.117260 |
| Activity rate (%) | +0.013589 | 0.040406 | +0.3363 | 0.738273 |
| ln(population density) | +0.126967 | 0.095657 | +1.3273 | 0.191411 |

## Direct interpretation
Conditional on the other included socioeconomic variables, income inequality is strongly negatively associated with social capital in this U.S. state cross-section. The sign matches Ferragina's substantive finding that inequitable income distribution is associated with lower social capital. GDP per capita, activity rate, and population density do not reach conventional 5% statistical significance in this U.S. specification.

This is association, not a causal estimate.

## Residual-based case selection
Largest negative residuals (observed S below model-predicted S):
1. Utah: observed -0.132; predicted +1.099; residual -1.231
2. Georgia: observed -1.236; predicted -0.379; residual -0.857
3. Indiana: observed -0.230; predicted +0.556; residual -0.787
4. Delaware: observed +0.344; predicted +1.130; residual -0.786
5. North Carolina: observed -0.947; predicted -0.263; residual -0.684
6. Alabama: observed -1.539; predicted -0.916; residual -0.623

Largest positive residuals (observed S above model-predicted S):
1. Maine: observed +1.895; predicted +0.254; residual +1.641
2. Vermont: observed +1.996; predicted +0.575; residual +1.421
3. Oregon: observed +1.347; predicted -0.005; residual +1.352
4. West Virginia: observed +0.249; predicted -0.614; residual +0.863
5. Washington: observed +1.354; predicted +0.528; residual +0.827
6. New Hampshire: observed +1.905; predicted +1.116; residual +0.789

These residuals are the correct Ferragina-style bridge to comparative historical case analysis. They are not evidence by themselves of a historical causal mechanism.

## Reproducibility / provenance
Canonical input:
03_Master_Panel/Putnam_US_Democracy_ESD_FERRAGINA_MASTER_v1.csv
Input blob SHA: f68f77aa1fe0102e66bdbb7f05e1a4d3c6349926

Previously stored comparison report:
06_Analysis/E_TO_S_FERRAGINA_STYLE_CROSS_SECTION_2026-09-25.md

Integrity guards:
- S not altered.
- E not altered.
- no interpolation/imputation.
- national divergence not proxied.
- longitudinal TWFE results are analytically separate from this Ferragina-style cross-section.
