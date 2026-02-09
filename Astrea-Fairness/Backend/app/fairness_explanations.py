"""
Comprehensive fairness metrics explanations and detailed bias/fairness checks.
Provides interpretable information for all metrics used in Astrea Fairness.
"""

METRICS_EXPLANATIONS = {
    "dp_diff": {
        "name": "Demographic Parity Difference",
        "description": "Measures the difference in positive prediction rates between demographic groups.",
        "range": "0 to 1 (0 is ideal - perfect parity)",
        "interpretation": {
            "0.0": "Perfect demographic parity - both groups have identical positive rates",
            "0.1": "Good - less than 10% difference in positive rates",
            "0.2": "Fair - up to 20% difference (acceptable in some contexts)",
            "0.3": "Concerning - significant difference in positive rates",
            "0.5": "Critical - substantial disparity between groups"
        },
        "formula": "max(P(Y=1|Group=A)) - min(P(Y=1|Group=B))",
        "impact": "Shows if one group is systematically preferred over another in decisions"
    },
    
    "dp_ratio": {
        "name": "Demographic Parity Ratio (80% Rule)",
        "description": "Ratio of positive prediction rates between groups (usually minority/majority).",
        "range": "0 to 1 (0.8-1.0 is legal threshold in employment)",
        "interpretation": {
            "1.0": "Perfect parity - groups have equal selection rates",
            "0.8": "Legal threshold - acceptable under 80% rule",
            "0.7": "Warning - below legal threshold, potential discrimination",
            "0.5": "Critical - significant disparity (50% of group's rate)"
        },
        "formula": "min(P(Y=1|Group)) / max(P(Y=1|Group))",
        "impact": "Common legal standard (used in employment discrimination cases)"
    },
    
    "eo_diff": {
        "name": "Equal Opportunity Difference",
        "description": "Difference in True Positive Rates (TPR) across groups for positive class.",
        "range": "0 to 1 (0 is ideal)",
        "interpretation": {
            "0.0": "Perfect equal opportunity - qualified individuals have equal acceptance rates",
            "0.1": "Good - similar opportunity across groups",
            "0.2": "Fair - moderate difference in opportunities",
            "0.3": "Concerning - noticeable disparity in opportunities",
            "0.5": "Critical - one group has 50% lower opportunity"
        },
        "formula": "max(TPR|Group=A) - min(TPR|Group=B)",
        "impact": "Ensures disadvantaged individuals get equal chances when qualified"
    },
    
    "fpr_diff": {
        "name": "False Positive Rate Difference",
        "description": "Difference in False Positive Rates (FPR) across groups.",
        "range": "0 to 1 (0 is ideal)",
        "interpretation": {
            "0.0": "Perfect calibration - false alarms equal across groups",
            "0.1": "Good - similar false alarm rates",
            "0.2": "Fair - acceptable false alarm variation",
            "0.3": "Concerning - one group has more false positives",
            "0.5": "Critical - one group is 50% more likely to be falsely accused"
        },
        "formula": "max(FPR|Group=A) - min(FPR|Group=B)",
        "impact": "Ensures innocent people aren't unfairly targeted disproportionately"
    },
    
    "pp_diff": {
        "name": "Predictive Parity Difference",
        "description": "Difference in Precision (positive predictive value) across groups.",
        "range": "0 to 1 (0 is ideal)",
        "interpretation": {
            "0.0": "Perfect precision parity",
            "0.1": "Good - predictions equally reliable",
            "0.2": "Fair - moderate precision difference",
            "0.3": "Concerning - significant precision gap",
            "0.5": "Critical - predictions 50% less reliable for one group"
        },
        "formula": "max(Precision|Group=A) - min(Precision|Group=B)",
        "impact": "Ensures predictions are equally trustworthy for all groups"
    },
    
    "theil_index": {
        "name": "Theil Index (Entropy-based Inequality)",
        "description": "Measures inequality in outcomes distribution. Sensitive to extremes.",
        "range": "0 to ln(n) where n is number of groups",
        "interpretation": {
            "0.0": "Perfect equality in outcomes",
            "0.05": "Very good - low inequality",
            "0.1": "Good - acceptable inequality level",
            "0.2": "Fair - moderate inequality",
            "0.3": "Concerning - notable inequality",
            "0.5": "Critical - severe inequality"
        },
        "formula": "(1/n) * Σ(yi/μ) * ln(yi/μ)",
        "impact": "Captures whether outcomes are concentrated in specific groups"
    },
    
    "atkinson_index": {
        "name": "Atkinson Index (Welfare Loss)",
        "description": "Measures the proportion of welfare loss due to inequality.",
        "range": "0 to 1 (0 is perfect equality)",
        "interpretation": {
            "0.0": "Perfect equality - no welfare loss",
            "0.1": "Very good - minimal welfare loss",
            "0.2": "Good - acceptable welfare loss",
            "0.3": "Fair - moderate welfare loss (~30%)",
            "0.5": "Concerning - half potential welfare lost to inequality",
            "0.8": "Critical - severe welfare inequality"
        },
        "formula": "1 - (Σ(yi^(1-ε))^(1/(1-ε))) / μ",
        "impact": "Reflects society's well-being impact from unequal outcomes"
    },
    
    "calibration_error": {
        "name": "Calibration Error",
        "description": "Difference between predicted probabilities and actual outcomes.",
        "range": "0 to 1 (0 is perfect calibration)",
        "interpretation": {
            "0.0": "Perfect calibration - predictions match reality",
            "0.05": "Excellent - very reliable predictions",
            "0.1": "Good - predictions are generally reliable",
            "0.2": "Fair - some prediction reliability issues",
            "0.3": "Concerning - predictions often wrong",
            "0.5": "Critical - predictions unreliable"
        },
        "impact": "Shows if the model's confidence matches actual performance"
    },
    
    "statistical_parity_ratio": {
        "name": "Statistical Parity Ratio",
        "description": "Ratio of selection rates: P(Y=1|Group=A) / P(Y=1|Group=B)",
        "range": "0 to 1+ (ideally 1.0)",
        "interpretation": {
            "1.0": "Perfect parity",
            "0.9-1.1": "Good - within 10% of parity",
            "0.8-1.0": "Fair - legal threshold range",
            "0.5": "Concerning - one group 50% less likely",
            "0.3": "Critical - one group 70% less likely"
        },
        "impact": "Direct measure of selection rate disparity"
    }
}

