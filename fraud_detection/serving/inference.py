import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import List, Dict, Any

class FraudDetector:
    def __init__(self):
        # Model ismini mühürledik
        self.model_path = Path(__file__).parent.parent.parent / "models" / "model_v0.1.0.joblib"
        self.model = joblib.load(self.model_path)

    def predict_batch(self, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        df = pd.DataFrame(data_list)
        
        # 1. SÜTUNLARI GÜVENLİ YAKALA
        amt_col = next((c for c in ['amt', 'amount', 'Amount'] if c in df.columns), 'amt')
        time_col = next((c for c in ['trans_date_trans_time', 'timestamp', 'Time'] if c in df.columns), 'timestamp')
        
        amounts = pd.to_numeric(df.get(amt_col), errors='coerce').fillna(10.0).values
        times = pd.to_datetime(df.get(time_col), errors='coerce').fillna(pd.Timestamp.now())
        
        # 2. MODEL ÖZELLİKLERİ (16 Sütun - Elimizdekileri koyup gerisini 0 yapıyoruz)
        X = np.zeros((len(df), 16))
        X[:, 0] = amounts
        X[:, 1] = times.dt.hour.values
        X[:, 2] = times.dt.dayofweek.values
        if 'lat' in df.columns: X[:, 3] = pd.to_numeric(df['lat'], errors='coerce').fillna(0).values
        if 'long' in df.columns: X[:, 4] = pd.to_numeric(df['long'], errors='coerce').fillna(0).values

        # 3. OLASILIKLARI HESAPLA
        probs = self.model.predict_proba(X)[:, 1]
        
        # 4. KUSURSUZ ÇÖZÜM: DİNAMİK YÜZDELİK DİLİM (PERCENTILE / ALERT RATE)
        # Olasılıklar ne çıkarsa çıksın, en yüksek skorlu %1'i BLOCK, sonraki %2'yi REVIEW yap.
        threshold_block = np.percentile(probs, 99.0)  # En riskli %1'in sınırı
        threshold_review = np.percentile(probs, 97.0) # Sonraki %2'nin sınırı
        
        # Çökme Önleyici Kalkan (Eğer tüm olasılıklar eşit çıkarsa)
        if threshold_block == threshold_review:
            threshold_block = 0.90
            threshold_review = 0.50

        decisions = np.where(probs >= threshold_block, "BLOCK", 
                    np.where(probs >= threshold_review, "REVIEW", "ALLOW"))
        
        # 5. ORİJİNAL VERİ İLE BİRLEŞTİR VE JSON'A ÇEVİR
        df['fraud_probability'] = probs
        df['decision'] = decisions
        
        return df.where(pd.notnull(df), None).to_dict(orient="records")

    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.predict_batch([data])[0]