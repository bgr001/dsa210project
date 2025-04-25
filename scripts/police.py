#police

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

df = pd.read_csv('datasets/imputed_suicide_total_data.csv')

# Filter focus countries and years (>= 2000) 
countries = ['United States', 'United Kingdom', 'Canada']
df_filtered = df[(df['Country'].isin(countries)) & (df['Year'] >= 2000) & (df['Year'] <= 2016)]

# Calculate total suicide rate.  
age_cols = df_filtered.columns[3:18]

df_filtered['Total_Suicide_Rate'] = df_filtered[age_cols].mean(axis=1)

# Plot.  
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_filtered, x='Police', y='Total_Suicide_Rate', hue='Country')
plt.title('Police per 1000 vs Suicide Rate (2000-2016)')
plt.xlabel('Police per 1000 people')
plt.ylabel('Suicide Rate per 100,000')
plt.grid(True)
plt.savefig('plots/focus_police_correlation.png')
plt.show()

# Calculate Pearson correlation for each country.  
for country in countries:
    country_data = df_filtered[df_filtered['Country'] == country]
    corr, p_value = pearsonr(country_data['Police'], country_data['Total_Suicide_Rate'])
    print(f"{country}: Pearson r = {corr:.3f}, p-value = {p_value:.3f}")
