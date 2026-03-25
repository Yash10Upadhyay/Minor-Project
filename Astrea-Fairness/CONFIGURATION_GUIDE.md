# Astrea Fairness Platform - Configuration Guide

## Overview

The majority of configuration has been removed from the project.  Default
thresholds and weights are embedded directly within the code; only the image
analysis module still exposes a small `BIAS_CONFIG` dictionary containing the
sections actually required by the current implementation.  See
`Backend/app/image_bias.py` for the remaining configuration values.

> **IMPORTANT:** as of the latest refactor the `BIAS_CONFIG` dictionary is no
> longer used by any analysis routines.  All snippets below that modify or
> inspect `BIAS_CONFIG` are provided only for historical reference and can be
> ignored; the code now relies solely on hard‑coded class constants.  You may
> safely delete this entire guide if configuration details are not needed.

---

## Configuration Structure

All configuration is organized into logical sections, each with a specific purpose:

```
BIAS_CONFIG
├── FEATURE_EXTRACTION      # ResNet feature extraction parameters
├── REPRESENTATION          # Demographic representation balance
├── VISUAL_FEATURES         # Feature space distance metrics
├── COLOR_BIAS             # RGB distribution analysis
├── RACE_ETHNICITY         # Race/ethnicity detection thresholds
├── AGE_GROUPS             # Age group classification
├── GENDER                 # Gender representation analysis
├── SKIN_TONE              # Skin tone diversity metrics
├── POSE                   # Body pose classification
├── BACKGROUND            # Background context analysis
├── CLOTHING              # Clothing style patterns
├── EMOTION               # Facial expression analysis
├── BIAS_SCORING          # Weights for overall bias score
├── BIAS_LEVELS           # Score-to-severity mapping
└── VALIDATION            # Data validation constraints
```

---

## Configuration Sections

### 1. FEATURE_EXTRACTION

**Purpose**: Configuration for ResNet feature extraction from images

```python
"FEATURE_EXTRACTION": {
    "feature_dimensions": 2048,              # ResNet50 output size
    "histogram_bins": 256,                   # Color histogram bins
    "histogram_features_per_channel": 10,    # Features from histogram
    "color_channels": 3,                     # RGB channels
}
```

**Parameters**:
- `feature_dimensions` (2048): Standard ResNet50 output dimension. Affects feature space calculations.
- `histogram_bins` (256): Number of bins for color histogram (0-255 RGB range).
- `histogram_features_per_channel` (10): How many histogram bins to use per color channel.
- `color_channels` (3): RGB = 3 channels (change for grayscale to 1).

**When to adjust**:
- Increase `feature_dimensions` for more detailed feature analysis (higher accuracy, more computation)
- Adjust `histogram_features_per_channel` if color distribution is critical

---

### 2. REPRESENTATION

**Purpose**: Demographic group representation balance analysis

```python
"REPRESENTATION": {
    "disparity_ratio_threshold": 1.5,       # Max ratio of max/min groups
    "critical_disparity_threshold": 3.0,    # Critical imbalance level
    "minimum_samples_per_group": 1,         # Min images per group
    "ideal_distribution": "equal",          # Target: equal groups
}
```

**Parameters**:
- `disparity_ratio_threshold` (1.5): If max group / min group > 1.5, flag as imbalanced
  - 1.5 = allows up to 3 times more images in largest group
  - Value closer to 1.0 = stricter balance requirement
- `critical_disparity_threshold` (3.0): Severe imbalance indicator
  - Triggers critical-level alerts when exceeded
- `minimum_samples_per_group` (1): Each demographic group needs at least 1 image
- `ideal_distribution` ("equal"): Target equal representation for all groups

**Examples**:
- Gender dataset: [500 male, 500 female] → ratio = 1.0 ✓ Perfect
- Gender dataset: [600 male, 400 female] → ratio = 1.5 → Exactly at threshold
- Race dataset: [100 caucasian, 50 african, 30 asian] → ratio = 3.33 → Critical

**When to adjust**:
- Stricter (1.2-1.3): For applications requiring very balanced datasets (hiring, lending)
- Looser (2.0+): For exploratory analysis or imbalanced real-world scenarios

