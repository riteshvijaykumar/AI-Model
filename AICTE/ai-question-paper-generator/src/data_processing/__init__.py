"""
Question Parser Module

Handles parsing of different question bank formats including CSV, Excel, JSON, and TXT files.
Provides a unified interface for loading questions regardless of input format.
"""

import pandas as pd
import json
import csv
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging


class QuestionParser:
    """Parser for various question bank file formats"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.txt']
    
    def parse_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Parse a question bank file and return structured question data
        
        Args:
            file_path: Path to the question bank file
            
        Returns:
            List of question dictionaries
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Question bank file not found: {file_path}")
        
        file_extension = file_path.suffix.lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        self.logger.info(f"Parsing question bank: {file_path}")
        
        if file_extension == '.csv':
            return self._parse_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            return self._parse_excel(file_path)
        elif file_extension == '.json':
            return self._parse_json(file_path)
        elif file_extension == '.txt':
            return self._parse_txt(file_path)
        else:
            raise ValueError(f"Parser not implemented for: {file_extension}")
    
    def _parse_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse CSV file"""
        try:
            df = pd.read_csv(file_path)
            return self._standardize_dataframe(df)
        except Exception as e:
            raise ValueError(f"Error parsing CSV file: {str(e)}")
    
    def _parse_excel(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse Excel file"""
        try:
            df = pd.read_excel(file_path)
            return self._standardize_dataframe(df)
        except Exception as e:
            raise ValueError(f"Error parsing Excel file: {str(e)}")
    
    def _parse_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return [self._standardize_question(q) for q in data]
            elif isinstance(data, dict):
                if 'questions' in data:
                    return [self._standardize_question(q) for q in data['questions']]
                else:
                    return [self._standardize_question(data)]
            else:
                raise ValueError("Invalid JSON structure")
        except Exception as e:
            raise ValueError(f"Error parsing JSON file: {str(e)}")
    
    def _parse_txt(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse TXT file (assumes simple format)"""
        try:
            questions = []
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by double newlines or numbered questions
            if '\n\n' in content:
                question_blocks = content.split('\n\n')
            else:
                question_blocks = content.split('\n')
            
            for i, block in enumerate(question_blocks):
                if block.strip():
                    question = {
                        'id': i + 1,
                        'question': block.strip(),
                        'topic': 'general',
                        'difficulty': 'medium',
                        'type': 'text',
                        'keywords': []
                    }
                    questions.append(question)
            
            return questions
        except Exception as e:
            raise ValueError(f"Error parsing TXT file: {str(e)}")
    
    def _standardize_dataframe(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convert DataFrame to standardized question format"""
        questions = []
        
        # Map common column names to standard format
        column_mapping = {
            'question': ['question', 'q', 'text', 'question_text'],
            'answer': ['answer', 'a', 'correct_answer', 'solution'],
            'topic': ['topic', 'subject', 'category', 'domain'],
            'difficulty': ['difficulty', 'level', 'difficulty_level'],
            'type': ['type', 'question_type', 'format'],
            'keywords': ['keywords', 'tags', 'key_words'],
            'options': ['options', 'choices', 'alternatives'],
            'explanation': ['explanation', 'rationale', 'reasoning']
        }
        
        # Create reverse mapping
        reverse_mapping = {}
        for standard_name, alternatives in column_mapping.items():
            for alt in alternatives:
                if alt in df.columns:
                    reverse_mapping[alt] = standard_name
                    break
        
        for idx, row in df.iterrows():
            question = {
                'id': idx + 1,
                'question': '',
                'topic': 'general',
                'difficulty': 'medium',
                'type': 'text',
                'keywords': []
            }
            
            # Map columns to standard format
            for col in df.columns:
                if col in reverse_mapping:
                    standard_name = reverse_mapping[col]
                    value = row[col]
                    
                    if pd.notna(value):
                        if standard_name == 'keywords' and isinstance(value, str):
                            question[standard_name] = [k.strip() for k in value.split(',')]
                        else:
                            question[standard_name] = value
                else:
                    # Keep original column name for non-standard columns
                    if pd.notna(row[col]):
                        question[col] = row[col]
            
            questions.append(question)
        
        return questions
    
    def _standardize_question(self, question: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize individual question format"""
        standardized = {
            'id': question.get('id', 1),
            'question': question.get('question', ''),
            'topic': question.get('topic', 'general'),
            'difficulty': question.get('difficulty', 'medium'),
            'type': question.get('type', 'text'),
            'keywords': question.get('keywords', [])
        }
        
        # Add any additional fields
        for key, value in question.items():
            if key not in standardized:
                standardized[key] = value
        
        return standardized
    
    def validate_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate and clean question data"""
        valid_questions = []
        
        for question in questions:
            if self._is_valid_question(question):
                valid_questions.append(question)
            else:
                self.logger.warning(f"Invalid question skipped: {question.get('id', 'unknown')}")
        
        return valid_questions
    
    def _is_valid_question(self, question: Dict[str, Any]) -> bool:
        """Check if a question is valid"""
        required_fields = ['question']
        
        for field in required_fields:
            if field not in question or not question[field]:
                return False
        
        return True
