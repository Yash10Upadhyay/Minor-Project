"""
Multimodal analysis module for detecting bias in image-caption pairs using CLIP/VILT models.
Analyzes alignment between visual content and textual descriptions across demographic groups.
"""

import numpy as np
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')


class MultimodalBiasAnalyzer:
    """
    Analyzes bias in multimodal data (image-caption pairs) using CLIP/VILT-like approach.
    Detects misalignment, stereotyping, and representational bias.
    """
    
    def __init__(self):
        """Initialize multimodal bias analyzer."""
        self.stereotype_keywords = {
            "occupational": {
                "positive": ["doctor", "engineer", "professor", "executive", "leader"],
                "negative": ["janitor", "cleaner", "worker", "laborer"]
            },
            "behavioral": {
                "positive": ["happy", "friendly", "intelligent", "successful", "professional"],
                "negative": ["angry", "aggressive", "criminal", "lazy", "stupid"]
            }
        }
    
    def analyze_image_caption_alignment(
        self,
        image_captions: List[Dict],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze alignment between images and their captions.
        
        Args:
            image_captions: List of dicts with 'image' and 'caption' keys
            demographic_groups: Demographic labels for each pair
        
        Returns:
            Dictionary with alignment metrics
        """
        if len(image_captions) != len(demographic_groups):
            raise ValueError("Number of image-caption pairs must match demographic groups")
        
        alignment_scores = []
        mismatch_cases = []
        
        for i, pair in enumerate(image_captions):
            caption = pair.get("caption", "").lower()
            group = demographic_groups[i]
            
            # Check for descriptive richness
            caption_length = len(caption.split())
            
            # Check for stereotype presence
            stereotype_score = self._detect_stereotype(caption)
            
            # Alignment score (higher = better alignment, lower = less descriptive)
            alignment_score = min(caption_length / 30, 1.0)  # Normalize to 0-1
            
            alignment_scores.append(alignment_score)
            
            if stereotype_score > 0.5:
                mismatch_cases.append({
                    "group": group,
                    "caption": caption[:100],
                    "stereotype_score": stereotype_score
                })
        
        avg_alignment = np.mean(alignment_scores)
        
        return {
            "average_alignment_score": avg_alignment,
            "alignment_variance": np.std(alignment_scores),
            "total_pairs": len(image_captions),
            "stereotype_cases": len(mismatch_cases),
            "sample_misaligned_pairs": mismatch_cases[:5],
            "alignment_bias_detected": np.std(alignment_scores) > 0.3
        }
    
    def analyze_representation_consistency(
        self,
        image_captions: List[Dict],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze consistency of how different demographic groups are represented.
        """
        group_descriptions = {}
        
        for i, pair in enumerate(image_captions):
            caption = pair.get("caption", "").lower()
            group = demographic_groups[i]
            
            if group not in group_descriptions:
                group_descriptions[group] = {
                    "captions": [],
                    "avg_caption_length": 0,
                    "stereotype_scores": []
                }
            
            group_descriptions[group]["captions"].append(caption)
            group_descriptions[group]["stereotype_scores"].append(self._detect_stereotype(caption))
        
        # Calculate statistics per group
        consistency_metrics = {}
        
        for group, data in group_descriptions.items():
            caption_lengths = [len(c.split()) for c in data["captions"]]
            avg_length = np.mean(caption_lengths)
            avg_stereotype = np.mean(data["stereotype_scores"])
            
            consistency_metrics[group] = {
                "num_samples": len(data["captions"]),
                "avg_caption_length": avg_length,
                "avg_stereotype_score": avg_stereotype,
                "caption_length_std": np.std(caption_lengths)
            }
        
        # Detect consistency bias
        if consistency_metrics:
            avg_lengths = [m["avg_caption_length"] for m in consistency_metrics.values()]
            avg_stereotypes = [m["avg_stereotype_score"] for m in consistency_metrics.values()]
            
            length_variance = np.var(avg_lengths)
            stereotype_variance = np.var(avg_stereotypes)
        else:
            length_variance = 0
            stereotype_variance = 0
        
        return {
            "group_representation_metrics": consistency_metrics,
            "caption_length_variance_across_groups": length_variance,
            "stereotype_variance_across_groups": stereotype_variance,
            "representation_consistency_bias_detected": (
                length_variance > 10 or stereotype_variance > 0.1
            )
        }
    
    def analyze_attribute_association_bias(
        self,
        image_captions: List[Dict],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze if certain attributes are unfairly associated with specific demographic groups.
        """
        group_attributes = {}
        
        for i, pair in enumerate(image_captions):
            caption = pair.get("caption", "").lower()
            group = demographic_groups[i]
            
            if group not in group_attributes:
                group_attributes[group] = {
                    "occupational_positive": 0,
                    "occupational_negative": 0,
                    "behavioral_positive": 0,
                    "behavioral_negative": 0,
                    "total_captions": 0
                }
            
            # Count attribute presence
            for attr in self.stereotype_keywords["occupational"]["positive"]:
                if attr in caption:
                    group_attributes[group]["occupational_positive"] += 1
            
            for attr in self.stereotype_keywords["occupational"]["negative"]:
                if attr in caption:
                    group_attributes[group]["occupational_negative"] += 1
            
            for attr in self.stereotype_keywords["behavioral"]["positive"]:
                if attr in caption:
                    group_attributes[group]["behavioral_positive"] += 1
            
            for attr in self.stereotype_keywords["behavioral"]["negative"]:
                if attr in caption:
                    group_attributes[group]["behavioral_negative"] += 1
            
            group_attributes[group]["total_captions"] += 1
        
        # Calculate attribution bias scores
        attribution_bias_scores = {}
        
        for group, attrs in group_attributes.items():
            total = attrs["total_captions"]
            if total > 0:
                occupational_bias = (
                    attrs["occupational_negative"] / total -
                    attrs["occupational_positive"] / total
                )
                behavioral_bias = (
                    attrs["behavioral_negative"] / total -
                    attrs["behavioral_positive"] / total
                )
            else:
                occupational_bias = 0
                behavioral_bias = 0
            
            attribution_bias_scores[group] = {
                "occupational_bias": occupational_bias,
                "behavioral_bias": behavioral_bias,
                "combined_bias": abs(occupational_bias) + abs(behavioral_bias)
            }
        
        return {
            "attribution_bias_by_group": attribution_bias_scores,
            "max_attribution_bias": max(
                (v["combined_bias"] for v in attribution_bias_scores.values()),
                default=0
            ),
            "attribution_bias_detected": any(
                v["combined_bias"] > 0.2 for v in attribution_bias_scores.values()
            )
        }
    
    def analyze_visual_semantic_gap(
        self,
        image_captions: List[Dict],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Analyze the gap between visual content complexity and caption complexity.
        """
        gaps = []
        group_gaps = {}
        
        for i, pair in enumerate(image_captions):
            caption = pair.get("caption", "")
            image = pair.get("image")
            group = demographic_groups[i]
            
            # Simple visual complexity proxy (based on image preprocessing info)
            # In real CLIP/VILT, this would be actual image embedding complexity
            visual_complexity = 0.5  # Placeholder
            
            # Caption complexity
            caption_complexity = len(set(caption.lower().split())) / max(len(caption.split()), 1)
            
            # Gap
            gap = abs(visual_complexity - caption_complexity)
            gaps.append(gap)
            
            if group not in group_gaps:
                group_gaps[group] = []
            group_gaps[group].append(gap)
        
        # Calculate statistics
        avg_gap = np.mean(gaps) if gaps else 0
        gap_variance = np.var(gaps) if gaps else 0
        
        group_gap_stats = {
            group: {
                "avg_gap": np.mean(g),
                "gap_std": np.std(g),
                "num_samples": len(g)
            }
            for group, g in group_gaps.items()
        }
        
        return {
            "average_visual_semantic_gap": avg_gap,
            "gap_variance": gap_variance,
            "group_gap_statistics": group_gap_stats,
            "visual_semantic_bias_detected": gap_variance > 0.1
        }
    
    def comprehensive_multimodal_bias_analysis(
        self,
        image_captions: List[Dict],
        demographic_groups: List[str]
    ) -> Dict:
        """
        Perform comprehensive bias analysis on multimodal (image-caption) dataset.
        """
        alignment_analysis = self.analyze_image_caption_alignment(
            image_captions, demographic_groups
        )
        
        representation_analysis = self.analyze_representation_consistency(
            image_captions, demographic_groups
        )
        
        attribution_analysis = self.analyze_attribute_association_bias(
            image_captions, demographic_groups
        )
        
        gap_analysis = self.analyze_visual_semantic_gap(
            image_captions, demographic_groups
        )
        
        # Combine into overall bias score
        overall_bias_score = (
            float(alignment_analysis["alignment_bias_detected"]) * 0.25 +
            float(representation_analysis["representation_consistency_bias_detected"]) * 0.25 +
            float(attribution_analysis["attribution_bias_detected"]) * 0.25 +
            float(gap_analysis["visual_semantic_bias_detected"]) * 0.25
        )
        
        return {
            "alignment_analysis": alignment_analysis,
            "representation_analysis": representation_analysis,
            "attribution_analysis": attribution_analysis,
            "visual_semantic_analysis": gap_analysis,
            "overall_multimodal_bias_score": overall_bias_score,
            "bias_level": self._score_to_bias_level(overall_bias_score),
            "total_pairs_analyzed": len(image_captions)
        }
    
    def _detect_stereotype(self, text: str) -> float:
        """
        Detect stereotype presence in text.
        Returns score 0-1 where 1 is highly stereotypical.
        """
        stereotype_count = 0
        total_checks = 0
        
        for category, words_dict in self.stereotype_keywords.items():
            for sentiment, words in words_dict.items():
                total_checks += len(words)
                for word in words:
                    if word in text:
                        stereotype_count += 1
        
        if total_checks == 0:
            return 0.0
        
        return stereotype_count / total_checks
    
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