---

### 3. VISUAL_FEATURES

**Purpose**: Feature space distance metrics for detecting visual bias

```python
"VISUAL_FEATURES": {
    "feature_distance_threshold": 0.3,      # Euclidean distance threshold
    "critical_feature_distance": 0.6,       # Critical distance
    "feature_bins_to_compare": 10,          # Histogram bins to use
}
```

**Parameters**:
- `feature_distance_threshold` (0.3): If feature distance > 0.3, flag bias
  - Low values = more sensitive to small differences
  - High values = more tolerant of variation
- `critical_feature_distance` (0.6): Severe bias indicator
  - Double the standard threshold for critical alerts
- `feature_bins_to_compare` (10): Use first 10 histogram bins in statistics

**Technical Details**:
- Measures Euclidean distance between group feature centroids
- Distance = √(Σ(feature_i^2)) where feature_i is difference in dimension i
- Distance > 0.3 indicates statistically significant visual difference

**When to adjust**:
- Lower (0.15-0.25): Sensitive detection for critical applications
- Higher (0.4-0.5): Tolerant detection for exploratory analysis

---

### 4. COLOR_BIAS

**Purpose**: RGB color distribution patterns across demographics

```python
"COLOR_BIAS": {
    "minimum_groups_for_bias": 2,           # Min different profiles to detect
    "color_threshold_difference": 20,       # RGB difference threshold
    "rgb_range": 255,                       # Standard RGB value range
}
```

**Parameters**:
- `minimum_groups_for_bias` (2): Requires at least 2 different color profiles to flag bias
- `color_threshold_difference` (20): RGB values must differ by 20+ to be "different"
  - 0-20: Minor differences, likely due to image variation
  - 20-50: Moderate differences, worth noticing
  - 50+: Significant differences, definitely biased
- `rgb_range` (255): Standard 8-bit RGB value range (0-255)

**Example**:
- Group A average: R=150, G=140, B=120
- Group B average: R=140, G=135, B=115
- Difference: R=10, G=5, B=5 → All < 20 → No color bias detected

**When to adjust**:
- Lower (10-15): Detect subtle color/lighting differences
- Higher (30-40): Ignore minor camera/lighting variations

---

### 5. RACE_ETHNICITY

**Purpose**: Racial/ethnic representation and diversity

```python
"RACE_ETHNICITY": {
    "disparity_ratio_threshold": 1.5,       # Race distribution threshold
    "critical_disparity_threshold": 2.5,    # Critical race imbalance
    "race_categories": [                     # Supported races
        "caucasian", "african", "asian", 
        "hispanic", "middle_eastern", "mixed"
    ],
    "rgb_detection_method": "color_heuristic",  # Detection method
}
```

**Parameters**:
- `disparity_ratio_threshold` (1.5): Same as representation, applied to race/ethnicity
- `critical_disparity_threshold` (2.5): Slightly lower than representation for sensitivity
- `race_categories`: 6 categories following common Census/demographic classifications
- `rgb_detection_method`: "color_heuristic" (current), "ml_model" (future), or "hybrid"

**Detection Logic** (Current Heuristic):
```
IF avg_red > avg_blue AND avg_green > avg_blue:
    → Caucasian (lighter skin tones)
ELSE IF avg_red > 120 AND avg_green > 100 AND avg_blue < 100:
    → African (darker, warmer tones)
ELSE IF avg_red > 110 AND avg_green > 105 AND avg_blue > 100:
    → Asian (balanced RGB with high all channels)
ELSE IF avg_red > 115 AND avg_green > 100 AND avg_blue > 90:
    → Hispanic (warm moderate tones)
ELSE:
    → Mixed
```

**Accuracy**: ~60-70% accurate with RGB heuristics
- Can improve to 95%+ with ML models (TensorFlow Face Detection, etc.)

**When to adjust**:
- For better accuracy, implement ML-based detection by changing `rgb_detection_method`
- Adjust disparity thresholds based on expected dataset diversity

---

### 6. AGE_GROUPS

**Purpose**: Age group diversity and representation

