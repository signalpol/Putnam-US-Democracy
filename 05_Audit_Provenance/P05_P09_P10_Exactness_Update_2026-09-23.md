# P05 / P09 / P10 Exactness Update — 2026-09-23

## Governing rule
Canonical Putnam variables require the same construct/behavior and the same statistic. A binary participation rate cannot replace an original mean count/frequency.

## P05 Group Membership
Putnam statistic: mean number of group memberships.
Current legacy CPS series must not be treated as canonical if it is a binary participation rate.
A modern CPS count question is a candidate only for waves where the questionnaire directly records number of groups/organizations. Each wave must be verified before inclusion.
Status: REBUILD_REQUIRED. Do not use legacy P05 values in canonical index until count-variable wave mapping is verified and state weighted means are recomputed.

## P09 Community Project
Putnam statistic: mean number of times worked on a community project in the previous year.
Existing CPS participation/rate series is not equivalent.
Status: NON_EQUIVALENT_LEGACY; canonical missing unless a direct annual count/frequency item is verified.

## P10 Volunteer Work
Putnam statistic: mean number of times did volunteer work in previous year.
CPS Volunteer/CEV measures volunteer status, frequency categories, hours, and (in older waves) weeks/hours by organizations. Frequency categories such as every day / few times a week / few times a month / once a month / less than once a month are not an observed count of times.
Converting categories to annual event counts would require midpoint/behavioral assumptions and is therefore not canonical under the strict replication rule.
Status: NON_EQUIVALENT_FOR_CANONICAL unless a direct number-of-times item is found. CPS hours/weeks/frequency retained for robustness only.

## Consequence
P05/P09/P10 legacy observed cells must not enter the canonical Putnam index until exact-statistic requirements are satisfied. Preserve them in the robustness layer; do not delete raw data.
