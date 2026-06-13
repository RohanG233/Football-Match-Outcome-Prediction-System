from src.api.services.prediction_service import (
    prediction_service
)


def test_prediction():

    result = prediction_service.predict(

        "France",

        "England",

        "Final"
    )

    assert (
        "home_win_probability"
        in result
    )

    assert (
        "draw_probability"
        in result
    )

    assert (
        "away_win_probability"
        in result
    )