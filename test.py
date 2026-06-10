from src.api.feature_builder import FeatureBuilder

builder = FeatureBuilder()

result = builder.build(
    "France",
    "England",
    "Final"
)

print(result)