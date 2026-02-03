\# Data pipeline design



This document defines the rules used to transform the raw Yemen health dataset into an analysis-ready dataset. All decisions are made to support transparent, reproducible analysis under conditions of incomplete and inconsistent reporting.



\## Unique key definition



The unique analytical unit is the district–month.



A unique key is defined as the combination of:

\- district identifier (pcode\_2)

\- reporting month (date)



All rows are expected to be unique at this level after cleaning.



\## Parsing and standardisation



Several geographic fields are stored as list-like strings (e.g. "\['Abyan']"). These values will be parsed to extract single clean strings before any grouping or aggregation.



Date fields will be parsed and standardised to a monthly datetime format.



\## Duplicate handling



Duplicate district–month records are expected in the raw dataset.



Duplicates are identified where the same district and month appear more than once.



Resolution rules:

\- For count variables (suspected cholera cases, cholera deaths, number of health workers): take the maximum reported value to avoid undercounting.

\- For percentage or rate variables (percent functioning health centres, attack rate, access problem percentages): take the median value to reduce sensitivity to outliers.

\- A boolean flag indicating whether a record was duplicated will be retained for quality diagnostics.



\## Governorate completion



Where governorate information is missing, it will be filled deterministically using district codes and existing pcode-to-governorate mappings present in the dataset. No manual or external geographic assumptions will be introduced.



\## Coverage metrics



Reporting coverage will be explicitly measured.



Coverage indicators include:

\- number of districts reporting per month

\- proportion of expected districts reporting per governorate per month



Coverage metrics will be calculated prior to aggregation and will be displayed alongside analytical outputs.



Months or areas with low coverage will be flagged as low-confidence.



\## Variable inclusion and exclusion



Core analytical variables:

\- percent functioning health centres

\- suspected cholera cases

\- suspected cholera deaths

\- attack rate (as reported)

\- percent of individuals reporting problems accessing health facilities



Diagnostic or contextual variables:

\- number of health workers

\- hub and geographic identifiers



Excluded from core analysis:

\- facility counts (clinics, hospitals, doctors, dentists) due to extreme missingness



Excluded variables remain in the dataset only for data availability assessment.



\## Quality control outputs



Before analysis, the following QC outputs will be produced:

\- missingness table by variable

\- duplicate count and resolution summary

\- reporting coverage over time

\- range and outlier checks for percentage and rate variables



No analytical results will be generated before QC outputs are reviewed.



\## Reproducibility



All processing steps will be implemented in reproducible scripts. The processed dataset will be regenerated entirely from raw data using the documented rules above.



