import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import ttest_ind

df = pd.read_csv('datasets/imputed_suicide_total_data.csv')
age_cols = df.columns[3:18]

# Prepare data by melting the age columns as they need to be rows.  
melted = df.melt(
    id_vars=['Country', 'Year', 'Recession'],
    value_vars=age_cols,
    var_name='Age Group',
    value_name='Suicide Rate'
)

# Convert Age Group to ordered categorical to be in the x axis.  
melted['Age Group'] = pd.Categorical(melted['Age Group'], categories=age_cols, ordered=True)

# Create a figure with two plots, both by age groups.  LHS: Recession vs Non-Recession Suicide Rates, RHS: Recession / Non-Recession Suicide Rates
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Age-Specific Impact of Economic Recessions on Suicide Rates', y=1.05)

# # 1. Absolute Effect Plot (Point Plot)
sns.pointplot(
    x='Age Group', 
    y='Suicide Rate', 
    hue='Recession',
    data=melted,
    estimator=np.mean,
    errorbar=None,
    palette={0: 'blue', 1: 'red'},
    linestyles=['--', '-'],
    ax=ax1
)
ax1.set_title('Suicide Rates')
ax1.set_xlabel('Age Group')
ax1.set_ylabel('Mean Suicide Rate (per 100,000)')
ax1.tick_params(axis='x', rotation=45)
ax1.legend(title='Recession', labels=['Non-Recession Years', 'Recession Years'])
ax1.grid(True, alpha=0.3)

# 2. Relative Effect Plot (Bar Plot)
# Calculate recession impact ratio: (recession rate)/(non-recession rate)
recession_effect = melted.groupby(['Age Group', 'Recession'], observed = False)['Suicide Rate'].mean().unstack()
recession_effect['Impact Ratio'] = recession_effect[1] / recession_effect[0]

sns.barplot(
    x=recession_effect.index,
    y='Impact Ratio',
    data=recession_effect.reset_index(),
    color='purple',
    ax=ax2
)
ax2.axhline(1, color='black', linestyle='--')  # Baseline ratio = 1
ax2.set_title('Relative Impact')
ax2.set_xlabel('Age Group')
ax2.set_ylabel('Ratio of Suicide Rates\n(Recession / Non-Recession)')
ax2.tick_params(axis='x', rotation=45)

# Annotate bars with ratio values
for p in ax2.patches:
    ax2.annotate(f"{p.get_height():.2f}", 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                xytext=(0, 5), 
                textcoords='offset points')

plt.tight_layout()
plt.savefig('plots/recession_impact_by_age.png', dpi=300, bbox_inches='tight')
plt.show()


# Hypothesis Test: Two-sample T-Test

results = []

for age_group in age_cols:
    non_recession = melted[(melted['Age Group'] == age_group) & (melted['Recession'] == 0)]['Suicide Rate']
    recession = melted[(melted['Age Group'] == age_group) & (melted['Recession'] == 1)]['Suicide Rate']
    
    # Run t-test
    t_stat, p_value = ttest_ind(recession, non_recession, equal_var=False)
    
    # Calculate means
    mean_non_recession = non_recession.mean()
    mean_recession = recession.mean()
    ratio = mean_recession / mean_non_recession
    
    # Determine significance
    significant = p_value < 0.05
    
    # Results: 
    results.append({
        'Age Group': age_group,
        'Mean (Non-Recession)': mean_non_recession,
        'Mean (Recession)': mean_recession,
        'Ratio (Recession/Non-Recession)': ratio,
        'T-statistic': t_stat,
        'p-value': p_value,
        'Significant (p < 0.05)': significant
    })

results_df = pd.DataFrame(results)
print(results_df)


# 2 YEAR LAGGED ANALYSIS
# Create a 2-year lagged recession column.  
df['Recession_lag2'] = df.groupby('Country')['Recession'].shift(-2) 
melted_lags = df.melt(
    id_vars=['Country', 'Year', 'Recession', 'Recession_lag2'],
    value_vars=age_cols,
    var_name='Age Group',
    value_name='Suicide Rate'
)
# Initialize results storage.  
lag_results = []

for age_group in age_cols:
    # Extract data for 2-year lag
    non_lag = melted_lags[(melted_lags['Age Group'] == age_group) & (melted_lags['Recession_lag2'] == 0)]['Suicide Rate']
    lag = melted_lags[(melted_lags['Age Group'] == age_group) & (melted_lags['Recession_lag2'] == 1)]['Suicide Rate']
    
    # t-test
    t_stat, p_value = ttest_ind(lag, non_lag, equal_var=False)
    
    # Store results.  
    lag_results.append({
        'Age Group': age_group,
        'Mean (Non-Lag)': non_lag.mean(),
        'Mean (2-Year Lag)': lag.mean(),
        'Ratio': lag.mean() / non_lag.mean(),
        'T-statistic': t_stat,
        'p-value': p_value,
        'Significant (p < 0.05)': p_value < 0.05
    })

print(pd.DataFrame(lag_results))


# Line chart for focus countries.  

df['Total_Suicide_Rate'] = df[age_cols].sum(axis=1)

# Filter for focus countries
focus_countries = ['United States', 'United Kingdom', 'Canada']
focus_df = df[df['Country'].isin(focus_countries)]

plt.figure(figsize=(12, 6))
for country in focus_countries:
    country_data = focus_df[focus_df['Country'] == country]
    plt.plot(country_data['Year'], country_data['Total_Suicide_Rate'], label=country)

recession_years = [1975, 1982, 1991, 2009]
for year in recession_years:
    plt.axvline(x=year, color='gray', linestyle='--', alpha=0.5)

# Adjust plot range and style
plt.xlim(1950, 2016)
plt.title('Total Suicide Rates in Focus Countries')
plt.xlabel('Year')
plt.ylabel('Suicide Rate per 100,000')
plt.legend()
plt.grid(False)  # Remove background grid to highlight recession years.  
plt.savefig('plots/recession_focus_countries.png', dpi=300, bbox_inches='tight')
plt.show()