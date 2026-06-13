from src.api.feature_builder import (
    FeatureBuilder
)


def test_feature_creation():

    builder = FeatureBuilder()

    features = builder.build(

        "France",

        "England",

        "Final"
    )

    assert features is not None

    assert (
        "home_win_rate"
        in features
    )

    assert (
        "away_win_rate"
        in features
    )