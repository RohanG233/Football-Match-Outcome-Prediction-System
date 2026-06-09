import pandas as pd

class DataSplitter:

    def __init__(self, df):

        # Work on copy
        self.df = df.copy()

        # Ensure date is datetime
        self.df["date"] = pd.to_datetime(
            self.df["date"]
        )

        # Sort chronologically
        self.df = (
            self.df
            .sort_values("date")
            .reset_index(drop=True)
        )

    def split(
        self,
        train_size=0.70,
        validation_size=0.15
    ):
        """
        Create train / validation / test splits.

        Example:

        First 70%  -> train
        Next 15%   -> validation
        Last 15%   -> test
        """

        total_rows = len(self.df)

        train_end = int(
            total_rows * train_size
        )

        validation_end = int(
            total_rows *
            (train_size + validation_size)
        )

        # Default all rows to test
        self.df["dataset_split"] = "test"

        # First chunk
        self.df.loc[
            :train_end - 1,
            "dataset_split"
        ] = "train"

        # Middle chunk
        self.df.loc[
            train_end:validation_end - 1,
            "dataset_split"
        ] = "validation"

        return self.df