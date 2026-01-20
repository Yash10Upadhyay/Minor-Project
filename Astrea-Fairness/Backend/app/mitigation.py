def recommend_mitigation(metrics: dict):
    """
    Returns human-readable bias issues and concrete fixes
    based on fairness metrics.
    """
    recommendations = []

    dp = abs(metrics.get("demographic_parity", 0))
    eo = abs(metrics.get("equal_opportunity", 0))
    fpr = abs(metrics.get("false_positive_rate_diff", 0))

    if dp > 0.1:
        recommendations.append({
            "issue": "Demographic Parity Bias Detected",
            "fix": (
                "Apply re-sampling or re-weighting techniques to balance outcomes "
                "across sensitive groups. Consider removing proxy features "
                "that indirectly encode the sensitive attribute."
            )
        })

    if eo > 0.1:
        recommendations.append({
            "issue": "Equal Opportunity Bias Detected",
            "fix": (
                "Ensure similar true positive rates across groups by "
                "training group-aware thresholds or using fairness-constrained optimization."
            )
        })

    if fpr > 0.1:
        recommendations.append({
            "issue": "False Positive Rate Disparity",
            "fix": (
                "Tune classification thresholds separately per group "
                "or apply post-processing calibration methods."
            )
        })

    if not recommendations:
        recommendations.append({
            "issue": "No Significant Bias Detected",
            "fix": "Continue monitoring fairness during retraining and deployment."
        })

    return recommendations
