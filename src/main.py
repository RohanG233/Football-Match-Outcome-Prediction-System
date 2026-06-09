from ingestion.pipeline import run_ingestion
from validation.pipeline import run_validation
from cleaning.pipeline import run_cleaning
from feature_engineering.pipeline import run_feature_engineering
from splitting.pipeline import run_splitting
from training.pipeline import run_training
from evaluation.pipeline import run_evaluation
from prediction.pipeline import run_prediction

PIPELINES = {
    "ingestion": run_ingestion,
    "validation": run_validation,
    "cleaning": run_cleaning,
    "feature_engineering": run_feature_engineering,
    "splitting": run_splitting,
    "training": run_training,
    "evaluation": run_evaluation,
    "prediction": run_prediction
}

def main():

    # Choose which pipeline to run
    pipeline_name = "prediction"

    if pipeline_name not in PIPELINES:
        raise ValueError(
            f"Unknown pipeline: {pipeline_name}"
        )

    PIPELINES[pipeline_name]()


if __name__ == "__main__":
    main()