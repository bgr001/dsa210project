import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('databases/imputed_suicide_total_data.csv')

age_cols = df.columns[3:18]

# Calculate correlation per age group.  
spending_correlations = []
personnel_correlations = []
for age in age_cols:
    spending_corr = df[[age, 'Spending']].corr().iloc[0,1]
    spending_correlations.append(spending_corr)
    corr = df[[age, 'Personnel']].corr().iloc[0,1]
    personnel_correlations.append(corr)



fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot spending correlations.  
sns.barplot(x=age_cols, y=spending_correlations, palette='viridis', ax=ax1)
ax1.set_title('Correlation with Military Spending')
ax1.set_ylabel('Pearson Correlation Coefficient')
ax1.set_xlabel('Age Groups')
ax1.axhline(0, color='black', linestyle='--')
ax1.tick_params(axis='x', rotation=45)

# Plot personnel correlations.  
sns.barplot(x=age_cols, y=personnel_correlations, palette='viridis', ax=ax2)
ax2.set_title('Correlation with Military Personnel')
ax2.set_xlabel('Age Groups')
ax2.axhline(0, color='black', linestyle='--')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('plots/military_age_correlation.png', dpi=300, bbox_inches='tight')
plt.show()