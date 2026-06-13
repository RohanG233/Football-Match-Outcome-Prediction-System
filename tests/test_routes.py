from fastapi.testclient import (
    TestClient
)

from src.api.app import app

def test_health():

    response = client.get(
        "/health"
    )

    assert (
        response.status_code
        == 200
    )

def test_teams():

    response = client.get(
        "/teams"
    )

    assert (
        response.status_code
        == 200
    )

def test_predict():

    response = client.post(

        "/predict",

        json={

            "home_team":
            "France",

            "away_team":
            "England",

            "stage":
            "Final"
        }
    )

    assert (
        response.status_code
        == 200
    )

def test_invalid_team():

    response = client.post(

        "/predict",

        json={

            "home_team":
            "Mars FC",

            "away_team":
            "England",

            "stage":
            "Final"
        }
    )

    assert (
        response.status_code
        == 400
    )

def test_invalid_stage():

    response = client.post(

        "/predict",

        json={

            "home_team":
            "France",

            "away_team":
            "England",

            "stage":
            "Moon Final"
        }
    )

    assert (
        response.status_code
        in [400,422]
    )





client = TestClient(app)