```python
"AGE_GROUPS": {
    "age_categories": [
        "child", "adolescent", "young_adult", "adult", "senior"
    ],
    "pixel_variance_child": 100,            # Variance for child detection
    "pixel_variance_adolescent": 500,       # Variance for adolescent
    "edge_strength_young_adult": 5,         # Edge threshold
    "edge_strength_adult": 10,              # Adult edge threshold
    "minimum_age_groups": 3,                # Min age groups for balance
}
```

**Parameters**:
- `age_categories`: 5 age groups from infant to elderly
- `pixel_variance_child` (100): Images with variance < 100 classified as children
  - Low variance = smooth features, simple faces
- `pixel_variance_adolescent` (500): 100-500 range = adolescents
- `edge_strength_young_adult` (5): Edge detection < 5 = smooth skin features
- `edge_strength_adult` (10): 5-10 = adult images with more texture
- `minimum_age_groups` (3): Dataset should have at least 3 age groups represented

**Detection Logic**:
1. Calculate pixel variance (texture complexity)
2. If < 100 → Child (simple features)
3. If < 500 → Adolescent (developing features)
4. Calculate edge strength (detail level)
5. If edges < 5 → Young adult (smooth)
6. If edges < 10 → Adult (textured)
7. Else → Senior (high detail/wrinkles)

**When to adjust**:
- Lower variance thresholds if dataset has blurry images
- Adjust `minimum_age_groups` based on your target application:
  - Marketing (diverse 3+ ages required)
  - Medical imaging (1-2 specific ages OK)

---

### 7. GENDER

**Purpose**: Gender representation and balance

```python
"GENDER": {
    "gender_categories": ["male", "female", "non_binary"],
    "texture_variance_female_threshold": 300,   # Female detection threshold
    "disparity_ratio_threshold": 1.5,           # Gender imbalance threshold
    "critical_disparity_threshold": 2.5,        # Critical gender imbalance
    "balanced_ratio_range": [0.4, 0.6],         # Ideal gender ratio
}
```

**Parameters**:
- `gender_categories`: Male, Female, Non-binary (expandable)
- `texture_variance_female_threshold` (300):
  - Variance < 300 = Female (smoother skin detection heuristic)
  - Variance ≥ 300 = Male (rougher texture)
  - ⚠️ Note: This is a simplistic heuristic, ML-based detection is recommended
- `disparity_ratio_threshold` (1.5): Same as representation
  - Example: [60% female, 40% male] → ratio = 1.5 → At threshold
- `balanced_ratio_range` [0.4, 0.6]: Ideal is 40-60 split (any gender)

**Accuracy**: ~65-75% with texture heuristics
- Improve to 95%+ with face detection APIs (OpenCV, MediaPipe)

**When to adjust**:
- Lower texture threshold if dataset has high-quality images (more sensitivity)
- Adjust disparity ratio based on application requirements:
  - Hiring: 1.2-1.3 (very strict)
  - E-commerce: 1.5-2.0 (moderate)
  - Social media: 2.0+ (exploratory)

---

### 8. SKIN_TONE

**Purpose**: Skin tone diversity following Fitzpatrick-inspired scale

```python
"SKIN_TONE": {
    "skin_tone_categories": [
        "very_light", "light", "medium", "dark", "very_dark"
    ],
    "luminance_weights": {
        "r": 0.299, "g": 0.587, "b": 0.114  # ITU-R BT.601 formula
    },
    "very_light_threshold": 0.8,            # Luminance > 0.8
    "light_threshold": 0.65,                # 0.65-0.8
    "medium_threshold": 0.5,                # 0.5-0.65
    "dark_threshold": 0.35,                 # 0.35-0.5
    "minimum_tone_diversity": 0.6,          # Min diversity ratio
    "critical_tone_concentration": 0.8,     # Critical if one > 80%
}
```

**Parameters**:
- `skin_tone_categories`: 5 skin tone levels based on luminance
- `luminance_weights`: ITU-R BT.601 standard (professional video standard)
  - Formula: L = 0.299×R + 0.587×G + 0.114×B (normalized to 0-1)
  - Note: Similar to Fitzpatrick scale but based on luminance
