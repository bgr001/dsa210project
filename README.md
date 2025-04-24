# Exploring the Link Between Violence Markers, Economic Shocks and Age-Specific Suicide Patterns
## Introduction

Although suicide, one of the leading causes of death globally, seems to be primarily linked with the mental state of an individual being disturbed by personal affairs, material conditions and the constant display of violence in the form of state control might play a bigger role. This study aims to explore the possible connections between age-based suicide rates and markers of violence, as well as the impact of global recessions on suicide rates. While mental health and its connection with suicide is well-studied, the role of state-sanctioned violence and conflicts is less understood. There is also a potential to reveal age-specific vulnerabilities.

## Methodology

The primary objective is to investigate whether structural violence exposure (conflicts, military spending, military personnel rate, police presence) and economic shocks correlate with suicide rates across countries and age groups.

### 1. Data Collection
Download the suicide rates by age, states involved in state-based conflicts, military spending as a share of gdp, military personnel as a share of total population, police officers per 1000 people datasets from Our World in Data. Recession years are hardcoded as there are only 4 officially recognized global recessions (1975, 1982, 1991, 2009) since 1950.

### 2. Data Cleanup
Merge the downloaded datasets, remove the rows with low-quality or missing data, remove countries with less than 30 entires and missing years in between their first and last entries. It should be noted that rows containing zeroes are eliminated first to filter out low-quality suicide data and police data should be merged in after any cleanup operations as it requires imputation due to missing data. Recession data is added last.

// Impute police data

### 3. Exploratory Data Analysis

### 4. Hypothesis Testing

--- Archived ---

Project Proposal
----
I plan to use the WHO's mortality database to analyze suicide rates over time by age group. My analysis will be enriched by data on economics recessions and possibly war periods in the U.S. I aim to expolore how times of crisis affect suicide rates and how these effects might vary by different age groups.

War periods data could be enriched by measuring severity using the number of troops sent and connected to suicide cases by taking into account the average age of troops. Price of gold historically could also indicate the degree of impact each conflict had on the American population.  
Economic recessions data could show the severity of the recession measuring the change in GDP and the duration of the recession.

Notes
----
- Presidential elections could also act as times of crisis. 
- Reported suicide rates by age: https://ourworldindata.org/grapher/suicide-rates-by-age-who-mdb?time=earliest..latest
- Dates of U.S. recessions: https://fred.stlouisfed.org/series/JHDUSRGDPBR (economic indicators such as declines in GDP could show the severity of the recessions in this database, % change in real GDP could be used)
- Duration of economic recessions: https://www.statista.com/statistics/1317029/us-recession-lengths-historical/
- Recession business cycle turning point dates: https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions
- COW War List: https://correlatesofwar.org/wp-content/uploads/CowWarList.pdf (severity of a war can be measured by total expenditure on conflict by GDP, inflation adjusted)
