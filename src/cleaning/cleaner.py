import pandas as pd

class DataCleaner:

    def __init__(self, df: pd.DataFrame):
        # Work on a copy so original dataframe
        # is never modified accidentally
        self.df = df.copy()

    def standardize_types(self):
        """
        Convert columns into expected datatypes.
        """
        self.df["year"] = self.df["year"].astype(int)
        self.df["home_goals"] = self.df["home_goals"].astype(int)
        self.df["away_goals"] = self.df["away_goals"].astype(int)
        self.df["match_id"] = self.df["match_id"].astype(int)
        self.df["date"] = pd.to_datetime(
            self.df["date"]
        )

    def trim_whitespace(self):
        """
        Remove leading/trailing spaces from text columns.
        """
        text_columns = [
            "stage",
            "home_team",
            "away_team",
            "winner"
        ]

        for col in text_columns:
            self.df[col] = (
                self.df[col]
                .astype(str)
                .str.strip()
            )

    def standardize_team_names(self):
        """
        Standardize known naming variations.
        """
        team_mapping = {
            "USA": "United States",
        }

        self.df["home_team"] = (
            self.df["home_team"]
            .replace(team_mapping)
        )

        self.df["away_team"] = (
            self.df["away_team"]
            .replace(team_mapping)
        )

    def correct_winner_column(self):
        """
        Recompute winner from score.
        """
        def calculate_winner(row):
            if row["home_goals"] > row["away_goals"]:
                return row["home_team"]
            elif row["away_goals"] > row["home_goals"]:
                return row["away_team"]
            return "Draw"

        self.df["winner"] = (
            self.df.apply(
                calculate_winner,
                axis=1
            )
        )

    def remove_invalid_rows(self):
        """
        Remove impossible football matches.
        """
        self.df = self.df[self.df["home_team"] != self.df["away_team"]]
        self.df = self.df[self.df["home_goals"] >= 0]
        self.df = self.df[self.df["away_goals"] >= 0]

    def remove_duplicates(self):
        """
        Remove duplicate match_ids.
        """
        self.df = self.df.drop_duplicates(subset=["match_id"])

    def handle_missing_values(self):
        """
        Remove rows containing critical nulls.
        """
        critical_columns = [
            "match_id",
            "home_team",
            "away_team",
            "date"
        ]

        self.df = self.df.dropna(subset=critical_columns)

    def clean(self):
        """
        Master cleaning pipeline.
        """
        self.standardize_types()
        self.trim_whitespace()
        self.standardize_team_names()
        self.correct_winner_column()
        self.remove_invalid_rows()
        self.remove_duplicates()
        self.handle_missing_values()
        return self.df