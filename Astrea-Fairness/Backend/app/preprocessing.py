"""
Data preprocessing module for cleaning, tokenization, and alignment.
Handles text, image, and multimodal data normalization.
"""

import numpy as np
import pandas as pd
from PIL import Image
import io
import string
import re
from typing import Union, List, Dict, Tuple


class TextPreprocessor:
    """Preprocessing for text data - cleaning and tokenization."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text by removing special characters, extra whitespace, etc."""
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text into words."""
        cleaned_text = TextPreprocessor.clean_text(text)
        tokens = cleaned_text.split()
        return tokens
    
    @staticmethod
    def normalize_text(text: str, max_length: int = 512) -> str:
        """Normalize text to consistent length and format."""
        cleaned_text = TextPreprocessor.clean_text(text)
        
        # Truncate if too long
        if len(cleaned_text) > max_length:
            cleaned_text = cleaned_text[:max_length]
        
        return cleaned_text


class ImagePreprocessor:
    """Preprocessing for image data - normalization and resizing."""
    
    @staticmethod
    def load_image(image_data: Union[bytes, str], target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """Load and preprocess image data."""
        try:
            # Load image from bytes
            if isinstance(image_data, bytes):
                image = Image.open(io.BytesIO(image_data))
            else:
                image = Image.open(image_data)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize to target size
            image = image.resize(target_size)
            
            # Convert to numpy array and normalize
            image_array = np.array(image, dtype=np.float32) / 255.0
            
            return image_array
        except Exception as e:
            raise ValueError(f"Failed to load image: {str(e)}")
    
    @staticmethod
    def normalize_image(image_array: np.ndarray) -> np.ndarray:
        """Normalize image using ImageNet mean and std."""
        imagenet_mean = np.array([0.485, 0.456, 0.406])
        imagenet_std = np.array([0.229, 0.224, 0.225])
        
        normalized = (image_array - imagenet_mean) / imagenet_std
        return normalized


class MultimodalPreprocessor:
    """Preprocessing for multimodal data - aligning images with captions."""
    
    @staticmethod
    def align_image_caption(image_data: Union[bytes, str], caption: str) -> Dict:
        """Align image and caption for multimodal analysis."""
        try:
            # Process image
            image_array = ImagePreprocessor.load_image(image_data)
            image_normalized = ImagePreprocessor.normalize_image(image_array)
            
            # Process caption
            caption_cleaned = TextPreprocessor.clean_text(caption)
            caption_tokens = TextPreprocessor.tokenize(caption)
            
            return {
                "image": image_normalized,
                "caption_text": caption_cleaned,
                "caption_tokens": caption_tokens,
                "image_shape": image_normalized.shape,
                "caption_length": len(caption_tokens)
            }
        except Exception as e:
            raise ValueError(f"Failed to align image-caption pair: {str(e)}")
    
    @staticmethod
    def batch_align_image_captions(image_caption_pairs: List[Dict]) -> List[Dict]:
        """Align multiple image-caption pairs."""
        aligned_pairs = []
        
        for pair in image_caption_pairs:
            try:
                aligned = MultimodalPreprocessor.align_image_caption(
                    pair.get("image"),
                    pair.get("caption", "")
                )
                aligned_pairs.append(aligned)
            except Exception as e:
                print(f"Warning: Failed to align pair - {str(e)}")
                continue
        
        return aligned_pairs


class DataPreprocessor:
    """Main preprocessing orchestrator for different data types."""
    
    @staticmethod
    def preprocess_dataset(
        data: Union[pd.DataFrame, List, bytes, str],
        data_type: str = "tabular",
        **kwargs
    ) -> Union[pd.DataFrame, np.ndarray, Dict]:
        """
        Preprocess dataset based on type.
        
        Args:
            data: Input data
            data_type: Type of data - 'tabular', 'text', 'image', 'multimodal'
            **kwargs: Additional arguments for specific preprocessing
        
        Returns:
            Preprocessed data
        """
        if data_type == "tabular":
            return DataPreprocessor._preprocess_tabular(data)
        elif data_type == "text":
            return DataPreprocessor._preprocess_text(data)
        elif data_type == "image":
            return DataPreprocessor._preprocess_image(data)
        elif data_type == "multimodal":
            return DataPreprocessor._preprocess_multimodal(data)
        else:
            raise ValueError(f"Unknown data type: {data_type}")
    
    @staticmethod
    def _preprocess_tabular(data: pd.DataFrame) -> pd.DataFrame:
        """Preprocess tabular data - handle missing values, normalization."""
        df = data.copy()
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        # Fill numeric missing values with median
        for col in numeric_cols:
            df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical missing values with mode
        for col in categorical_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
        
        return df
    
    @staticmethod
    def _preprocess_text(data: Union[pd.DataFrame, List[str]]) -> pd.DataFrame:
        """Preprocess text data - clean and tokenize."""
        if isinstance(data, list):
            texts = data
        elif isinstance(data, pd.DataFrame):
            texts = data.iloc[:, 0].tolist() if len(data.columns) > 0 else []
        else:
            texts = [str(data)]
        
        processed = {
            "original": texts,
            "cleaned": [TextPreprocessor.clean_text(text) for text in texts],
            "tokens": [TextPreprocessor.tokenize(text) for text in texts],
            "token_count": [len(TextPreprocessor.tokenize(text)) for text in texts]
        }
        
        return pd.DataFrame(processed)
    
    @staticmethod
    def _preprocess_image(data: List[bytes]) -> List[np.ndarray]:
        """Preprocess image data - normalize and resize."""
        processed_images = []
        
        for image_bytes in data:
            try:
                image = ImagePreprocessor.load_image(image_bytes)
                normalized = ImagePreprocessor.normalize_image(image)
                processed_images.append(normalized)
            except Exception as e:
                print(f"Warning: Failed to process image - {str(e)}")
                continue
        
        return processed_images
    
    @staticmethod
    def _preprocess_multimodal(data: List[Dict]) -> List[Dict]:
        """Preprocess multimodal data - align images and captions."""
        return MultimodalPreprocessor.batch_align_image_captions(data)
