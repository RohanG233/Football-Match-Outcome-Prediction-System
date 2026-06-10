from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report
)

from common.model_features import MODEL_FEATURES

class MatchOutcomeTrainer:

    def __init__(self):

        # Features that are available BEFORE kickoff
        self.feature_columns = MODEL_FEATURES

        # Multi-class classifier
        self.model = XGBClassifier(

            objective="multi:softprob",

            num_class=3,

            n_estimators=300,

            max_depth=6,

            learning_rate=0.05,

            subsample=0.8,

            colsample_bytree=0.8,

            random_state=42,

            eval_metric="mlogloss"
        )

    def prepare_data(self, train_df, validation_df):

        # Convert string labels into numbers
        self.target_mapping = {
            "HomeWin": 0,
            "Draw": 1,
            "AwayWin": 2
        }

        # Reverse mapping for future predictions
        self.reverse_mapping = {
            0: "HomeWin",
            1: "Draw",
            2: "AwayWin"
        }

        # Select training features
        X_train = train_df[
            self.feature_columns
        ]

        # Encode target column
        y_train = (
            train_df["target"]
            .map(self.target_mapping)
        )

        # Select validation features
        X_validation = validation_df[
            self.feature_columns
        ]

        # Encode validation target
        y_validation = (
            validation_df["target"]
            .map(self.target_mapping)
        )

        # Check for unexpected target values
        if y_train.isnull().any():
            raise ValueError(
                "Unknown target value found in training set."
            )

        if y_validation.isnull().any():
            raise ValueError(
                "Unknown target value found in validation set."
            )

        return (
            X_train,
            y_train,
            X_validation,
            y_validation
        )

    def train(
        self,
        X_train,
        y_train
    ):

        self.model.fit(
            X_train,
            y_train
        )

        return self.model

    def evaluate(
        self,
        X_validation,
        y_validation
    ):

        predictions = self.model.predict(
            X_validation
        )

        accuracy = accuracy_score(
            y_validation,
            predictions
        )

        print(
            f"\nValidation Accuracy: "
            f"{accuracy:.4f}"
        )

        print(
            classification_report(
                y_validation,
                predictions
            )
        )

        return accuracy