"""
Model Trainer Module

Provides utilities for training and evaluating AI models used in the question selection system.
Handles model training, validation, and performance evaluation.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import joblib
import logging
from pathlib import Path
import yaml


class ModelTrainer:
    """Handles training and evaluation of AI models"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self.models = {}
        self.vectorizers = {}
        self.training_history = {}
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file not found: {config_path}")
            return {}
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}
    
    def train_topic_classifier(self, questions: List[Dict[str, Any]], 
                             model_type: str = "logistic_regression") -> Dict[str, Any]:
        """
        Train topic classification model
        
        Args:
            questions: List of question dictionaries
            model_type: Type of model to train
            
        Returns:
            Training results and metrics
        """
        # Prepare training data
        texts = []
        labels = []
        
        for q in questions:
            if 'topic' in q and q['topic'] and 'question' in q and q['question']:
                texts.append(q['question'])
                labels.append(q['topic'])
        
        if len(texts) < 10:
            raise ValueError("Insufficient training data for topic classification")
        
        # Create pipeline
        pipeline = self._create_pipeline(model_type, 'topic')
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Train model
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(pipeline, texts, labels, cv=5, scoring='accuracy')
        
        # Store model
        self.models['topic'] = pipeline
        
        # Training results
        results = {
            'model_type': model_type,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'classes': len(set(labels)),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        self.training_history['topic'] = results
        self.logger.info(f"Topic classifier trained: {accuracy:.3f} accuracy")
        
        return results
    
    def train_difficulty_classifier(self, questions: List[Dict[str, Any]], 
                                  model_type: str = "random_forest") -> Dict[str, Any]:
        """Train difficulty classification model"""
        # Prepare training data
        texts = []
        labels = []
        
        for q in questions:
            if 'difficulty' in q and q['difficulty'] and 'question' in q and q['question']:
                texts.append(q['question'])
                labels.append(q['difficulty'])
        
        if len(texts) < 10:
            raise ValueError("Insufficient training data for difficulty classification")
        
        # Create pipeline
        pipeline = self._create_pipeline(model_type, 'difficulty')
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Train model
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(pipeline, texts, labels, cv=5, scoring='accuracy')
        
        # Store model
        self.models['difficulty'] = pipeline
        
        # Training results
        results = {
            'model_type': model_type,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'classes': len(set(labels)),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        self.training_history['difficulty'] = results
        self.logger.info(f"Difficulty classifier trained: {accuracy:.3f} accuracy")
        
        return results
    
    def train_type_classifier(self, questions: List[Dict[str, Any]], 
                            model_type: str = "naive_bayes") -> Dict[str, Any]:
        """Train question type classification model"""
        # Prepare training data
        texts = []
        labels = []
        
        for q in questions:
            if 'type' in q and q['type'] and 'question' in q and q['question']:
                texts.append(q['question'])
                labels.append(q['type'])
        
        if len(texts) < 10:
            raise ValueError("Insufficient training data for type classification")
        
        # Create pipeline
        pipeline = self._create_pipeline(model_type, 'type')
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        # Train model
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(pipeline, texts, labels, cv=5, scoring='accuracy')
        
        # Store model
        self.models['type'] = pipeline
        
        # Training results
        results = {
            'model_type': model_type,
            'accuracy': accuracy,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'classes': len(set(labels)),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
        
        self.training_history['type'] = results
        self.logger.info(f"Type classifier trained: {accuracy:.3f} accuracy")
        
        return results
    
    def _create_pipeline(self, model_type: str, task: str) -> Pipeline:
        """Create ML pipeline for given model type and task"""
        # Get configuration
        config = self.config.get('ai_models', {}).get(f'{task}_classifier', {})
        
        # Create vectorizer
        vectorizer_params = {
            'max_features': config.get('max_features', 5000),
            'stop_words': 'english',
            'ngram_range': tuple(config.get('ngram_range', [1, 2]))
        }
        vectorizer = TfidfVectorizer(**vectorizer_params)
        
        # Create model
        if model_type == "logistic_regression":
            model = LogisticRegression(
                max_iter=1000,
                random_state=42,
                class_weight='balanced'
            )
        elif model_type == "random_forest":
            model = RandomForestClassifier(
                n_estimators=config.get('n_estimators', 100),
                random_state=42,
                class_weight='balanced'
            )
        elif model_type == "naive_bayes":
            model = MultinomialNB(alpha=0.1)
        elif model_type == "svm":
            model = SVC(
                kernel='rbf',
                random_state=42,
                class_weight='balanced',
                probability=True
            )
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return Pipeline([
            ('vectorizer', vectorizer),
            ('classifier', model)
        ])
    
    def hyperparameter_tuning(self, questions: List[Dict[str, Any]], 
                            task: str, model_type: str) -> Dict[str, Any]:
        """Perform hyperparameter tuning for a model"""
        # Prepare data
        texts = []
        labels = []
        
        for q in questions:
            if task in q and q[task] and 'question' in q and q['question']:
                texts.append(q['question'])
                labels.append(q[task])
        
        if len(texts) < 50:
            raise ValueError("Insufficient data for hyperparameter tuning")
        
        # Create base pipeline
        pipeline = self._create_pipeline(model_type, task)
        
        # Define parameter grid
        param_grid = self._get_param_grid(model_type)
        
        # Perform grid search
        grid_search = GridSearchCV(
            pipeline,
            param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(texts, labels)
        
        # Results
        results = {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }
        
        # Store best model
        self.models[task] = grid_search.best_estimator_
        
        self.logger.info(f"Hyperparameter tuning completed for {task}: {grid_search.best_score_:.3f}")
        
        return results
    
    def _get_param_grid(self, model_type: str) -> Dict[str, List]:
        """Get parameter grid for hyperparameter tuning"""
        if model_type == "logistic_regression":
            return {
                'vectorizer__max_features': [3000, 5000, 10000],
                'vectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'classifier__C': [0.1, 1, 10],
                'classifier__solver': ['liblinear', 'lbfgs']
            }
        elif model_type == "random_forest":
            return {
                'vectorizer__max_features': [3000, 5000, 10000],
                'vectorizer__ngram_range': [(1, 1), (1, 2)],
                'classifier__n_estimators': [50, 100, 200],
                'classifier__max_depth': [None, 10, 20]
            }
        elif model_type == "naive_bayes":
            return {
                'vectorizer__max_features': [3000, 5000, 10000],
                'vectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
                'classifier__alpha': [0.1, 0.5, 1.0, 2.0]
            }
        elif model_type == "svm":
            return {
                'vectorizer__max_features': [3000, 5000],
                'vectorizer__ngram_range': [(1, 1), (1, 2)],
                'classifier__C': [0.1, 1, 10],
                'classifier__gamma': ['scale', 'auto']
            }
        else:
            return {}
    
    def evaluate_model(self, model_name: str, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate a trained model on new data"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        model = self.models[model_name]
        
        # Prepare test data
        texts = []
        labels = []
        
        for q in questions:
            if model_name in q and q[model_name] and 'question' in q and q['question']:
                texts.append(q['question'])
                labels.append(q[model_name])
        
        if not texts:
            raise ValueError("No test data available")
        
        # Predict
        predictions = model.predict(texts)
        probabilities = model.predict_proba(texts)
        
        # Calculate metrics
        accuracy = accuracy_score(labels, predictions)
        report = classification_report(labels, predictions, output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(labels, predictions)
        
        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'predictions': predictions.tolist(),
            'probabilities': probabilities.tolist(),
            'test_samples': len(texts)
        }
    
    def save_models(self, model_dir: str = "data/models"):
        """Save trained models to disk"""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)
        
        for model_name, model in self.models.items():
            model_path = model_dir / f"{model_name}_model.pkl"
            joblib.dump(model, model_path)
            self.logger.info(f"Saved {model_name} model to {model_path}")
        
        # Save training history
        history_path = model_dir / "training_history.json"
        import json
        with open(history_path, 'w') as f:
            json.dump(self.training_history, f, indent=2)
    
    def load_models(self, model_dir: str = "data/models"):
        """Load trained models from disk"""
        model_dir = Path(model_dir)
        
        for model_file in model_dir.glob("*_model.pkl"):
            model_name = model_file.stem.replace('_model', '')
            try:
                model = joblib.load(model_file)
                self.models[model_name] = model
                self.logger.info(f"Loaded {model_name} model from {model_file}")
            except Exception as e:
                self.logger.error(f"Error loading {model_name} model: {str(e)}")
        
        # Load training history
        history_path = model_dir / "training_history.json"
        if history_path.exists():
            try:
                import json
                with open(history_path, 'r') as f:
                    self.training_history = json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading training history: {str(e)}")
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get summary of training results"""
        summary = {
            'models_trained': len(self.models),
            'training_history': self.training_history
        }
        
        for model_name, history in self.training_history.items():
            summary[f'{model_name}_accuracy'] = history.get('accuracy', 0)
            summary[f'{model_name}_cv_mean'] = history.get('cv_mean', 0)
        
        return summary
    
    def compare_models(self, questions: List[Dict[str, Any]], task: str) -> Dict[str, Any]:
        """Compare different model types for a given task"""
        model_types = ["logistic_regression", "random_forest", "naive_bayes", "svm"]
        results = {}
        
        for model_type in model_types:
            try:
                if task == 'topic':
                    result = self.train_topic_classifier(questions, model_type)
                elif task == 'difficulty':
                    result = self.train_difficulty_classifier(questions, model_type)
                elif task == 'type':
                    result = self.train_type_classifier(questions, model_type)
                else:
                    continue
                
                results[model_type] = result
            except Exception as e:
                self.logger.error(f"Error training {model_type} for {task}: {str(e)}")
                results[model_type] = {'error': str(e)}
        
        return results
