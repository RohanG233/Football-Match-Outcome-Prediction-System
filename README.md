# Football Match Outcome Prediction System

## Overview

Football Match Outcome Prediction System is an end-to-end machine learning project that predicts the probability of a Home Win, Draw, or Away Win for international football matches.

The project follows a production-style ML workflow including data ingestion, validation, cleaning, feature engineering, model training, evaluation, prediction serving through FastAPI, and a Streamlit user interface.

App Demo : https://football-match-outcome-prediction-system-f9bnntbwjdmxpufw8g3w5.streamlit.app/

---

## Problem Statement

Predicting football match outcomes is a multi-class classification problem where the objective is to estimate the probability of:

- Home Win
- Draw
- Away Win

The system uses historical FIFA World Cup match data to learn team performance patterns and generate predictions.

---

## Features

- Automated data ingestion pipeline
- Data validation and quality checks
- Data cleaning pipeline
- Feature engineering pipeline
- XGBoost model training
- Model evaluation and comparison
- FastAPI prediction service
- Swagger API documentation
- Streamlit web interface
- PostgreSQL data storage

---

## Project Architecture

CSV / API Data
↓
Data Ingestion
↓
Data Validation
↓
Data Cleaning
↓
Feature Engineering
↓
Model Training
↓
Model Evaluation
↓
Saved Model
↓
FastAPI
↓
Streamlit UI

---

## Tech Stack

### Machine Learning

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost

### Backend

- FastAPI
- Uvicorn

### Database

- PostgreSQL
- SQLAlchemy

### Frontend

- Streamlit

### Deployment

- GitHub
- Render
- Streamlit Cloud

---

## Feature Engineering

The model uses historical match information to create features such as:

- Team experience
- Historical win rate
- Recent form
- Goals scored
- Goals conceded
- Head-to-head statistics
- Tournament stage information

These features help the model understand team strength before a match is played.

---

## Model Training

Algorithm used:

- XGBoost Classifier

Target Classes:

- HomeWin
- Draw
- AwayWin

The dataset is split into training and testing sets before model training.

---

## API Endpoints

### Health Check

GET /health

### Teams

GET /teams

Returns all available teams.

### Prediction

POST /predict

Request:

{
"home_team": "France",
"away_team": "England",
"stage": "Final"
}

Response:

{
"home_win_probability": 49.53,
"draw_probability": 19.84,
"away_win_probability": 30.63
}

---

## Streamlit UI

The Streamlit application provides a user-friendly interface where users can:

- Select teams
- Select tournament stage
- Generate predictions
- View outcome probabilities

---

## Installation

Clone repository:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Run FastAPI:

uvicorn src.api.app:app --reload

Run Streamlit:

streamlit run app.py

---

## Results

The model predicts probabilities for:

- Home Win
- Draw
- Away Win

Example:

France vs England

Home Win: 49.53%
Draw: 19.84%
Away Win: 30.63%

---

## Learning Outcomes

Through this project, I gained experience in:

- Data engineering pipelines
- Feature engineering
- Machine learning workflows
- Model evaluation
- REST API development
- Database integration
- Full-stack ML application development

---

## Future Improvements

- Redis caching
- Docker support
- CI/CD pipeline
- Automated retraining
- Model monitoring
- Hyperparameter optimization
- Ensemble models
- Advanced football analytics features

---


## Author

Rohan
