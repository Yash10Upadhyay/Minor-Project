def calculate_fairness_score(metrics: dict) -> float:
    penalties = [
        metrics["dp_diff"],
        abs(1 - metrics["dp_ratio"]),
        metrics["eo_diff"],
        metrics["fpr_diff"],
        metrics["pp_diff"]
    ]

    score = (1 - sum(penalties) / len(penalties)) * 100
    return round(max(0, min(score, 100)), 2)

def interpret_bias(score: float) -> str:
    if score >= 85:
        return "Low Bias"
    elif score >= 65:
        return "Moderate Bias"
    else:
        return "High Bias"
