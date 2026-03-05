"""Feature engineering — the contract between training and serving.
INVARIANT: Training and serving MUST call this SAME function.
"""

import numpy as np
import pandas as pd
from fraud_detection.data.schema import CardType, MerchantCategory

# --- Encoding Maps ---
# Frozen: Changing these requires model retraining.
MERCHANT_CATEGORY_MAP = {cat.value: idx for idx, cat in enumerate(MerchantCategory)}
CARD_TYPE_MAP = {ct.value: idx for idx, ct in enumerate(CardType)}
HIGH_RISK_CATEGORIES = {"online_shopping", "electronics", "travel"}

# --- Feature Column Order ---
# Frozen: Model expects features in this exact order.
FEATURE_COLUMNS = [
    "amount", "amount_log", "customer_age", "is_online", "is_foreign",
    "merchant_category_encoded", "card_type_encoded", "transaction_hour",
    "transaction_day_of_week", "is_night", "is_weekend", "is_high_risk_category",
    "hour_sin", "hour_cos", "day_sin", "day_cos"
]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw transaction data into model-ready features."""
    required = ["amount", "customer_age", "is_online", "is_foreign", 
                "merchant_category", "card_type", "timestamp"]
    
    missing = set(required) - set(df.columns)
    if missing:
        raise KeyError(f"Missing required columns: {missing}")

    features = pd.DataFrame(index=df.index)

    # --- Direct & Log Features ---
    features["amount"] = df["amount"].astype(float)
    features["amount_log"] = np.log1p(df["amount"]).astype(float)
    features["customer_age"] = df["customer_age"].astype(int)
    features["is_online"] = df["is_online"].astype(int)
    features["is_foreign"] = df["is_foreign"].astype(int)

    # --- Categorical Encoding ---
    features["merchant_category_encoded"] = df["merchant_category"].map(MERCHANT_CATEGORY_MAP)
    features["card_type_encoded"] = df["card_type"].map(CARD_TYPE_MAP)

    # --- Time Features ---
    ts = pd.to_datetime(df["timestamp"])
    hour = ts.dt.hour
    day = ts.dt.dayofweek

    features["transaction_hour"] = hour
    features["transaction_day_of_week"] = day
    features["is_night"] = ((hour >= 22) | (hour < 6)).astype(int)
    features["is_weekend"] = (day >= 5).astype(int)
    features["is_high_risk_category"] = df["merchant_category"].isin(HIGH_RISK_CATEGORIES).astype(int)

    # --- Cyclical Encoding (Sin/Cos) ---
    features["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    features["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    features["day_sin"] = np.sin(2 * np.pi * day / 7)
    features["day_cos"] = np.cos(2 * np.pi * day / 7)

    return features[FEATURE_COLUMNS]