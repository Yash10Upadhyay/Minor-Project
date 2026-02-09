def calculate_fairness_score(metrics: dict) -> float:
    """
    Calculate fairness score (0-100) from metrics.
    Lower metric values = higher fairness.
    
    Uses only the core bias metrics (dp_diff, dp_ratio, eo_diff, fpr_diff, pp_diff).
    Inequality metrics (theil, atkinson) are reported separately.
    """
    # Extract core fairness metrics only (exclude theil_index, atkinson_index, equalized_odds)
    penalties = [
        min(metrics.get("dp_diff", 0), 1.0),           # Demographic parity diff [0-1]
        max(0, min(1 - metrics.get("dp_ratio", 1), 1.0)),  # 80% rule: 1 - dp_ratio [0-1]
        min(metrics.get("eo_diff", 0), 1.0),           # Equal opportunity diff [0-1]
        min(metrics.get("fpr_diff", 0), 1.0),          # False positive rate diff [0-1]
        min(metrics.get("pp_diff", 0), 1.0)            # Predictive parity diff [0-1]
    ]
    
    # Average penalties, then invert to get score (0 penalty = 100 score)
    avg_penalty = sum(penalties) / len(penalties)
    score = (1 - avg_penalty) * 100
    
    # Clamp to [0, 100]
    return round(max(0, min(score, 100)), 2)

def interpret_bias(score: float) -> str:
    if score >= 85:
        return "Low Bias"
    elif score >= 65:
        return "Moderate Bias"
    else:
        return "High Bias"
