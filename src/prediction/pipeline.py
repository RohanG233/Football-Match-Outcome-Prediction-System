import pandas as pd

from database.db import engine

from prediction.predictor import (
    MatchPredictor
)


def run_prediction():

    df = pd.read_sql(
        "SELECT * FROM match_features",
        engine
    )

    predictor = MatchPredictor()

    result = predictor.predict(
        home_team="France",
        away_team="England",
        stage="Semi Finals",
        historical_df=df
    )

    print("\nPrediction:\n")

    for key, value in result.items():
        print(
            f"{key}: {value}"
        )