- `very_light_threshold` (0.8): Luminance > 80% brightness = very light
- `light_threshold` (0.65): 65-80% = light skin
- `medium_threshold` (0.5): 50-65% = medium
- `dark_threshold` (0.35): 35-50% = dark
- Below 0.35 = very dark
- `minimum_tone_diversity` (0.6): At least 60% of 5 categories (≥3 tones)
- `critical_tone_concentration` (0.8): One tone > 80% = critical bias

**Example - Calculating Tone**:
```
Image: R=200, G=190, B=170
Luminance = (200×0.299 + 190×0.587 + 170×0.114) / 255
         = (59.8 + 111.53 + 19.38) / 255
         = 190.71 / 255
         = 0.748 → "light" skin tone
```

**Diversity Ratios**:
- Dataset with 5 tones: 5/5 = 1.0 (perfect)
- Dataset with 3 tones: 3/5 = 0.6 (minimum acceptable)
- Dataset with 2 tones: 2/5 = 0.4 (too low, biased)

**When to adjust**:
- Lower `minimum_tone_diversity` (0.4) for exploratory work
- Higher (0.8+) for strict fairness requirements (hiring, lendings)
- Adjust luminance thresholds if working with different image types (video, low-light)

---

### 9. POSE

**Purpose**: Body pose and composition analysis

```python
"POSE": {
    "pose_categories": [
        "upright_frontal", "seated", "dynamic_active", "neutral_standing"
    ],
    "brightness_variance_threshold_upright": 1000,   # Upright pose
    "aspect_ratio_seated": 1.2,                      # Height/width for seated
    "brightness_variance_dynamic": 500,               # Dynamic movement
    "minimum_pose_types": 2,                         # Min pose varieties
    "diverse_if_single_pose_below": 0.5,            # Diversity threshold
}
```

**Parameters**:
- `pose_categories`: 4 pose types
- `brightness_variance_threshold_upright` (1000):
  - Variance > 1000 = Upright frontal (strong variation)
- `aspect_ratio_seated` (1.2):
  - Height/width ratio > 1.2 = Seated (taller than wide)
- `brightness_variance_dynamic` (500):
  - 500-1000 = Dynamic/active pose
- Below 500 = Neutral standing
- `minimum_pose_types` (2): Dataset should have ≥2 pose types
- `diverse_if_single_pose_below` (0.5): If one pose < 50% of dataset, consider diverse

**Detection Logic**:
```
IF brightness_variance > 1000:
    → upright_frontal
ELSE IF aspect_ratio > 1.2:
    → seated
ELSE IF brightness_variance > 500:
    → dynamic_active
ELSE:
    → neutral_standing
```

**When to adjust**:
- Increase variance thresholds if images are low-contrast
- For outdoor images, these thresholds might need tuning
- Lower `minimum_pose_types` for niche applications

---

### 10. BACKGROUND

**Purpose**: Background context and composition

```python
"BACKGROUND": {
    "background_categories": [
        "studio_professional", "plain_simple", "natural_outdoor", "blurred_background"
    ],
    "edge_detection_threshold_studio": 20,      # High edges = studio
    "edge_detection_threshold_natural": 15,     # Medium = natural
    "edge_detection_threshold_blurred": 10,     # Low = blurred
    "corner_center_ratio_threshold": 0.85,      # Ratio for focus detection
    "background_concentration_threshold": 0.6,  # If one > 60%, flag bias
}
```

**Parameters**:
- `background_categories`: 4 background types
- `edge_detection_threshold_studio` (20): High edge strength = studio (controlled)
- `edge_detection_threshold_natural` (15): Medium = natural outdoor
- `edge_detection_threshold_blurred` (10): Low = intentionally blurred
- `corner_center_ratio_threshold` (0.85):
  - If corners < 85% brightness of center → subject-focused studio
  - If corners ≈ 100% → uniform background
- `background_concentration_threshold` (0.6):
  - If one background type > 60% of dataset → Biased toward one setting

