from pathlib import Path
from fastapi import APIRouter, HTTPException
from src.api.services.team_service import TeamService
from src.api.services.prediction_service import prediction_service
from src.api.schemas import (
    PredictRequest,
    PredictResponse
)

from src.database.prediction_repository import (
    prediction_repository
)

router = APIRouter()

@router.get("/health")
def health():

    return {
        "status": "healthy"
    }

@router.get("/")
def root():
    return {
        "message": "FIFA Match Predictor API is running"
    }

@router.get("/health")
def health():
    model_exists = Path(
        "src/artifacts/match_outcome_model.joblib"
    ).exists()

    return {
        "status": "healthy",
        "model_exists": model_exists
    }

@router.get("/teams")
def get_teams():

    teams = TeamService.get_all_teams()

    return {
        "count": len(teams),
        "teams": teams
    }

@router.post("/predict")
def predict(request: PredictRequest):

    try:

        result = prediction_service.predict(
            request.home_team,
            request.away_team,
            request.stage
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/model-info")
def model_info():

    return {

        "model_type": "XGBoost",

        "target": "Match Outcome",

        "classes": [
            "Home Win",
            "Draw",
            "Away Win"
        ]
    }

@router.get("/predictions")
def get_predictions(
    limit: int = 50
):

    data = (
        prediction_repository
        .get_predictions(limit)
    )

    return data.to_dict(
        orient="records"
    )


@router.get("/prediction-stats")
def prediction_stats():

    return (
        prediction_repository
        .get_prediction_stats()
    )

@router.get(
    "/predictions/{prediction_id}"
)
def get_prediction(
    prediction_id: int
):

    result = (
        prediction_repository
        .get_prediction_by_id(
            prediction_id
        )
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return result