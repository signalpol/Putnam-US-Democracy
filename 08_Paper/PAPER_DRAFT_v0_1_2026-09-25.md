# Social Capital and Democratic Erosion in the American States, 2000–2023

## Working Paper Draft v0.1 — 25 September 2026

### Abstract — provisional

Why has democratic performance deteriorated unevenly across the American states in the twenty-first century? This study revisits Robert Putnam's social-capital framework and asks whether changes in economic conditions and civic connectedness help explain variation in state-level democratic performance from 2000 through 2023. The analysis is organized as a 50-state panel with the Berkeley State Democracy Index 2.0 as the principal dependent variable. Economic conditions are measured with state-level real GDP, per-capita personal income, unemployment, and income inequality. Social capital is treated more cautiously because no single public measure provides a methodologically identical annual series for all fifty states across the full period. The study therefore preserves the observed historical Hawes–Rocha–Meier/Compton longitudinal social-capital series and the later Current Population Survey Civic Engagement and Volunteering measures as distinct measurement regimes rather than interpolating missing years or mechanically splicing unlike indices. The empirical design tests direct economic and social-capital relationships with democracy, lagged temporal ordering, mediation, Trump-era interactions, and reverse-causality robustness. The central question is not whether Putnam's argument should be assumed to hold, but how much explanatory leverage social capital retains once economic change, temporal ordering, and state heterogeneity are explicitly modeled.

## 1. Introduction

American democratic erosion is commonly discussed as a national phenomenon, but many of the institutions through which citizens vote, organize, receive representation, and encounter political authority are administered by states. The result is substantial subnational variation. States operate under the same federal constitutional order while differing in electoral rules, partisan competition, economic trajectories, civic organization, and the density of social relationships. This combination makes the American states a useful setting for examining why democratic performance changes over time.

This paper develops a state-level test of a proposition rooted in Robert Putnam's theory of social capital: democratic institutions may function differently where citizens possess different stocks of civic connectedness, associational participation, reciprocity, and cooperative capacity. Putnam's original work established a powerful connection between civic community and institutional performance, while *Bowling Alone* documented long-run deterioration in several forms of American civic engagement. Yet a persistent empirical difficulty is measurement. Putnam's state-level measures are strong for cross-sectional differences but are not an annual twenty-first-century panel. Hawes, Rocha, and Meier subsequently developed a dynamic state-level social-capital measure, creating an important bridge from static comparisons to longitudinal analysis. Their published measure, however, relies substantially on proprietary survey material and does not provide a public, continuously extendable component series for the entire 2000–2023 period.

This measurement problem is not a reason to abandon the social-capital hypothesis. It is a reason to test it more carefully. The present study therefore separates the theoretical concept from any single empirical proxy. It preserves observed social-capital measures in their original measurement regimes, refuses to interpolate structurally missing years, and avoids treating later CPS civic-engagement measures as numerically identical to the Hawes index. This approach sacrifices the appearance of a perfectly balanced annual S series in exchange for measurement transparency.

The study asks three linked questions. First, are changes in state economic conditions associated with subsequent changes in democratic performance? Second, does social capital independently predict democratic performance, and does it mediate part of the relationship between economic conditions and democracy? Third, did these relationships change during the Trump era, when national political conflict increasingly interacted with state electoral administration, partisan institutions, and democratic rules?

The empirical design covers 2000–2023 and begins from a canonical 50-state-by-24-year grid of 1,200 state-year observations. Democratic performance is measured with the Berkeley State Democracy Index 2.0. Economic conditions are represented by real GDP, per-capita personal income, unemployment, and the Gini coefficient. Social capital is represented in two observed regimes: the Hawes-family longitudinal index used in the Compton replication data for the earlier period, and state-level behavioral indicators from the CPS Civic Engagement and Volunteering Supplement for the later period. The principal temporal structure is E(t-2) → S(t-1) → D(t), supplemented by direct effects, interactions, and reverse-causality tests.

The paper contributes in three ways. First, it places Putnam's social-capital argument directly into the contemporary literature on subnational democratic performance. Second, it combines a long state-democracy panel with explicit economic and civic mechanisms rather than treating democratic erosion as exclusively partisan or institutional. Third, it makes the measurement discontinuity in American social-capital data an explicit part of the research design rather than hiding it through interpolation or silent proxy substitution.

## 2. Theory and Hypotheses — framework

The theoretical sequence begins with economic conditions. Economic change can alter the resources, stability, and incentives that sustain civic participation. Persistent unemployment, income insecurity, or widening inequality may reduce organizational participation and weaken reciprocal networks, although economic growth alone need not generate civic connectedness. The first empirical relationship is therefore between lagged economic conditions and subsequent observed social capital.

The second relationship concerns democracy. Social capital can matter politically because networks of association and repeated interaction can lower coordination costs, circulate information, generate expectations of reciprocity, and increase citizens' capacity to monitor and respond to public institutions. These mechanisms imply that states with stronger civic connectedness may exhibit different democratic trajectories from otherwise comparable states with weaker civic infrastructure.

