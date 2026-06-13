import pandas as pd

from datetime import datetime

from src.database.db import engine


class PredictionRepository:

    TABLE_NAME = "predictions"

    def save_prediction(
        self,
        prediction
    ):

        row = pd.DataFrame([{

            "home_team":
            prediction["home_team"],

            "away_team":
            prediction["away_team"],

            "stage":
            prediction["stage"],

            "home_win_probability":
            prediction["home_win_probability"],

            "draw_probability":
            prediction["draw_probability"],

            "away_win_probability":
            prediction["away_win_probability"],

            "created_at":
            datetime.utcnow()
        }])

        row.to_sql(
            self.TABLE_NAME,
            engine,
            if_exists="append",
            index=False
        )

    def get_predictions(
        self,
        limit=50
    ):

        query = f"""
        SELECT *
        FROM {self.TABLE_NAME}
        ORDER BY created_at DESC
        LIMIT {limit}
        """

        return pd.read_sql(
            query,
            engine
        )

    def get_prediction_stats(self):

        query = """
        SELECT COUNT(*) as total_predictions
        FROM predictions
        """

        result = pd.read_sql(
            query,
            engine
        )

        return {
            "total_predictions":
            int(
                result.iloc[0][
                    "total_predictions"
                ]
            )
        }
    
    def get_prediction_by_id(
        self,
        prediction_id
    ):

        query = f"""
        SELECT *
        FROM predictions
        WHERE id = {prediction_id}
        """

        result = pd.read_sql(
            query,
            engine
        )

        if len(result) == 0:
            return None

        return result.iloc[0].to_dict()


prediction_repository = (
    PredictionRepository()
)