from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator

class MerchantCategory(str, Enum):
    GROCERY = "grocery"
    ELECTRONICS = "electronics"
    RESTAURANT = "restaurant"
    TRAVEL = "travel"
    ENTERTAINMENT = "entertainment"
    GAS_STATION = "gas_station"
    ONLINE_SHOPPING = "online_shopping"
    HEALTHCARE = "healthcare"
    OTHER = "other"

class CardType(str, Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"

class FraudDecision(str, Enum):
    """API output decisions."""
    ALLOW = "allow"
    BLOCK = "block"
    REVIEW = "review"

class TransactionRaw(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    timestamp: datetime
    amount: float = Field(..., gt=0)
    merchant_id: str = Field(..., min_length=1)
    merchant_category: MerchantCategory
    customer_id: str = Field(..., min_length=1)
    customer_age: int = Field(..., ge=18, le=100)
    customer_country: str = Field(..., min_length=2, max_length=2)
    card_type: CardType
    is_online: bool
    is_foreign: bool

    @field_validator("customer_country")
    @classmethod
    def normalize_country_code(cls, v: str) -> str:
        return v.upper()

class PredictionRequest(BaseModel):
    """API request body."""
    transaction: TransactionRaw

class PredictionResponse(BaseModel):
    """API response body."""
    transaction_id: str
    fraud_probability: float = Field(..., ge=0.0, le=1.0)
    decision: FraudDecision
    model_version: str
    latency_ms: float