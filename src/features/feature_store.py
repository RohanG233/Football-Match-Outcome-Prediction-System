import pandas as pd
from src.database.db import engine


class FeatureStore:

    def __init__(self):

        # Load precomputed match features once
        self.df = pd.read_sql(
            "SELECT * FROM match_features",
            engine
        )

        # Ensure datetime ordering for correctness
        self.df["date"] = pd.to_datetime(self.df["date"])

        self.df = self.df.sort_values("date")
    

    def get_team_stats(self, team, before_date=None):

        data = self.df[self.df["date"] < before_date] if before_date else self.df

        team_data = data[
            (data["home_team"] == team) |
            (data["away_team"] == team)
        ]

        if len(team_data) == 0:
            return self._default_stats()

        wins = len(team_data[team_data["winner"] == team])

        matches = len(team_data)

        goals_scored = (
            team_data.apply(
                lambda x:
                    x["home_goals"] if x["home_team"] == team
                    else x["away_goals"],
                axis=1
            ).sum()
        )

        goals_conceded = (
            team_data.apply(
                lambda x:
                    x["away_goals"] if x["home_team"] == team
                    else x["home_goals"],
                axis=1
            ).sum()
        )

        recent_matches = team_data.tail(5)

        recent_form = 0

        for _, row in recent_matches.iterrows():

            if row["winner"] == team:
                recent_form += 3

            elif row["winner"] == "Draw":
                recent_form += 1

        return {
            "matches": matches,
            "win_rate": wins / matches,
            "avg_goals_scored": goals_scored / matches,
            "avg_goals_conceded": goals_conceded / matches,
            "recent_form": recent_form
        }

    def get_head_to_head_stats(
        self,
        home_team,
        away_team,
        before_date=None
    ):

        data = (
            self.df[self.df["date"] < before_date]
            if before_date
            else self.df
        )

        h2h = data[
            (
                (data["home_team"] == home_team) &
                (data["away_team"] == away_team)
            )
            |
            (
                (data["home_team"] == away_team) &
                (data["away_team"] == home_team)
            )
        ]

        if len(h2h) == 0:
            return {
                "home_wins": 0,
                "away_wins": 0,
                "matches": 0
            }

        home_wins = len(
            h2h[h2h["winner"] == home_team]
        )

        away_wins = len(
            h2h[h2h["winner"] == away_team]
        )

        return {
            "home_wins": home_wins,
            "away_wins": away_wins,
            "matches": len(h2h)
        }

    def _default_stats(self):

        return {
            "matches": 0,
            "win_rate": 0.5,
            "avg_goals_scored": 1.2,
            "avg_goals_conceded": 1.2,
            "recent_form": 0
        }