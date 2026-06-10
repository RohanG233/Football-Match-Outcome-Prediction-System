from pathlib import Path
from fastapi import APIRouter, HTTPException
from src.api.services.team_service import TeamService
from src.api.services.prediction_service import prediction_service
from src.api.schemas import (
    PredictRequest,
    PredictResponse
)

router = APIRouter()


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