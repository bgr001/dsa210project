# facet military

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv('datasets/imputed_suicide_total_data.csv')

# Filter for selected countries
countries = ['United States', 'United Kingdom', 'Canada']
df_filtered = df[df['Country'].isin(countries)]

# MILITARY SPENDING

# Melt age group columns.  
age_cols = df_filtered.columns[3:18]
df_melted = df_filtered.melt(id_vars=['Country', 'Year', 'Spending'], 
                            value_vars=age_cols,
                            var_name='Age Group', 
                            value_name='Suicide Rate')

# Create facet grid of scatterplots.  
g = sns.FacetGrid(df_melted, col='Age Group', col_wrap=5, height=3)
g.map_dataframe(sns.scatterplot, x='Spending', y='Suicide Rate', hue='Country')
g.set_axis_labels('Military Spending (% GDP)', 'Suicide Rate (per 100,000)')
g.add_legend(title='Country', bbox_to_anchor=(1.004, 0.45), loc='center right', borderaxespad=0.)
plt.tight_layout(rect=[0, 0, 0.9, 0.95]) 

plt.savefig('plots/focus_spending_age_correlation.png')
plt.show()


# Perform Spearman test for each age group.  
results = []
for age_group in age_cols:
    for country in countries:
        country_data = df_filtered[df_filtered['Country'] == country]
        corr, pval = stats.spearmanr(country_data['Spending'], country_data[age_group])
        results.append({
            'Country': country,
            'Age Group': age_group,
            'Correlation': corr,
            'P-value': pval
        })

# Create results dataframe and print.  
results_df = pd.DataFrame(results)
print("Military Spending\n")
print(results_df.sort_values(by='Country'))


# MILITARY PERSONNEL

# Melt age group columns.  
age_cols = df_filtered.columns[3:18]
df_melted = df_filtered.melt(id_vars=['Country', 'Year', 'Personnel'], 
                            value_vars=age_cols,
                            var_name='Age Group', 
                            value_name='Suicide Rate')

# Create facet grid of scatterplots.  
g = sns.FacetGrid(df_melted, col='Age Group', col_wrap=5, height=3)
g.map_dataframe(sns.scatterplot, x='Personnel', y='Suicide Rate', hue='Country')
g.set_axis_labels('Military Personnel (% GDP)', 'Suicide Rate (per 100,000)')
g.add_legend(title='Country', bbox_to_anchor=(1.004, 0.45), loc='center right', borderaxespad=0.)
plt.tight_layout(rect=[0, 0, 0.9, 0.95]) 

plt.savefig('plots/focus_personnel_age_correlation.png')
plt.show()


# Perform Spearman test for each age group.  
results = []
for age_group in age_cols:
    for country in countries:
        country_data = df_filtered[df_filtered['Country'] == country]
        corr, pval = stats.spearmanr(country_data['Personnel'], country_data[age_group])
        results.append({
            'Country': country,
            'Age Group': age_group,
            'Correlation': corr,
            'P-value': pval
        })

# Create results dataframe and print.  
results_df = pd.DataFrame(results)
print("Military Personnel\n")
print(results_df.sort_values(by='Country'))
