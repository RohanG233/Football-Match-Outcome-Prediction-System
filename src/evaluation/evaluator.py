import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    log_loss
)


class MatchOutcomeEvaluator:

    def __init__(self):

        # Load trained model
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

        self.target_mapping = {
            "HomeWin": 0,
            "Draw": 1,
            "AwayWin": 2
        }

    def prepare_data(self, test_df):

        X_test = test_df[
            self.feature_columns
        ]

        y_test = (
            test_df["target"]
            .map(self.target_mapping)
        )

        return X_test, y_test

    def evaluate(
        self,
        X_test,
        y_test
    ):

        predictions = self.model.predict(
            X_test
        )

        probabilities = (
            self.model.predict_proba(
                X_test
            )
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print(
            f"\nTest Accuracy: "
            f"{accuracy:.4f}"
        )

        print(
            "\nClassification Report:\n"
        )

        print(
            classification_report(
                y_test,
                predictions
            )
        )

        print(
            "\nConfusion Matrix:\n"
        )

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        print(
            "\nLog Loss:"
        )

        print(
            log_loss(
                y_test,
                probabilities
            )
        )

        return accuracy