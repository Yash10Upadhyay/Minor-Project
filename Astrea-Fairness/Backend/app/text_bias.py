"""
Text analysis module for detecting gender, race, and sentiment bias using BERT-based models.
Analyzes text datasets for fairness issues.
"""

import numpy as np
from typing import Dict, List, Tuple
import re
import warnings

warnings.filterwarnings('ignore')

# Try to import transformers; fallback to keyword-based if not available
try:
    from transformers import pipeline
    import torch
    BERT_AVAILABLE = True
except ImportError:
    BERT_AVAILABLE = False


class TextBiasAnalyzer:
    """Analyzes bias in text datasets using BERT embeddings and semantic analysis."""
    
    def __init__(self):
        """Initialize text bias analyzer with BERT models."""
        self.bert_available = BERT_AVAILABLE
        
        # Initialize BERT models if available
        if self.bert_available:
            try:
                # Zero-shot classification for gender, race, sentiment
                self.zero_shot_classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli"
                )
                # Sentiment analysis
                self.sentiment_classifier = pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english"
                )
            except Exception as e:
                print(f"Warning: Could not load BERT models: {e}")
                self.bert_available = False
        
        # Fallback keyword dictionaries for when BERT is not available
        self.gender_keywords = {
            "male": ["man", "men", "male", "boy", "he", "his", "him", "father", "brother", "son", "husband"],
            "female": ["woman", "women", "female", "girl", "she", "her", "hers", "mother", "sister", "daughter", "wife"],
            "neutral": ["person", "people", "human", "individual", "they", "them", "theirs", "child", "teen"]
        }
        
        self.race_keywords = {
            "african": ["african", "black", "afro", "negro"],
            "asian": ["asian", "chinese", "japanese", "korean", "indian", "vietnamese", "thai", "philippines"],
            "european": ["white", "caucasian", "european"],
            "hispanic": ["hispanic", "latino", "mexican", "spanish", "puerto rico"],
            "middle_eastern": ["arab", "muslim", "persian", "turkish", "lebanese"]
        }
        
        self.sentiment_keywords = {
            "positive": ["good", "great", "excellent", "amazing", "wonderful", "perfect", "love", "brilliant", "fantastic"],
            "negative": ["bad", "terrible", "awful", "horrible", "hate", "poor", "worst", "disgusting", "pathetic"],
            "neutral": ["ok", "fine", "average", "normal", "usual", "common", "okay"]
        }
    
    def detect_gender_bias(self, texts: List[str]) -> Dict:
        """
        Detect gender bias in text data using BERT or keywords.
        
        Args:
            texts: List of text samples
        
        Returns:
            Dictionary with gender bias metrics
        """
        if self.bert_available:
            return self._detect_gender_bias_bert(texts)
        else:
            return self._detect_gender_bias_keywords(texts)
    
    def _detect_gender_bias_bert(self, texts: List[str]) -> Dict:
        """Detect gender bias using BERT zero-shot classification."""
        gender_scores = {"male": [], "female": [], "neutral": []}
        text_gender_mapping = []
        
        for text in texts:
            if len(text.strip()) == 0:
                continue
            
            try:
                # Use zero-shot classification for gender
                result = self.zero_shot_classifier(
                    text[:512],  # Limit to 512 chars for BERT
                    ["gender-biased toward male", "gender-biased toward female", "gender-neutral"],
                    multi_class=False
                )
                
                scores = result["scores"] if isinstance(result, dict) else [0, 0, 0]
                if isinstance(result, list) and len(result) > 0:
                    scores = result[0].get("scores", [0, 0, 0])
                
                gender_scores["male"].append(scores[0] if len(scores) > 0 else 0)
                gender_scores["female"].append(scores[1] if len(scores) > 1 else 0)
                gender_scores["neutral"].append(scores[2] if len(scores) > 2 else 0)
                
                text_gender_mapping.append({
                    "text_preview": text[:100],
                    "male_bias": float(scores[0]) if len(scores) > 0 else 0,
                    "female_bias": float(scores[1]) if len(scores) > 1 else 0,
                    "neutral": float(scores[2]) if len(scores) > 2 else 0
                })
            except Exception as e:
                print(f"Error processing text with BERT: {e}")
                continue
        
        # Calculate averages
        avg_male = np.mean(gender_scores["male"]) if gender_scores["male"] else 0
        avg_female = np.mean(gender_scores["female"]) if gender_scores["female"] else 0
        avg_neutral = np.mean(gender_scores["neutral"]) if gender_scores["neutral"] else 0
        
        # Calculate gender bias score
        gender_bias_score = abs(avg_male - avg_female)
        
        return {
            "gender_bias_scores": {
                "male_bias": float(avg_male),
                "female_bias": float(avg_female),
                "neutral": float(avg_neutral)
            },
            "gender_bias_score": float(gender_bias_score),
            "bias_level": self._score_to_bias_level(gender_bias_score),
            "detail_mapping": text_gender_mapping[:10]
        }
    
    def _detect_gender_bias_keywords(self, texts: List[str]) -> Dict:
        """Fallback: detect gender bias using keyword matching."""
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
            "gender_bias_score": float(gender_bias_score),
            "bias_level": self._score_to_bias_level(gender_bias_score),
            "detail_mapping": text_gender_mapping[:10]  # Return first 10 for preview
        }
    
    def detect_race_bias(self, texts: List[str]) -> Dict:
        """
        Detect racial bias in text data using BERT or keywords.
        
        Args:
            texts: List of text samples
        
        Returns:
            Dictionary with racial bias metrics
        """
        if self.bert_available:
            return self._detect_race_bias_bert(texts)
        else:
            return self._detect_race_bias_keywords(texts)
    
    def _detect_race_bias_bert(self, texts: List[str]) -> Dict:
        """Detect race bias using BERT zero-shot classification."""
        race_scores = {race: [] for race in self.race_keywords.keys()}
        text_race_mapping = []
        
        for text in texts:
            if len(text.strip()) == 0:
                continue
            
            try:
                race_labels = [
                    "mentions african or black people",
                    "mentions asian people",
                    "mentions european or white people",
                    "mentions hispanic or latino people",
                    "mentions middle eastern people"
                ]
                
                result = self.zero_shot_classifier(
                    text[:512],
                    race_labels,
                    multi_class=True
                )
                
                scores = [0] * len(race_labels)
                if isinstance(result, dict) and "scores" in result:
                    scores = result["scores"]
                elif isinstance(result, list) and len(result) > 0 and "scores" in result[0]:
                    scores = result[0]["scores"]
                
                for i, race in enumerate(self.race_keywords.keys()):
                    race_scores[race].append(scores[i] if i < len(scores) else 0)
                
                text_race_mapping.append({
                    "text_preview": text[:100],
                    "race_scores": {race: float(scores[i]) if i < len(scores) else 0 
                                   for i, race in enumerate(self.race_keywords.keys())}
                })
            except Exception as e:
                print(f"Error processing race with BERT: {e}")
                continue
        
        # Calculate averages
        avg_scores = {race: np.mean(scores) if scores else 0 for race, scores in race_scores.items()}
        race_bias_score = self._calculate_representation_bias({k: v*100 for k, v in avg_scores.items()})
        
        return {
            "race_bias_scores": {k: float(v) for k, v in avg_scores.items()},
            "race_bias_score": float(race_bias_score),
            "bias_level": self._score_to_bias_level(race_bias_score),
            "detail_mapping": text_race_mapping[:10]
        }
    
    def _detect_race_bias_keywords(self, texts: List[str]) -> Dict:
        """Fallback: detect racial bias using keyword matching."""
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
            "race_bias_score": float(race_bias_score),
            "bias_level": self._score_to_bias_level(race_bias_score),
            "detail_mapping": text_race_mapping[:10]
        }
    
    def detect_sentiment_bias(self, texts: List[str]) -> Dict:
        """
        Detect sentiment bias in text data using BERT.
        Analyzes if positive/negative sentiments are associated with specific demographics.
        
        Args:
            texts: List of text samples
        
        Returns:
            Dictionary with sentiment bias metrics
        """
        if self.bert_available:
            return self._detect_sentiment_bias_bert(texts)
        else:
            return self._detect_sentiment_bias_keywords(texts)
    
    def _detect_sentiment_bias_bert(self, texts: List[str]) -> Dict:
        """Detect sentiment bias using BERT sentiment analysis."""
        sentiment_scores = []
        sentiment_distribution = {"positive": 0, "negative": 0, "neutral": 0}
        
        for text in texts:
            if len(text.strip()) == 0:
                continue
            
            try:
                result = self.sentiment_classifier(text[:512])
                if isinstance(result, list) and len(result) > 0:
                    label = result[0]["label"].lower()
                    score = result[0]["score"]
                    
                    # Map to sentiment
                    if "positive" in label:
                        sentiment_scores.append(score)
                        sentiment_distribution["positive"] += 1
                    elif "negative" in label:
                        sentiment_scores.append(-score)
                        sentiment_distribution["negative"] += 1
                    else:
                        sentiment_distribution["neutral"] += 1
            except Exception as e:
                print(f"Error processing sentiment with BERT: {e}")
                continue
        
        total_mentions = sum(sentiment_distribution.values())
        sentiment_percentages = {
            sent: (count / total_mentions * 100) if total_mentions > 0 else 0
            for sent, count in sentiment_distribution.items()
        }
        
        sentiment_bias_score = self._calculate_representation_bias(sentiment_percentages)
        
        return {
            "sentiment_distribution": sentiment_distribution,
            "sentiment_percentages": sentiment_percentages,
            "average_sentiment_score": float(np.mean(sentiment_scores)) if sentiment_scores else 0,
            "sentiment_bias_score": float(sentiment_bias_score),
            "bias_level": self._score_to_bias_level(sentiment_bias_score)
        }
    
    def _detect_sentiment_bias_keywords(self, texts: List[str]) -> Dict:
        """Fallback: detect sentiment bias using keyword matching."""
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
            "average_sentiment_score": float(np.mean(sentiment_scores)) if sentiment_scores else 0,
            "sentiment_bias_score": float(sentiment_bias_score),
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
            avg_word_length = float(np.mean([len(word) for word in words])) if words else 0.0
            unique_words = len(set(word.lower() for word in words))
            sentence_count = len(re.split(r'[.!?]+', text))
            avg_sentence_length = float(len(words)) / max(sentence_count, 1) if words else 0.0

            # Complexity score (simple heuristic)
            complexity = (avg_word_length + unique_words / max(len(words), 1)) / 2 if words else 0.0
            complexity_scores.append(float(complexity))

        complexity_mean = float(np.mean(complexity_scores)) if complexity_scores else 0.0
        complexity_std = float(np.std(complexity_scores)) if complexity_scores else 0.0

        return {
            "average_complexity": complexity_mean,
            "complexity_variance": complexity_std,
            "complexity_bias_detected": bool(complexity_std > complexity_mean * 0.5)  # High variance = bias
        }
    
    def comprehensive_text_bias_analysis(self, texts: List[str]) -> Dict:
        """
        Perform comprehensive bias analysis on text dataset.
        """
        # Support two input formats:
        # - List[str] (plain texts)
        # - List[dict] with keys {'text': ..., 'news': <source>} so news bias is checked
        records = []
        if isinstance(texts, list) and len(texts) > 0 and isinstance(texts[0], dict):
            # extract texts and news sources
            for r in texts:
                records.append({
                    "text": str(r.get("text", "")),
                    "news": r.get("news") or r.get("source") or r.get("media")
                })
            plain_texts = [r["text"] for r in records]
        else:
            plain_texts = [str(t) for t in (texts or [])]

        gender_analysis = self.detect_gender_bias(plain_texts)
        race_analysis = self.detect_race_bias(plain_texts)
        sentiment_analysis = self.detect_sentiment_bias(plain_texts)
        complexity_analysis = self.detect_language_complexity_bias(plain_texts)

        news_analysis = None
        if records:
            # collect sources
            sources = [r.get("news") for r in records if r.get("news")]
            if sources:
                news_analysis = self.detect_news_bias(sources)

        # Combine into overall bias score using weighted average
        overall_bias_score = (
            float(gender_analysis.get("gender_bias_score", 0)) * 0.4 +
            float(race_analysis.get("race_bias_score", 0)) * 0.4 +
            float(sentiment_analysis.get("sentiment_bias_score", 0)) * 0.2 +
            (float(news_analysis.get("news_bias_score", 0)) * 0.1 if news_analysis else 0)
        )

        result = {
            "gender_analysis": gender_analysis,
            "race_analysis": race_analysis,
            "sentiment_analysis": sentiment_analysis,
            "language_complexity_analysis": complexity_analysis,
            "overall_text_bias_score": float(overall_bias_score),
            "bias_level": self._score_to_bias_level(overall_bias_score),
            "total_texts_analyzed": len(plain_texts),
            "using_bert": bool(self.bert_available)
        }

        if news_analysis is not None:
            # build per-record news field analysis
            per_record = []
            mapping = news_analysis.get("source_mapping", {}) if isinstance(news_analysis, dict) else {}

            # map label to numeric for per-record scoring
            def _label_to_numeric(label: str) -> float:
                if not label:
                    return 0.0
                vl = str(label).lower()
                if any(k in vl for k in ("left", "liberal", "progress")):
                    return -1.0
                if any(k in vl for k in ("right", "conserv")):
                    return 1.0
                return 0.0

            for r in records:
                src = r.get("news")
                if not src:
                    per_record.append({
                        "text_preview": r.get("text", "")[:100],
                        "news_source": None,
                        "news_label": "unknown",
                        "news_numeric": 0.0
                    })
                    continue

                label = mapping.get(src, mapping.get(str(src).lower(), "unknown"))
                numeric = _label_to_numeric(label)
                per_record.append({
                    "text_preview": r.get("text", "")[:100],
                    "news_source": src,
                    "news_label": label,
                    "news_numeric": float(numeric)
                })

            # attach detailed news analysis
            result["news_analysis"] = {
                "summary": news_analysis,
                "per_record": per_record
            }

        return result

    def detect_news_bias(self, sources: List[str]) -> Dict:
        """Detect bias of news sources using the HuggingFace 'newsmediabias/news-bias-full-data' dataset when available.

        Returns a mapping of source -> known bias label (if found) and distribution statistics.
        """
        sources = [str(s).strip() for s in sources if s]
        if not sources:
            return {"news_bias_score": 0.0, "source_mapping": {}, "distribution": {}}

        source_mapping = {}
        distribution = {}

        if not DATASETS_AVAILABLE:
            # Datasets not installed: return unknowns
            for s in sources:
                source_mapping[s] = "unknown"
            return {"news_bias_score": 0.0, "source_mapping": source_mapping, "distribution": {}}

        try:
            ds = load_dataset("newsmediabias/news-bias-full-data")
            # pick first split that exists
            split = list(ds.keys())[0]
            table = ds[split]

            # heuristics: find candidate columns for source and bias
            cols = table.column_names
            source_col = None
            bias_col = None
            for c in cols:
                lc = c.lower()
                if any(x in lc for x in ("source", "site", "media", "publication", "domain")):
                    source_col = c
                if any(x in lc for x in ("bias", "lean", "ideology", "rating")):
                    bias_col = c

            # build mapping
            mapping = {}
            if source_col and bias_col:
                for row in table:
                    src = str(row[source_col]).strip()
                    b = row[bias_col]
                    mapping[src.lower()] = str(b)

            for s in sources:
                key = s.lower()
                label = mapping.get(key, "unknown")
                source_mapping[s] = label
                distribution[label] = distribution.get(label, 0) + 1

            # simple news bias score: how many known non-neutral labels proportion
            known = [v for v in source_mapping.values() if v != "unknown"]
            if not known:
                news_bias_score = 0.0
            else:
                # map labels to a crude numeric bias (left/right/center unknown) if possible
                # attempt simple mapping
                left_keywords = ("left", "liberal", "progress")
                right_keywords = ("right", "conserv")
                center_keywords = ("center", "mixed", "balanced")
                vals = []
                for v in known:
                    vl = v.lower()
                    if any(k in vl for k in left_keywords):
                        vals.append(-1)
                    elif any(k in vl for k in right_keywords):
                        vals.append(1)
                    elif any(k in vl for k in center_keywords):
                        vals.append(0)
                    else:
                        vals.append(0)
                # bias score normalized 0-1 = abs(mean)
                import statistics
                mean_val = statistics.mean(vals) if vals else 0
                news_bias_score = abs(mean_val)

            return {
                "news_bias_score": float(news_bias_score),
                "source_mapping": source_mapping,
                "distribution": distribution
            }
        except Exception as e:
            # on failure, return unknowns
            for s in sources:
                source_mapping[s] = "unknown"
            return {"news_bias_score": 0.0, "source_mapping": source_mapping, "distribution": {}}

        # Combine into overall bias score using weighted average
        overall_bias_score = (
            float(gender_analysis.get("gender_bias_score", 0)) * 0.4 +
            float(race_analysis.get("race_bias_score", 0)) * 0.4 +
            float(sentiment_analysis.get("sentiment_bias_score", 0)) * 0.2
        )

        return {
            "gender_analysis": gender_analysis,
            "race_analysis": race_analysis,
            "sentiment_analysis": sentiment_analysis,
            "language_complexity_analysis": complexity_analysis,
            "overall_text_bias_score": float(overall_bias_score),
            "bias_level": self._score_to_bias_level(overall_bias_score),
            "total_texts_analyzed": len(texts),
            "using_bert": bool(self.bert_available)
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
