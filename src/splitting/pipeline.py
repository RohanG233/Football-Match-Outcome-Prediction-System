import pandas as pd

from database.db import engine
from splitting.splitter import DataSplitter


def run_splitting():

    # Load feature-engineered dataset
    df = pd.read_sql(
        "SELECT * FROM match_features",
        engine
    )

    print(f"Loaded {len(df)} rows from match_features")

    splitter = DataSplitter(df)
    split_df = splitter.split()

    print(split_df["dataset_split"].value_counts())

    # Replace table with updated version
    split_df.to_sql(
        "match_features",
        engine,
        if_exists="replace",
        index=False
    )

    print("Dataset split column added successfully.")