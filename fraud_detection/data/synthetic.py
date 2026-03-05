import uuid
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from fraud_detection.data.schema import CardType, MerchantCategory

def generate_synthetic_transactions(n=10000, seed=42):
    rng = np.random.default_rng(seed)
    categories = [c.value for c in MerchantCategory]
    cards = [c.value for c in CardType]
    
    data = []
    start_date = datetime.now() - timedelta(days=90)
    
    for _ in range(n):
        is_fraud = rng.random() < 0.017 # %1.7 dolandırıcılık oranı
        amount = rng.lognormal(6.5, 1.2) if is_fraud else rng.lognormal(4.5, 1.0)
        
        data.append({
            "transaction_id": str(uuid.uuid4()),
            "timestamp": start_date + timedelta(seconds=int(rng.integers(0, 90*24*3600))),
            "amount": round(min(amount, 50000), 2),
            "merchant_id": f"m_{rng.integers(1, 1000)}",
            "merchant_category": rng.choice(categories),
            "customer_id": f"c_{rng.integers(1, 5000)}",
            "customer_age": int(rng.integers(18, 80)),
            "customer_country": "US",
            "card_type": rng.choice(cards),
            "is_online": rng.random() < (0.7 if is_fraud else 0.3),
            "is_foreign": rng.random() < (0.4 if is_fraud else 0.1),
            "is_fraud": int(is_fraud)
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_synthetic_transactions()
    out_path = Path("data/raw/transactions.csv")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Veri uretildi: {out_path} ({len(df)} satir)")