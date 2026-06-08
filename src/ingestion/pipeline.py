from pathlib import Path

from storage.raw_storage import RawDataStorage
from ingestion.ingestor import CSVIngestor


def run_ingestion():

    # Get project root folder
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

    # Build CSV path safely
    csv_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "world_cup_last_50_years.csv"
    )

    print("CSV Path:", csv_path)

    ingestor = CSVIngestor(csv_path)

    df = ingestor.ingest()

    storage = RawDataStorage()

    storage.save(df)

    print(df.head())

    print("Ingestion completed successfully")