from fastapi import FastAPI
from src.api.routes import router



app = FastAPI(
    title="FIFA Match Predictor API",
    description="Predict FIFA World Cup match outcomes",
    version="1.0.0"
)

app.include_router(router)