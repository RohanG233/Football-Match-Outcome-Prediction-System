import joblib
import pandas as pd

from pathlib import Path

from src.api.feature_builder import FeatureBuilder
from src.common.model_features import MODEL_FEATURES
from src.api.logger import logger

from src.database.prediction_repository import (
    prediction_repository
)


class PredictionService:

    def __init__(self):

        model_path = Path(
            "src/artifacts/match_outcome_model.joblib"
        )

        if not model_path.exists():
            raise FileNotFoundError(
                "Trained model not found. Train model first."
            )

        self.model = joblib.load(model_path)

    def predict(
        self,
        home_team,
        away_team,
        stage
    ):

        try:
        # Build model features
            features = FeatureBuilder().build(
                home_team=home_team,
                away_team=away_team,
                stage=stage
            )
        
        except ValueError as e:
            raise ValueError(str(e))
        

        # Convert to dataframe
        X = pd.DataFrame([features])

        missing_features = [

            feature
            for feature in MODEL_FEATURES
            if feature not in X.columns
        ]

        if missing_features:

            raise ValueError(
                f"Missing features: {missing_features}"
            )

        # Ensure prediction uses EXACT same
        # feature order as training
        X = X[MODEL_FEATURES]

        # Generate probabilities
        probs = self.model.predict_proba(X)[0]

        logger.info(
            f"Prediction request: "
            f"{home_team} vs {away_team}"
        )

        result = {

            "home_team": home_team,

            "away_team": away_team,

            "stage": stage,

            "home_win_probability": round(
                float(probs[0] * 100),
                2
            ),

            "draw_probability": round(
                float(probs[1] * 100),
                2
            ),

            "away_win_probability": round(
                float(probs[2] * 100),
                2
            )
        }

        prediction_repository.save_prediction(
            result
        )

        return result


prediction_service = PredictionService()