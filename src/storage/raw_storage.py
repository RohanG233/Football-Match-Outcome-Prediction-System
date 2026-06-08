import pandas as pd

from database.db import engine


class RawDataStorage:

    def save(
        self,
        df: pd.DataFrame
    ):

        df.to_sql(
            name="raw_matches",
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

        print(
            f"{len(df)} rows inserted successfully"
        )