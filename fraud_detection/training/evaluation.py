"""Model evaluation with fraud-detection-specific metrics.
WHY: Accuracy is useless for imbalanced data (1.7% fraud).
"""

import logging
from typing import Any
import numpy as np
from sklearn.metrics import (
    auc, confusion_matrix, f1_score, precision_recall_curve,
    precision_score, recall_score, roc_auc_score,
)

logger = logging.getLogger(__name__)

def evaluate_model(y_true: np.ndarray, y_pred_proba: np.ndarray, threshold: float = 0.5) -> dict[str, Any]:
    """Evaluate model with focus on Precision and Recall."""
    y_pred = (y_pred_proba >= threshold).astype(int)
    
    # Precision-Recall curve and AUC
    precision_curve, recall_curve, _ = precision_recall_curve(y_true, y_pred_proba)
    auc_pr = auc(recall_curve, precision_curve)
    
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    metrics = {
        "threshold": threshold,
        "auc_roc": float(roc_auc_score(y_true, y_pred_proba)),
        "auc_pr": float(auc_pr),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "tp": int(tp), "fp": int(fp), "tn": int(tn), "fn": int(fn)
    }

    logger.info(f"AUC-ROC: {metrics['auc_roc']:.4f} | Recall: {metrics['recall']:.4f}")
    return metrics