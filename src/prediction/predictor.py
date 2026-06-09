import joblib
import pandas as pd


class MatchPredictor:

    def __init__(self):

        self.model = joblib.load(
            "src/artifacts/match_outcome_model.joblib"
        )

        self.feature_columns = [

            "stage_encoded",

            "is_knockout",
            "is_semi_final",
            "is_final",

            "home_matches_played",
            "away_matches_played",

            "experience_diff",

            "home_win_rate",
            "away_win_rate",

            "home_recent_form",
            "away_recent_form",

            "home_avg_goals_scored",
            "away_avg_goals_scored",

            "home_avg_goals_conceded",
            "away_avg_goals_conceded",

            "h2h_home_wins",
            "h2h_away_wins",
            "h2h_matches",

            "win_rate_diff",
            "form_diff",
            "scoring_diff",
            "defense_diff",
            "h2h_diff"
        ]

        self.class_mapping = {
            0: "HomeWin",
            1: "Draw",
            2: "AwayWin"
        }

    def predict(
        self,
        home_team,
        away_team,
        stage,
        historical_df
    ):

        # --------------------------
        # Home team historical stats
        # --------------------------

        home_matches = historical_df[
            (historical_df["home_team"] == home_team)
            |
            (historical_df["away_team"] == home_team)
        ]

        away_matches = historical_df[
            (historical_df["home_team"] == away_team)
            |
            (historical_df["away_team"] == away_team)
        ]

        home_matches_played = len(
            home_matches
        )

        away_matches_played = len(
            away_matches
        )

        # --------------------------
        # Win rates
        # --------------------------

        home_win_rate = (
            (home_matches["winner"] == home_team)
            .mean()
        )

        away_win_rate = (
            (away_matches["winner"] == away_team)
            .mean()
        )

        # --------------------------
        # Goals scored
        # --------------------------

        home_avg_goals_scored = (
            home_matches["home_goals"]
            .mean()
        )

        away_avg_goals_scored = (
            away_matches["away_goals"]
            .mean()
        )

        # --------------------------
        # Goals conceded
        # --------------------------

        home_avg_goals_conceded = (
            home_matches["away_goals"]
            .mean()
        )

        away_avg_goals_conceded = (
            away_matches["home_goals"]
            .mean()
        )

        # --------------------------
        # H2H
        # --------------------------

        h2h = historical_df[
            (
                (historical_df["home_team"] == home_team)
                &
                (historical_df["away_team"] == away_team)
            )
            |
            (
                (historical_df["home_team"] == away_team)
                &
                (historical_df["away_team"] == home_team)
            )
        ]

        h2h_matches = len(h2h)

        h2h_home_wins = (
            h2h["winner"] == home_team
        ).sum()

        h2h_away_wins = (
            h2h["winner"] == away_team
        ).sum()

        # --------------------------
        # Stage encoding
        # --------------------------

        stage_encoded = {
            "Group Stage": 0,
            "Round of 16": 1,
            "Quarter Finals": 2,
            "Semi Finals": 3,
            "Final": 4
        }.get(stage, 0)

        # --------------------------
        # Feature Row
        # --------------------------

        feature_row = {

            "stage_encoded": stage_encoded,

            "is_knockout":
                int(stage != "Group Stage"),

            "is_semi_final":
                int(stage == "Semi Finals"),

            "is_final":
                int(stage == "Final"),

            "home_matches_played":
                home_matches_played,

            "away_matches_played":
                away_matches_played,

            "experience_diff":
                home_matches_played
                -
                away_matches_played,

            "home_win_rate":
                home_win_rate,

            "away_win_rate":
                away_win_rate,

            "home_recent_form":
                home_win_rate,

            "away_recent_form":
                away_win_rate,

            "home_avg_goals_scored":
                home_avg_goals_scored,

            "away_avg_goals_scored":
                away_avg_goals_scored,

            "home_avg_goals_conceded":
                home_avg_goals_conceded,

            "away_avg_goals_conceded":
                away_avg_goals_conceded,

            "h2h_home_wins":
                h2h_home_wins,

            "h2h_away_wins":
                h2h_away_wins,

            "h2h_matches":
                h2h_matches,

            "win_rate_diff":
                home_win_rate
                -
                away_win_rate,

            "form_diff":
                home_win_rate
                -
                away_win_rate,

            "scoring_diff":
                home_avg_goals_scored
                -
                away_avg_goals_scored,

            "defense_diff":
                away_avg_goals_conceded
                -
                home_avg_goals_conceded,

            "h2h_diff":
                h2h_home_wins
                -
                h2h_away_wins
        }

        X = pd.DataFrame(
            [feature_row]
        )

        probabilities = (
            self.model.predict_proba(X)
        )[0]

        return {

            "home_team": home_team,

            "away_team": away_team,

            "home_win_probability":
                round(
                    probabilities[0] * 100,
                    2
                ),

            "draw_probability":
                round(
                    probabilities[1] * 100,
                    2
                ),

            "away_win_probability":
                round(
                    probabilities[2] * 100,
                    2
                )
        }