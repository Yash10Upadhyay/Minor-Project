"""
Image analysis module for detecting demographic representation imbalance using ResNet.
Identifies bias in image datasets based on visual features.
"""

import numpy as np
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class ImageBiasAnalyzer:
    """Analyzes demographic representation bias in image datasets using ResNet features."""
    
    def __init__(self):
        """Initialize the image bias analyzer."""
        self.feature_dimensions = 2048  # ResNet50 feature dimension
    
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
        
        Args:
            images: List of preprocessed images
            demographic_groups: List of demographic labels for each image
        
        Returns:
            Dictionary with bias metrics
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
            "imbalance_detected": disparity_ratio > 1.5,  # Threshold: 1.5x imbalance
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
        
        for i, group1 in enumerate(groups):
            for j, group2 in enumerate(groups):
                if i < j:
                    mean1 = np.mean(group_features[group1], axis=0)
                    mean2 = np.mean(group_features[group2], axis=0)
                    distance = np.linalg.norm(mean1 - mean2)
                    key = f"{group1}_vs_{group2}"
                    feature_distance_matrix[key] = float(distance)
        
        return {
            "group_feature_statistics": feature_bias_metrics,
            "feature_distance_matrix": feature_distance_matrix,
            "visual_feature_bias_detected": len(feature_distance_matrix) > 0 and max(feature_distance_matrix.values()) > 0.3
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
    
    def comprehensive_image_bias_analysis(
        self,
        images: List[np.ndarray],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Perform comprehensive bias analysis on image dataset.
        """
        representation_analysis = self.analyze_demographic_representation(
            images, demographic_groups
        )
        
        feature_bias = self.detect_visual_feature_bias(images, demographic_groups)
        
        color_bias = self.analyze_color_bias(images, demographic_groups)
        
        # Combine results
        overall_bias_score = (
            (1 - representation_analysis["demographic_parity_score"]) * 0.5 +
            (float(feature_bias["visual_feature_bias_detected"]) * 0.3) +
            (float(color_bias["color_bias_detected"]) * 0.2)
        )
        
        return {
            "representation_analysis": representation_analysis,
            "feature_bias_analysis": feature_bias,
            "color_bias_analysis": color_bias,
            "overall_image_bias_score": overall_bias_score,
            "bias_level": self._score_to_bias_level(overall_bias_score)
        }
    
    @staticmethod
    def _score_to_bias_level(score: float) -> str:
        """Convert bias score to interpretable level."""
        if score < 0.2:
            return "Low"
        elif score < 0.5:
            return "Moderate"
        elif score < 0.8:
            return "High"
        else:
            return "Critical"