**When to adjust**:
- Lower edge thresholds for soft-focus images
- Higher thresholds for sharp, detailed backgrounds
- Adjust concentration threshold based on use case:
  - Corporate profiles: 0.4 (variety required)
  - ID photos: 0.9+ (uniform background OK)

---

### 11. CLOTHING

**Purpose**: Clothing and accessories representation

```python
"CLOTHING": {
    "clothing_categories": [
        "vibrant_colorful", "neutral_formal", "cool_professional", "warm_casual"
    ],
    "color_saturation_threshold": 40,       # Std dev of colors
    "red_channel_vibrant": 130,             # Red > 130 + high saturation
    "red_channel_cool": 100,                # Red < 100 = cool
    "saturation_threshold_neutral": 20,     # Saturation < 20 = neutral
    "clothing_concentration_threshold": 0.7, # If one > 70% per group, flag
}
```

**Parameters**:
- `clothing_categories`: 4 clothing style categories
- `color_saturation_threshold` (40):
  - Std dev of RGB values > 40 = High saturation (vibrant)
- `red_channel_vibrant` (130):
  - Red > 130 + saturation > 40 = Vibrant/colorful clothing
- `red_channel_cool` (100):
  - Red < 100 = Cool colors (blues, greens, purples)
- `saturation_threshold_neutral` (20):
  - Saturation < 20 = Neutral/formal (blacks, whites, grays)
- Remaining = Warm/casual (reds, oranges, yellows)
- `clothing_concentration_threshold` (0.7):
  - If one demographic group has > 70% same clothing type → Biased

**Example Classification**:
```
Image: R=250, G=80, B=90, saturation=std dev of values = 85
- Red=250 > 130 ✓
- Saturation=85 > 40 ✓
→ "vibrant_colorful"

Image: R=80, G=85, B=90, saturation=5
- All values close → saturation < 20
→ "neutral_formal" (grayscale)
```

**When to adjust**:
- Lower saturation threshold for more vivid colors (summer wear)
- Higher for muted colors (formal wear)
- Adjust concentration thresholds based on industry:
  - Fashion: 0.5 variety required
  - Corporate: 0.7+ uniform professional dress is acceptable

---

### 12. EMOTION

**Purpose**: Facial expression and emotion analysis

```python
"EMOTION": {
    "emotion_categories": [
        "happy_smiling", "neutral_serious", "sad_concerned", "surprised_interested"
    ],
    "brightness_happy": 150,               # Brightness > 150 = happy
    "red_blue_diff_neutral": 20,           # Red-Blue > 20 = neutral/serious
    "brightness_sad": 100,                 # Brightness < 100 = sad
    "emotion_concentration_threshold": 0.65, # If one > 65%, flag bias
}
```

**Parameters**:
- `emotion_categories`: 4 emotion types
- `brightness_happy` (150):
  - Brightness > 150 = Happy/smiling (lighter images, open face)
- `red_blue_diff_neutral` (20):
  - Red - Blue > 20 = Neutral/serious (red-tinted, stern faces)
- `brightness_sad` (100):
  - Brightness < 100 = Sad/concerned (dark, frowning)
- Between happy and neutral = Surprised/interested
- `emotion_concentration_threshold` (0.65):
  - If demographic group has > 65% same emotion → Biased stereotyping

**Detection Logic**:
```
IF brightness > 150:
    → happy_smiling
ELSE IF (red - blue) > 20:
    → neutral_serious
ELSE IF brightness < 100:
    → sad_concerned
ELSE:
    → surprised_interested
```

**When to adjust**:
- Lower brightness thresholds for low-light images
- Adjust for cultural differences in expression
- Concentration threshold:
  - Marketing: 0.5 (variety needed)
  - Character analysis: 0.8+ (specific emotion OK)

---

### 13. BIAS_SCORING

**Purpose**: Weighted contribution of each dimension to overall bias score

