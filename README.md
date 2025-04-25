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
| Recession                        | Binary       | Year                 | [1975, 1982, 1991, 2009]                  | Hardcoded                                                                                             | IMF       | 1950-2020               |

## Methodology and Findings

### 1. Data Collection
Download the suicide rates by age, states involved in state-based conflicts, military spending as a share of gdp, military personnel as a share of total population, police officers per 1000 people datasets from Our World in Data. Recession years are hardcoded as there are only 4 global recessions (1975, 1982, 1991, 2009) since 1950 officially recognized by the IMF.

### 2. Data Cleanup
Merge the downloaded datasets, remove the rows with low-quality or missing data, remove countries with less than 30 entires and missing years in between their first and last entries. It should be noted that rows containing zeroes are eliminated first to filter out low-quality suicide data and police data should be merged in after any cleanup operations as it requires imputation due to missing data. Recession data is added last.

At this point, it can be observed that the data for police officers per 1,000 people has many gaps, especially in the early years. Consequently, only the time period from 2000 to 2016 is taken into consideration for analyses involving the use of this dataset. The missing values in this time period are imputed using forward and backward fill by country as the observed gaps are short. The scope of this operation, along with all analyses involving police data, is restricted to the focus countries (United States, the United Kingdom, and Canada) to limit the number of required imputations.

### 3. Exploratory Data Analysis and Hypothesis Testing
#### I. Recession
Plotting the mean suicide rate in recession years and non-recession years versus age groups results in the subplot on the left-hand side, while the right-hand side shows the ratio of these two rates. 
!!! IMG RECESSION_IMPACT_BY_AGE
It can be seen that although there is almost always an increase in suicide rates in recession years, this change is quite minimal to the point that it is nonexistent in the age group 55-59. A hypothesis test can be conducted to see whether the changes in suicide rates are statistically significant.

$H_0:$ The mean suicide rate in recession years is equal to the mean suicide rate in non-recession years for all age groups. $\mu_{\text{rec}} = \mu_{\text{non-rec}}$

$H_A:$ The mean suicide rate in recession years is different than the mean suicide rate in non-recession years for all age groups. $\mu_{\text{rec}} \neq \mu_{\text{non-rec}}$

Performing a two-sample t-test shows that the findings are statistically insignificant (each having a p value > .05); therefore, we fail to reject the null hypothesis. A snippet of these findings can be found below, while full results can be observed in the terminal output of `recession.py`. In the case that a recession has delayed effects on suicide data, the same analysis can be conducted with a 2-year lag on suicide data following each recession. The results do not change, however.  
| Age Group | Mean (Non-Recession) | Mean (Recession) | Ratio (Recession/Non-Recession) | T-statistic | p-value | Significant (p < 0.05) |
|-----------|----------------------|------------------|---------------------------------|-------------|---------|------------------------|
| 15-19     | 5.670014             | 6.009458         | 1.059867                        | 0.780788    | 0.437175 | False                  |
| 20-24     | 10.956867            | 11.953862        | 1.090993                        | 1.148659    | 0.254039 | False                  |
| 25-29     | 12.090031            | 13.389762        | 1.107504                        | 1.362063    | 0.177069 | False                  |

As shown below, there is not a marked increase in suicide rates in focus countries following global recessions.
!!! IMG recession_focus_countries

#### II. Conflict
Most countries in the dataset have not been in any state-based conflicts in the year range, so conflict analysis conducted on all of the countries in the dataset leads to counterintuitive results such as below.
!!! IMG conflict_boxplot
Instead, focus countries can be used for further conflict analysis. Canada, except for its earlier years, has no conflict history; while the two imperial countries, the US and the UK, have plenty.
!!! IMG conflict_focus
A hypothesis test can be done to determine if the differences are significant enough.

$H_0:$ The mean suicide rate in conflict years is equal to the mean suicide rate in non-conflict years for both countries. $\mu_{\text{con}} = \mu_{\text{non-con}}$

$H_A:$ The mean suicide rate in conflict years is different than the mean suicide rate in non-conflict years for both countries. $\mu_{\text{con}} \neq \mu_{\text{non-con}}$

