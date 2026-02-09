import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

# -------------------------
# Helpers
# -------------------------

def _safe_div(a, b):
    return float(a / b) if b != 0 else 0.0

# -------------------------
# Group Fairness Metrics
# -------------------------

def demographic_parity_difference(df, sensitive, y_pred):
    rates = df.groupby(sensitive)[y_pred].mean().fillna(0)
    return float(rates.max() - rates.min())

def demographic_parity_ratio(df, sensitive, y_pred):
    rates = df.groupby(sensitive)[y_pred].mean().fillna(0)
    return _safe_div(rates.min(), rates.max())

def equal_opportunity_difference(df, sensitive, y_true, y_pred):
    tpr = df[df[y_true] == 1].groupby(sensitive)[y_pred].mean().reindex(df[sensitive].unique(), fill_value=0)
    return float(tpr.max() - tpr.min())

def false_positive_rate_difference(df, sensitive, y_true, y_pred):
    fpr = df[df[y_true] == 0].groupby(sensitive)[y_pred].mean().reindex(df[sensitive].unique(), fill_value=0)
    return float(fpr.max() - fpr.min())

def equalized_odds_difference(df, sensitive, y_true, y_pred):
    return max(
        equal_opportunity_difference(df, sensitive, y_true, y_pred),
        false_positive_rate_difference(df, sensitive, y_true, y_pred)
    )

def predictive_parity_difference(df, sensitive, y_true, y_pred):
    groups = df[sensitive].unique()
    precisions = []
    for g in groups:
        grp = df[(df[sensitive] == g) & (df[y_pred] == 1)]
        tp = int((grp[y_true] == 1).sum()) if y_true in df.columns else 0
        denom = len(grp)
        precisions.append(_safe_div(tp, denom))
    if not precisions:
        return 0.0
    return float(max(precisions) - min(precisions))

# -------------------------
# Individual Fairness
# -------------------------

def theil_index(y_pred):
    """Theil inequality index (entropy-based), normalized to [0, 1]."""
    y = np.array(y_pred, dtype=float)
    if len(y) == 0 or np.sum(y) == 0:
        return 0.0
    mu = np.mean(y)
    if mu <= 0:
        return 0.0
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = y / mu
        valid = ratio > 0
        if not np.any(valid):
            return 0.0
        result = np.mean((ratio[valid] * np.log(ratio[valid])))
        n = len(y)
        max_theil = np.log(n) if n > 1 else 1.0
        normalized = min(result / max_theil if max_theil > 0 else 0, 1.0)
    return float(max(0, normalized))

def atkinson_index(y_pred, epsilon=0.5):
    """Atkinson inequality index, normalized to [0, 1]."""
    y = np.array(y_pred, dtype=float)
    if len(y) == 0 or np.sum(y) == 0:
        return 0.0
    mu = np.mean(y)
    if mu <= 0:
        return 0.0
    with np.errstate(divide='ignore', invalid='ignore'):
        if epsilon == 1:
            result = 1 - np.exp(np.mean(np.log(y + 1e-9))) / mu
        else:
            term = np.mean(y ** (1 - epsilon))
            if term <= 0:
                return 0.0
            result = 1 - (term ** (1 / (1 - epsilon))) / mu
    return float(max(0, min(result, 1.0)))

# -------------------------
# Distribution Bias
# -------------------------

def ks_bias_test(df, sensitive, y_pred):
    groups = df[sensitive].unique()
    results = {}

    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            g1 = df[df[sensitive] == groups[i]][y_pred]
            g2 = df[df[sensitive] == groups[j]][y_pred]
            stat, p = ks_2samp(g1, g2)
            results[f"{groups[i]} vs {groups[j]}"] = {
                "ks_stat": round(stat, 4),
                "p_value": round(p, 4)
            }

    return results

# -------------------------
# Master Audit
# -------------------------

def run_fairness_audit(df, sensitive, y_true, y_pred):
    metrics = {
        "dp_diff": demographic_parity_difference(df, sensitive, y_pred),
        "dp_ratio": demographic_parity_ratio(df, sensitive, y_pred),
        # True positive rate difference (equal opportunity)
        "eo_diff": equal_opportunity_difference(df, sensitive, y_true, y_pred),
        "fpr_diff": false_positive_rate_difference(df, sensitive, y_true, y_pred),
        # Equalized odds = max(TPR diff, FPR diff)
        "equalized_odds": equalized_odds_difference(df, sensitive, y_true, y_pred),
        "pp_diff": predictive_parity_difference(df, sensitive, y_true, y_pred),
        "theil_index": theil_index(df[y_pred]),
        "atkinson_index": atkinson_index(df[y_pred]),
    }

    return {
        "dataset_size": len(df),
        "group_distribution": df[sensitive].value_counts().to_dict(),
        "positive_rate_by_group": df.groupby(sensitive)[y_pred].mean().to_dict(),
        "metrics": {k: round(v, 4) for k, v in metrics.items()},
        "distribution_shift": ks_bias_test(df, sensitive, y_pred),
    }
