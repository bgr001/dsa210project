import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('datasets/imputed_suicide_total_data.csv')

age_groups = df.columns[3:18]
df_melt = pd.melt(df, id_vars=['Conflict'], value_vars=age_groups, 
                  var_name='Age Group', value_name='Suicide Rate')

# Separate conflict and non-conflict data.  
conflict_data = df_melt[df_melt['Conflict'] == 1]['Suicide Rate']
non_conflict_data = df_melt[df_melt['Conflict'] == 0]['Suicide Rate']

# EDA stats.  
conflict_stats = {
    'Median': np.median(conflict_data),
    'Q1': np.percentile(conflict_data, 25),
    'Q3': np.percentile(conflict_data, 75)
}
non_conflict_stats = {
    'Median': np.median(non_conflict_data),
    'Q1': np.percentile(non_conflict_data, 25),
    'Q3': np.percentile(non_conflict_data, 75)
}

# Create box plot.  
plt.figure(figsize=(10, 6))
box = plt.boxplot([conflict_data, non_conflict_data], 
                  labels=['Conflict', 'Non-Conflict'],
                  positions=[1, 1.4],
                  widths=0.35,
                  patch_artist=True)

box['boxes'][0].set_facecolor('blue')
box['boxes'][1].set_facecolor('red')

plt.title('Suicide Rates: Conflict vs Non-Conflict')
plt.ylabel('Suicide Rate (per 100,000)')
plt.grid(True, axis='y')

# Legend stats.  
stats_text = (
    f"Conflict:\n"
    f"Median: {conflict_stats['Median']:.2f}\n"
    f"Q1: {conflict_stats['Q1']:.2f}\n"
    f"Q3: {conflict_stats['Q3']:.2f}\n\n"
    f"Non-Conflict:\n"
    f"Median: {non_conflict_stats['Median']:.2f}\n"
    f"Q1: {non_conflict_stats['Q1']:.2f}\n"
    f"Q3: {non_conflict_stats['Q3']:.2f}"
)
plt.text(1.6, plt.ylim()[1] * 0.85, stats_text, 
         verticalalignment='top', 
         bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('plots/conflict_boxplot.png')
plt.show()