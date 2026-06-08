from ingestion.pipeline import run_ingestion
from validation.pipeline import run_validation

PIPELINES = {
    "ingestion": run_ingestion,
    "validation": run_validation,
}

def main():

    # Choose which pipeline to run
    pipeline_name = "validation"

    if pipeline_name not in PIPELINES:
        raise ValueError(
            f"Unknown pipeline: {pipeline_name}"
        )

    PIPELINES[pipeline_name]()


if __name__ == "__main__":
    main()