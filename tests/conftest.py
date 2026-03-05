import pytest
import pandas as pd
from fraud_detection.data.schema import CardType, MerchantCategory, TransactionRaw

@pytest.fixture
def sample_transaction():
    """Valid transaction for testing."""
    return TransactionRaw(
        transaction_id="test-txn-001",
        timestamp="2026-06-15T14:30:00",
        amount=150.00,
        merchant_id="m_001",
        merchant_category=MerchantCategory.GROCERY,
        customer_id="c_001",
        customer_age=35,
        customer_country="US",
        card_type=CardType.VISA,
        is_online=False,
        is_foreign=False
    )

@pytest.fixture
def sample_transactions_df() -> pd.DataFrame:
    """Small DataFrame for testing pipelines."""
    return pd.DataFrame({
        "transaction_id": ["txn-1", "txn-2", "txn-3", "txn-4", "txn-5"],
        "timestamp": pd.to_datetime([
            "2025-06-15 14:30:00", "2025-06-15 02:15:00", 
            "2025-06-16 10:00:00", "2025-06-17 23:45:00", 
            "2025-06-18 08:20:00"
        ]),
        "amount": [50.0, 5000.0, 150.0, 25.0, 800.0],
        "merchant_id": ["m1", "m2", "m3", "m4", "m5"],
        "merchant_category": ["grocery", "electronics", "restaurant", "travel", "online_shopping"],
        "customer_id": ["c1", "c2", "c3", "c4", "c5"],
        "customer_age": [25, 45, 30, 60, 35],
        "customer_country": ["US", "GB", "DE", "TR", "US"],
        "card_type": ["visa", "mastercard", "amex", "visa", "mastercard"],
        "is_online": [False, True, False, True, True],
        "is_foreign": [False, True, False, True, False],
        "is_fraud": [0, 1, 0, 1, 0],
    })