from validation.validator import DataValidator
from database.db import engine
import pandas as pd

def run_validation():

    # STEP 1: Load raw data directly from Supabase (Postgres)
    # This avoids dependency on ingestion step
    df = pd.read_sql(
        "SELECT * FROM raw_matches",
        engine
    )

    # STEP 2: Initialize validator with DB data
    validator = DataValidator(df)

    # STEP 3: Run all validation rules
    errors = validator.validate()

    # STEP 4: If any validation errors exist, stop pipeline
    if errors:

        print("\nVALIDATION FAILED\n")

        # Print all errors for debugging
        for error in errors:
            print(error)

        # Hard stop pipeline (important in ML pipelines)
        raise Exception("Validation failed.")

    # STEP 5: Success message
    print("\nVALIDATION PASSED\n")

    # STEP 6: Return validated dataframe for next stage
    return df