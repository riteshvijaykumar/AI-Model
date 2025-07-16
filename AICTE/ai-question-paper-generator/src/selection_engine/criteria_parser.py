"""
Criteria Parser Module

Parses and validates user selection criteria into standardized format.
Supports various input formats and provides validation and normalization.
"""

import re
from typing import Dict, Any, List, Optional, Union
import logging


class CriteriaParser:
    """Parses and validates selection criteria"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.valid_difficulties = ['easy', 'medium', 'hard', 'expert']
        self.valid_types = ['text', 'multiple_choice', 'true_false', 'essay', 'numeric', 'code']
        
    def parse_criteria(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate criteria dictionary"""
        parsed = {}
        
        # Parse individual criteria
        if 'topic' in criteria:
            parsed['topic'] = self._parse_topic(criteria['topic'])
        
        if 'difficulty' in criteria:
            parsed['difficulty'] = self._parse_difficulty(criteria['difficulty'])
        
        if 'type' in criteria:
            parsed['type'] = self._parse_type(criteria['type'])
        
        if 'keywords' in criteria:
            parsed['keywords'] = self._parse_keywords(criteria['keywords'])
        
        if 'count' in criteria:
            parsed['count'] = self._parse_count(criteria['count'])
        
        if 'exclude_keywords' in criteria:
            parsed['exclude_keywords'] = self._parse_keywords(criteria['exclude_keywords'])
        
        if 'text_contains' in criteria:
            parsed['text_contains'] = str(criteria['text_contains'])
        
        if 'min_length' in criteria:
            parsed['min_length'] = self._parse_length(criteria['min_length'])
        
        if 'max_length' in criteria:
            parsed['max_length'] = self._parse_length(criteria['max_length'])
        
        if 'diversity' in criteria:
            parsed['diversity'] = self._parse_boolean(criteria['diversity'])
        
        if 'reference_text' in criteria:
            parsed['reference_text'] = str(criteria['reference_text'])
        
        # Add any custom criteria
        for key, value in criteria.items():
            if key not in parsed:
                parsed[key] = value
        
        # Validate parsed criteria
        self._validate_criteria(parsed)
        
        return parsed
    
    def _parse_topic(self, topic: Union[str, List[str]]) -> List[str]:
        """Parse topic criteria"""
        if isinstance(topic, str):
            # Split by comma if multiple topics
            topics = [t.strip() for t in topic.split(',')]
        elif isinstance(topic, list):
            topics = [str(t).strip() for t in topic]
        else:
            topics = [str(topic)]
        
        return [t for t in topics if t]
    
    def _parse_difficulty(self, difficulty: Union[str, List[str]]) -> List[str]:
        """Parse difficulty criteria"""
        if isinstance(difficulty, str):
            difficulties = [d.strip().lower() for d in difficulty.split(',')]
        elif isinstance(difficulty, list):
            difficulties = [str(d).strip().lower() for d in difficulty]
        else:
            difficulties = [str(difficulty).lower()]
        
        # Validate difficulties
        valid_difficulties = []
        for diff in difficulties:
            if diff in self.valid_difficulties:
                valid_difficulties.append(diff)
            else:
                self.logger.warning(f"Invalid difficulty: {diff}")
        
        return valid_difficulties if valid_difficulties else ['medium']
    
    def _parse_type(self, q_type: Union[str, List[str]]) -> List[str]:
        """Parse question type criteria"""
        if isinstance(q_type, str):
            types = [t.strip().lower() for t in q_type.split(',')]
        elif isinstance(q_type, list):
            types = [str(t).strip().lower() for t in q_type]
        else:
            types = [str(q_type).lower()]
        
        # Validate types
        valid_types = []
        for qtype in types:
            if qtype in self.valid_types:
                valid_types.append(qtype)
            else:
                self.logger.warning(f"Invalid question type: {qtype}")
        
        return valid_types if valid_types else ['text']
    
    def _parse_keywords(self, keywords: Union[str, List[str]]) -> List[str]:
        """Parse keyword criteria"""
        if isinstance(keywords, str):
            # Split by comma or semicolon
            keywords = re.split(r'[,;]', keywords)
        elif isinstance(keywords, list):
            keywords = [str(k) for k in keywords]
        else:
            keywords = [str(keywords)]
        
        return [k.strip() for k in keywords if k.strip()]
    
    def _parse_count(self, count: Union[str, int]) -> int:
        """Parse count criteria"""
        try:
            count_int = int(count)
            if count_int <= 0:
                self.logger.warning(f"Invalid count: {count}, using default")
                return 20
            return min(count_int, 1000)  # Cap at 1000
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid count format: {count}, using default")
            return 20
    
    def _parse_length(self, length: Union[str, int]) -> int:
        """Parse length criteria"""
        try:
            length_int = int(length)
            if length_int < 0:
                self.logger.warning(f"Invalid length: {length}, using 0")
                return 0
            return length_int
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid length format: {length}, using 0")
            return 0
    
    def _parse_boolean(self, value: Union[str, bool]) -> bool:
        """Parse boolean criteria"""
        if isinstance(value, bool):
            return value
        elif isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 'on']
        else:
            return bool(value)
    
    def _validate_criteria(self, criteria: Dict[str, Any]):
        """Validate parsed criteria for consistency"""
        # Check length constraints
        if 'min_length' in criteria and 'max_length' in criteria:
            if criteria['min_length'] > criteria['max_length']:
                self.logger.warning("min_length > max_length, swapping values")
                criteria['min_length'], criteria['max_length'] = (
                    criteria['max_length'], criteria['min_length']
                )
        
        # Check count is reasonable
        if 'count' in criteria and criteria['count'] > 1000:
            self.logger.warning("Count too large, capping at 1000")
            criteria['count'] = 1000
        
        # Validate keyword conflicts
        if 'keywords' in criteria and 'exclude_keywords' in criteria:
            overlap = set(criteria['keywords']) & set(criteria['exclude_keywords'])
            if overlap:
                self.logger.warning(f"Keyword overlap detected: {overlap}")
    
    def parse_string_criteria(self, criteria_string: str) -> Dict[str, Any]:
        """Parse criteria from string format"""
        criteria = {}
        
        # Parse key:value pairs
        pairs = criteria_string.split(',')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Handle special cases
                if key == 'count':
                    criteria[key] = self._parse_count(value)
                elif key in ['min_length', 'max_length']:
                    criteria[key] = self._parse_length(value)
                elif key == 'difficulty':
                    criteria[key] = self._parse_difficulty(value)
                elif key == 'type':
                    criteria[key] = self._parse_type(value)
                elif key in ['keywords', 'exclude_keywords']:
                    criteria[key] = self._parse_keywords(value)
                elif key == 'diversity':
                    criteria[key] = self._parse_boolean(value)
                else:
                    criteria[key] = value
        
        return self.parse_criteria(criteria)
    
    def criteria_to_string(self, criteria: Dict[str, Any]) -> str:
        """Convert criteria to string format"""
        parts = []
        
        for key, value in criteria.items():
            if isinstance(value, list):
                value_str = ','.join(str(v) for v in value)
            else:
                value_str = str(value)
            
            parts.append(f"{key}:{value_str}")
        
        return ','.join(parts)
    
    def get_criteria_template(self, template_name: str) -> Dict[str, Any]:
        """Get predefined criteria template"""
        templates = {
            'easy_math': {
                'topic': ['mathematics', 'math'],
                'difficulty': ['easy'],
                'count': 15
            },
            'medium_science': {
                'topic': ['science', 'physics', 'chemistry', 'biology'],
                'difficulty': ['medium'],
                'count': 20
            },
            'hard_programming': {
                'topic': ['programming', 'coding', 'computer science'],
                'difficulty': ['hard'],
                'type': ['code'],
                'count': 10
            },
            'mixed_general': {
                'difficulty': ['easy', 'medium'],
                'count': 25,
                'diversity': True
            }
        }
        
        return templates.get(template_name, {})
    
    def validate_criteria_completeness(self, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if criteria are complete and suggest improvements"""
        suggestions = {}
        
        # Check if at least one filter is provided
        filter_keys = ['topic', 'difficulty', 'type', 'keywords', 'text_contains']
        if not any(key in criteria for key in filter_keys):
            suggestions['filters'] = "Consider adding topic, difficulty, or keyword filters"
        
        # Check if count is specified
        if 'count' not in criteria:
            suggestions['count'] = "Consider specifying the number of questions needed"
        
        # Check for conflicting criteria
        if 'keywords' in criteria and 'exclude_keywords' in criteria:
            overlap = set(criteria.get('keywords', [])) & set(criteria.get('exclude_keywords', []))
            if overlap:
                suggestions['conflict'] = f"Keywords appear in both include and exclude: {overlap}"
        
        return suggestions