The third relationship is indirect. If economic conditions affect civic connectedness and civic connectedness affects democratic performance, social capital may mediate part of the association between economic change and democracy. This is an empirical proposition, not an assumption. A null mediation result would be theoretically informative because it would suggest that economic conditions influence democracy through channels other than Putnam-style civic capacity.

Finally, the Trump era provides a theoretically meaningful period interaction. The study will test whether the association between social capital and democratic performance changed when national partisan conflict became more directly entangled with state-level election administration and democratic institutions. The interaction is not coded as evidence of a predetermined break; it is a test of whether the estimated relationship differs across political periods.

Provisional hypotheses for testing are:

H1: State economic conditions at t-2 are associated with observed social capital at t-1.

H2: Observed social capital at t-1 is associated with state democratic performance at t, conditional on economic conditions and state/time structure.

H3: Part of the relationship between economic conditions and democratic performance operates indirectly through social capital.

H4: The relationship between social capital and democratic performance differs in the Trump-era period relative to the preceding period.

H5 (reverse-causality robustness): Prior democratic performance may predict subsequent social capital; models will explicitly test D(t-1) → S(t) rather than assuming one-way causation.

## 3. Data and Measurement

### 3.1 Unit and period

The canonical data architecture contains the fifty U.S. states observed from 2000 through 2023, yielding 1,200 possible state-year rows. This grid is an organizing frame, not a license to manufacture observations. Variables retain their original temporal coverage, and unavailable observations remain missing.

### 3.2 Democratic performance (D)

The dependent variable is the Berkeley State Democracy Index 2.0. The project has verified a complete 50-state series for 2000–2023, providing 1,200 state-year observations. This measure supplies the common outcome scale against which economic and social-capital predictors will be evaluated.

### 3.3 Economic conditions (E)

The economic block contains four retained measures. E1 is real state GDP from the Bureau of Economic Analysis. E2 is per-capita personal income from BEA. E3 is the state unemployment rate from the Bureau of Labor Statistics Local Area Unemployment Statistics program. E4 is the ACS one-year Gini coefficient (B19083), available for the eligible state-year observations from 2006 onward with the 2020 one-year ACS structural gap retained as missing. No interpolation is used.

### 3.4 Social capital (S)

Social capital is the central measurement challenge. Hawes, Rocha, and Meier developed a dynamic state-level measure designed to capture behavioral components of Putnam's concept across states and over time. The Compton replication data preserve the Hawes-family three-year moving-average social-capital variable (`socap_ma`). Within the present study window, this measure provides 528 observed state-year values: 48 contiguous states for each year from 2000 through 2010. Alaska and Hawaii are not assigned synthetic values.

For the contemporary period, the project uses the Census/AmeriCorps CPS Civic Engagement and Volunteering state-level files. The acquired 2017–2023 workbook provides observed state rates in 2017, 2019, 2021, and 2023 for all fifty states. Seventeen behavioral measures are retained separately, including formal volunteering, organizational membership, charitable giving, informal helping, interaction with friends and neighbors, issue learning and discussion, contacting officials, local voting, public-meeting attendance, collective neighborhood action, and related forms of civic engagement.

These two measurement regimes are not mechanically spliced. The Hawes-family index and the later CEV indicators differ in source design, component structure, and scale. The canonical S file therefore places them on the same state-year keys while retaining separate columns and explicit provenance flags. Years without an observed compatible measure remain missing. A modern composite index may be constructed and evaluated in a later measurement step, but it will not be designated as the study's final social-capital variable without an explicit substantive decision and validation.

## 4. Empirical Strategy — next implementation

The baseline design will exploit within-state and over-time variation while preserving the temporal ordering E(t-2) → S(t-1) → D(t). Estimation will proceed in stages: descriptive trends and coverage diagnostics; bivariate and partial associations; panel models with state and time structure; mediation tests; Trump-era interactions; and reverse-causality robustness. Because S is observed under distinct measurement regimes, the analysis will report regime-specific estimates before considering any pooled specification. This prevents a change in measurement instrument from being mistaken for a change in social capital itself.

Missing observations will not be linearly interpolated. Models will use observed data, with sample sizes and coverage reported for every specification. Results from the early Hawes-family regime and the later CPS/CEV regime will be compared as complementary evidence rather than treated as a single seamless annual series unless subsequent validation demonstrates empirical comparability.

## 5. Status at Draft v0.1

D is acquired for the full 2000–2023 state-year grid. E1–E4 are acquired with their documented source-specific coverage. S has been organized into a canonical observed panel with Hawes/Compton and CPS/CEV kept distinct and all structural gaps preserved. The next paper step is to merge E, S, and D into the analysis master, produce descriptive tables and figures, and estimate the first panel specifications. No substantive hypothesis is treated as confirmed at this stage.