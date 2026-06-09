import pandas as pd
from database.db import engine
from cleaning.cleaner import DataCleaner

def run_cleaning():

    # Load validated raw data
    df = pd.read_sql(
        "SELECT * FROM raw_matches",
        engine
    )
    print(f"Loaded {len(df)} rows from raw_matches")

    # Run cleaning
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean()

    print(f"Rows after cleaning: {len(cleaned_df)}")

    # Store cleaned dataset
    cleaned_df.to_sql(
        "clean_matches",
        engine,
        if_exists="replace",
        index=False
    )

    print("Cleaned data stored in clean_matches")
    return cleaned_df