def recommend_mitigation(metrics: dict):
    """
    Returns human-readable bias issues and concrete fixes
    based on fairness metrics.
    """
    recommendations = []

    # Use metric keys produced by run_fairness_audit
    dp = abs(metrics.get("dp_diff", 0))
    eo = abs(metrics.get("eo_diff", 0))
    fpr = abs(metrics.get("fpr_diff", 0))

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

    # Also check dp_ratio (80% rule) from metrics if present
    dp_ratio = metrics.get("dp_ratio", None)
    if dp_ratio is not None and dp_ratio < 0.8:
        recommendations.append({
            "issue": "Legal Compliance (80% Rule)",
            "fix": "Selection rates violate the 80% rule. Investigate and mitigate disproportionate selection."
        })

    if not recommendations:
        recommendations.append({
            "issue": "No Significant Bias Detected",
            "fix": "Continue monitoring fairness during retraining and deployment."
        })

    return recommendations
