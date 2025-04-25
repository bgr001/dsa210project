import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

df = pd.read_csv('datasets/imputed_suicide_total_data.csv')

# Filter for the US and the UK.  
countries = ['United Kingdom', 'United States']
df_filtered = df[df['Country'].isin(countries)]

# Calculate total suicide rate by summing age columns.  
age_columns = df.columns[3:18]
df_filtered['Total_Suicide_Rate'] = df_filtered[age_columns].sum(axis=1)

# Create box plot.   
plt.figure(figsize=(10, 6))
box_plot = sns.boxplot(
    x='Country', 
    y='Total_Suicide_Rate', 
    hue='Conflict', 
    data=df_filtered,
    palette={1: 'red', 0: 'blue'}
)
plt.title('Suicide Rates in Conflict vs Non-Conflict Years')
plt.ylabel('Total Suicide Rate')
plt.xlabel('Country')

handles, _ = box_plot.get_legend_handles_labels()
box_plot.legend(handles, ['No Conflict', 'Conflict'], title='Conflict Status')

plt.savefig('plots/conflict_focus.png', dpi=300, bbox_inches='tight')
plt.show()


#Hypothesis Test 

results = []

for country in ['United Kingdom', 'United States']:
    country_data = df_filtered[df_filtered['Country'] == country]
    non_conflict = country_data[country_data['Conflict'] == 0]['Total_Suicide_Rate']
    conflict = country_data[country_data['Conflict'] == 1]['Total_Suicide_Rate']
    
    # Run the test (conflict =/= non-conflict).  
    t_stat, p_value = ttest_ind(conflict, non_conflict, equal_var=False, alternative='greater')
    
    # Calculate means and ratio.  
    mean_non_conflict = non_conflict.mean()
    mean_conflict = conflict.mean()
    ratio = mean_conflict / mean_non_conflict
    
    results.append({
        'Country': country,
        'Mean (Non-Conflict)': mean_non_conflict,
        'Mean (Conflict)': mean_conflict,
        'Ratio': ratio,
        'T-statistic': t_stat,
        'p-value': p_value,
        'Significant (p < 0.05)': p_value < 0.05
    })

results_df = pd.DataFrame(results)
print(results_df)