import pandas as pd


class DataValidator:
    """
    Production-grade dataset validator.
    - Schema checks
    - Type validation
    - Null checks
    - Business rules
    - Fail-fast support
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.errors = []

        # -----------------------------
        # Expected schema definition
        # -----------------------------
        self.expected_schema = {
            "year": "int",
            "date": "datetime",
            "stage": "object",
            "home_team": "object",
            "away_team": "object",
            "home_goals": "int",
            "away_goals": "int",
            "winner": "object",
            "match_id": "int",
        }

    # =====================================================
    # 1. SCHEMA VALIDATION
    # =====================================================
    def validate_schema(self):

        missing_columns = set(self.expected_schema.keys()) - set(self.df.columns)

        for col in missing_columns:
            self.errors.append(f"[SCHEMA] Missing column: {col}")

    # =====================================================
    # 2. TYPE VALIDATION
    # =====================================================
    def validate_types(self):

        for col, expected_type in self.expected_schema.items():

            if col not in self.df.columns:
                continue

            try:
                if expected_type == "datetime":
                    self.df[col] = pd.to_datetime(self.df[col], errors="raise")

                elif expected_type == "int":
                    if not pd.api.types.is_numeric_dtype(self.df[col]):
                        self.errors.append(f"[TYPE] {col} must be numeric")

                elif expected_type == "object":
                    if not pd.api.types.is_string_dtype(self.df[col]) and not pd.api.types.is_object_dtype(self.df[col]):
                        self.errors.append(f"[TYPE] {col} must be string/object")

            except Exception as e:
                self.errors.append(f"[TYPE] {col} conversion failed: {str(e)}")

    # =====================================================
    # 3. NULL VALIDATION
    # =====================================================
    def validate_nulls(self):

        null_counts = self.df.isnull().sum()

        for col, count in null_counts.items():
            if count > 0:
                self.errors.append(f"[NULL] {col} has {count} null values")

    # =====================================================
    # 4. BUSINESS RULES
    # =====================================================
    def validate_business_rules(self):

        # -----------------------------
        # match_id uniqueness
        # -----------------------------
        if "match_id" in self.df.columns:
            duplicates = self.df["match_id"].duplicated().sum()
            if duplicates > 0:
                self.errors.append(f"[RULE] {duplicates} duplicate match_id values")

        # -----------------------------
        # Goals must be >= 0
        # -----------------------------
        if "home_goals" in self.df.columns:
            neg_home = (self.df["home_goals"] < 0).sum()
            if neg_home > 0:
                self.errors.append(f"[RULE] {neg_home} negative home_goals")

        if "away_goals" in self.df.columns:
            neg_away = (self.df["away_goals"] < 0).sum()
            if neg_away > 0:
                self.errors.append(f"[RULE] {neg_away} negative away_goals")

        # -----------------------------
        # Same team match check
        # -----------------------------
        if "home_team" in self.df.columns and "away_team" in self.df.columns:
            same_team = (self.df["home_team"] == self.df["away_team"]).sum()
            if same_team > 0:
                self.errors.append(f"[RULE] {same_team} matches have identical teams")

    # =====================================================
    # 5. RUN ALL VALIDATIONS
    # =====================================================
    def validate(self):

        self.validate_schema()
        self.validate_types()
        self.validate_nulls()
        self.validate_business_rules()

        return self.errors

    # =====================================================
    # 6. FAIL FAST MODE (PIPELINE SAFE)
    # =====================================================
    def raise_if_invalid(self):

        if self.errors:
            error_message = "\n".join(self.errors)
            raise Exception(f"VALIDATION FAILED:\n{error_message}")

        print("VALIDATION PASSED")