```python
"BIAS_SCORING": {
    "representation_weight": 0.15,         # 15% - Demographic balance
    "feature_bias_weight": 0.12,           # 12% - Feature space
    "color_bias_weight": 0.10,             # 10% - Color distribution
    "race_bias_weight": 0.15,              # 15% - Race/ethnicity (CRITICAL)
    "age_bias_weight": 0.10,               # 10% - Age groups
    "gender_bias_weight": 0.12,            # 12% - Gender (CRITICAL)
    "skin_tone_bias_weight": 0.10,         # 10% - Skin tone diversity
    "pose_bias_weight": 0.08,              #  8% - Body pose
    "background_bias_weight": 0.05,        #  5% - Background context
    "clothing_bias_weight": 0.02,          #  2% - Clothing patterns
    "emotion_bias_weight": 0.01,           #  1% - Emotion patterns
}
```

**Parameters**:
All weights must sum to exactly 1.0 (validation enforced)

**Weight Assignments** (by importance):
1. **Critical (27%)**: Race (15%) + Gender (12%)
   - These are legally protected categories
   - Most likely to cause discrimination lawsuits
   
2. **Important (35%)**: Representation (15%) + Feature (12%) + Color (10%)
   - Overall dataset balance
   - Visual feature distinctiveness
   - Color/lighting consistency
   
3. **Supporting (28%)**: Skin Tone (10%) + Age (10%) + Pose (8%)
   - Intersectional fairness (skin tone + age)
   - Compositional consistency
   
4. **Minor (10%)**: Background (5%) + Clothing (2%) + Emotion (1%)
   - Context consistency
   - Attribute association
   - Expression stereotyping

**How It Works**:
```
overall_score = Σ(dimension_score × dimension_weight)

Example:
- Representation bias detected (1.0) × 0.15 = 0.15
- Race bias detected (1.0) × 0.15 = 0.15
- Gender bias detected (1.0) × 0.12 = 0.12
- Age bias NOT detected (0.0) × 0.10 = 0.00
- ... (others 0.0)

Overall Score = 0.15 + 0.15 + 0.12 = 0.42 → "Moderate" bias
```

**When to adjust weights**:
- For hiring: Increase gender (0.20) + race (0.20), decrease emotion (0.0)
- For marketing: Increase age (0.15), skin tone (0.15), add body representation
- For medical: Increase feature bias (0.20), reduce emotions (0.0)

---

### 14. BIAS_LEVELS

**Purpose**: Convert numerical bias scores to interpretable severity levels

```python
"BIAS_LEVELS": {
    "low_threshold": 0.2,              # Score < 0.2 = Low
    "moderate_threshold": 0.5,         # 0.2-0.5 = Moderate
    "high_threshold": 0.8,             # 0.5-0.8 = High
    "critical_threshold": 1.0,         # 0.8+ = Critical
    "weight_critical": 3.0,            # Multiplier for critical issues
    "weight_moderate": 2.0,            # Multiplier for moderate issues
    "weight_minor": 1.0,               # Multiplier for minor issues
}
```

**Severity Levels**:

| Level | Score Range | Meaning | Action |
|-------|-------------|---------|--------|
| **Low** | 0.0 - 0.2 | ✓ Acceptable | No action needed |
| **Moderate** | 0.2 - 0.5 | ⚠️ Review | Collect more balanced data |
| **High** | 0.5 - 0.8 | ⚠️ Urgent | Significant bias detected, remediate |
| **Critical** | 0.8 - 1.0 | 🚨 Severe | Major fairness concerns, halt deployment |

**Examples**:
```
Score 0.1 = Low bias ✓
Score 0.35 = Moderate bias ⚠️
Score 0.65 = High bias ⚠️
Score 0.92 = Critical bias 🚨
```

**Issue Weighting**:
- Critical issues: Multiplied by 3.0 (race, gender discrimination)
- Moderate issues: Multiplied by 2.0 (age, skin tone, pose)
- Minor issues: Multiplied by 1.0 (emotion, clothing)

**When to adjust thresholds**:
- Stricter (0.15, 0.4, 0.65, 1.0) for high-stakes applications
- Looser (0.25, 0.55, 0.85, 1.0) for exploratory analysis

---

### 15. VALIDATION

**Purpose**: Data validation constraints for analysis

