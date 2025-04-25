# military correlation
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('datasets/imputed_suicide_total_data.csv')

# Calculate correlation.  
correlation = df[['Personnel', 'Spending']].corr()

# Generate the correlation matrix heatmap.  
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation between Military Personnel and Spending')
plt.savefig('plots/military_cross_correlation.png')
plt.show()

print(f"Correlation between Personnel and Spending: {correlation.loc['Personnel', 'Spending']:.3f}")