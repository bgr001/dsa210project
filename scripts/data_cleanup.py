import pandas as pd

# Download the data.  
suicide_data = "https://ourworldindata.org/grapher/suicide-rates-by-age-who-mdb.csv?v=1&csvType=full&useColumnShortNames=false"
conflict_data = "https://ourworldindata.org/grapher/states-involved-in-state-based-conflicts.csv?v=1&csvType=full&useColumnShortNames=false"
military_spending_data = "https://ourworldindata.org/grapher/military-spending-as-a-share-of-gdp-sipri.csv?v=1&csvType=full&useColumnShortNames=false"
military_personnel_data = "https://ourworldindata.org/grapher/military-personnel-as-a-share-of-total-population.csv?v=1&csvType=full&useColumnShortNames=false"
police_data = "https://ourworldindata.org/grapher/police-officers-per-1000-people.csv?v=1&csvType=full&useColumnShortNames=false"

# COMMENT THE FIRST BLOCK AND UNCOMMENT BELOW TO USE THE LOCAL DATASETS. Remove the storage option.  
# suicide_data = "datasets/raw/suicide_data.csv" 
# conflict_data = "datasets/raw/conflicts_data.csv"
# military_spending_data = "datasets/raw/military_spending_data.csv"
# military_personnel_data = "datasets/raw/military_personnel_data.csv"
# police_data = "datasets/raw/police_data.csv"

# Construct the dataframes.  
storage = {'User-Agent': 'Our World In Data data fetch/1.0'}
df = pd.read_csv(suicide_data, storage_options = storage) 
conflicts_df = pd.read_csv(conflict_data, storage_options = storage) 
military_spending_df = pd.read_csv(military_spending_data, storage_options = storage)
military_personnel_df = pd.read_csv(military_personnel_data, storage_options = storage)
police_df = pd.read_csv(police_data, storage_options = storage)
global_recessions = [1975, 1982, 1991, 2009]

# Save the datasets.  
df.to_csv("datasets/raw/suicide_data.csv", index=False)
conflicts_df.to_csv("datasets/raw/conflicts_data.csv", index=False)
military_spending_df.to_csv("datasets/raw/military_spending_data.csv", index=False)
military_personnel_df.to_csv("datasets/raw/military_personnel_data.csv", index=False)
police_df.to_csv("datasets/raw/police_data.csv", index=False)

# Clean up column names.  
df = df.rename(columns={"Entity": "Country"})
new_columns = list(df.columns[:3])
for column in df.columns[3:]:
    shorter = column.replace("Death rate from self-inflicted injuries per 100,000 population - Sex: Both sexes - Age group: ", '')
    shorter = shorter.replace(" years", '')
    new_columns.append(shorter)
df.columns = new_columns

# Remove the rows that contain any zeroes.  
df = df[df[df.columns[3:]].ne(0).all(axis=1)]

# Merge the datasets and rename the new columns.  
df_addition = [conflicts_df, military_spending_df, military_personnel_df ]#, police_df]
col_names = ['Conflict', 'Spending', 'Personnel', 'Police']

for index in range(len(df_addition)):
    df = pd.merge(
        df, df_addition[index][['Code','Year',df_addition[index].columns[3]]], on = ['Code', 'Year'], how = 'left')
    df = df.rename(columns={df.columns[18+index]:col_names[index]})

# The Conflicts column has binary values of type int instead of float.  
df['Conflict'] = df['Conflict'].astype('Int64')


# Remove the rows that contain any empty values.  
df = df[df[df.columns[3:]].notna().all(axis=1)]

# # Remove countries with less than 30 entries.  
counts = df["Country"].value_counts()
kept = counts[counts >= 30].index
df = df[df["Country"].isin(kept)]

# Remove countries missing any years in between.  
ranges = df.groupby("Country")["Year"].agg(["min", "max", "count"])
ranges["expected_years"] = ranges["max"] - ranges["min"] + 1
ranges["missing_years"] = ranges["expected_years"] - ranges["count"]

valid = ranges[ranges["missing_years"] == 0].index
df = df[df["Country"].isin(valid)]

# Separately add the police column as it does not have as many rows.  
df = pd.merge(df, police_df[['Code', 'Year', police_df.columns[3]]], on = ['Code', 'Year'], how = 'left')
df = df.rename(columns={df.columns[21]:col_names[3]})

# Add recession years.  
df['Recession'] = df['Year'].isin(global_recessions).astype(int)

df.to_csv("datasets/suicide_total_data.csv", index=False)