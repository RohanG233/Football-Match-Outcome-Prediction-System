import requests
import os

API_URL = os.getenv(
    "API_URL",
    "https://football-match-outcome-prediction-system.onrender.com"
)


class APIClient:

    @staticmethod
    def get_teams():

        response = requests.get(
            f"{API_URL}/teams"
        )

        response.raise_for_status()

        return response.json()["teams"]

    @staticmethod
    def predict(
        home_team,
        away_team,
        stage
    ):

        response = requests.post(

            f"{API_URL}/predict",

            json={
                "home_team": home_team,
                "away_team": away_team,
                "stage": stage
            }
        )

        response.raise_for_status()

        return response.json()