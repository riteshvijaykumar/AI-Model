"""
Question Selector Module

Main logic for selecting questions based on user criteria and AI recommendations.
Combines filtering, scoring, and AI-powered selection to create optimal question sets.
"""

import random
import numpy as np
from typing import List, Dict, Any, Optional, Set
from collections import defaultdict
import logging

from ..ai_model.question_classifier import QuestionClassifier
from ..ai_model.relevance_scorer import RelevanceScorer
from .filter_manager import FilterManager
from .criteria_parser import CriteriaParser


class QuestionSelector:
    """Main question selection engine"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        
        # Initialize components
        self.classifier = QuestionClassifier()
        self.scorer = RelevanceScorer()
        self.filter_manager = FilterManager()
        self.criteria_parser = CriteriaParser()
        
        # Question bank storage
        self.questions = []
        self.question_index = {}
        
        # Selection parameters
        self.default_count = 20
        self.diversity_factor = 0.3
        self.relevance_threshold = 0.5
        
    def load_questions(self, questions: List[Dict[str, Any]]):
        """Load questions into the selector"""
        self.questions = questions
        self.question_index = {q['id']: q for q in questions}
        
        # Classify questions if needed
        self._classify_questions()
        
        self.logger.info(f"Loaded {len(questions)} questions")
    
    def _classify_questions(self):
        """Classify questions that don't have complete metadata"""
        for question in self.questions:
            if not question.get('topic') or not question.get('difficulty'):
                classification = self.classifier.classify_question(question['question'])
                
                if not question.get('topic'):
                    question['topic'] = classification['topic']
                    question['topic_confidence'] = classification['topic_confidence']
                
                if not question.get('difficulty'):
                    question['difficulty'] = classification['difficulty']
                    question['difficulty_confidence'] = classification['difficulty_confidence']
                
                if not question.get('type'):
                    question['type'] = classification['type']
                    question['type_confidence'] = classification['type_confidence']
    
    def select_questions(self, **criteria) -> List[Dict[str, Any]]:
        """
        Select questions based on criteria
        
        Args:
            **criteria: Selection criteria (topic, difficulty, type, count, etc.)
        
        Returns:
            List of selected questions
        """
        # Parse and validate criteria
        parsed_criteria = self.criteria_parser.parse_criteria(criteria)
        
        # Apply filters
        filtered_questions = self.filter_manager.apply_filters(
            self.questions, parsed_criteria
        )
        
        if not filtered_questions:
            self.logger.warning("No questions match the specified criteria")
            return []
        
        # Score questions
        scored_questions = self.scorer.score_questions(
            filtered_questions, parsed_criteria
        )
        
        # Select final set
        selected_questions = self._select_final_set(
            scored_questions, parsed_criteria
        )
        
        self.logger.info(f"Selected {len(selected_questions)} questions")
        return selected_questions
    
    def _select_final_set(self, scored_questions: List[Dict[str, Any]], 
                         criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Select final set of questions with diversity and relevance"""
        target_count = criteria.get('count', self.default_count)
        
        if len(scored_questions) <= target_count:
            return scored_questions
        
        # Sort by relevance score
        scored_questions.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        # Apply diversity selection
        if criteria.get('diversity', True):
            return self._diverse_selection(scored_questions, target_count)
        else:
            return scored_questions[:target_count]
    
    def _diverse_selection(self, scored_questions: List[Dict[str, Any]], 
                          target_count: int) -> List[Dict[str, Any]]:
        """Select diverse set of questions"""
        selected = []
        remaining = scored_questions.copy()
        
        # Track diversity metrics
        topic_counts = defaultdict(int)
        difficulty_counts = defaultdict(int)
        type_counts = defaultdict(int)
        
        while len(selected) < target_count and remaining:
            best_question = None
            best_score = -1
            
            for question in remaining:
                # Calculate diversity bonus
                diversity_bonus = self._calculate_diversity_bonus(
                    question, topic_counts, difficulty_counts, type_counts
                )
                
                # Combined score
                total_score = (
                    question.get('relevance_score', 0) * (1 - self.diversity_factor) +
                    diversity_bonus * self.diversity_factor
                )
                
                if total_score > best_score:
                    best_score = total_score
                    best_question = question
            
            if best_question:
                selected.append(best_question)
                remaining.remove(best_question)
                
                # Update counts
                topic_counts[best_question.get('topic', '')] += 1
                difficulty_counts[best_question.get('difficulty', '')] += 1
                type_counts[best_question.get('type', '')] += 1
        
        return selected
    
    def _calculate_diversity_bonus(self, question: Dict[str, Any],
                                  topic_counts: Dict[str, int],
                                  difficulty_counts: Dict[str, int],
                                  type_counts: Dict[str, int]) -> float:
        """Calculate diversity bonus for a question"""
        topic = question.get('topic', '')
        difficulty = question.get('difficulty', '')
        q_type = question.get('type', '')
        
        # Lower counts get higher bonuses
        topic_bonus = 1.0 / (topic_counts.get(topic, 0) + 1)
        difficulty_bonus = 1.0 / (difficulty_counts.get(difficulty, 0) + 1)
        type_bonus = 1.0 / (type_counts.get(q_type, 0) + 1)
        
        return (topic_bonus + difficulty_bonus + type_bonus) / 3.0
    
    def get_question_recommendations(self, target_question: str, 
                                   count: int = 10) -> List[Dict[str, Any]]:
        """Get similar questions based on semantic similarity"""
        similar_questions = self.classifier.find_similar_questions(
            target_question, self.questions, count
        )
        
        return [q for q, similarity in similar_questions]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the question bank"""
        if not self.questions:
            return {}
        
        stats = {
            'total_questions': len(self.questions),
            'topics': defaultdict(int),
            'difficulties': defaultdict(int),
            'types': defaultdict(int)
        }
        
        for question in self.questions:
            stats['topics'][question.get('topic', 'unknown')] += 1
            stats['difficulties'][question.get('difficulty', 'unknown')] += 1
            stats['types'][question.get('type', 'unknown')] += 1
        
        return stats
    
    def train_models(self) -> Dict[str, float]:
        """Train AI models on current question bank"""
        if not self.questions:
            return {}
        
        results = {}
        
        # Train classifiers
        if len(self.questions) >= 50:
            results['topic_accuracy'] = self.classifier.train_topic_classifier(self.questions)
            results['difficulty_accuracy'] = self.classifier.train_difficulty_classifier(self.questions)
            results['type_accuracy'] = self.classifier.train_type_classifier(self.questions)
        
        # Train relevance scorer
        if len(self.questions) >= 100:
            results['relevance_score'] = self.scorer.train_relevance_model(self.questions)
        
        return results
    
    def export_selected_questions(self, questions: List[Dict[str, Any]], 
                                 output_path: str):
        """Export selected questions to file"""
        from ..export.spreadsheet_generator import SpreadsheetGenerator
        
        generator = SpreadsheetGenerator()
        generator.generate_spreadsheet(questions, output_path)
    
    def save_selection_criteria(self, criteria: Dict[str, Any], name: str):
        """Save selection criteria for reuse"""
        # Implementation would save to config file
        pass
    
    def load_selection_criteria(self, name: str) -> Dict[str, Any]:
        """Load saved selection criteria"""
        # Implementation would load from config file
        return {}
