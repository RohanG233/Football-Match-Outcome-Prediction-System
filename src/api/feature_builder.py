from src.features.feature_store import FeatureStore


class FeatureBuilder:

    def __init__(self):

        self.store = FeatureStore()

    def build(
        self,
        home_team,
        away_team,
        stage,
        match_date=None
    ):

        home_stats = self.store.get_team_stats(
            home_team,
            before_date=match_date
        )

        if home_stats is None:
            raise ValueError(
                f"No historical data found for team: {home_team}"
            )

        away_stats = self.store.get_team_stats(
            away_team,
            before_date=match_date
        )

        if away_stats is None:
            raise ValueError(
                f"No historical data found for team: {away_team}"
            )

        h2h_stats = self.store.get_head_to_head_stats(
            home_team,
            away_team,
            before_date=match_date
        )

        return {

            # Tournament stage features
            "stage_encoded": self._encode_stage(stage),

            "is_knockout": int(
                stage != "Group Stage"
            ),

            "is_semi_final": int(
                stage == "Semi-finals"
            ),

            "is_final": int(
                stage == "Final"
            ),

            # Experience features
            "home_matches_played": home_stats["matches"],
            "away_matches_played": away_stats["matches"],

            "experience_diff": (
                home_stats["matches"]
                -
                away_stats["matches"]
            ),

            # Win rate features
            "home_win_rate": home_stats["win_rate"],
            "away_win_rate": away_stats["win_rate"],

            # Recent form features
            "home_recent_form": home_stats["recent_form"],
            "away_recent_form": away_stats["recent_form"],

            # Goal scoring features
            "home_avg_goals_scored": (
                home_stats["avg_goals_scored"]
            ),

            "away_avg_goals_scored": (
                away_stats["avg_goals_scored"]
            ),

            # Defensive features
            "home_avg_goals_conceded": (
                home_stats["avg_goals_conceded"]
            ),

            "away_avg_goals_conceded": (
                away_stats["avg_goals_conceded"]
            ),

            # Head-to-head features
            "h2h_home_wins": (
                h2h_stats["home_wins"]
            ),

            "h2h_away_wins": (
                h2h_stats["away_wins"]
            ),

            "h2h_matches": (
                h2h_stats["matches"]
            ),

            # Difference features
            "win_rate_diff": (
                home_stats["win_rate"]
                -
                away_stats["win_rate"]
            ),

            "form_diff": (
                home_stats["recent_form"]
                -
                away_stats["recent_form"]
            ),

            "scoring_diff": (
                home_stats["avg_goals_scored"]
                -
                away_stats["avg_goals_scored"]
            ),

            "defense_diff": (
                home_stats["avg_goals_conceded"]
                -
                away_stats["avg_goals_conceded"]
            ),

            "h2h_diff": (
                h2h_stats["home_wins"]
                -
                h2h_stats["away_wins"]
            )
        }

    def _encode_stage(self, stage):

        mapping = {
            "Group Stage": 1,
            "Round of 16": 2,
            "Quarter-finals": 3,
            "Semi-finals": 4,
            "Final": 5
        }

        return mapping.get(stage, 0)