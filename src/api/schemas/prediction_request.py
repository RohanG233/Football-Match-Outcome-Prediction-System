from pydantic import BaseModel, Field
from typing import Literal

stage: Literal[
    "Group Stage",
    "Round of 16",
    "Quarter-finals",
    "Semi-finals",
    "Final"
]

class PredictionRequest(BaseModel):

    home_team: str = Field(
        min_length=1,
        max_length=100
    )

    away_team: str = Field(
        min_length=1,
        max_length=100
    )

    stage: str