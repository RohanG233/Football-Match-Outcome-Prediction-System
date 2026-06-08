from pathlib import Path
import pandas as pd


class CSVIngestor:
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def ingest(self) -> pd.DataFrame:

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"{self.file_path} does not exist"
            )

        df = pd.read_csv(self.file_path)

        if df.empty:
            raise ValueError(
                "CSV file is empty"
            )

        return df