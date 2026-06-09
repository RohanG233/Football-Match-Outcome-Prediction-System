import pandas as pd
import joblib

from database.db import engine

from training.trainer import (
    MatchOutcomeTrainer
)


def run_training():

    print(
        "\nLoading match features..."
    )

    df = pd.read_sql(
        "SELECT * FROM match_features",
        engine
    )

    train_df = df[
        df["dataset_split"] == "train"
    ]

    validation_df = df[
        df["dataset_split"] == "validation"
    ]

    test_df = df[
        df["dataset_split"] == "test"
    ]

    print(
        f"Train Rows: {len(train_df)}"
    )

    print(
        f"Validation Rows: "
        f"{len(validation_df)}"
    )

    print(
        f"Test Rows: {len(test_df)}"
    )

    trainer = MatchOutcomeTrainer()

    (
        X_train,
        y_train,
        X_validation,
        y_validation
    ) = trainer.prepare_data(
        train_df,
        validation_df
    )

    trainer.train(
        X_train,
        y_train
    )

    trainer.evaluate(
        X_validation,
        y_validation
    )

    joblib.dump(
        trainer.model,
        "src/artifacts/match_outcome_model.joblib"
    )

    print(
        "\nModel saved successfully."
    )