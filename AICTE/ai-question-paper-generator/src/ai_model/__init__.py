"""
Question Classifier Module

AI-powered question classification system that categorizes questions by topic,
difficulty, type, and other attributes using machine learning models.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sentence_transformers import SentenceTransformer
import joblib
import logging
from pathlib import Path


class QuestionClassifier:
    """AI model for classifying questions by various attributes"""
    
    def __init__(self, model_dir: str = "data/models"):
        self.logger = logging.getLogger(__name__)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize models
        self.topic_model = None
        self.difficulty_model = None
        self.type_model = None
        
        # Initialize vectorizers
        self.topic_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.difficulty_vectorizer = TfidfVectorizer(
            max_features=3000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.type_vectorizer = TfidfVectorizer(
            max_features=2000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Sentence transformer for semantic similarity
        self.sentence_model = None
        self._load_sentence_model()
        
        # Load pre-trained models if available
        self._load_models()
    
    def _load_sentence_model(self):
        """Load sentence transformer model"""
        try:
            self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.logger.info("Sentence transformer model loaded successfully")
        except Exception as e:
            self.logger.warning(f"Failed to load sentence transformer: {e}")
    
    def _load_models(self):
        """Load pre-trained models from disk"""
        try:
            topic_model_path = self.model_dir / "topic_model.pkl"
            difficulty_model_path = self.model_dir / "difficulty_model.pkl"
            type_model_path = self.model_dir / "type_model.pkl"
            
            topic_vectorizer_path = self.model_dir / "topic_vectorizer.pkl"
            difficulty_vectorizer_path = self.model_dir / "difficulty_vectorizer.pkl"
            type_vectorizer_path = self.model_dir / "type_vectorizer.pkl"
            
            if topic_model_path.exists():
                self.topic_model = joblib.load(topic_model_path)
                self.topic_vectorizer = joblib.load(topic_vectorizer_path)
                self.logger.info("Topic classification model loaded")
            
            if difficulty_model_path.exists():
                self.difficulty_model = joblib.load(difficulty_model_path)
                self.difficulty_vectorizer = joblib.load(difficulty_vectorizer_path)
                self.logger.info("Difficulty classification model loaded")
            
            if type_model_path.exists():
                self.type_model = joblib.load(type_model_path)
                self.type_vectorizer = joblib.load(type_vectorizer_path)
                self.logger.info("Type classification model loaded")
                
        except Exception as e:
            self.logger.warning(f"Failed to load pre-trained models: {e}")
    
    def train_topic_classifier(self, questions: List[Dict[str, Any]]) -> float:
        """Train topic classification model"""
        # Prepare training data
        texts = [q['question'] for q in questions if 'topic' in q and q['topic']]
        labels = [q['topic'] for q in questions if 'topic' in q and q['topic']]
        
        if len(texts) < 10:
            self.logger.warning("Insufficient training data for topic classification")
            return 0.0
        
        # Vectorize text
        X = self.topic_vectorizer.fit_transform(texts)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.topic_model = LogisticRegression(max_iter=1000)
        self.topic_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.topic_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.logger.info(f"Topic classifier trained with accuracy: {accuracy:.3f}")
        
        # Save model
        joblib.dump(self.topic_model, self.model_dir / "topic_model.pkl")
        joblib.dump(self.topic_vectorizer, self.model_dir / "topic_vectorizer.pkl")
        
        return accuracy
    
    def train_difficulty_classifier(self, questions: List[Dict[str, Any]]) -> float:
        """Train difficulty classification model"""
        # Prepare training data
        texts = [q['question'] for q in questions if 'difficulty' in q and q['difficulty']]
        labels = [q['difficulty'] for q in questions if 'difficulty' in q and q['difficulty']]
        
        if len(texts) < 10:
            self.logger.warning("Insufficient training data for difficulty classification")
            return 0.0
        
        # Vectorize text
        X = self.difficulty_vectorizer.fit_transform(texts)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.difficulty_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.difficulty_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.difficulty_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.logger.info(f"Difficulty classifier trained with accuracy: {accuracy:.3f}")
        
        # Save model
        joblib.dump(self.difficulty_model, self.model_dir / "difficulty_model.pkl")
        joblib.dump(self.difficulty_vectorizer, self.model_dir / "difficulty_vectorizer.pkl")
        
        return accuracy
    
    def train_type_classifier(self, questions: List[Dict[str, Any]]) -> float:
        """Train question type classification model"""
        # Prepare training data
        texts = [q['question'] for q in questions if 'type' in q and q['type']]
        labels = [q['type'] for q in questions if 'type' in q and q['type']]
        
        if len(texts) < 10:
            self.logger.warning("Insufficient training data for type classification")
            return 0.0
        
        # Vectorize text
        X = self.type_vectorizer.fit_transform(texts)
        y = np.array(labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.type_model = MultinomialNB()
        self.type_model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.type_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.logger.info(f"Type classifier trained with accuracy: {accuracy:.3f}")
        
        # Save model
        joblib.dump(self.type_model, self.model_dir / "type_model.pkl")
        joblib.dump(self.type_vectorizer, self.model_dir / "type_vectorizer.pkl")
        
        return accuracy
    
    def predict_topic(self, question: str) -> Tuple[str, float]:
        """Predict topic of a question"""
        if not self.topic_model:
            return "general", 0.5
        
        try:
            X = self.topic_vectorizer.transform([question])
            prediction = self.topic_model.predict(X)[0]
            probability = self.topic_model.predict_proba(X)[0].max()
            
            return prediction, probability
        except Exception as e:
            self.logger.error(f"Error predicting topic: {e}")
            return "general", 0.5
    
    def predict_difficulty(self, question: str) -> Tuple[str, float]:
        """Predict difficulty of a question"""
        if not self.difficulty_model:
            return "medium", 0.5
        
        try:
            X = self.difficulty_vectorizer.transform([question])
            prediction = self.difficulty_model.predict(X)[0]
            probability = self.difficulty_model.predict_proba(X)[0].max()
            
            return prediction, probability
        except Exception as e:
            self.logger.error(f"Error predicting difficulty: {e}")
            return "medium", 0.5
    
    def predict_type(self, question: str) -> Tuple[str, float]:
        """Predict type of a question"""
        if not self.type_model:
            return "text", 0.5
        
        try:
            X = self.type_vectorizer.transform([question])
            prediction = self.type_model.predict(X)[0]
            probability = self.type_model.predict_proba(X)[0].max()
            
            return prediction, probability
        except Exception as e:
            self.logger.error(f"Error predicting type: {e}")
            return "text", 0.5
    
    def classify_question(self, question: str) -> Dict[str, Any]:
        """Classify a question across all attributes"""
        topic, topic_confidence = self.predict_topic(question)
        difficulty, difficulty_confidence = self.predict_difficulty(question)
        question_type, type_confidence = self.predict_type(question)
        
        return {
            'topic': topic,
            'topic_confidence': topic_confidence,
            'difficulty': difficulty,
            'difficulty_confidence': difficulty_confidence,
            'type': question_type,
            'type_confidence': type_confidence
        }
    
    def get_semantic_similarity(self, question1: str, question2: str) -> float:
        """Get semantic similarity between two questions"""
        if not self.sentence_model:
            return 0.0
        
        try:
            embeddings = self.sentence_model.encode([question1, question2])
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(similarity)
        except Exception as e:
            self.logger.error(f"Error computing semantic similarity: {e}")
            return 0.0
    
    def find_similar_questions(self, target_question: str, 
                             question_bank: List[Dict[str, Any]], 
                             top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """Find similar questions in the question bank"""
        if not self.sentence_model:
            return []
        
        try:
            # Get embedding for target question
            target_embedding = self.sentence_model.encode([target_question])
            
            # Get embeddings for all questions in bank
            bank_texts = [q['question'] for q in question_bank]
            bank_embeddings = self.sentence_model.encode(bank_texts)
            
            # Calculate similarities
            similarities = []
            for i, q in enumerate(question_bank):
                similarity = np.dot(target_embedding[0], bank_embeddings[i]) / (
                    np.linalg.norm(target_embedding[0]) * np.linalg.norm(bank_embeddings[i])
                )
                similarities.append((q, float(similarity)))
            
            # Sort by similarity and return top k
            similarities.sort(key=lambda x: x[1], reverse=True)
            return similarities[:top_k]
            
        except Exception as e:
            self.logger.error(f"Error finding similar questions: {e}")
            return []
