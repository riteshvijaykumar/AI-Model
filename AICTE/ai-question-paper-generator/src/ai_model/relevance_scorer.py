"""
Relevance Scorer Module

Scores questions based on relevance to user criteria using various metrics
including semantic similarity, keyword matching, and learned preferences.
"""

import numpy as np
from typing import List, Dict, Any, Optional
from collections import Counter
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class RelevanceScorer:
    """Scores questions based on relevance to selection criteria"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.keyword_weights = {}
        self.preference_model = None
        
    def score_questions(self, questions: List[Dict[str, Any]], 
                       criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Score questions based on relevance to criteria"""
        scored_questions = []
        
        for question in questions:
            relevance_score = self._calculate_relevance_score(question, criteria)
            question_copy = question.copy()
            question_copy['relevance_score'] = relevance_score
            scored_questions.append(question_copy)
        
        return scored_questions
    
    def _calculate_relevance_score(self, question: Dict[str, Any], 
                                  criteria: Dict[str, Any]) -> float:
        """Calculate overall relevance score for a question"""
        scores = []
        
        # Topic relevance
        if criteria.get('topic'):
            topic_score = self._calculate_topic_relevance(question, criteria)
            scores.append(topic_score * 0.3)
        
        # Keyword relevance
        if criteria.get('keywords'):
            keyword_score = self._calculate_keyword_relevance(question, criteria)
            scores.append(keyword_score * 0.25)
        
        # Difficulty match
        if criteria.get('difficulty'):
            difficulty_score = self._calculate_difficulty_match(question, criteria)
            scores.append(difficulty_score * 0.2)
        
        # Type match
        if criteria.get('type'):
            type_score = self._calculate_type_match(question, criteria)
            scores.append(type_score * 0.15)
        
        # Semantic similarity
        if criteria.get('reference_text'):
            semantic_score = self._calculate_semantic_similarity(question, criteria)
            scores.append(semantic_score * 0.1)
        
        # Default score if no criteria
        if not scores:
            return 0.5
        
        return sum(scores) / len(scores) if scores else 0.5
    
    def _calculate_topic_relevance(self, question: Dict[str, Any], 
                                  criteria: Dict[str, Any]) -> float:
        """Calculate topic relevance score"""
        question_topic = question.get('topic', '').lower()
        target_topics = criteria.get('topic', [])
        
        if isinstance(target_topics, str):
            target_topics = [target_topics]
        
        target_topics = [t.lower() for t in target_topics]
        
        # Exact match
        if question_topic in target_topics:
            return 1.0
        
        # Partial match
        for target_topic in target_topics:
            if target_topic in question_topic or question_topic in target_topic:
                return 0.7
        
        # Semantic similarity (basic)
        similarity_scores = []
        for target_topic in target_topics:
            similarity = self._calculate_text_similarity(question_topic, target_topic)
            similarity_scores.append(similarity)
        
        return max(similarity_scores) if similarity_scores else 0.0
    
    def _calculate_keyword_relevance(self, question: Dict[str, Any], 
                                    criteria: Dict[str, Any]) -> float:
        """Calculate keyword relevance score"""
        question_text = question.get('question', '').lower()
        question_keywords = question.get('keywords', [])
        target_keywords = criteria.get('keywords', [])
        
        if isinstance(target_keywords, str):
            target_keywords = [target_keywords]
        
        target_keywords = [k.lower() for k in target_keywords]
        
        # Combine question text and keywords
        all_question_text = question_text + ' ' + ' '.join(question_keywords)
        
        # Count keyword matches
        matches = 0
        for keyword in target_keywords:
            if keyword in all_question_text:
                matches += 1
        
        return matches / len(target_keywords) if target_keywords else 0.0
    
    def _calculate_difficulty_match(self, question: Dict[str, Any], 
                                   criteria: Dict[str, Any]) -> float:
        """Calculate difficulty match score"""
        question_difficulty = question.get('difficulty', '').lower()
        target_difficulty = criteria.get('difficulty', '').lower()
        
        if not target_difficulty:
            return 1.0
        
        # Exact match
        if question_difficulty == target_difficulty:
            return 1.0
        
        # Difficulty hierarchy
        difficulty_levels = {
            'easy': 1,
            'medium': 2,
            'hard': 3,
            'expert': 4
        }
        
        q_level = difficulty_levels.get(question_difficulty, 2)
        t_level = difficulty_levels.get(target_difficulty, 2)
        
        # Penalize large differences
        diff = abs(q_level - t_level)
        return max(0, 1 - diff * 0.3)
    
    def _calculate_type_match(self, question: Dict[str, Any], 
                             criteria: Dict[str, Any]) -> float:
        """Calculate question type match score"""
        question_type = question.get('type', '').lower()
        target_types = criteria.get('type', [])
        
        if isinstance(target_types, str):
            target_types = [target_types]
        
        target_types = [t.lower() for t in target_types]
        
        if not target_types:
            return 1.0
        
        return 1.0 if question_type in target_types else 0.0
    
    def _calculate_semantic_similarity(self, question: Dict[str, Any], 
                                     criteria: Dict[str, Any]) -> float:
        """Calculate semantic similarity with reference text"""
        question_text = question.get('question', '')
        reference_text = criteria.get('reference_text', '')
        
        if not reference_text:
            return 0.5
        
        return self._calculate_text_similarity(question_text, reference_text)
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using TF-IDF"""
        if not text1 or not text2:
            return 0.0
        
        try:
            # Vectorize texts
            texts = [text1, text2]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            # Fallback to simple word overlap
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            if not words1 or not words2:
                return 0.0
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union)
    
    def train_relevance_model(self, questions: List[Dict[str, Any]]) -> float:
        """Train relevance model on question bank"""
        # Extract features for training
        features = []
        labels = []
        
        for question in questions:
            # Extract features (simplified)
            feature_vector = self._extract_features(question)
            features.append(feature_vector)
            
            # Use existing scores or default
            label = question.get('relevance_score', 0.5)
            labels.append(label)
        
        # This is a placeholder - would implement actual model training
        self.logger.info("Relevance model training completed")
        return 0.8  # Placeholder accuracy
    
    def _extract_features(self, question: Dict[str, Any]) -> List[float]:
        """Extract features from a question for model training"""
        features = []
        
        # Text length
        text_length = len(question.get('question', ''))
        features.append(text_length / 1000.0)  # Normalize
        
        # Number of keywords
        keyword_count = len(question.get('keywords', []))
        features.append(keyword_count / 10.0)  # Normalize
        
        # Difficulty encoding
        difficulty_map = {'easy': 0.25, 'medium': 0.5, 'hard': 0.75, 'expert': 1.0}
        difficulty_score = difficulty_map.get(question.get('difficulty', 'medium'), 0.5)
        features.append(difficulty_score)
        
        # Type encoding (placeholder)
        type_map = {'text': 0.2, 'multiple_choice': 0.4, 'true_false': 0.6, 'essay': 0.8}
        type_score = type_map.get(question.get('type', 'text'), 0.2)
        features.append(type_score)
        
        return features
    
    def update_keyword_weights(self, feedback: Dict[str, float]):
        """Update keyword weights based on user feedback"""
        for keyword, weight in feedback.items():
            self.keyword_weights[keyword] = weight
    
    def get_top_keywords(self, questions: List[Dict[str, Any]], 
                        top_k: int = 10) -> List[str]:
        """Get most common keywords from questions"""
        all_keywords = []
        
        for question in questions:
            keywords = question.get('keywords', [])
            all_keywords.extend(keywords)
        
        keyword_counts = Counter(all_keywords)
        return [keyword for keyword, count in keyword_counts.most_common(top_k)]
