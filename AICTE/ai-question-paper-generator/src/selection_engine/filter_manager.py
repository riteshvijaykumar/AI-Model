"""
Filter Manager Module

Manages various filtering operations on question banks based on user criteria.
Supports filtering by topic, difficulty, type, keywords, and custom filters.
"""

import re
from typing import List, Dict, Any, Optional, Callable
from collections import defaultdict
import logging


class FilterManager:
    """Manages filtering operations on question banks"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.custom_filters = {}
        
    def apply_filters(self, questions: List[Dict[str, Any]], 
                     criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply all filters based on criteria"""
        filtered_questions = questions.copy()
        
        # Apply individual filters
        if criteria.get('topic'):
            filtered_questions = self.filter_by_topic(filtered_questions, criteria['topic'])
        
        if criteria.get('difficulty'):
            filtered_questions = self.filter_by_difficulty(filtered_questions, criteria['difficulty'])
        
        if criteria.get('type'):
            filtered_questions = self.filter_by_type(filtered_questions, criteria['type'])
        
        if criteria.get('keywords'):
            filtered_questions = self.filter_by_keywords(filtered_questions, criteria['keywords'])
        
        if criteria.get('text_contains'):
            filtered_questions = self.filter_by_text_content(filtered_questions, criteria['text_contains'])
        
        if criteria.get('exclude_keywords'):
            filtered_questions = self.filter_exclude_keywords(filtered_questions, criteria['exclude_keywords'])
        
        if criteria.get('min_length'):
            filtered_questions = self.filter_by_min_length(filtered_questions, criteria['min_length'])
        
        if criteria.get('max_length'):
            filtered_questions = self.filter_by_max_length(filtered_questions, criteria['max_length'])
        
        # Apply custom filters
        for filter_name, filter_value in criteria.items():
            if filter_name in self.custom_filters:
                filtered_questions = self.custom_filters[filter_name](filtered_questions, filter_value)
        
        self.logger.info(f"Filtered {len(questions)} questions to {len(filtered_questions)}")
        return filtered_questions
    
    def filter_by_topic(self, questions: List[Dict[str, Any]], 
                       topics: List[str]) -> List[Dict[str, Any]]:
        """Filter questions by topic"""
        if isinstance(topics, str):
            topics = [topics]
        
        topics = [t.lower() for t in topics]
        
        filtered = []
        for question in questions:
            question_topic = question.get('topic', '').lower()
            if any(topic in question_topic or question_topic in topic for topic in topics):
                filtered.append(question)
        
        return filtered
    
    def filter_by_difficulty(self, questions: List[Dict[str, Any]], 
                           difficulties: List[str]) -> List[Dict[str, Any]]:
        """Filter questions by difficulty level"""
        if isinstance(difficulties, str):
            difficulties = [difficulties]
        
        difficulties = [d.lower() for d in difficulties]
        
        filtered = []
        for question in questions:
            question_difficulty = question.get('difficulty', '').lower()
            if question_difficulty in difficulties:
                filtered.append(question)
        
        return filtered
    
    def filter_by_type(self, questions: List[Dict[str, Any]], 
                      types: List[str]) -> List[Dict[str, Any]]:
        """Filter questions by type"""
        if isinstance(types, str):
            types = [types]
        
        types = [t.lower() for t in types]
        
        filtered = []
        for question in questions:
            question_type = question.get('type', '').lower()
            if question_type in types:
                filtered.append(question)
        
        return filtered
    
    def filter_by_keywords(self, questions: List[Dict[str, Any]], 
                          keywords: List[str]) -> List[Dict[str, Any]]:
        """Filter questions by keywords"""
        if isinstance(keywords, str):
            keywords = [keywords]
        
        keywords = [k.lower() for k in keywords]
        
        filtered = []
        for question in questions:
            question_text = question.get('question', '').lower()
            question_keywords = [k.lower() for k in question.get('keywords', [])]
            
            # Check if any keyword matches
            for keyword in keywords:
                if (keyword in question_text or 
                    any(keyword in qk for qk in question_keywords)):
                    filtered.append(question)
                    break
        
        return filtered
    
    def filter_by_text_content(self, questions: List[Dict[str, Any]], 
                              text_pattern: str) -> List[Dict[str, Any]]:
        """Filter questions by text content (supports regex)"""
        try:
            pattern = re.compile(text_pattern, re.IGNORECASE)
            filtered = []
            
            for question in questions:
                question_text = question.get('question', '')
                if pattern.search(question_text):
                    filtered.append(question)
            
            return filtered
        except re.error:
            # Fallback to simple string matching
            text_pattern = text_pattern.lower()
            return [q for q in questions if text_pattern in q.get('question', '').lower()]
    
    def filter_exclude_keywords(self, questions: List[Dict[str, Any]], 
                               exclude_keywords: List[str]) -> List[Dict[str, Any]]:
        """Filter out questions containing specific keywords"""
        if isinstance(exclude_keywords, str):
            exclude_keywords = [exclude_keywords]
        
        exclude_keywords = [k.lower() for k in exclude_keywords]
        
        filtered = []
        for question in questions:
            question_text = question.get('question', '').lower()
            question_keywords = [k.lower() for k in question.get('keywords', [])]
            
            # Check if any exclude keyword matches
            exclude = False
            for keyword in exclude_keywords:
                if (keyword in question_text or 
                    any(keyword in qk for qk in question_keywords)):
                    exclude = True
                    break
            
            if not exclude:
                filtered.append(question)
        
        return filtered
    
    def filter_by_min_length(self, questions: List[Dict[str, Any]], 
                            min_length: int) -> List[Dict[str, Any]]:
        """Filter questions by minimum text length"""
        return [q for q in questions if len(q.get('question', '')) >= min_length]
    
    def filter_by_max_length(self, questions: List[Dict[str, Any]], 
                            max_length: int) -> List[Dict[str, Any]]:
        """Filter questions by maximum text length"""
        return [q for q in questions if len(q.get('question', '')) <= max_length]
    
    def filter_by_date_range(self, questions: List[Dict[str, Any]], 
                            start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Filter questions by date range (if date metadata exists)"""
        from datetime import datetime
        
        try:
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            filtered = []
            for question in questions:
                if 'created_date' in question:
                    question_date = datetime.fromisoformat(question['created_date'])
                    if start_dt <= question_date <= end_dt:
                        filtered.append(question)
            
            return filtered
        except ValueError:
            self.logger.warning("Invalid date format for date range filter")
            return questions
    
    def filter_by_custom_field(self, questions: List[Dict[str, Any]], 
                              field_name: str, field_value: Any) -> List[Dict[str, Any]]:
        """Filter questions by custom field value"""
        return [q for q in questions if q.get(field_name) == field_value]
    
    def filter_by_similarity_threshold(self, questions: List[Dict[str, Any]], 
                                     reference_question: str, 
                                     threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Filter questions by similarity to reference question"""
        from ..ai_model.question_classifier import QuestionClassifier
        
        classifier = QuestionClassifier()
        if not classifier.sentence_model:
            self.logger.warning("Sentence model not available for similarity filtering")
            return questions
        
        filtered = []
        for question in questions:
            similarity = classifier.get_semantic_similarity(
                reference_question, question.get('question', '')
            )
            if similarity >= threshold:
                filtered.append(question)
        
        return filtered
    
    def add_custom_filter(self, name: str, filter_func: Callable):
        """Add a custom filter function"""
        self.custom_filters[name] = filter_func
        self.logger.info(f"Added custom filter: {name}")
    
    def remove_custom_filter(self, name: str):
        """Remove a custom filter"""
        if name in self.custom_filters:
            del self.custom_filters[name]
            self.logger.info(f"Removed custom filter: {name}")
    
    def get_filter_statistics(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about filterable fields"""
        stats = {
            'total_questions': len(questions),
            'topics': defaultdict(int),
            'difficulties': defaultdict(int),
            'types': defaultdict(int),
            'length_stats': {
                'min': float('inf'),
                'max': 0,
                'avg': 0
            }
        }
        
        total_length = 0
        for question in questions:
            # Count topics
            topic = question.get('topic', 'unknown')
            stats['topics'][topic] += 1
            
            # Count difficulties
            difficulty = question.get('difficulty', 'unknown')
            stats['difficulties'][difficulty] += 1
            
            # Count types
            q_type = question.get('type', 'unknown')
            stats['types'][q_type] += 1
            
            # Length statistics
            length = len(question.get('question', ''))
            total_length += length
            stats['length_stats']['min'] = min(stats['length_stats']['min'], length)
            stats['length_stats']['max'] = max(stats['length_stats']['max'], length)
        
        if questions:
            stats['length_stats']['avg'] = total_length / len(questions)
        
        return stats
    
    def suggest_filters(self, questions: List[Dict[str, Any]], 
                       target_count: int) -> Dict[str, Any]:
        """Suggest filter combinations to reach target count"""
        stats = self.get_filter_statistics(questions)
        suggestions = {}
        
        current_count = len(questions)
        
        if current_count <= target_count:
            return {'message': 'No filtering needed'}
        
        # Calculate reduction ratio needed
        reduction_ratio = target_count / current_count
        
        # Suggest topic filters
        for topic, count in stats['topics'].items():
            if count >= target_count * 0.8:  # If topic has enough questions
                suggestions[f'topic_{topic}'] = {
                    'filter': {'topic': topic},
                    'expected_count': count
                }
        
        # Suggest difficulty filters
        for difficulty, count in stats['difficulties'].items():
            if count >= target_count * 0.8:
                suggestions[f'difficulty_{difficulty}'] = {
                    'filter': {'difficulty': difficulty},
                    'expected_count': count
                }
        
        return suggestions
