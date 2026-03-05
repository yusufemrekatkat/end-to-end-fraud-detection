import logging
from fastapi import FastAPI, HTTPException
from typing import Any, Dict, List
from contextlib import asynccontextmanager
from fraud_detection.serving.inference import FraudDetector

logger = logging.getLogger(__name__)
detector = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global detector
    detector = FraudDetector()
    yield

app = FastAPI(title="Fraud Sentinel AI", lifespan=lifespan)

@app.post("/predict")
async def predict(raw_request: Dict[str, Any]):
    if detector is None: raise HTTPException(status_code=503, detail="Model yüklenmedi.")
    transaction = raw_request.get("transaction", raw_request)
    return detector.predict(transaction)

@app.post("/predict-batch")
async def predict_batch(raw_requests: List[Dict[str, Any]]):
    if detector is None: raise HTTPException(status_code=503, detail="Model yüklenmedi.")
    try:
        return detector.predict_batch(raw_requests)
    except Exception as e:
        logger.error(f"Batch Hatası: {e}")
        raise HTTPException(status_code=400, detail=str(e))