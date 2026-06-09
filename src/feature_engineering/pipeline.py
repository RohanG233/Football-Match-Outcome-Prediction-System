import pandas as pd
from database.db import engine
from feature_engineering.feature_builder import FeatureBuilder


def run_feature_engineering():

    # Load cleaned data from database
    df = pd.read_sql(
        "SELECT * FROM clean_matches",
        engine
    )

    print(f"Loaded {len(df)} rows from clean_matches")

    # Create feature builder
    builder = FeatureBuilder(df)

    # Generate features
    feature_df = builder.build_features()

    print(f"Generated {len(feature_df.columns)} features")

    # Store features into database
    feature_df.to_sql(
        "match_features",
        engine,
        if_exists="replace",
        index=False
    )

    print("Features stored in match_features")
    return feature_df