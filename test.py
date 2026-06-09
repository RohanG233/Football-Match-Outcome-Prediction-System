import pandas as pd
from src.database.db import engine

table_name = "clean_matches"

df = pd.read_sql(
    f"SELECT * FROM match_features LIMIT 1",
    engine
)

print("Columns:")
for col in df.columns:
    print(col)