BIAS_CHECKS = {
    "systematic_bias": {
        "name": "Systematic Bias Check",
        "description": "Determines if there is consistent preference for/against a group",
        "thresholds": {
            "dp_diff": 0.1,  # Demographic parity difference threshold
            "dp_ratio": 0.8  # 80% rule threshold
        },
        "severity_levels": {
            "none": {"description": "No systematic bias detected", "color": "green"},
            "minor": {"description": "Minor systematic bias (<10% difference)", "color": "yellow"},
            "moderate": {"description": "Moderate bias (10-25% difference)", "color": "orange"},
            "severe": {"description": "Severe systematic bias (>25% difference)", "color": "red"}
        }
    },
    
    "opportunity_bias": {
        "name": "Opportunity Bias Check",
        "description": "Tests if qualified individuals have equal opportunity across groups",
        "thresholds": {
            "eo_diff": 0.15  # Equal opportunity threshold
        },
        "severity_levels": {
            "none": {"description": "Equal opportunity for qualified individuals", "color": "green"},
            "minor": {"description": "Slight opportunity disparity (<15%)", "color": "yellow"},
            "moderate": {"description": "Moderate opportunity gap (15-30%)", "color": "orange"},
            "severe": {"description": "Severe opportunity disparity (>30%)", "color": "red"}
        }
    },
    
    "error_bias": {
        "name": "Error Rate Bias Check",
        "description": "Checks if errors (false positives/negatives) are distributed fairly",
        "thresholds": {
            "fpr_diff": 0.15,  # False positive rate threshold
            "fnr_diff": 0.15   # False negative rate threshold
        },
        "severity_levels": {
            "none": {"description": "Error rates balanced across groups", "color": "green"},
            "minor": {"description": "Minor error disparity (<15%)", "color": "yellow"},
            "moderate": {"description": "Moderate error gap (15-30%)", "color": "orange"},
            "severe": {"description": "Severe error disparity (>30%)", "color": "red"}
        }
    },
    
    "outcome_quality_bias": {
        "name": "Outcome Quality Bias Check",
        "description": "Verifies if predictions are equally reliable for all groups",
        "thresholds": {
            "pp_diff": 0.15  # Predictive parity threshold
        },
        "severity_levels": {
            "none": {"description": "Predictions equally reliable", "color": "green"},
            "minor": {"description": "Minor precision disparity (<15%)", "color": "yellow"},
            "moderate": {"description": "Moderate precision gap (15-30%)", "color": "orange"},
            "severe": {"description": "Severe precision disparity (>30%)", "color": "red"}
        }
    },
    
    "inequality_bias": {
        "name": "Outcome Inequality Check",
        "description": "Measures overall inequality in outcomes distribution",
        "thresholds": {
            "theil_index": 0.2,
            "atkinson_index": 0.2
        },
        "severity_levels": {
            "none": {"description": "Low outcome inequality", "color": "green"},
            "minor": {"description": "Minor inequality detected", "color": "yellow"},
            "moderate": {"description": "Moderate outcome inequality", "color": "orange"},
            "severe": {"description": "Severe outcome inequality", "color": "red"}
        }
    }
}

