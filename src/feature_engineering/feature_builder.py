import pandas as pd
from collections import defaultdict


class FeatureBuilder:

    def __init__(self, df):

        # Work on a copy to avoid modifying original dataframe
        self.df = df.copy()

        # Convert date to datetime for chronological calculations
        self.df["date"] = pd.to_datetime(self.df["date"])

        # Sort by date so historical features only use past matches
        self.df = self.df.sort_values("date").reset_index(drop=True)

    def create_target(self):
        """
        Create model label.
        """

        def get_target(row):

            if row["winner"] == "Draw":
                return "Draw"

            if row["winner"] == row["home_team"]:
                return "HomeWin"

            return "AwayWin"

        self.df["target"] = self.df.apply(
            get_target,
            axis=1
        )

    def create_stage_features(self):
        """
        Convert tournament stages into model-friendly numbers.
        """

        stage_mapping = {
            "Group Stage": 1,
            "Round of 16": 2,
            "Quarter-finals": 3,
            "Semi-finals": 4,
            "Final": 5
        }

        self.df["stage_encoded"] = (
            self.df["stage"]
            .map(stage_mapping)
            .fillna(0)
        )

        self.df["is_knockout"] = (
            self.df["stage_encoded"] > 1
        ).astype(int)

        self.df["is_semi_final"] = (
            self.df["stage"] == "Semi-finals"
        ).astype(int)

        self.df["is_final"] = (
            self.df["stage"] == "Final"
        ).astype(int)

    def create_experience_features(self):
        """
        Count matches played before current match.
        """

        matches_played = defaultdict(int)

        home_experience = []
        away_experience = []

        for _, row in self.df.iterrows():

            home_team = row["home_team"]
            away_team = row["away_team"]

            home_experience.append(
                matches_played[home_team]
            )

            away_experience.append(
                matches_played[away_team]
            )

            matches_played[home_team] += 1
            matches_played[away_team] += 1

        self.df["home_matches_played"] = home_experience
        self.df["away_matches_played"] = away_experience

        self.df["experience_diff"] = (
            self.df["home_matches_played"]
            -
            self.df["away_matches_played"]
        )

    def create_win_rate_features(self):
        """
        Historical win rate before current match.
        """

        stats = defaultdict(
            lambda: {
                "wins": 0,
                "matches": 0
            }
        )

        home_rates = []
        away_rates = []

        for _, row in self.df.iterrows():

            home = row["home_team"]
            away = row["away_team"]

            home_matches = stats[home]["matches"]
            away_matches = stats[away]["matches"]

            home_rates.append(
                stats[home]["wins"] / home_matches
                if home_matches > 0
                else 0.5
            )

            away_rates.append(
                stats[away]["wins"] / away_matches
                if away_matches > 0
                else 0.5
            )

            stats[home]["matches"] += 1
            stats[away]["matches"] += 1

            if row["winner"] == home:
                stats[home]["wins"] += 1

            elif row["winner"] == away:
                stats[away]["wins"] += 1

        self.df["home_win_rate"] = home_rates
        self.df["away_win_rate"] = away_rates

    def create_recent_form_features(self):
        """
        Last 5 match performance.
        """

        history = defaultdict(list)

        home_form = []
        away_form = []

        for _, row in self.df.iterrows():

            home = row["home_team"]
            away = row["away_team"]

            home_form.append(
                sum(history[home][-5:])
            )

            away_form.append(
                sum(history[away][-5:])
            )

            if row["winner"] == home:
                history[home].append(3)
                history[away].append(0)

            elif row["winner"] == away:
                history[away].append(3)
                history[home].append(0)

            else:
                history[home].append(1)
                history[away].append(1)

        self.df["home_recent_form"] = home_form
        self.df["away_recent_form"] = away_form

    def create_goal_statistics_features(self):
        """
        Historical scoring and defensive strength.
        """

        goals_scored = defaultdict(list)
        goals_conceded = defaultdict(list)

        home_attack = []
        away_attack = []

        home_defense = []
        away_defense = []

        for _, row in self.df.iterrows():

            home = row["home_team"]
            away = row["away_team"]

            home_attack.append(
                sum(goals_scored[home]) / len(goals_scored[home])
                if goals_scored[home]
                else 0
            )

            away_attack.append(
                sum(goals_scored[away]) / len(goals_scored[away])
                if goals_scored[away]
                else 0
            )

            home_defense.append(
                sum(goals_conceded[home]) / len(goals_conceded[home])
                if goals_conceded[home]
                else 0
            )

            away_defense.append(
                sum(goals_conceded[away]) / len(goals_conceded[away])
                if goals_conceded[away]
                else 0
            )

            goals_scored[home].append(row["home_goals"])
            goals_conceded[home].append(row["away_goals"])

            goals_scored[away].append(row["away_goals"])
            goals_conceded[away].append(row["home_goals"])

        self.df["home_avg_goals_scored"] = home_attack
        self.df["away_avg_goals_scored"] = away_attack

        self.df["home_avg_goals_conceded"] = home_defense
        self.df["away_avg_goals_conceded"] = away_defense

    def create_head_to_head_features(self):
        """
        Historical meetings between teams.
        """

        h2h = defaultdict(
            lambda: {
                "home_wins": 0,
                "away_wins": 0,
                "matches": 0
            }
        )

        home_h2h = []
        away_h2h = []
        matches = []

        for _, row in self.df.iterrows():

            key = tuple(
                sorted([
                    row["home_team"],
                    row["away_team"]
                ])
            )

            home_h2h.append(h2h[key]["home_wins"])
            away_h2h.append(h2h[key]["away_wins"])
            matches.append(h2h[key]["matches"])
            
            h2h[key]["matches"] += 1

            if row["winner"] == row["home_team"]:
                h2h[key]["home_wins"] += 1

            elif row["winner"] == row["away_team"]:
                h2h[key]["away_wins"] += 1

        self.df["h2h_home_wins"] = home_h2h
        self.df["h2h_away_wins"] = away_h2h
        self.df["h2h_matches"] = matches

    def create_difference_features(self):
        """
        Relative team strength features.
        """
        self.df["win_rate_diff"] = (self.df["home_win_rate"] - self.df["away_win_rate"])
        self.df["form_diff"] = (self.df["home_recent_form"] - self.df["away_recent_form"])
        self.df["scoring_diff"] = (self.df["home_avg_goals_scored"] - self.df["away_avg_goals_scored"])
        self.df["defense_diff"] = (self.df["home_avg_goals_conceded"] -self.df["away_avg_goals_conceded"])
        self.df["h2h_diff"] = (self.df["h2h_home_wins"] - self.df["h2h_away_wins"])

    def build_features(self):
        self.create_target()
        self.create_stage_features()
        self.create_experience_features()
        self.create_win_rate_features()
        self.create_recent_form_features()
        self.create_goal_statistics_features()
        self.create_head_to_head_features()
        self.create_difference_features()
        return self.df