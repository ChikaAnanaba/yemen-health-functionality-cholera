## Analytical Framework and Methods

## Purpose and scope

This analysis examines reported health system functionality and suspected cholera cases at district level in Yemen between January 2019 and May 2021. The purpose is to identify where multiple stress signals converge, rather than to estimate disease burden or infer causal relationships.

The work is designed to mirror the types of exploratory, coverage-aware analyses often required in humanitarian settings, where data completeness varies over time and across locations.

## Data preparation and quality assessment

The raw dataset contains district-level monthly indicators related to health facility functionality, cholera cases and deaths, and selected access proxies. Initial review identified several data quality issues, including list-like geographic fields stored as strings, duplicate district–month records, and substantial missingness in some facility-level variables.

Geographic identifiers were standardised, dates were parsed consistently, and a district–month unit of analysis was constructed. Duplicate district–month records were resolved using documented rules: count variables were aggregated using maximum values to avoid undercounting, while percentage-based indicators were aggregated using medians to reduce sensitivity to outliers. A flag was retained to indicate where duplication had occurred.

Reporting coverage was assessed by calculating the number of districts reporting in each month. This revealed a marked decline in coverage in 2021, with the number of reporting districts falling by more than two-thirds compared to earlier periods. Months with low reporting coverage were explicitly flagged and excluded from trend-based analyses to reduce the risk of misinterpreting reporting gaps as substantive change.

## Decision signal 1: Persistently low health facility functionality

The first signal identifies districts with consistently low reported health facility functionality. Analysis focuses on districts with a minimum reporting history to reduce sensitivity to sporadic reporting, and uses median values rather than single-month observations.

This signal is intended to highlight areas where reported functionality appears chronically constrained over time, rather than districts experiencing short-term fluctuations.

## Decision signal 2: Sustained cholera pressure

The second signal captures sustained cholera pressure based on repeated months of elevated suspected cholera case counts. Emphasis is placed on persistence rather than peak magnitude, reflecting the operational importance of prolonged transmission pressure in humanitarian contexts.

Districts are ranked using the number of high-case months, with additional consideration of total reported cases where reporting histories are comparable.

## Decision signal 3: Co-movement between functionality and cholera

The third signal explores whether changes in reported health facility functionality align temporally with changes in suspected cholera cases within districts. This is implemented as a within-district correlation scan, subject to minimum data requirements and variance checks to avoid spurious results.

These correlations are interpreted strictly as signals, not as evidence of causal relationships. Potential explanations include overlapping access constraints, changes in surveillance intensity, population movement, or other contextual factors not captured in the data.

## Synthesis and prioritisation logic

Rather than constructing a composite index or applying arbitrary weights, the three signals are brought together through a simple convergence framework. Each district is flagged based on the number of independent signals present.

This approach prioritises transparency and interpretability, allowing users to see which signals are driving a district’s inclusion rather than obscuring this information in a single score.

## Limitations and interpretation

Reported indicators reflect partner-reported operational status and surveillance data, which may be influenced by access constraints, insecurity, reporting practices, and population displacement. The absence of a signal should not be interpreted as the absence of need.

Findings are intended to support prioritisation and hypothesis generation, and should be interpreted alongside qualitative information and field-level knowledge.
