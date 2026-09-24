# CSPP Hawes Social Capital discovery — 2026-09-25

Official Michigan State University Correlates of State Policy Project (CSPP) is a free public state-year repository.

Critical discovery from official CSPP codebooks:
- soc_capital: Hawes et al. social capital measure; codebook v2.4 reports coverage 1986-2009.
- soc_capital_ma: Hawes et al. weighted moving-average social capital measure; codebook v2.6 reports coverage 1984-2011.
- Original source attribution: Hawes, Daniel P., Rene Rocha, Kenneth Meier, “Social Capital in the 50 States: Measuring State-Level Social Capital, 1986–2004,” SPPQ 13(1):121–138.

The article itself says underlying MRI survey data were available 1986-2004 and describes its moving-average formula using two prior and two succeeding observations. Therefore CSPP dates beyond 2004 must NOT automatically be interpreted as newly observed MRI measurements. In particular, the 2005+ values require direct inspection of the CSPP numeric series and provenance before being used as observed S_t.

Official CSPP v2.6 provides complete CSV download and codebook. The web endpoint for the full CSV was identified as:
https://ippsr.msu.edu/sites/default/files/cspp/correlates2-6.csv
but direct binary download was not retrievable through the current execution path in this session.

Research rule: acquire and preserve both soc_capital and soc_capital_ma, but canonical dynamic mediation should prefer unsmoothed observed values and must not treat moving-average extension as independent post-2004 observation.
