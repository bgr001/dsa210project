# Exploring the Link Between Violence Markers, Economic Shocks and Age-Specific Suicide Patterns
## Introduction

Although suicide, one of the leading causes of death globally, seems to be primarily linked with the mental state of an individual being disturbed by personal affairs, material conditions and the constant display of violence in the form of state control might play a bigger role. This study aims to explore the possible connections between age-based suicide rates and markers of violence, as well as the impact of global recessions on suicide rates. While mental health and its connection with suicide is well-studied, the role of state-sanctioned violence and conflicts is less understood. There is also a potential to reveal age-specific vulnerabilities.

Research Question: How do structural violence exposure (conflicts, military spending, military personnel rate, police presence) and economic shocks correlate with suicide rates across countries and age groups?

## Variables and Data Sources

| Variable                          | Data Type    | Based On             | Dataset                                                  | Link                                                                                          | Source  | Time Period     |
|----------------------------------|--------------|----------------------|-------------------------------------------------------|-----------------------------------------------------------------------------------------------|---------|-----------------|
| Suicide rates                    | Numeric      | Country-Year, Age Group | Reported suicide rates by age                        | [Link](https://ourworldindata.org/grapher/suicide-rates-by-age-who-mdb)                      | WHO     | 1950–2021       |
| Conflict status                  | Binary       | Country-Year         | States involved in state-based conflicts             | [Link](https://ourworldindata.org/grapher/states-involved-in-state-based-conflicts)          | UCDP    | 1946–2023       |
| Military spending per GDP        | Numeric      | Country-Year         | Military spending as a share of GDP                  | [Link](https://ourworldindata.org/grapher/military-spending-as-a-share-of-gdp-sipri)         | SIPRI   | 1948–2023       |
| Military personnel per population| Numeric      | Country-Year         | Military personnel as a share of total population    | [Link](https://ourworldindata.org/grapher/military-personnel-as-a-share-of-total-population) | COW     | 1816–2016       |
| Police officers per 1,000 people | Numeric      | Country-Year         | Police officers per 1,000 people                     | [Link](https://ourworldindata.org/grapher/police-officers-per-1000-people)                   | OWID    | 1973–2015       |
| Recession                        | Binary       | Year                 | —                  | —                                                                                             | IMF       | 1950-2020               |

## Methodology and Findings

### 1. Data Collection
Download the suicide rates by age, states involved in state-based conflicts, military spending as a share of gdp, military personnel as a share of total population, police officers per 1000 people datasets from Our World in Data. Recession years are hardcoded as there are only 4 global recessions (1975, 1982, 1991, 2009) since 1950 officially recognized by the IMF.

### 2. Data Cleanup
Merge the downloaded datasets, remove the rows with low-quality or missing data, remove countries with less than 30 entires and missing years in between their first and last entries. It should be noted that rows containing zeroes are eliminated first to filter out low-quality suicide data and police data should be merged in after any cleanup operations as it requires imputation due to missing data. Recession data is added last.

At this point, it can be observed that the data for police officers per 1,000 people has many gaps, especially in the early years. Consequently, only the time period from 2000 to 2016 is taken into consideration for analyses involving the use of this dataset. The missing values in this time period are imputed using forward and backward fill by country as the observed gaps are short. The scope of this operation, along with all analyses involving police data, is restricted to the United States, the United Kingdom, and Canada to limit the number of required imputations.

### 3. Exploratory Data Analysis and Hypothesis Testing
#### I. Recession
Plotting the mean suicide rate in recession years and non-recession years versus age groups results in the subplot on the left-hand side, while the right-hand side shows the ratio of these two rates. 
!!RECESSION_IMPACT_BY_AGE
It can be seen that although there is almost always an increase in suicide rates in recession years, this change is quite minimal to the point that it is nonexistent in the age group 55-59. A hypothesis test can be conducted to see whether the changes in suicide rates are statistically significant.

$H_0:$ The mean suicide rate in recession years is equal to the mean suicide rate in non-recession years for all age groups. $\mu_{\text{rec}} = \mu_{\text{non-rec}}$

$H_A:$ The mean suicide rate in recession years is different than the mean suicide rate in non-recession years for all age groups. $\mu_{\text{rec}} \neq \mu_{\text{non-rec}}$

Performing a two-sample t-test shows that the findings are statistically insignificant (each having a p value > .05); therefore, we fail to reject the null hypothesis. A snippet of these findings can be found below, while full results can be observed in the terminal output of `recession.py`.
| Age Group | Mean (Non-Recession) | Mean (Recession) | Ratio (Recession/Non-Recession) | T-statistic | p-value | Significant (p < 0.05) |
|-----------|----------------------|------------------|---------------------------------|-------------|---------|------------------------|
| 15-19     | 5.670014             | 6.009458         | 1.059867                        | 0.780788    | 0.437175 | False                  |
| 20-24     | 10.956867            | 11.953862        | 1.090993                        | 1.148659    | 0.254039 | False                  |
| 25-29     | 12.090031            | 13.389762        | 1.107504                        | 1.362063    | 0.177069 | False                  |

II. 
## Replicate this Study
