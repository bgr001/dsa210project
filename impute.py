import pandas as pd

df = pd.read_csv('dsa210/suicide_total_data.csv')

# Countries to impute, they have mostly reliable police data.  
countries = ['United States', 'United Kingdom', 'Canada']

# Ensure the police officers column is of type float and filter because only the police officers data for years >= 2000 will be imputed.  
df['Police'] = df['Police'].astype(float)
subset = df[(df['Year'] >= 2000) & (df['Country'].isin(countries))]

# Large gaps are not found in this time period and imputation will be uinvariate, so apply forward and backward fill.  
df.loc[subset.index, 'Police'] = subset.groupby('Country')['Police'].transform(lambda x: x.ffill().bfill())

df.to_csv("dsa210/imputed_suicide_total_data.csv", index=False)