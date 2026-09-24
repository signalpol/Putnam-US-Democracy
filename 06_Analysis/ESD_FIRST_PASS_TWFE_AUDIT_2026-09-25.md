# E–S–D First-Pass Analysis Audit — 2026-09-25

## Status
PARTIAL — core two-way fixed-effects coefficients executed against GitHub canonical master panel; inferential standard errors and mediation significance tests not yet executed.

## Canonical input
- File: `03_Master_Panel/Putnam_US_Democracy_ESD_Master_Panel_v0_21.csv`
- Blob SHA: `b48a0a312000917a7707be136301f619620684f6`
- Grid: 50 states x 2000–2023 = 1,200 rows
- Missing values preserved; no interpolation.

## Timing
Main historical specification:
`E(t-2) -> S(t-1) -> D(t)`

S is `S_HAWES_COMPTON_socap_ma`, observed for the contiguous 48 states through 2010.

## Executed first-pass TWFE results
State and year effects removed by two-way demeaning.

### A. E(t-2) -> S(t-1)
N = 480 state-years.
- ln(real GDP): 0.2583946008
- ln(PCPI): -3.6738208547
- unemployment: -0.0881320046
- within R2 = 0.0853154299

### B. S(t-1) + E(t-2) -> D(t)
N = 480 state-years.
- S: 0.0535728507
- ln(real GDP): -1.9104001364
- ln(PCPI): 1.0757293584
- unemployment: -0.0343239698
- within R2 = 0.0529248900

### Gini restricted sample
E4 begins in 2006, so the lagged Hawes overlap is much smaller (N=192).
- Gini -> S coefficient: -3.2426966732; within R2 = 0.0091000616
- D model: S coefficient 0.1242120667; Gini coefficient 0.4336150044; within R2 = 0.0168640076

## Interpretation guard
These are coefficients only. No statistical-significance claim is authorized from this pass because clustered/robust standard errors, confidence intervals, and formal indirect-effect inference have not yet been computed. The signs are not treated as causal findings.

## Next required execution
1. state-clustered or two-way-clustered inference;
2. formal mediation/indirect-effect test appropriate for panel data;
3. reverse specification D(t-1) -> S(t);
4. sensitivity to alternative S specifications and CEV waves;
5. Trump-era interaction only where the S observation structure permits identification.
