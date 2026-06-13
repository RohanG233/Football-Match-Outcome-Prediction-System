import requests


API_URL = "http://127.0.0.1:8000"


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