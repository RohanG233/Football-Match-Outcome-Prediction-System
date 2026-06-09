import pandas as pd

from database.db import engine

from evaluation.evaluator import (
    MatchOutcomeEvaluator
)


def run_evaluation():

    print(
        "\nLoading match features..."
    )

    df = pd.read_sql(
        "SELECT * FROM match_features",
        engine
    )

    test_df = df[
        df["dataset_split"] == "test"
    ]

    print(
        f"Test Rows: {len(test_df)}"
    )

    evaluator = (
        MatchOutcomeEvaluator()
    )

    X_test, y_test = (
        evaluator.prepare_data(
            test_df
        )
    )

    evaluator.evaluate(
        X_test,
        y_test
    )