FAIRNESS_CHECKS = {
    "legal_compliance": {
        "name": "Legal Compliance Check (80% Rule)",
        "description": "Tests compliance with employment law requirements (US Equal Employment Opportunity Commission)",
        "criteria": {
            "dp_ratio": {
                "threshold": 0.8,
                "interpretation": "Selection rate of minority group should be ≥80% of majority group"
            }
        },
        "result_interpretation": {
            "compliant": {"description": "Model meets 80% rule requirement", "status": "✓ PASS"},
            "non_compliant": {"description": "Model violates 80% rule", "status": "✗ FAIL"}
        }
    },
    
    "calibration_fairness": {
        "name": "Calibration Fairness Check",
        "description": "Ensures predicted probabilities are accurate within each group",
        "criteria": {
            "group_calibration": "Predicted P(Y=1) matches actual P(Y=1|predicted class)",
            "cross_group_calibration": "Calibration quality is similar across all groups"
        },
        "levels": {
            "excellent": {"threshold": "<0.05", "description": "Predictions highly trustworthy for all groups"},
            "good": {"threshold": "<0.10", "description": "Predictions reliable for all groups"},
            "fair": {"threshold": "<0.20", "description": "Predictions generally reliable"},
            "poor": {"threshold": ">0.20", "description": "Predictions unreliable"}
        }
    },
    
    "individual_fairness": {
        "name": "Individual Fairness Check",
        "description": "Tests if similar individuals receive similar treatment",
        "criteria": {
            "consistency": "Similar individuals should get similar predictions",
            "non_discrimination": "Sensitive attributes shouldn't be primary decision factor"
        },
        "measured_by": ["Theil Index", "Atkinson Index", "outcome_variance"]
    },
    
    "group_fairness": {
        "name": "Group Fairness Check",
        "description": "Tests if demographic groups receive equitable treatment",
        "criteria": {
            "demographic_parity": "Equal positive prediction rates across groups",
            "equal_opportunity": "Equal true positive rates for qualified individuals",
            "equalized_odds": "Equal TPR and FPR across groups"
        },
        "measured_by": ["dp_diff", "eo_diff", "fpr_diff"]
    },
    
    "procedural_fairness": {
        "name": "Procedural Fairness Check",
        "description": "Evaluates if the decision process is transparent and contestable",
        "criteria": {
            "transparency": "Model decisions can be explained",
            "contestability": "Individuals can appeal/challenge decisions",
            "consistency": "Similar cases treated similarly"
        },
        "note": "Requires additional implementation for full assessment"
    }
}

def generate_detailed_fairness_report(metrics, group_distribution):
    """Generate comprehensive fairness report based on metrics."""
    
    report = {
        "summary": {},
        "bias_checks": {},
        "fairness_assessments": {},
        "recommendations": []
    }
    
    # Bias Checks
    for check_name, check_def in BIAS_CHECKS.items():
        result = evaluate_bias_check(check_name, metrics)
        report["bias_checks"][check_name] = result
    
    # Fairness Checks
    for check_name, check_def in FAIRNESS_CHECKS.items():
        result = evaluate_fairness_check(check_name, metrics)
        report["fairness_assessments"][check_name] = result
    
    # Generate recommendations
    report["recommendations"] = generate_recommendations(metrics, report["bias_checks"])
    
    return report


