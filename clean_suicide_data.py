import pandas as pd
import requests

def clean_data(file_path):
    df = pd.read_csv(file_path, storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
    
    # Clean up column names.  

    df = df.rename(columns={"Entity": "Country"})
    new_columns = list(df.columns[:3])
    for column in df.columns[3:]:
        shorter = column.replace("Death rate from self-inflicted injuries per 100,000 population - Sex: Both sexes - Age group: ", '')
        shorter = shorter.replace(" years", '')
        new_columns.append(shorter)
    df.columns = new_columns

    # Remove rows with any zeroes.  

    age_columns = df.columns[3:]
    df = df[df[age_columns].ne(0).all(axis=1)]
    
    # Remove countries with less than 30 entries.  

    counts = df["Country"].value_counts()
    kept = counts[counts >= 30].index
    df = df[df["Country"].isin(kept)]
    
    # Remove countries missing any years in between.  

    ranges = df.groupby("Country")["Year"].agg(["min", "max", "count"])
    ranges["expected_years"] = ranges["max"] - ranges["min"] + 1
    ranges["missing_years"] = ranges["expected_years"] - ranges["count"]
    
    valid = ranges[ranges["missing_years"] == 0].index
    df = df[df["Country"].isin(valid)]
    
    return df

cleaned_data = clean_data("https://ourworldindata.org/grapher/suicide-rates-by-age-who-mdb.csv?v=1&csvType=full&useColumnShortNames=false")
cleaned_data.to_csv("dsa210/suicide_data.csv", index=False)
