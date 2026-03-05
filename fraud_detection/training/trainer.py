import json
import logging
import joblib
from datetime import datetime, timezone
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from fraud_detection.config import get_settings
from fraud_detection.data.loader import load_csv
from fraud_detection.features.engineering import FEATURE_COLUMNS, engineer_features
from fraud_detection.training.evaluation import evaluate_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train():
    settings = get_settings()
    data_path = settings.project_root / settings.data_raw_dir / "transactions.csv"
    
    # 1. Load & Engineer
    df = load_csv(data_path)
    X = engineer_features(df)
    y = df["is_fraud"].astype(int)

    # 2. Stratified Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=settings.test_size, 
        random_state=settings.random_seed, stratify=y
    )

    # 3. Train
    logger.info("Training RandomForest (balanced)...")
    model = RandomForestClassifier(
        n_estimators=100, max_depth=10, 
        class_weight="balanced", random_state=settings.random_seed
    )
    model.fit(X_train, y_train)

    # 4. Evaluate
    y_proba = model.predict_proba(X_test)[:, 1]
    metrics = evaluate_model(y_test.values, y_proba, settings.fraud_threshold)

    # 5. Save Artifacts
    models_dir = settings.project_root / settings.models_dir
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = models_dir / f"model_v{settings.model_version}.joblib"
    joblib.dump(model, model_path)
    
    metadata = {
        "version": settings.model_version,
        "metrics": metrics,
        "features": FEATURE_COLUMNS,
        "date": datetime.now(timezone.utc).isoformat()
    }
    
    with open(models_dir / f"model_v{settings.model_version}_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Model saved to {model_path}")
    return metrics

if __name__ == "__main__":
    train()