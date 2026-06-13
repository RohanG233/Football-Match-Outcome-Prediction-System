from src.database.prediction_repository import (
    prediction_repository
)


def test_prediction_stats():

    stats = (
        prediction_repository
        .get_prediction_stats()
    )

    assert (
        "total_predictions"
        in stats
    )