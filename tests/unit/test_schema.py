import pytest
from pydantic import ValidationError
from fraud_detection.data.schema import TransactionRaw

def test_valid_transaction(sample_transaction):
    """Should accept valid data."""
    assert sample_transaction.transaction_id == "test-txn-001"

def test_negative_amount_rejected(sample_transaction):
    """Should raise error for negative amount."""
    data = sample_transaction.model_dump()
    data["amount"] = -10.0
    with pytest.raises(ValidationError):
        TransactionRaw(**data)

def test_invalid_age_rejected(sample_transaction):
    """Should raise error for age out of range."""
    data = sample_transaction.model_dump()
    data["customer_age"] = 150
    with pytest.raises(ValidationError):
        TransactionRaw(**data)