```python
"VALIDATION": {
    "minimum_images_required": 4,          # At least 4 images
    "maximum_images_allowed": 10000,       # Max 10K images per analysis
    "minimum_demographics": 1,             # At least 1 demographic group
    "maximum_demographics": 50,            # Max 50 groups
    "validate_image_dimensions": True,     # Check consistency
    "require_3_channels": True,            # Must be RGB (3 channels)
}
```

**Parameters**:
- `minimum_images_required` (4):
  - Need at least 4 images for statistical meaning
  - 1-2 images = just examples
  - 3-4 = minimum for basic analysis
  - 10+ = good for patterns
  
- `maximum_images_allowed` (10000):
  - Process limit to prevent memory issues
  - Can increase with more RAM
  
- `minimum_demographics` (1):
  - Can analyze single demographic (e.g., just women)
  
- `maximum_demographics` (50):
  - Complex interactions beyond 50 groups
  
- `validate_image_dimensions` (True):
  - All images should be similar size
  - Prevents skewed analyses
  
- `require_3_channels` (True):
  - Must be RGB (3 channels)
  - Grayscale (1 channel) requires preprocessing

**When to adjust**:
- Lower `minimum_images_required` for high-cost data (medical)
- Increase `maximum_images_allowed` for large-scale audits
- Set `require_3_channels` False for grayscale medical images

---

## Configuration Usage in Code

### Reading Configuration

```python
from image_bias import ImageBiasAnalyzer, BIAS_CONFIG

# Access configuration
disparity_threshold = BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"]
# Value: 1.5

# Get all configuration
analyzer = ImageBiasAnalyzer()
config_summary = analyzer.get_configuration_summary()
print(config_summary)
```

### Using Configuration in Methods

All analysis methods automatically use configuration:

```python
# Race analysis uses:
race_config = self.config["RACE_ETHNICITY"]
# - race_disparity_threshold
# - critical_disparity_threshold
# - race_categories
# - rgb_detection_method

# Gender analysis uses:
gender_config = self.config["GENDER"]
# - gender_categories
# - texture_variance_female_threshold
# - disparity_ratio_threshold
# - critical_disparity_threshold
```

### Modifying Configuration

To customize for specific use case:

```python
from image_bias import BIAS_CONFIG

# Adjust thresholds
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.2  # Stricter
BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 1.0  # Perfect balance required
BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.7  # Lower critical threshold

# Then create analyzer
analyzer = ImageBiasAnalyzer()  # Uses updated config
```

### Validating Configuration

Configuration is automatically validated on analyzer initialization:

```python
analyzer = ImageBiasAnalyzer()  # Validates:
# - All weights sum to 1.0
# - Thresholds in ascending order
# - All required sections exist
# - No missing key parameters
```

---

## Configuration Best Practices

### 1. Keep Thresholds Consistent
If changing representation disparity ratio, update related thresholds:
```python
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.3
BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 1.3
BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 1.3
```

### 2. Document Custom Configurations
```python
# HIGH-STAKES HIRING APPLICATION
# Requirements: Must detect even small gender imbalances
custom_config = {
    "gender_threshold": 1.1,    # Allow 10% difference
    "race_weight": 0.25,        # Double race importance
    "feature_distance": 0.15,   # Detect subtle feature differences
}
```

### 3. Test Configuration Changes
```python
# Before applying to production:
analyzer = ImageBiasAnalyzer()
test_result = analyzer.comprehensive_image_bias_analysis(test_images, test_groups)
print(f"Bias score: {test_result['overall_image_bias_score']}")
print(f"Bias level: {test_result['bias_level']}")
```

### 4. Use Version Control for Configurations
```python
# Keep history of configuration changes
CONFIGURATIONS = {
    "v1.0_initial": {...},
    "v2.0_stricter": {...},  # For high-stakes applications
    "v2.1_hiring": {...},    # Custom for hiring
}
```

### 5. Log Configuration When Running Analysis
```python
result = analyzer.comprehensive_image_bias_analysis(images, groups)
print("Configuration used:")
print(f"- Representation threshold: {BIAS_CONFIG['REPRESENTATION']['disparity_ratio_threshold']}")
print(f"- Gender weight: {BIAS_CONFIG['BIAS_SCORING']['gender_bias_weight']}")
```

---

## Common Configuration Scenarios

