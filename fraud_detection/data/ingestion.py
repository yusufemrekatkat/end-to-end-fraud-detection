"""
Advanced Data Ingestion Layer.
Handles all messy fields, missing data, and invalid enums.
"""
import logging
from datetime import datetime
from typing import Any, Dict
from fraud_detection.data.schema import TransactionRaw, MerchantCategory, CardType

logger = logging.getLogger(__name__)

class DataCleaner:
    @staticmethod
    def clean_raw_input(raw_data: Dict[str, Any]) -> TransactionRaw:
        data = raw_data.copy()

        # 1. KİMLİKLER (Boş ID gelirse otomatik doldur)
        for key in ["transaction_id", "merchant_id", "customer_id"]:
            val = data.get(key, "")
            if not val or not isinstance(val, str) or len(str(val).strip()) == 0:
                data[key] = f"AUTO_ID_{datetime.now().strftime('%S%f')}"

        # 2. KATEGORİLER VE ENUM'LAR (Hatalıysa varsayılana çek)
        valid_categories = [c.value for c in MerchantCategory]
        if data.get("merchant_category") not in valid_categories:
            data["merchant_category"] = MerchantCategory.OTHER

        valid_cards = [c.value for c in CardType]
        if data.get("card_type") not in valid_cards:
            data["card_type"] = CardType.VISA

        # 3. MİKTAR VE YAŞ (Sıfır veya geçersizse 10.0 ve 35 yap)
        try:
            amt = float(data.get("amount", 10.0))
            data["amount"] = amt if amt > 0 else 10.0
        except (ValueError, TypeError):
            data["amount"] = 10.0

        try:
            data["customer_age"] = int(data.get("customer_age", 35))
        except (ValueError, TypeError):
            data["customer_age"] = 35

        # 4. ÜLKE VE DURUM
        data["customer_country"] = str(data.get("customer_country", "US")).upper()[:2]
        data["is_online"] = bool(data.get("is_online", True))
        data["is_foreign"] = bool(data.get("is_foreign", False))

        # 5. TARİH DÜZELTME
        ts = data.get("timestamp")
        if not ts or not isinstance(ts, str):
            data["timestamp"] = datetime.now()
        else:
            for fmt in ("%Y-%m-%d %H:%M:%S", "%d-%m-%Y %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
                try:
                    data["timestamp"] = datetime.strptime(ts, fmt)
                    break
                except ValueError:
                    continue
            if isinstance(data["timestamp"], str):
                 data["timestamp"] = datetime.now()

        return TransactionRaw(**data)