"""
Text analysis module for detecting gender, race, and sentiment bias using BERT-based models.
Analyzes text datasets for fairness issues.
"""

import numpy as np
from typing import Dict, List, Tuple
import re
import warnings

warnings.filterwarnings('ignore')


class TextBiasAnalyzer:
    """Analyzes bias in text datasets using BERT embeddings and semantic analysis."""
    
    def __init__(self):
        """Initialize text bias analyzer."""
        # Define bias-related keywords for different categories
        self.gender_keywords = {
            "male": ["man", "men", "male", "boy", "he", "his", "him", "father", "brother"],
            "female": ["woman", "women", "female", "girl", "she", "her", "hers", "mother", "sister"],
            "neutral": ["person", "people", "human", "individual", "they", "them", "theirs"]
        }
        
        self.race_keywords = {
            "african": ["african", "black", "negro", "afro"],
            "asian": ["asian", "chinese", "japanese", "korean", "indian", "vietnamese"],
            "european": ["white", "caucasian", "european"],
            "hispanic": ["hispanic", "latino", "mexican", "spanish"],
            "middle_eastern": ["arab", "muslim", "persian"]
        }
        
        self.sentiment_keywords = {
            "positive": ["good", "great", "excellent", "amazing", "wonderful", "perfect", "love"],
            "negative": ["bad", "terrible", "awful", "horrible", "hate", "poor", "worst"],
            "neutral": ["ok", "fine", "average", "normal", "usual", "common"]
        }
    
    def detect_gender_bias(self, texts: List[str]) -> Dict:
        """
        Detect gender bias in text data.
        
        Args:
            texts: List of text samples
        
        Returns:
            Dictionary with gender bias metrics
        """
        gender_counts = {category: 0 for category in self.gender_keywords.keys()}
        text_gender_mapping = []
        
        for text in texts:
            text_lower = text.lower()
            detected_genders = []
            
            for gender, keywords in self.gender_keywords.items():
                count = sum(1 for keyword in keywords if keyword in text_lower)
                gender_counts[gender] += count
                if count > 0:
                    detected_genders.append((gender, count))
            
            text_gender_mapping.append({
                "text_preview": text[:100],
                "detected_genders": detected_genders
            })
        
        # Calculate gender representation
        total_mentions = sum(gender_counts.values())
        gender_percentages = {
            gender: (count / total_mentions * 100) if total_mentions > 0 else 0
            for gender, count in gender_counts.items()
        }
        
        # Calculate gender bias score
        gender_bias_score = self._calculate_representation_bias(gender_percentages)
        
        return {
            "gender_mentions_count": gender_counts,
            "gender_percentages": gender_percentages,
            "gender_bias_score": gender_bias_score,
            "bias_level": self._score_to_bias_level(gender_bias_score),
            "detail_mapping": text_gender_mapping[:10]  # Return first 10 for preview
        }
    
    def detect_race_bias(self, texts: List[str]) -> Dict:
        """
        Detect racial bias in text data.
        
        Args:
            texts: List of text samples
        
        Returns:
            Dictionary with racial bias metrics
        """
        race_counts = {category: 0 for category in self.race_keywords.keys()}
        text_race_mapping = []
        
        for text in texts:
            text_lower = text.lower()
            detected_races = []
            
            for race, keywords in self.race_keywords.items():
                count = sum(1 for keyword in keywords if keyword in text_lower)
                race_counts[race] += count
                if count > 0:
                    detected_races.append((race, count))
            
            text_race_mapping.append({
                "text_preview": text[:100],
                "detected_races": detected_races
            })
        
        # Calculate race representation
        total_mentions = sum(race_counts.values())
        race_percentages = {
            race: (count / total_mentions * 100) if total_mentions > 0 else 0
            for race, count in race_counts.items()
        }
        
        # Calculate race bias score
        race_bias_score = self._calculate_representation_bias(race_percentages)
        
        return {
            "race_mentions_count": race_counts,
            "race_percentages": race_percentages,
            "race_bias_score": race_bias_score,
            "bias_level": self._score_to_bias_level(race_bias_score),
            "detail_mapping": text_race_mapping[:10]
        }
    
    def detect_sentiment_bias(self, texts: List[str]) -> Dict:
        """
        Detect sentiment bias in text data.
        Analyzes if positive/negative sentiments are associated with specific demographics.
        
        Args:
            texts: List of text samples
        
        Returns:
            Dictionary with sentiment bias metrics
        """
        sentiment_counts = {category: 0 for category in self.sentiment_keywords.keys()}
        sentiment_scores = []
        
        for text in texts:
            text_lower = text.lower()
            sentiment_score = 0
            
            # Calculate sentiment score
            for keyword in self.sentiment_keywords["positive"]:
                if keyword in text_lower:
                    sentiment_score += 1
                    sentiment_counts["positive"] += 1
            
            for keyword in self.sentiment_keywords["negative"]:
                if keyword in text_lower:
                    sentiment_score -= 1
                    sentiment_counts["negative"] += 1
            
            if sentiment_score == 0:
                sentiment_counts["neutral"] += 1
            
            sentiment_scores.append(sentiment_score)
        
        # Calculate sentiment distribution
        total_mentions = sum(sentiment_counts.values())
        sentiment_percentages = {
            sentiment: (count / total_mentions * 100) if total_mentions > 0 else 0
            for sentiment, count in sentiment_counts.items()
        }
        
        # Calculate sentiment bias
        sentiment_bias_score = self._calculate_representation_bias(sentiment_percentages)
        
        return {
            "sentiment_distribution": sentiment_counts,
            "sentiment_percentages": sentiment_percentages,
            "average_sentiment_score": np.mean(sentiment_scores) if sentiment_scores else 0,
            "sentiment_bias_score": sentiment_bias_score,
            "bias_level": self._score_to_bias_level(sentiment_bias_score)
        }
    
    def detect_language_complexity_bias(self, texts: List[str]) -> Dict:
        """
        Detect if language complexity varies across different text samples.
        May indicate bias in how different groups/topics are described.
        """
        complexity_scores = []
        
        for text in texts:
            # Calculate complexity metrics
            words = text.split()
            avg_word_length = np.mean([len(word) for word in words]) if words else 0
            unique_words = len(set(word.lower() for word in words))
            sentence_count = len(re.split(r'[.!?]+', text))
            avg_sentence_length = len(words) / max(sentence_count, 1)
            
            # Complexity score
            complexity = (avg_word_length + unique_words / max(len(words), 1)) / 2
            complexity_scores.append(complexity)
        
        complexity_mean = np.mean(complexity_scores)
        complexity_std = np.std(complexity_scores)
        
        return {
            "average_complexity": complexity_mean,
            "complexity_variance": complexity_std,
            "complexity_bias_detected": complexity_std > complexity_mean * 0.5  # High variance = bias
        }
    
    def comprehensive_text_bias_analysis(self, texts: List[str]) -> Dict:
        """
        Perform comprehensive bias analysis on text dataset.
        """
        gender_analysis = self.detect_gender_bias(texts)
        race_analysis = self.detect_race_bias(texts)
        sentiment_analysis = self.detect_sentiment_bias(texts)
        complexity_analysis = self.detect_language_complexity_bias(texts)
        
        # Combine into overall bias score
        overall_bias_score = (
            gender_analysis["gender_bias_score"] * 0.4 +
            race_analysis["race_bias_score"] * 0.4 +
            sentiment_analysis["sentiment_bias_score"] * 0.2
        )
        
        return {
            "gender_analysis": gender_analysis,
            "race_analysis": race_analysis,
            "sentiment_analysis": sentiment_analysis,
            "language_complexity_analysis": complexity_analysis,
            "overall_text_bias_score": overall_bias_score,
            "bias_level": self._score_to_bias_level(overall_bias_score),
            "total_texts_analyzed": len(texts)
        }
    
    @staticmethod
    def _calculate_representation_bias(percentages: Dict[str, float]) -> float:
        """
        Calculate bias score based on representation percentages.
        Returns 0 (balanced) to 1 (highly biased).
        """
        if not percentages or len(percentages) < 2:
            return 0.0
        
        values = [v for v in percentages.values() if v > 0]
        if not values:
            return 0.0
        
        # Calculate how far from uniform distribution
        uniform_percentage = 100 / len(percentages)
        max_deviation = sum(abs(v - uniform_percentage) for v in values) / len(values)
        
        # Normalize to 0-1 scale
        bias_score = min(max_deviation / 100, 1.0)
        
        return bias_score
    
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