### Scenario 1: Corporate Hiring
**Goal**: Detect gender and race bias in interview pool

```python
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.1  # Very strict
BIAS_CONFIG["GENDER"]["disparity_ratio_threshold"] = 1.1
BIAS_CONFIG["RACE_ETHNICITY"]["disparity_ratio_threshold"] = 1.2
BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.20  # Increase
BIAS_CONFIG["BIAS_SCORING"]["race_bias_weight"] = 0.20   # Increase
BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.6   # Lower threshold
```

### Scenario 2: Product Photography
**Goal**: Ensure diverse representation in product images

```python
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.5  # Standard
BIAS_CONFIG["SKIN_TONE"]["minimum_tone_diversity"] = 0.8  # All 5 tones
BIAS_CONFIG["POSE"]["minimum_pose_types"] = 3  # Multiple poses
BIAS_CONFIG["EMOTION"]["emotion_concentration_threshold"] = 0.5  # Variety
```

### Scenario 3: Medical Imaging Dataset
**Goal**: Ensure clinical diversity for ML training

```python
BIAS_CONFIG["AGE_GROUPS"]["minimum_age_groups"] = 5  # All age groups
BIAS_CONFIG["SKIN_TONE"]["minimum_tone_diversity"] = 0.9  # Almost all
BIAS_CONFIG["VALIDATION"]["require_3_channels"] = False  # Allow grayscale
BIAS_CONFIG["BIAS_SCORING"]["feature_bias_weight"] = 0.25  # Increase
```

### Scenario 4: Social Media Content Audit
**Goal**: Exploratory analysis for diversity monitoring

```python
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 2.0  # Loose
BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.9  # High threshold
BIAS_CONFIG["EMOTION"]["emotion_concentration_threshold"] = 0.7  # More variation OK
# Use defaults for others
```

---

## Configuration Impact Examples

### Example 1: Representation Threshold Impact

**Same Dataset**: [950 male, 50 female] images

| Threshold | Ratio | Result | Alert |
|-----------|-------|--------|-------|
| 1.1 | 19:1 | 🚨 Severe | Critical |
| 1.5 | 19:1 | 🚨 Severe | Critical |
| 2.0 | 19:1 | 🚨 Severe | Critical |
| 3.0 | 19:1 | ⚠️ High but OK | Logged |
| 5.0 | 19:1 | Low priority | Minor |

### Example 2: Bias Weighting Impact

**Same Issues Detected**: Gender bias + Age bias

| Config Set | Gender Weight | Age Weight | Overall Score | Level |
|------------|---------------|-----------|---------------|-------|
| Default | 0.12 | 0.10 | 0.22 | Low |
| Hiring | 0.25 | 0.08 | 0.33 | Moderate |
| Medical | 0.10 | 0.25 | 0.35 | Moderate |
| Marketing | 0.15 | 0.20 | 0.35 | Moderate |

---

## Troubleshooting Configuration

### Issue: "Weights must sum to 1.0"
**Solution**: Check all weights, ensure sum = 1.0
```python
weights = BIAS_CONFIG["BIAS_SCORING"]
total = sum(v for k, v in weights.items() if k.endswith("_weight"))
print(f"Total: {total}")  # Should be 1.0
```

### Issue: Too many false positives
**Solution**: Raise thresholds
```python
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 2.0
BIAS_CONFIG["BIAS_LEVELS"]["critical_threshold"] = 0.8
```

### Issue: Not detecting obvious bias
**Solution**: Lower thresholds
```python
BIAS_CONFIG["REPRESENTATION"]["disparity_ratio_threshold"] = 1.2
BIAS_CONFIG["BIAS_SCORING"]["gender_bias_weight"] = 0.25
```

---

## Summary

The BIAS_CONFIG system provides:
✅ **Centralized** configuration in one place
✅ **Documented** each parameter with purpose and impact
✅ **Validated** automatically on initialization
✅ **Flexible** for different application requirements
✅ **Auditable** configuration history and changes
✅ **Consistent** across all analysis dimensions

All thresholds, weights, and parameters can be customized based on your specific fairness requirements and application domain.