def evaluate_bias_check(check_name, metrics):
    """Evaluate a specific bias check."""
    if check_name == "systematic_bias":
        dp_diff = metrics.get("dp_diff", 0)
        severity = "none" if dp_diff < 0.05 else ("minor" if dp_diff < 0.15 else ("moderate" if dp_diff < 0.25 else "severe"))
        return {
            "check": check_name,
            "result": dp_diff,
            "severity": severity,
            "description": BIAS_CHECKS[check_name]["severity_levels"][severity]["description"]
        }
    
    elif check_name == "opportunity_bias":
        eo_diff = metrics.get("eo_diff", 0)
        severity = "none" if eo_diff < 0.1 else ("minor" if eo_diff < 0.15 else ("moderate" if eo_diff < 0.30 else "severe"))
        return {
            "check": check_name,
            "result": eo_diff,
            "severity": severity,
            "description": BIAS_CHECKS[check_name]["severity_levels"][severity]["description"]
        }
    
    elif check_name == "error_bias":
        fpr_diff = metrics.get("fpr_diff", 0)
        severity = "none" if fpr_diff < 0.1 else ("minor" if fpr_diff < 0.15 else ("moderate" if fpr_diff < 0.30 else "severe"))
        return {
            "check": check_name,
            "result": fpr_diff,
            "severity": severity,
            "description": BIAS_CHECKS[check_name]["severity_levels"][severity]["description"]
        }
    
    elif check_name == "outcome_quality_bias":
        pp_diff = metrics.get("pp_diff", 0)
        severity = "none" if pp_diff < 0.1 else ("minor" if pp_diff < 0.15 else ("moderate" if pp_diff < 0.30 else "severe"))
        return {
            "check": check_name,
            "result": pp_diff,
            "severity": severity,
            "description": BIAS_CHECKS[check_name]["severity_levels"][severity]["description"]
        }
    
    elif check_name == "inequality_bias":
        theil = metrics.get("theil_index", 0)
        severity = "none" if theil < 0.1 else ("minor" if theil < 0.15 else ("moderate" if theil < 0.25 else "severe"))
        return {
            "check": check_name,
            "result": theil,
            "severity": severity,
            "description": BIAS_CHECKS[check_name]["severity_levels"][severity]["description"]
        }
    
    return {}


def evaluate_fairness_check(check_name, metrics):
    """Evaluate a specific fairness check."""
    if check_name == "legal_compliance":
        dp_ratio = metrics.get("dp_ratio", 0)
        compliant = dp_ratio >= 0.8
        return {
            "check": check_name,
            "result": dp_ratio,
            "status": "PASS" if compliant else "FAIL",
            "description": FAIRNESS_CHECKS[check_name]["result_interpretation"]["compliant" if compliant else "non_compliant"]["description"]
        }
    
    elif check_name == "calibration_fairness":
        # Simplified calibration check
        return {
            "check": check_name,
            "status": "PENDING",
            "description": "Requires additional implementation for full assessment"
        }
    
    elif check_name == "individual_fairness":
        theil = metrics.get("theil_index", 0)
        fairness_level = "excellent" if theil < 0.05 else ("good" if theil < 0.1 else ("fair" if theil < 0.2 else "poor"))
        return {
            "check": check_name,
            "result": theil,
            "fairness_level": fairness_level,
            "description": FAIRNESS_CHECKS[check_name]["criteria"]
        }
    
    elif check_name == "group_fairness":
        return {
            "check": check_name,
            "metrics": {
                "demographic_parity": metrics.get("dp_diff", 0),
                "equal_opportunity": metrics.get("eo_diff", 0),
                "false_positive_rate": metrics.get("fpr_diff", 0),
                "equalized_odds": metrics.get("equalized_odds", 0)
            },
            "description": FAIRNESS_CHECKS[check_name]["criteria"]
        }
    
    else:
        return {"check": check_name, "status": "NOT_IMPLEMENTED"}


def generate_recommendations(metrics, bias_checks):
    """Generate actionable recommendations based on metrics and bias checks."""
    recommendations = []
    
    # Check each metric and generate recommendations
    if metrics.get("dp_diff", 0) > 0.15:
        recommendations.append({
            "issue": "Demographic Parity Disparity",
            "severity": "High",
            "suggestion": "Review decision-making process. Consider re-weighting training data or adjusting thresholds per group."
        })
    
    if metrics.get("eo_diff", 0) > 0.20:
        recommendations.append({
            "issue": "Equal Opportunity Gap",
            "severity": "High",
            "suggestion": "Qualified individuals from some groups have lower approval rates. Consider fairness-aware retraining."
        })
    
    if metrics.get("fpr_diff", 0) > 0.20:
        recommendations.append({
            "issue": "Error Rate Disparity",
            "severity": "Medium",
            "suggestion": "False positive rates differ significantly. Tune decision thresholds separately per group."
        })
    
    if metrics.get("dp_ratio", 0) < 0.8:
        recommendations.append({
            "issue": "Legal Compliance (80% Rule)",
            "severity": "Critical",
            "suggestion": "Model may violate employment discrimination laws. Immediate remediation required."
        })
    
    if metrics.get("theil_index", 0) > 0.25:
        recommendations.append({
            "issue": "High Outcome Inequality",
            "severity": "Medium",
            "suggestion": "Outcomes are concentrated in specific groups. Consider stratified fairness constraints."
        })
    
    if len(recommendations) == 0:
        recommendations.append({
            "issue": "No Major Issues",
            "severity": "Low",
            "suggestion": "Model appears fair across measured metrics. Continue monitoring during deployment."
        })
    
    return recommendations
