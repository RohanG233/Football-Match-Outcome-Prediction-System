fifa_predictor/

├── configs/
│ ├── database.yaml
│ ├── model.yaml
│ └── features.yaml
│
├── data/
│ ├── raw/
│ ├── validated/
│ ├── cleaned/
│ └── features/
│
├── src/
│
│ ├── ingestion/
│ │ ├── api_loader.py
│ │ ├── csv_loader.py
│ │ └── ingest_pipeline.py
│ │
│ ├── validation/
│ │ ├── schema_validator.py
│ │ ├── null_validator.py
│ │ └── validation_pipeline.py
│ │
│ ├── cleaning/
│ │ ├── clean_matches.py
│ │ ├── clean_players.py
│ │ └── cleaning_pipeline.py
│ │
│ ├── database/
│ │ ├── connection.py
│ │ ├── models.py
│ │ ├── raw_repository.py
│ │ ├── feature_repository.py
│ │ └── prediction_repository.py
│ │
│ ├── features/
│ │ ├── team_features.py
│ │ ├── player_features.py
│ │ ├── match_features.py
│ │ └── feature_pipeline.py
│ │
│ ├── training/
│ │ ├── split_data.py
│ │ ├── train_xgboost.py
│ │ ├── train_random_forest.py
│ │ └── training_pipeline.py
│ │
│ ├── evaluation/
│ │ ├── metrics.py
│ │ ├── model_comparison.py
│ │ └── evaluation_pipeline.py
│ │
│ ├── registry/
│ │ ├── mlflow_logger.py
│ │ └── model_registry.py
│ │
│ └── prediction/
│ ├── feature_builder.py
│ ├── predictor.py
│ └── cache.py
│
├── models/
│ ├── xgboost/
│ └── champion/
│
├── notebooks/
│
├── tests/
│ ├── test_ingestion.py
│ ├── test_validation.py
│ ├── test_cleaning.py
│ ├── test_features.py
│ ├── test_training.py
│ └── test_prediction.py
│
├── scripts/
│ ├── run_ingestion.py
│ ├── run_features.py
│ ├── run_training.py
│ └── run_evaluation.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
