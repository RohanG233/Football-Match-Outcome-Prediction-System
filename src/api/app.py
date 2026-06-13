from fastapi import FastAPI
from src.api.routes import router
from src.api.exceptions import (
    value_error_handler
)

app = FastAPI(
    title="Football Match Outcome Prediction System",
    description="Predict a National Football Match Outcomes",
    version="1.0.0"
)

app.add_exception_handler(
    ValueError,
    value_error_handler
)

app.include_router(router)