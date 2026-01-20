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
    rates = df.groupby(sensitive)[y_pred].mean()
    return float(rates.max() - rates.min())

def demographic_parity_ratio(df, sensitive, y_pred):
    rates = df.groupby(sensitive)[y_pred].mean()
    return _safe_div(rates.min(), rates.max())

def equal_opportunity_difference(df, sensitive, y_true, y_pred):
    tpr = df[df[y_true] == 1].groupby(sensitive)[y_pred].mean()
    return float(tpr.max() - tpr.min())

def false_positive_rate_difference(df, sensitive, y_true, y_pred):
    fpr = df[df[y_true] == 0].groupby(sensitive)[y_pred].mean()
    return float(fpr.max() - fpr.min())

def equalized_odds_difference(df, sensitive, y_true, y_pred):
    return max(
        equal_opportunity_difference(df, sensitive, y_true, y_pred),
        false_positive_rate_difference(df, sensitive, y_true, y_pred)
    )

def predictive_parity_difference(df, sensitive, y_true, y_pred):
    precision = df[df[y_pred] == 1].groupby(sensitive).apply(
        lambda x: _safe_div((x[y_true] == 1).sum(), len(x))
    )
    return float(precision.max() - precision.min())

# -------------------------
# Individual Fairness
# -------------------------

def theil_index(y_pred):
    y = np.array(y_pred)
    mu = np.mean(y)
    if mu == 0:
        return 0.0
    return float(np.mean((y / mu) * np.log((y / mu) + 1e-9)))

def atkinson_index(y_pred, epsilon=0.5):
    y = np.array(y_pred)
    mu = np.mean(y)
    if mu == 0:
        return 0.0
    return float(1 - (np.mean(y ** (1 - epsilon)) ** (1 / (1 - epsilon))) / mu)

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
        "eo_diff": equalized_odds_difference(df, sensitive, y_true, y_pred),
        "fpr_diff": false_positive_rate_difference(df, sensitive, y_true, y_pred),
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
