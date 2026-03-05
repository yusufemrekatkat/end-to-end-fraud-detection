import numpy as np
import pandas as pd
from fraud_detection.features.engineering import engineer_features, FEATURE_COLUMNS

def test_feature_columns_match(sample_transactions_df):
    """Output columns must match the frozen FEATURE_COLUMNS list."""
    features = engineer_features(sample_transactions_df)
    assert list(features.columns) == FEATURE_COLUMNS

def test_is_night_logic(sample_transactions_df):
    """Verify is_night is 1 for hours 22-05."""
    features = engineer_features(sample_transactions_df)
    # Row 1 is 02:15 -> Night should be 1
    assert features.iloc[1]["is_night"] == 1
    # Row 0 is 14:30 -> Night should be 0
    assert features.iloc[0]["is_night"] == 0