As seen in the table below, the difference in means is statistically significant for the UK, while it is statistically insignificant for the U.S. Though, we still fail to reject the null hypothesis, as the differences are not significant enough in at least one country under investigation. 
| Country           | Mean (Non-Conflict) | Mean (Conflict) | Ratio    | T-statistic | p-value        | Significant (p < 0.05) |
|-------------------|---------------------|-----------------|----------|-------------|----------------|------------------------|
| United Kingdom    | 133.171346          | 190.933660      | 1.433744 | 7.170544    | 4.846189e-10   | True                   |
| United States     | 251.018640          | 252.197484      | 1.004696 | 0.226009    | 4.109527e-01   | False                  |

#### III. Military Spending and Personnel
To avoid the use of a redundant variable, the Pearson correlation of these two variables is checked. A Pearson correlation score of  $0.688$ suggests that they are moderately correlated, though neither is redundant. As seen in the charts below, the two variables have almost no correlation with age-based suicide rates.
!!!  IMG military_age_correlation.png
Instead, focus countries could provide a possibly meaningful correlation. Below are two sets of scatterplots to visualize how the suicide rates of each age group correlates with military spending per GDP and military personnel per population in focus countries.
!!! IMG focus_spending_age_correlation.png
!!! IMG focus_personnel_age_correlation.png

It can be observed in the scatterplots that there seems to be a high positive correlation between military spending / personnel and suicide rates, especially in the 60-79 age range. However, the computed Spearman and Pearson correlation coefficients appear to be extremely low (some as low as $e^{-39}$) despite the majorly moderate correlation observed among the plots. Such extreme statistical results (infinitesimal p-values) suggest a potential data issue (possibly time-series autocorrelation where both variables follow similar long-term trends), which brings the independence of data points into question. Although it can be reasoned that rising military spending correlating with higher suicide rates could be linked to austerity measures, even such causations would unlikely lead to the observed extremities.

#### IV. Police Officers
The number of police officers per 1,000 population indicates, to an extent, the police presence among populations. For this dataset, due to the given reasons in section 2. Data Cleanup, only the focus countries from 2000 to 2016 are investigated. According to the plot below, there appears to be a negative correlation between suicide rates and police officers. 
!!! IMG focus_police_correlation.png

Crisis intervention by the police could be playing a role in this. Though, in the design phase of this experiment, police data was chosen as a violence marker; as such, a hypothesis test can be done.

$H_0:$ There is no correlation between the number of police officers per 1000 people and suicide rates in the focus countries in 2000-2016. $\rho = 0$

$H_A:$ There is a positive correlation between the number of police officers per 1000 people and suicide rates in the focus countries in 2000-2016. $\rho \neq 0$

The results are found in the table below. There seems to be a negative trend in each country between the two variables, though only in the United States and the United Kingdom is the correlation significant (p-value < 0.05). Because statistical evidence is not significant enough in all focus countries in the specified time period, we fail to reject the null hypothesis.
| Country         | Pearson r | p-value |
|----------------|-----------|---------|
| United States  | -0.659    | 0.004   |
| United Kingdom | -0.696    | 0.002   |
| Canada         | -0.403    | 0.109   |

## Conclusion
While this research examined potential associations between suicide rates and economic shocks (global recessions) or violence markers (conflict status, military spending, military personnel per population, police officers per 1,000 people), no statistically significant correlations were found in the studied countries. No clear evidence suggests that suicide rates systematically vary with recessions, with or without lag, in this dataset. Neither military spending, personnel ratios, nor police density showed a meaningful relationship with suicide trends. One point to note is that an absence of correlation here does not imply these factors are irrelevant to suicide prevention; rather, their relationship may be indirect, context-dependent, or observable only under different analytical conditions.

The analysis was restricted to a handful of, mostly developed, countries, as suicide data is either scarce or low-quality in developing nations. Broader geographic, but especially historical data, might yield different insights. Unmeasured variables such as mental health policies, income inequality or wealth accumulation could influence suicide rates independently. Subsequent studies could benefit from a holistic analysis, incorporating many other variables such as domestic conflicts, into a developed country in depth.  

## Replicate this Study
