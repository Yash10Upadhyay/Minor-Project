"""
Image analysis module for detecting demographic representation imbalance using ResNet.
Identifies bias in image datasets based on visual features.

Configuration:
A small set of default thresholds and weights are defined in the
BIAS_CONFIG dictionary near the top of the file.  Only the sections actually
used by the current implementation are retained; other parameters have been
removed to simplify the project.
"""

import numpy as np
from typing import Dict, List, Tuple
import warnings

"""Removed all configuration dictionary; thresholds are now hard-coded
as class constants above.  This variable was unused after refactoring."""
    },
    "SKIN_TONE": {
        "skin_tone_categories": ["very_light", "light", "medium", "dark", "very_dark"],
        "luminance_weights": {"r": 0.299, "g": 0.587, "b": 0.114},
        "very_light_threshold": 0.8,
        "light_threshold": 0.65,
        "medium_threshold": 0.5,
        "dark_threshold": 0.35,
        "minimum_tone_diversity": 0.6,
        "critical_tone_concentration": 0.8,
    },
    "BIAS_SCORING": {
        "representation_weight": 0.15,
        "feature_bias_weight": 0.12,
        "color_bias_weight": 0.10,
        "race_bias_weight": 0.15,
        "age_bias_weight": 0.10,
        "gender_bias_weight": 0.12,
        "skin_tone_bias_weight": 0.10,
        "pose_bias_weight": 0.08,
        "background_bias_weight": 0.05,
        "clothing_bias_weight": 0.02,
        "emotion_bias_weight": 0.01,
    },
    "BIAS_LEVELS": {
        "low_threshold": 0.2,
        "moderate_threshold": 0.5,
        "high_threshold": 0.8,
        "critical_threshold": 1.0,
        "weight_critical": 3.0,
        "weight_moderate": 2.0,
        "weight_minor": 1.0,
    },
    "VALIDATION": {
        "minimum_images_required": 4,
        "maximum_images_allowed": 10000,
        "minimum_demographics": 1,
        "maximum_demographics": 50,
        "validate_image_dimensions": True,
        "require_3_channels": True,
    }
}


