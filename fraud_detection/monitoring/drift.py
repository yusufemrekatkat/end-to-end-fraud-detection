"""Data drift detection using Population Stability Index (PSI).
Detects when production data deviates from training data.
"""

import numpy as np
import pandas as pd

def calculate_psi(reference: np.ndarray, current: np.ndarray, n_bins: int = 10) -> float:
    """Calculate PSI between two distributions."""
    breakpoints = np.unique(np.percentile(reference, np.linspace(0, 100, n_bins + 1)))
    
    ref_counts = np.histogram(reference, bins=breakpoints)[0]
    cur_counts = np.histogram(current, bins=breakpoints)[0]
    
    # Proportions with epsilon to avoid div by zero
    ref_pct = (ref_counts / len(reference)) + 1e-4
    cur_pct = (cur_counts / len(current)) + 1e-4
    
    psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
    return float(psi)