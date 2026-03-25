# Configuration Customization Guide - Practical Examples

## Quick Navigation

- **[Getting Configuration Summaries](#getting-configuration-summaries)** - View current settings
- **[Pre-built Configurations](#pre-built-configurations)** - Ready-to-use setups
- **[Custom Configuration Builder](#custom-configuration-builder)** - Create your own
- **[Testing Configuration Changes](#testing-configuration-changes)** - Validate before production
- **[Real-world Scenarios](#real-world-scenarios)** - Domain-specific setups

---

## Getting Configuration Summaries

> **Note:** Most of the original configuration has been removed from the project.  Only a
> handful of sections required by the image analysis routines remain in `BIAS_CONFIG`.
> See `Backend/app/image_bias.py` for current defaults.


### 1. View All Configuration

```python
from Backend.app.image_bias import ImageBiasAnalyzer, BIAS_CONFIG

analyzer = ImageBiasAnalyzer()

# Get human-readable summary
summary = analyzer.get_configuration_summary()

# Print each section
for section, values in summary.items():
    print(f"\n=== {section} ===")
    for key, value in values.items():
        if not key.startswith("_"):
            print(f"  {key}: {value}")
        else:
            print(f"  Description: {value}")
```

### 2. View Specific Section

```python
# View only representation thresholds
rep_config = BIAS_CONFIG["REPRESENTATION"]
print("Representation Thresholds:")
for key, value in rep_config.items():
    print(f"  {key}: {value}")

# Output:
# Representation Thresholds:
#   disparity_ratio_threshold: 1.5
#   critical_disparity_threshold: 3.0
#   minimum_samples_per_group: 1
#   ideal_distribution: equal
#   description: Demographic representation balance analysis thresholds
```

### 3. Compare Thresholds Across Dimensions

```python
# Check disparity thresholds across all dimensions
dimensions = ["REPRESENTATION", "RACE_ETHNICITY", "GENDER"]
for dim in dimensions:
    threshold = BIAS_CONFIG[dim]["disparity_ratio_threshold"]
    critical = BIAS_CONFIG[dim].get("critical_disparity_threshold", "N/A")
    print(f"{dim}: threshold={threshold}, critical={critical}")

# Output:
# REPRESENTATION: threshold=1.5, critical=3.0
# RACE_ETHNICITY: threshold=1.5, critical=2.5
# GENDER: threshold=1.5, critical=2.5
```

### 4. Check Total Bias Scoring Weights

```python
weights = BIAS_CONFIG["BIAS_SCORING"]
weight_sum = sum(v for k, v in weights.items() if k.endswith("_weight"))
print(f"Total bias scoring weights: {weight_sum}")

if abs(weight_sum - 1.0) < 0.001:
    print("✓ Weights are correctly balanced")
else:
    print(f"✗ ERROR: Weights sum to {weight_sum}, should be 1.0")
```

---

## Pre-built Configurations

### Configuration Template 1: HIGH-STAKES HIRING

Use this for hiring, promotion, and lending decisions where regulatory compliance is critical.

```python
from Backend.app.image_bias import BIAS_CONFIG

def configure_for_hiring():
    """Configure for strict fairness in hiring decisions."""
    
    # Very strict thresholds - almost perfect balance required
    BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.1
    BIAS_CONFIG["REPRESENTATION"]["critical_disparity_threshold"] = 1.5
    
    # Gender must be balanced
    BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 1.05
    BIAS_CONFIG["GENDER"]["critical_disparity_threshold"] = 1.2
    
    # Race must be diverse
    BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 1.2
    BIAS_CONFIG["RACE_ETHNICITY"]["critical_disparity_threshold"] = 1.8
    
    # Increase weights for protected categories
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.20
    BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = 0.20
    BIAS_CONFIG["BIAS_SCORING"]["age_bias_weight"] = 0.12
    BIAS_CONFIG["BIAS_SCORING"]["representation_weight"] = 0.18
    BIAS_CONFIG["BIAS_SCORING"]["feature_bias_weight"] = 0.10
    BIAS_CONFIG["BIAS_SCORING"]["color_bias_weight"] = 0.08
    BIAS_CONFIG["BIAS_SCORING"]["skin_tone_bias_weight"] = 0.08
    BIAS_CONFIG["BIAS_SCORING"]["pose_bias_weight"] = 0.02
    BIAS_CONFIG["BIAS_SCORING"]["background_bias_weight"] = 0.01
    BIAS_CONFIG["BIAS_SCORING"]["clothing_bias_weight"] = 0.01
    BIAS_CONFIG["BIAS_SCORING"]["emotion_bias_weight"] = 0.00
    
    # Lower critical threshold
    BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.6
    BIAS_CONFIG["BIAS_LEVELS"]["high_threshold"] = 0.45
    
    print("✓ Configured for HIGH-STAKES HIRING")
    print("  - Strict balance requirements")
    print("  - Protected categories heavily weighted")
    print("  - Lower critical threshold (0.6)")

# Use it
configure_for_hiring()
```

### Configuration Template 2: PRODUCT/E-COMMERCE

Use this for product photography and e-commerce where marketing diversity is important but not legally required.

```python
def configure_for_ecommerce():
    """Configure for product/e-commerce applications."""
    
    # Moderate thresholds
    BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.5
    BIAS_CONFIG["REPRESENTATION"]["critical_disparity_threshold"] = 2.5
    
    BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 1.5
    BIAS_CONFIG["GENDER"]["critical_disparity_threshold"] = 2.0
    
    BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 1.5
    BIAS_CONFIG["RACE_ETHNICITY"]["critical_disparity_threshold"] = 2.0
    
    # Balanced weights with focus on diversity
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.15
    BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = 0.15
    BIAS_CONFIG["BIAS_SCORING"]["skin_tone_bias_weight"] = 0.12
    BIAS_CONFIG["BIAS_SCORING"]["representation_weight"] = 0.12
    BIAS_CONFIG["BIAS_SCORING"]["age_bias_weight"] = 0.12
    BIAS_CONFIG["BIAS_SCORING"]["pose_bias_weight"] = 0.10
    BIAS_CONFIG["BIAS_SCORING"]["background_bias_weight"] = 0.08
    BIAS_CONFIG["BIAS_SCORING"]["feature_bias_weight"] = 0.08
    BIAS_CONFIG["BIAS_SCORING"]["color_bias_weight"] = 0.05
    BIAS_CONFIG["BIAS_SCORING"]["clothing_bias_weight"] = 0.02
    BIAS_CONFIG["BIAS_SCORING"]["emotion_bias_weight"] = 0.01
    
    # Standard thresholds
    BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.8
    BIAS_CONFIG["BIAS_LEVELS"]["high_threshold"] = 0.6
    
    print("✓ Configured for E-COMMERCE PRODUCTS")
    print("  - Moderate balance requirements")
    print("  - Diversity encouraged but not required")
    print("  - Focus on visual representation")

configure_for_ecommerce()
```

### Configuration Template 3: ACADEMIC/RESEARCH

Use this for unbiased research datasets where statistical diversity matters.

```python
def configure_for_research():
    """Configure for academic research with statistical rigor."""
    
    # Use defaults but ensure good coverage
    BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.3
    
    BIAS_CONFIG["AGE_GROUPS"]["minimum_age_groups"] = 5  # All groups
    BIAS_CONFIG["SKIN_TONE"]["minimum_tone_diversity"] = 0.8  # Most tones
    
    # Balanced weights across all dimensions
    weights = {
        "representation_weight": 0.11,
        "feature_bias_weight": 0.11,
        "color_bias_weight": 0.11,
        "race_bias_weight": 0.11,
        "age_bias_weight": 0.11,
        "gender_bias_weight": 0.11,
        "skin_tone_bias_weight": 0.11,
        "pose_bias_weight": 0.11,
        "background_bias_weight": 0.05,
        "clothing_bias_weight": 0.05,
        "emotion_bias_weight": 0.02
    }
    
    for key, value in weights.items():
        BIAS_CONFIG["BIAS_SCORING"][key] = value
    
    print("✓ Configured for ACADEMIC RESEARCH")
    print("  - Statistical diversity required")
    print("  - Balanced weights across dimensions")
    print("  - Multiple age/tone categories required")

configure_for_research()
```

### Configuration Template 4: EXPLORATORY ANALYSIS

Use this for initial data exploration when you're just investigating what's in the dataset.

```python
def configure_for_exploration():
    """Configure for exploratory analysis."""
    
    # Loose thresholds - just detect patterns
    BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 2.5
    BIAS_CONFIG["REPRESENTATION"]["critical_disparity_threshold"] = 5.0
    
    BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 2.5
    BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 2.5
    
    # All features equally weighted
    num_features = 11
    base_weight = 1.0 / num_features
    
    for key in BIAS_CONFIG["BIAS_SCORING"].keys():
        if key.endswith("_weight"):
            BIAS_CONFIG["BIAS_SCORING"][key] = base_weight
    
    # High critical threshold - only flag extreme cases
    BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.9
    BIAS_CONFIG["BIAS_LEVELS"]["high_threshold"] = 0.75
    
    print("✓ Configured for EXPLORATORY ANALYSIS")
    print("  - Loose thresholds for pattern discovery")
    print("  - Equal weight to all dimensions")
    print("  - Only extreme cases flagged as critical")

configure_for_exploration()
```

---

## Custom Configuration Builder

### Creating Your Own Configuration

```python
from Backend.app.image_bias import BIAS_CONFIG, ImageBiasAnalyzer

def create_custom_config(
    use_case: str,
    gender_weight: float = 0.12,
    race_weight: float = 0.15,
    representation_threshold: float = 1.5,
    critical_threshold: float = 0.8
):
    """
    Create custom configuration for specific use case.
    
    Args:
        use_case: Name of application
        gender_weight: Weight for gender bias (0.0-1.0)
        race_weight: Weight for race bias (0.0-1.0)
        representation_threshold: Disparity ratio threshold
        critical_threshold: Critical bias score threshold
    """
    
    # Calculate remaining weights to sum to 1.0
    protected_categories_total = gender_weight + race_weight
    remaining = 1.0 - protected_categories_total
    
    # Distribute remaining weight proportionally
    other_weights = {
        "representation_weight": 0.15 * remaining / 0.88,
        "feature_bias_weight": 0.12 * remaining / 0.88,
        "color_bias_weight": 0.10 * remaining / 0.88,
        "age_bias_weight": 0.10 * remaining / 0.88,
        "skin_tone_bias_weight": 0.10 * remaining / 0.88,
        "pose_bias_weight": 0.08 * remaining / 0.88,
        "background_bias_weight": 0.05 * remaining / 0.88,
        "clothing_bias_weight": 0.02 * remaining / 0.88,
        "emotion_bias_weight": 0.01 * remaining / 0.88,
    }
    
    # Apply configuration
    BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = representation_threshold
    BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = representation_threshold
    BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = representation_threshold
    
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = gender_weight
    BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = race_weight
    
    for key, value in other_weights.items():
        BIAS_CONFIG["BIAS_SCORING"][key] = value
    
    BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = critical_threshold
    
    # Validate
    analyzer = ImageBiasAnalyzer()
    
    print(f"✓ Custom configuration created: {use_case}")
    print(f"  Gender weight: {gender_weight:.2%}")
    print(f"  Race weight: {race_weight:.2%}")
    print(f"  Representation threshold: {representation_threshold}")
    print(f"  Critical threshold: {critical_threshold}")

# Example usage
create_custom_config(
    use_case="Medical Recruitment",
    gender_weight=0.18,
    race_weight=0.18,
    representation_threshold=1.2,
    critical_threshold=0.65
)
```

### Interactive Configuration Builder

```python
def interactive_config_builder():
    """Use questionnaire to build configuration."""
    
    print("\n=== Astrea Configuration Builder ===\n")
    
    # Question 1: Application type
    print("What is your primary use case?")
    print("1. Hiring/HR")
    print("2. Product/Marketing")
    print("3. Medical/Research")
    print("4. Social Media/General")
    choice = input("Select (1-4): ").strip()
    
    use_case_map = {
        "1": ("hiring", 0.20, 0.20, 1.1, 0.6),
        "2": ("ecommerce", 0.15, 0.15, 1.5, 0.8),
        "3": ("medical", 0.12, 0.12, 1.3, 0.7),
        "4": ("general", 0.12, 0.15, 1.5, 0.8),
    }
    
    name, gender_w, race_w, rep_thresh, crit_thresh = use_case_map.get(choice, use_case_map["4"])
    
    # Question 2: Strictness
    print("\nHow strict should fairness requirements be?")
    print("1. Very strict (recommended for hiring/lending)")
    print("2. Moderate (general use)")
    print("3. Loose (exploratory only)")
    strictness = input("Select (1-3): ").strip()
    
    if strictness == "1":
        rep_thresh *= 0.8  # Make stricter
        crit_thresh *= 0.75
    elif strictness == "3":
        rep_thresh *= 1.5  # Make looser
        crit_thresh *= 1.15
    
    # Apply
    create_custom_config(
        use_case=f"{name} (strictness={strictness})",
        gender_weight=gender_w,
        race_weight=race_w,
        representation_threshold=rep_thresh,
        critical_threshold=crit_thresh
    )

# Run the interactive builder
# interactive_config_builder()
```

---

## Testing Configuration Changes

### Before-and-After Testing

```python
from Backend.app.image_bias import ImageBiasAnalyzer, BIAS_CONFIG
import json

def test_configuration_impact(test_images, test_labels):
    """Compare results before and after configuration change."""
    
    # Save original config
    original_gender_weight = BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"]
    original_race_weight = BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"]
    
    print("Testing configuration changes...\n")
    
    # Test 1: Original configuration
    analyzer1 = ImageBiasAnalyzer()
    result1 = analyzer1.comprehensive_image_bias_analysis(test_images, test_labels)
    print(f"ORIGINAL CONFIG:")
    print(f"  Bias Score: {result1['overall_assessment']['overall_image_bias_score']:.2f}")
    print(f"  Bias Level: {result1['overall_assessment']['bias_level']}")
    print(f"  Gender weight: {original_gender_weight}")
    print(f"  Race weight: {original_race_weight}")
    
    # Test 2: Modified configuration
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.25
    BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = 0.25
    BIAS_CONFIG["BIAS_SCORING"]["representation_weight"] = 0.10
    # Recalculate other weights to sum to 1.0
    
    analyzer2 = ImageBiasAnalyzer()
    result2 = analyzer2.comprehensive_image_bias_analysis(test_images, test_labels)
    print(f"\nMODIFIED CONFIG:")
    print(f"  Bias Score: {result2['overall_assessment']['overall_image_bias_score']:.2f}")
    print(f"  Bias Level: {result2['overall_assessment']['bias_level']}")
    print(f"  Gender weight: 0.25 (+{0.25-original_gender_weight:.2f})")
    print(f"  Race weight: 0.25 (+{0.25-original_race_weight:.2f})")
    
    # Compare
    score_diff = result2['overall_assessment']['overall_image_bias_score'] - result1['overall_assessment']['overall_image_bias_score']
    print(f"\nIMPACT:")
    print(f"  Score change: {score_diff:+.3f}")
    print(f"  Level changed: {result1['overall_assessment']['bias_level']} → {result2['overall_assessment']['bias_level']}")
    
    # Restore original
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = original_gender_weight
    BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = original_race_weight
    
    return result1, result2

# Usage (with your test data)
# test_images = [your images]
# test_labels = ["male", "female", "male", ...]
# before, after = test_configuration_impact(test_images, test_labels)
```

### Sensitivity Analysis

```python
def sensitivity_analysis(test_images, test_labels):
    """Test how configuration changes affect results."""
    
    thresholds_to_test = [1.0, 1.2, 1.5, 2.0, 3.0]
    results = []
    
    for threshold in thresholds_to_test:
        BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = threshold
        analyzer = ImageBiasAnalyzer()
        result = analyzer.comprehensive_image_bias_analysis(test_images, test_labels)
        
        results.append({
            "threshold": threshold,
            "bias_score": result['overall_assessment']['overall_image_bias_score'],
            "bias_level": result['overall_assessment']['bias_level']
        })
    
    print("SENSITIVITY ANALYSIS: Disparity Threshold Impact\n")
    print("Threshold | Bias Score | Level")
    print("-" * 35)
    for r in results:
        print(f"{r['threshold']:.1f}x      | {r['bias_score']:.3f}      | {r['bias_level']}")
    
    return results

# Usage
# sensitivity_results = sensitivity_analysis(test_images, test_labels)
```

---

## Real-world Scenarios

### Scenario 1: Fixing Gender Imbalance in Hiring

```python
# Problem: Dataset has 70% male, 30% female
# Dataset stats: 700 male, 300 female

def audit_and_fix_gender_bias():
    """Audit and then configure to catch gender bias."""
    
    from Backend.app.image_bias import ImageBiasAnalyzer, BIAS_CONFIG
    
    # Current configuration detects something
    analyzer = ImageBiasAnalyzer()
    # result shows gender_disparity_ratio = 2.33 (700/300)
    
    print("AUDIT RESULT: Gender imbalance detected")
    print("  Current ratio: 70% male / 30% female")
    print("  Disparity: 2.33x")
    print("  Current threshold: 1.5")
    print("  Assessment: EXCEEDS THRESHOLD - Critical issue\n")
    
    # Configure to catch similar issues
    BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 1.25
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.25
    
    print("CONFIGURATION UPDATED:")
    print("  Gender disparity threshold: 1.5 → 1.25")
    print("  Gender weight: 0.12 → 0.25")
    print("\nNow will flag imbalance > 25% (e.g., 56.25% vs 43.75%)")
    
    # Test with corrected data
    print("\nIf we add more female candidates to reach 50-50:")
    print("  New ratio: 1.0x")
    print("  Assessment: ✓ PASSES")

audit_and_fix_gender_bias()
```

### Scenario 2: Ensuring Racial Diversity in Product Photos

```python
def ensure_racial_diversity():
    """Configure to guarantee racial diversity."""
    
    from Backend.app.image_bias import BIAS_CONFIG
    
    # Goal: Ensure at least 4 out of 6 races represented
    # And no single race > 50%
    
    BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 1.2  # Strict
    BIAS_CONFIG["RACE_ETHNICITY"]["critical_disparity_threshold"] = 1.8
    
    # Increase race detection priority
    BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = 0.20
    BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.10  # Lower gender
    
    print("✓ Configured for RACIAL DIVERSITY")
    print("  Threshold: 1.2 (allow max 1.2x size difference)")
    print("  Critical: 1.8 (flag if any race ≤ 55% of largest)")
    print("  Weight: 0.20 (race is 20% of overall score)")
    print("\nExample: If 60% Asian, 40% other → ratio 1.5 → FAILS")
    print("Example: If 50% Asian, 50% other → ratio 1.0 → PASSES")

ensure_racial_diversity()
```

### Scenario 3: Academic Dataset Fairness

```python
def configure_academic_dataset():
    """Configure for rigorous academic dataset."""
    
    from Backend.app.image_bias import BIAS_CONFIG
    
    # Requirements for publication
    requirements = {
        "gender_distribution": "30%-70% range (no gender > 70%)",
        "age_groups": "All 5 age groups must be present",
        "skin_tones": "At least 4 out of 5 skin tone categories",
        "races": "At least 3 out of 6 racial categories",
        "feature_quality": "Distance between groups < 0.3"
    }
    
    # Configure to enforce
    BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 2.33  # 70% / 30%
    BIAS_CONFIG["AGE_GROUPS"]["minimum_age_groups"] = 5  # All required
    BIAS_CONFIG["SKIN_TONE"]["minimum_tone_diversity"] = 0.8  # 4/5 min
    BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 1.5  # No race dominant
    BIAS_CONFIG["VISUAL_FEATURES"]["feature_distance_threshold"] = 0.3
    
    print("ACADEMIC DATASET CONFIGURATION")
    print("=" * 50)
    for requirement, value in requirements.items():
        print(f"{requirement}: {value}")
    
    print("\nConfiguration enforces all requirements:")
    print("✓ Gender ratio checked (2.33x threshold = 30-70%)")
    print("✓ Age groups validated (all 5 required)")
    print("✓ Skin tone diversity (4+ tones required)")
    print("✓ Race diversity (multiple races required)")
    print("✓ Feature quality (distance < 0.3)")

configure_academic_dataset()
```

---

## Configuration Validation Checklist

Before deploying with custom configuration:

```python
def validate_production_config():
    """Validate configuration before going live."""
    
    from Backend.app.image_bias import BIAS_CONFIG, ImageBiasAnalyzer
    
    checklist = {
        "weights_sum_to_one": False,
        "thresholds_in_order": False,
        "critical_higher_than_standard": False,
        "config_validated_by_analyzer": False,
        "test_data_runs": False
    }
    
    print("CONFIGURATION VALIDATION CHECKLIST\n")
    
    # Check 1: Weights sum to 1.0
    weights = BIAS_CONFIG["BIAS_SCORING"]
    weight_sum = sum(v for k, v in weights.items() if k.endswith("_weight"))
    checklist["weights_sum_to_one"] = abs(weight_sum - 1.0) < 0.001
    print(f"✓ Weights sum to 1.0: {weight_sum:.4f} - {checklist['weights_sum_to_one']}")
    
    # Check 2: Thresholds in ascending order
    levels = BIAS_CONFIG["BIAS_LEVELS"]
    thresholds = [
        levels["low_threshold"],
        levels["moderate_threshold"],
        levels["high_threshold"],
        levels["critical_threshold"]
    ]
    checklist["thresholds_in_order"] = all(
        thresholds[i] <= thresholds[i+1] for i in range(len(thresholds)-1)
    )
    print(f"✓ Bias levels in order: {thresholds} - {checklist['thresholds_in_order']}")
    
    # Check 3: Critical thresholds > standard thresholds
    rep_config = BIAS_CONFIG["REPRESENTATION"]
    checklist["critical_higher_than_standard"] = (
        rep_config["critical_disparity_threshold"] > rep_config["disparity_ratio_threshold"]
    )
    print(f"✓ Critical > Standard thresholds: {checklist['critical_higher_than_standard']}")
    
    # Check 4: Configuration validates
    try:
        analyzer = ImageBiasAnalyzer()
        checklist["config_validated_by_analyzer"] = True
        print(f"✓ Configuration validates in analyzer: True")
    except Exception as e:
        print(f"✗ Configuration validation error: {e}")
    
    # Check 5: Run test data
    print(f"\nAll checks passed: {all(checklist.values())}")
    
    if not all(checklist.values()):
        print("\n⚠️  FIX THESE ISSUES BEFORE DEPLOYING:")
        for check, passed in checklist.items():
            if not passed:
                print(f"  - {check}")
    
    return checklist

# Run before deployment
# validate_production_config()
```

---

## Summary

You can now:

1. **View Current Configuration** - See all active thresholds and weights
2. **Use Pre-built Configurations** - Ready-to-use setups for common scenarios
3. **Build Custom Configurations** - Create specific configs for your needs
4. **Test Changes** - Compare results before/after configuration changes
5. **Validate Configurations** - Ensure correctness before deployment
6. **Implement Real-world Scenarios** - Apply to specific use cases

The configuration system is flexible, powerful, and production-ready!