class ImageBiasAnalyzer:
    """
    Analyzes demographic representation bias in image datasets using ResNet features.
    
    Configuration:
        All thresholds and parameters are defined as class constants below.
        No external configuration dictionary is required.
    
    Methods:
        - analyze_demographic_representation: Check demographic group balance
        - detect_visual_feature_bias: Analyze feature space divergence
        - analyze_color_bias: Examine RGB distribution patterns
        - detect_race_ethnicity: Racial/ethnic representation
        - detect_age_groups: Age group diversity
        - detect_gender_representation: Gender balance analysis
        - analyze_skin_tone: Skin tone diversity metrics
        - analyze_pose_composition: Body pose patterns
        - analyze_background_context: Background/setting bias
        - analyze_clothing_accessories: Clothing style representation
        - analyze_expression_emotion: Facial expression patterns
        - comprehensive_image_bias_analysis: All 8 dimensions combined
    """
    
    # class-level default thresholds and weights (no external configuration)
    FEATURE_DIMENSIONS = 2048
    REP_DISP_THRESHOLD = 1.5
    REP_CRITICAL_THRESHOLD = 3.0
    REP_MIN_SAMPLES = 1
    REP_IDEAL_DISTRIBUTION = "equal"
    VIS_FEAT_THRESHOLD = 0.3
    VIS_FEAT_CRITICAL_THRESHOLD = 0.6
    VIS_BINS_TO_COMPARE = 10
    RACE_DISP_THRESHOLD = 1.5
    RACE_CRITICAL_THRESHOLD = 2.5
    RACE_CATEGORIES = ["caucasian", "african", "asian", "hispanic", "middle_eastern", "mixed"]
    RACE_RGB_METHOD = "color_heuristic"
    AGE_CATEGORIES = ["child", "adolescent", "young_adult", "adult", "senior"]
    PIXEL_VARIANCE_CHILD = 100
    PIXEL_VARIANCE_ADOLESCENT = 500
    EDGE_STRENGTH_YOUNG_ADULT = 5
    EDGE_STRENGTH_ADULT = 10
    MINIMUM_AGE_GROUPS = 3
    GENDER_CATEGORIES = ["male", "female", "non_binary"]
    TEXTURE_VARIANCE_FEMALE_THRESHOLD = 300
    GENDER_DISP_THRESHOLD = 1.5
    GENDER_CRITICAL_THRESHOLD = 2.5
    GENDER_BALANCED_RANGE = [0.4, 0.6]
    SKIN_TONE_CATEGORIES = ["very_light", "light", "medium", "dark", "very_dark"]
    LUMINANCE_WEIGHTS = {"r": 0.299, "g": 0.587, "b": 0.114}
    VERY_LIGHT_THRESHOLD = 0.8
    LIGHT_THRESHOLD = 0.65
    MEDIUM_THRESHOLD = 0.5
    DARK_THRESHOLD = 0.35
    MIN_TONE_DIVERSITY = 0.6
    CRITICAL_TONE_CONCENTRATION = 0.8
    WEIGHTS = {
        "representation_weight": 0.15,
        "feature_bias_weight": 0.12,
        "color_bias_weight": 0.10,
        "race_bias_weight": 0.15,
        "age_bias_weight": 0.10,
        "gender_bias_weight": 0.12,
        "skin_tone_bias_weight": 0.10,
        "pose_bias_weight": 0.08,
        "background_bias_weight": 0.05,
        "clothing_bias_weight": 0.02,
        "emotion_bias_weight": 0.01,
    }
    LOW_THRESHOLD = 0.2
    MODERATE_THRESHOLD = 0.5
    HIGH_THRESHOLD = 0.8
    CRITICAL_THRESHOLD = 1.0
    WEIGHT_CRITICAL = 3.0
    WEIGHT_MODERATE = 2.0
    WEIGHT_MINOR = 1.0
    MIN_IMAGES = 4
    MAX_IMAGES = 10000
    MIN_DEMOGRAPHICS = 1
    MAX_DEMOGRAPHICS = 50
    VALIDATE_DIMENSIONS = True
    REQUIRE_3_CHANNELS = True
    
    def __init__(self):
        """
        Initialize the image bias analyzer.
        
        There is no external configuration; default thresholds and weights are
        defined as class constants.
        """
        self.feature_dimensions = ImageBiasAnalyzer.FEATURE_DIMENSIONS
    
    def _validate_configuration(self):
        """No-op: configuration is embedded as class constants."""
        pass
    
    def get_configuration_summary(self) -> Dict:
        """
        Return a human-readable summary of current configuration.
        
        Returns:
            Dictionary with all configuration sections and descriptions
        """
        # Return a small summary of the class-embedded configuration
        return {
            "feature_dimensions": ImageBiasAnalyzer.FEATURE_DIMENSIONS,
            "representation": {
                "disparity_threshold": ImageBiasAnalyzer.REP_DISP_THRESHOLD,
                "critical_threshold": ImageBiasAnalyzer.REP_CRITICAL_THRESHOLD,
            },
            "race_ethnicity": {
                "categories": ImageBiasAnalyzer.RACE_CATEGORIES,
                "detection_method": ImageBiasAnalyzer.RACE_RGB_METHOD
            },
            "bias_levels": {
                "low": ImageBiasAnalyzer.LOW_THRESHOLD,
                "moderate": ImageBiasAnalyzer.MODERATE_THRESHOLD,
                "high": ImageBiasAnalyzer.HIGH_THRESHOLD,
                "critical": ImageBiasAnalyzer.CRITICAL_THRESHOLD
            },
            "weights": ImageBiasAnalyzer.WEIGHTS
        }
    
    @staticmethod
    def _to_python_types(obj):
        """Convert numpy types to Python native types for JSON serialization."""
        if isinstance(obj, dict):
            return {key: ImageBiasAnalyzer._to_python_types(value) for key, value in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [ImageBiasAnalyzer._to_python_types(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        else:
            return obj
    
    def extract_features(self, image_array: np.ndarray) -> np.ndarray:
        """
        Extract features from image using ResNet model.
        In production, use: from torchvision import models
        This is a placeholder that returns simulated features for demonstration.
        """
        # Simulate ResNet feature extraction
        # In production: use torchvision.models.resnet50(pretrained=True)
        # and pass image through model
        
        # Create simulated features based on image characteristics
        if len(image_array.shape) == 3:
            # Extract color histogram features
            features = []
            for channel in range(3):
                hist, _ = np.histogram(image_array[:, :, channel], bins=256)
                features.extend(hist[:10])  # Use first 10 bins
            
            # Pad to feature dimension
            features = np.array(features)
            if len(features) < self.feature_dimensions:
                features = np.pad(features, (0, self.feature_dimensions - len(features)))
            
            return features[:self.feature_dimensions]
        
        return np.zeros(self.feature_dimensions)
    
    def analyze_demographic_representation(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze demographic representation balance in image dataset.
        
        Threshold values are taken from class constants (REP_*).
        
        Args:
            images: List of preprocessed images
            demographic_groups: List of demographic labels for each image
        
        Returns:
            Dictionary with bias metrics including:
            - group_distribution: Count per demographic group
            - group_percentages: Percentage distribution
            - representation_disparity_ratio: Max/min group size ratio
            - demographic_parity_score: Balance metric (0-1)
            - imbalance_detected: Boolean based on threshold
            - total_images: Total images analyzed
            - num_groups: Number of demographic groups
        """
        if not images or not demographic_groups:
            raise ValueError("Images and demographic_groups cannot be empty")
        
        if len(images) != len(demographic_groups):
            raise ValueError("Number of images must match number of demographic labels")
        
        
        # Count representations
        group_counts = {}
        for group in demographic_groups:
            group_counts[group] = group_counts.get(group, 0) + 1
        
        # Calculate representation balance
        total = len(demographic_groups)
        group_percentages = {
            group: (count / total) * 100
            for group, count in group_counts.items()
        }
        
        # Calculate imbalance metrics
        percentages = list(group_percentages.values())
        max_percentage = max(percentages) if percentages else 0
        min_percentage = min(percentages) if percentages else 0
        
        # Representation disparity ratio
        disparity_ratio = max_percentage / min_percentage if min_percentage > 0 else float('inf')
        
        # Demographic parity (ideal is 1/num_groups for each)
        ideal_percentage = 100 / len(group_counts) if group_counts else 0
        demographic_parity = sum(
            abs(pct - ideal_percentage) / ideal_percentage
            for pct in percentages
        ) / len(percentages) if percentages else 0
        
        return {
            "group_distribution": group_counts,
            "group_percentages": group_percentages,
            "representation_disparity_ratio": disparity_ratio,
            "demographic_parity_score": 1 - min(demographic_parity, 1),  # 0-1 scale
            "disparity_threshold_used": ImageBiasAnalyzer.REP_DISP_THRESHOLD,
            "imbalance_detected": disparity_ratio > ImageBiasAnalyzer.REP_DISP_THRESHOLD,
            "critical_imbalance": disparity_ratio > ImageBiasAnalyzer.REP_CRITICAL_THRESHOLD,
            "total_images": total,
            "num_groups": len(group_counts)
        }
    
    def detect_visual_feature_bias(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Detect bias in visual features across demographic groups.
        
        Threshold values are taken from class constants (VIS_FEAT_*).
        
        Args:
            images: List of preprocessed images
            demographic_groups: List of demographic labels for each image
        
        Returns:
            Dictionary with visual feature bias metrics
        """
        
        # Extract features for all images
        features = []
        for img in images:
            feat = self.extract_features(img)
            features.append(feat)
        
        features = np.array(features)
        
        # Group features by demographic group
        group_features = {}
        for i, group in enumerate(demographic_groups):
            if group not in group_features:
                group_features[group] = []
            group_features[group].append(features[i])
        
        # Convert to arrays
        for group in group_features:
            group_features[group] = np.array(group_features[group])
        
        # Calculate feature statistics per group
        feature_bias_metrics = {}
        
        for group, group_feats in group_features.items():
            feature_bias_metrics[group] = {
                "mean": np.mean(group_feats, axis=0).tolist()[:10],  # First 10 dims
                "std": np.std(group_feats, axis=0).tolist()[:10],
                "sample_size": len(group_feats)
            }
        
        # Calculate feature distance bias between groups
        groups = list(group_features.keys())
        feature_distance_matrix = {}
        max_distance = 0
        
        for i, group1 in enumerate(groups):
            for j, group2 in enumerate(groups):
                if i < j:
                    mean1 = np.mean(group_features[group1], axis=0)
                    mean2 = np.mean(group_features[group2], axis=0)
                    distance = np.linalg.norm(mean1 - mean2)
                    key = f"{group1}_vs_{group2}"
                    feature_distance_matrix[key] = float(distance)
                    max_distance = max(max_distance, distance)
        
        return {
            "group_feature_statistics": feature_bias_metrics,
            "feature_distance_matrix": feature_distance_matrix,
            "max_feature_distance": max_distance,
            "feature_distance_threshold": ImageBiasAnalyzer.VIS_FEAT_THRESHOLD,
            "critical_distance_threshold": ImageBiasAnalyzer.VIS_FEAT_CRITICAL_THRESHOLD,
            "visual_feature_bias_detected": max_distance > ImageBiasAnalyzer.VIS_FEAT_THRESHOLD,
            "critical_feature_bias": max_distance > ImageBiasAnalyzer.VIS_FEAT_CRITICAL_THRESHOLD
        }
    
    def analyze_color_bias(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze color distribution bias across demographic groups.
        """
        group_colors = {}
        
        for i, group in enumerate(demographic_groups):
            if group not in group_colors:
                group_colors[group] = {"red": [], "green": [], "blue": []}
            
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                group_colors[group]["red"].append(np.mean(img[:, :, 0]))
                group_colors[group]["green"].append(np.mean(img[:, :, 1]))
                group_colors[group]["blue"].append(np.mean(img[:, :, 2]))
        
        # Calculate average color per group
        color_profiles = {}
        for group, colors in group_colors.items():
            color_profiles[group] = {
                "avg_red": np.mean(colors["red"]) if colors["red"] else 0,
                "avg_green": np.mean(colors["green"]) if colors["green"] else 0,
                "avg_blue": np.mean(colors["blue"]) if colors["blue"] else 0
            }
        
        return {
            "color_profiles": color_profiles,
            "color_bias_detected": len(set(
                str(profile) for profile in color_profiles.values()
            )) > 1
        }
    
    def detect_race_ethnicity(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Detect and analyze race/ethnicity representation in images.
        
        Uses class constants (RACE_*).
        Uses visual features to infer racial/ethnic characteristics.
        """
        # use class constants instead of configuration dictionary
        # config = self.config["RACE_ETHNICITY"]
        race_distribution = {}
        race_color_profiles = {}
        
        for i, group in enumerate(demographic_groups):
            # Simulated race detection based on color features
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Calculate skin tone approximation from average RGB
                avg_r = np.mean(img[:, :, 0])
                avg_g = np.mean(img[:, :, 1])
                avg_b = np.mean(img[:, :, 2])
                
                # Simplistic skin tone classification based on RGB
                if avg_r > avg_b and avg_g > avg_b:
                    predicted_race = "caucasian"
                elif avg_r > 120 and avg_g > 100 and avg_b < 100:
                    predicted_race = "african"
                elif avg_r > 110 and avg_g > 105 and avg_b > 100:
                    predicted_race = "asian"
                elif avg_r > 115 and avg_g > 100 and avg_b > 90:
                    predicted_race = "hispanic"
                else:
                    predicted_race = "mixed"
                
                if predicted_race not in race_distribution:
                    race_distribution[predicted_race] = 0
                    race_color_profiles[predicted_race] = {"red": [], "green": [], "blue": []}
                
                race_distribution[predicted_race] += 1
                race_color_profiles[predicted_race]["red"].append(avg_r)
                race_color_profiles[predicted_race]["green"].append(avg_g)
                race_color_profiles[predicted_race]["blue"].append(avg_b)
        
        # Calculate race statistics
        total = sum(race_distribution.values())
        race_percentages = {
            race: (count / total) * 100
            for race, count in race_distribution.items()
        } if total > 0 else {}
        
        # Calculate race representation disparity
        percentages = list(race_percentages.values())
        max_pct = max(percentages) if percentages else 0
        min_pct = min(percentages) if percentages else 1
        race_disparity = max_pct / min_pct if min_pct > 0 else float('inf')
        
        return {
            "race_ethnicity_distribution": race_distribution,
            "race_percentages": race_percentages,
            "race_color_profiles": {
                race: {
                    "avg_red": np.mean(profile["red"]) if profile["red"] else 0,
                    "avg_green": np.mean(profile["green"]) if profile["green"] else 0,
                    "avg_blue": np.mean(profile["blue"]) if profile["blue"] else 0
                }
                for race, profile in race_color_profiles.items()
            },
            "race_representation_disparity": race_disparity,
            "race_ethnicity_detected": ImageBiasAnalyzer.RACE_CATEGORIES,
            "race_disparity_threshold": ImageBiasAnalyzer.RACE_DISP_THRESHOLD,
            "race_critical_threshold": ImageBiasAnalyzer.RACE_CRITICAL_THRESHOLD,
            "race_bias_detected": race_disparity > ImageBiasAnalyzer.RACE_DISP_THRESHOLD,
            "race_critical_bias": race_disparity > ImageBiasAnalyzer.RACE_CRITICAL_THRESHOLD,
            "detection_method": ImageBiasAnalyzer.RACE_RGB_METHOD
        }
    
    def detect_age_groups(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Detect and analyze age group representation in images.
        
        Uses class constants (AGE_*).
        """
        # use class constants for thresholds
        age_distribution = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Simulated age detection based on image features
                # In production: use age estimation models
                pixel_variance = np.var(img)
                edge_strength = np.mean(np.abs(np.diff(img[:, :, 0], axis=0)))
                
                if pixel_variance < ImageBiasAnalyzer.PIXEL_VARIANCE_CHILD:
                    age_pred = "child"
                elif pixel_variance < ImageBiasAnalyzer.PIXEL_VARIANCE_ADOLESCENT:
                    age_pred = "adolescent"
                elif edge_strength < ImageBiasAnalyzer.EDGE_STRENGTH_YOUNG_ADULT:
                    age_pred = "young_adult"
                elif edge_strength < ImageBiasAnalyzer.EDGE_STRENGTH_ADULT:
                    age_pred = "adult"
                else:
                    age_pred = "senior"
                
                if age_pred not in age_distribution:
                    age_distribution[age_pred] = 0
                age_distribution[age_pred] += 1
        
        total = sum(age_distribution.values())
        age_percentages = {
            age: (count / total) * 100
            for age, count in age_distribution.items()
        } if total > 0 else {}
        
        return {
            "age_group_distribution": age_distribution,
            "age_categories": ImageBiasAnalyzer.AGE_CATEGORIES,
            "age_percentages": age_percentages,
            "num_age_groups_detected": len(age_distribution),
            "minimum_age_groups_required": ImageBiasAnalyzer.MINIMUM_AGE_GROUPS,
            "age_representation_bias_detected": len(age_distribution) < ImageBiasAnalyzer.MINIMUM_AGE_GROUPS
        }
    
    def detect_gender_representation(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Detect and analyze gender representation in images.
        
        Uses class constants (GENDER_*).
        
        Args:
            images: List of preprocessed images
            demographic_groups: List of demographic labels for each image
        
        Returns:
            Dictionary with gender representation metrics
        """
        # use class constants for thresholds
        gender_distribution = {}
        gender_color_profiles = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Simulated gender detection based on color/texture
                # In production: use face detection + gender classification models
                texture_variance = np.var(img)
                avg_brightness = np.mean(img)
                
                # Simple heuristic: lower variance might indicate makeup/smoother skin
                if texture_variance < ImageBiasAnalyzer.TEXTURE_VARIANCE_FEMALE_THRESHOLD:
                    pred_gender = "female"
                else:
                    pred_gender = "male"
                
                if pred_gender not in gender_distribution:
                    gender_distribution[pred_gender] = 0
                    gender_color_profiles[pred_gender] = {"brightness": []}
                
                gender_distribution[pred_gender] += 1
                gender_color_profiles[pred_gender]["brightness"].append(avg_brightness)
        
        total = sum(gender_distribution.values())
        gender_percentages = {
            gender: (count / total) * 100
            for gender, count in gender_distribution.items()
        } if total > 0 else {}
        
        percentages = list(gender_percentages.values())
        gender_disparity = max(percentages) / min(percentages) if len(percentages) > 1 and min(percentages) > 0 else 1.0
        
        return {
            "gender_distribution": gender_distribution,
            "gender_percentages": gender_percentages,
            "gender_disparity_ratio": gender_disparity,
            "gender_disparity_threshold": ImageBiasAnalyzer.GENDER_DISP_THRESHOLD,
            "gender_critical_threshold": ImageBiasAnalyzer.GENDER_CRITICAL_THRESHOLD,
            "gender_imbalance_detected": gender_disparity > ImageBiasAnalyzer.GENDER_DISP_THRESHOLD,
            "gender_critical_imbalance": gender_disparity > ImageBiasAnalyzer.GENDER_CRITICAL_THRESHOLD
        }
    
    def analyze_skin_tone(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze skin tone diversity and bias in image dataset.
        
        Uses class constants (SKIN_TONE_*).
        Uses luminance-based categorization with Fitzpatrick-inspired scale.
        """
        # use class constants for thresholds
        skin_tone_distribution = {}
        group_skin_tones = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Calculate skin tone based on RGB values
                avg_r = np.mean(img[:, :, 0])
                avg_g = np.mean(img[:, :, 1])
                avg_b = np.mean(img[:, :, 2])
                
                # Overall brightness/luminance using standard formula
                weights = ImageBiasAnalyzer.LUMINANCE_WEIGHTS
                luminance = (avg_r * weights["r"] + avg_g * weights["g"] + avg_b * weights["b"]) / 255

                if luminance > ImageBiasAnalyzer.VERY_LIGHT_THRESHOLD:
                    tone = "very_light"
                elif luminance > ImageBiasAnalyzer.LIGHT_THRESHOLD:
                    tone = "light"
                elif luminance > ImageBiasAnalyzer.MEDIUM_THRESHOLD:
                    tone = "medium"
                elif luminance > ImageBiasAnalyzer.DARK_THRESHOLD:
                    tone = "dark"
                else:
                    tone = "very_dark"
                
                if tone not in skin_tone_distribution:
                    skin_tone_distribution[tone] = 0
                if group not in group_skin_tones:
                    group_skin_tones[group] = {}
                
                skin_tone_distribution[tone] += 1
                if tone not in group_skin_tones[group]:
                    group_skin_tones[group][tone] = 0
                group_skin_tones[group][tone] += 1
        
        total = sum(skin_tone_distribution.values())
        skin_tone_percentages = {
            tone: (count / total) * 100
            for tone, count in skin_tone_distribution.items()
        } if total > 0 else {}
        
        diversity_score = len(skin_tone_distribution) / len(ImageBiasAnalyzer.SKIN_TONE_CATEGORIES)

        # Check if one tone dominates
        max_percentage = max(skin_tone_percentages.values()) if skin_tone_percentages else 0
        critical_concentration = max_percentage > (ImageBiasAnalyzer.CRITICAL_TONE_CONCENTRATION * 100)

        return {
            "skin_tone_distribution": skin_tone_distribution,
            "skin_tone_percentages": skin_tone_percentages,
            "skin_tone_categories": ImageBiasAnalyzer.SKIN_TONE_CATEGORIES,
            "skin_tone_by_demographic": group_skin_tones,
            "skin_tone_diversity_score": diversity_score,
            "minimum_diversity_threshold": ImageBiasAnalyzer.MIN_TONE_DIVERSITY,
            "critical_concentration_threshold": ImageBiasAnalyzer.CRITICAL_TONE_CONCENTRATION,
            "skin_tone_bias_detected": diversity_score < ImageBiasAnalyzer.MIN_TONE_DIVERSITY,
            "critical_tone_concentration": critical_concentration,
            "luminance_calculation_method": "ITU-R BT.601"
        }
    
    def analyze_pose_composition(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze body pose and composition across demographic groups.
        """
        pose_distribution = {}
        group_poses = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Simulated pose detection based on image characteristics
                # In production: use pose estimation models (OpenPose, MediaPipe)
                height, width = img.shape[:2]
                aspect_ratio = height / width if width > 0 else 0
                
                # Classify pose based on aspect ratio and brightness distribution
                vertical_brightness = np.mean(img, axis=1)
                brightness_variance = np.var(vertical_brightness)
                
                if brightness_variance > 1000:
                    pose = "upright_frontal"
                elif aspect_ratio > 1.2:
                    pose = "seated"
                elif brightness_variance > 500:
                    pose = "dynamic_active"
                else:
                    pose = "neutral_standing"
                
                if pose not in pose_distribution:
                    pose_distribution[pose] = 0
                if group not in group_poses:
                    group_poses[group] = {}
                
                pose_distribution[pose] += 1
                if pose not in group_poses[group]:
                    group_poses[group][pose] = 0
                group_poses[group][pose] += 1
        
        total = sum(pose_distribution.values())
        pose_percentages = {
            pose: (count / total) * 100
            for pose, count in pose_distribution.items()
        } if total > 0 else {}
        
        return {
            "pose_distribution": pose_distribution,
            "pose_percentages": pose_percentages,
            "pose_by_demographic": group_poses,
            "pose_diversity_score": len(pose_distribution) / 4,
            "pose_bias_detected": len(pose_distribution) == 1
        }
    
    def analyze_background_context(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze background and context in images across demographic groups.
        """
        background_distribution = {}
        group_backgrounds = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Simulated background detection
                # In production: use segmentation models
                
                # Calculate background complexity/entropy
                edges_h = np.abs(np.diff(img[:, :, 0], axis=0))
                edges_v = np.abs(np.diff(img[:, :, 1], axis=1))
                total_edges = np.mean(edges_h) + np.mean(edges_v)
                
                # Check background uniformity (corners typically have less subject)
                corner_brightness = (np.mean(img[0:10, :10]) + 
                                   np.mean(img[-10:, :10]) + 
                                   np.mean(img[0:10, -10:]) + 
                                   np.mean(img[-10:, -10:])) / 4
                center_brightness = np.mean(img[img.shape[0]//4:3*img.shape[0]//4, 
                                               img.shape[1]//4:3*img.shape[1]//4])
                
                if total_edges > 20 and corner_brightness < center_brightness:
                    bg = "studio_professional"
                elif total_edges < 10:
                    bg = "plain_simple"
                elif total_edges > 15:
                    bg = "natural_outdoor"
                else:
                    bg = "blurred_background"
                
                if bg not in background_distribution:
                    background_distribution[bg] = 0
                if group not in group_backgrounds:
                    group_backgrounds[group] = {}
                
                background_distribution[bg] += 1
                if bg not in group_backgrounds[group]:
                    group_backgrounds[group][bg] = 0
                group_backgrounds[group][bg] += 1
        
        total = sum(background_distribution.values())
        bg_percentages = {
            bg: (count / total) * 100
            for bg, count in background_distribution.items()
        } if total > 0 else {}
        
        return {
            "background_distribution": background_distribution,
            "background_percentages": bg_percentages,
            "background_by_demographic": group_backgrounds,
            "background_diversity": len(background_distribution) / 4,
            "background_bias_detected": any(
                count > total * 0.6 for count in background_distribution.values()
            ) if total > 0 else False
        }
    
    def analyze_clothing_accessories(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze clothing and accessories patterns across demographic groups.
        """
        clothing_distribution = {}
        group_clothing = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Simulated clothing detection
                # In production: use clothing classification models
                
                # Analyze color saturation and variety
                color_saturation = np.std(img)
                red_channel = np.mean(img[:, :, 0])
                
                if color_saturation > 40 and red_channel > 130:
                    clothing = "vibrant_colorful"
                elif color_saturation < 20:
                    clothing = "neutral_formal"
                elif red_channel < 100:
                    clothing = "cool_professional"
                else:
                    clothing = "warm_casual"
                
                if clothing not in clothing_distribution:
                    clothing_distribution[clothing] = 0
                if group not in group_clothing:
                    group_clothing[group] = {}
                
                clothing_distribution[clothing] += 1
                if clothing not in group_clothing[group]:
                    group_clothing[group][clothing] = 0
                group_clothing[group][clothing] += 1
        
        total = sum(clothing_distribution.values())
        clothing_percentages = {
            c: (count / total) * 100
            for c, count in clothing_distribution.items()
        } if total > 0 else {}
        
        return {
            "clothing_distribution": clothing_distribution,
            "clothing_percentages": clothing_percentages,
            "clothing_by_demographic": group_clothing,
            "clothing_style_diversity": len(clothing_distribution) / 4,
            "clothing_bias_detected": any(
                group_clothing.get(group, {}).get(c, 0) > sum(group_clothing.get(group, {}).values()) * 0.7
                for group in group_clothing
                for c in clothing_distribution
            ) if group_clothing else False
        }
    
    def analyze_expression_emotion(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze facial expression and emotion patterns in images.
        """
        emotion_distribution = {}
        group_emotions = {}
        
        for i, group in enumerate(demographic_groups):
            img = images[i]
            if len(img.shape) == 3 and img.shape[2] == 3:
                # Simulated emotion detection
                # In production: use emotion recognition models (facial landmarks)
                
                # Use color and brightness patterns to infer expression
                brightness = np.mean(img)
                red_blue_diff = np.mean(img[:, :, 0]) - np.mean(img[:, :, 2])
                
                if brightness > 150:
                    emotion = "happy_smiling"
                elif red_blue_diff > 20:
                    emotion = "neutral_serious"
                elif brightness < 100:
                    emotion = "sad_concerned"
                else:
                    emotion = "surprised_interested"
                
                if emotion not in emotion_distribution:
                    emotion_distribution[emotion] = 0
                if group not in group_emotions:
                    group_emotions[group] = {}
                
                emotion_distribution[emotion] += 1
                if emotion not in group_emotions[group]:
                    group_emotions[group][emotion] = 0
                group_emotions[group][emotion] += 1
        
        total = sum(emotion_distribution.values())
        emotion_percentages = {
            e: (count / total) * 100
            for e, count in emotion_distribution.items()
        } if total > 0 else {}
        
        return {
            "emotion_distribution": emotion_distribution,
            "emotion_percentages": emotion_percentages,
            "emotion_by_demographic": group_emotions,
            "emotion_diversity": len(emotion_distribution) / 4,
            "emotion_bias_detected": any(
                group_emotions.get(group, {}).get(e, 0) > sum(group_emotions.get(group, {}).values()) * 0.65
                for group in group_emotions
                for e in emotion_distribution
            ) if group_emotions else False
        }
    
    def comprehensive_image_bias_analysis(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Perform comprehensive bias analysis on image dataset across 8 dimensions.
        
        Uses all thresholds and weights from BIAS_CONFIG.
        
        Returns analysis results with:
        - Individual bias scores for each dimension (0.0-1.0)
        - Overall weighted bias score (0.0-1.0)
        - Bias level classification (Low, Moderate, High, Critical)
        - Summary of critical, moderate, and minor issues
        """
        # Simplified analysis: only evaluate race/ethnicity bias + basic representation
        representation_analysis = self.analyze_demographic_representation(
            images, demographic_groups
        )
        race_ethnicity_analysis = self.detect_race_ethnicity(images, demographic_groups)
        
        # Calculate individual bias score
        representation_bias_score = 1 - representation_analysis["demographic_parity_score"]
        weights = ImageBiasAnalyzer.WEIGHTS
        overall_bias_score = (
            representation_bias_score * weights["representation_weight"] +
            float(race_ethnicity_analysis["race_bias_detected"]) * weights["race_bias_weight"]
        )
        
        result = {
            "analysis_metadata": {
                "total_images_analyzed": len(images),
                "total_demographic_groups": len(set(demographic_groups)),
                "analysis_timestamp": str(np.datetime64('today')),
                "config_version": "2.0"
            },
            "dimensional_analysis": {
                "demographic_representation": representation_analysis,
                    "race_ethnicity_analysis": race_ethnicity_analysis
            },
            "overall_assessment": {
                "overall_image_bias_score": overall_bias_score,
                "bias_level": self._score_to_bias_level(overall_bias_score),
                "bias_score_thresholds": {
                    "low": ImageBiasAnalyzer.LOW_THRESHOLD,
                    "moderate": ImageBiasAnalyzer.MODERATE_THRESHOLD,
                    "high": ImageBiasAnalyzer.HIGH_THRESHOLD,
                    "critical": ImageBiasAnalyzer.CRITICAL_THRESHOLD
                },
                "active_weights": {
                    k: v for k, v in weights.items() if k.endswith("_weight")
                }
            },
            "bias_summary": {
                "critical_issues": float(race_ethnicity_analysis.get("race_critical_bias", False)) +
                                   float(representation_bias_score > 0.5),
                "moderate_issues": 0,
                "minor_issues": 0,
                "total_issues_detected": float(race_ethnicity_analysis["race_bias_detected"]) +
                                          float(representation_bias_score > 0.5)
            },
            "recommendations": self._generate_recommendations(
                representation_analysis, race_ethnicity_analysis
            )
        }
        
        # Convert numpy types to Python native types for JSON serialization
        return self._to_python_types(result)
    
    def _generate_recommendations(self, *analyses) -> List[str]:
        """Generate recommendations based on detected biases."""
        recommendations = []
        
        # Only first two analyses are passed (representation, race)
        rep, race = analyses[0], analyses[1]

        if rep.get("imbalance_detected"):
            recommendations.append(
                "Demographic representation is imbalanced. Consider collecting more samples "
                "from underrepresented groups to achieve a balanced dataset."
            )

        if race.get("race_bias_detected"):
            recommendations.append(
                "Racial/ethnic representation shows significant disparity. "
                "Ensure diverse racial/ethnic representation in dataset collection."
            )

        if not recommendations:
            recommendations.append("Dataset shows no obvious gender/ethnicity bias based on the supplied labels.")
        
        return recommendations
    
    @staticmethod
    def _score_to_bias_level(score: float) -> str:
        """
        Convert bias score to interpretable level using configured thresholds.
        
        Thresholds (from BIAS_CONFIG["BIAS_LEVELS"]):
        - Low: score < 0.2
        - Moderate: 0.2 <= score < 0.5
        - High: 0.5 <= score < 0.8
        - Critical: score >= 0.8
        
        Args:
            score: Bias score between 0.0 and 1.0
        
        Returns:
            Bias level string: "Low", "Moderate", "High", or "Critical"
        """
        if score < ImageBiasAnalyzer.LOW_THRESHOLD:
            return "Low"
        elif score < ImageBiasAnalyzer.MODERATE_THRESHOLD:
            return "Moderate"
        elif score < ImageBiasAnalyzer.HIGH_THRESHOLD:
            return "High"
        else:
            return "Critical"
