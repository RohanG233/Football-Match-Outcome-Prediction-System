from src.features.feature_store import (
    FeatureStore
)


def test_team_stats():

    store = FeatureStore()

    stats = store.get_team_stats(
        "France"
    )

    assert stats is not None

    assert "matches" in stats

    assert "win_rate" in stats