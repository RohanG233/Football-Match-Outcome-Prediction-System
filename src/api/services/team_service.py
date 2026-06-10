import pandas as pd

from src.database.db import engine


class TeamService:

    @staticmethod
    def get_all_teams():

        query = """
        SELECT DISTINCT home_team
        FROM match_features
        """

        home_teams = pd.read_sql(
            query,
            engine
        )

        query = """
        SELECT DISTINCT away_team
        FROM match_features
        """

        away_teams = pd.read_sql(
            query,
            engine
        )

        teams = set(
            home_teams["home_team"]
        ).union(
            set(
                away_teams["away_team"]
            )
        )

        return sorted(
            list(teams)
        )