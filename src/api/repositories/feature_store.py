import pandas as pd

from src.database.db import engine


class FeatureStore:

    @staticmethod
    def get_latest_team_stats(team_name):
        """
        Retrieve the latest feature row available
        for a given team.
        """

        query = """
        SELECT *
        FROM match_features
        WHERE home_team = %(team)s
           OR away_team = %(team)s
        ORDER BY date DESC
        LIMIT 1
        """

        df = pd.read_sql(
            query,
            engine,
            params={
                "team": team_name
            }
        )

        if df.empty:
            return None

        return df.iloc[0]