"""
Basic unit tests for the AI Question Bank Selection System
"""

import unittest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.data_processing.question_parser import QuestionParser
from src.selection_engine.question_selector import QuestionSelector
from src.selection_engine.criteria_parser import CriteriaParser
from src.selection_engine.filter_manager import FilterManager
from src.export.spreadsheet_generator import SpreadsheetGenerator


class TestQuestionParser(unittest.TestCase):
    """Test question parser functionality"""
    
    def setUp(self):
        self.parser = QuestionParser()
        self.sample_data = [
            {
                'id': 1,
                'question': 'What is 2+2?',
                'topic': 'mathematics',
                'difficulty': 'easy',
                'type': 'numeric',
                'keywords': ['math', 'addition'],
                'answer': '4'
            },
            {
                'id': 2,
                'question': 'What is the capital of France?',
                'topic': 'geography',
                'difficulty': 'easy',
                'type': 'text',
                'keywords': ['geography', 'capitals'],
                'answer': 'Paris'
            }
        ]
    
    def test_standardize_question(self):
        """Test question standardization"""
        question = {'question': 'Test question', 'topic': 'test'}
        standardized = self.parser._standardize_question(question)
        
        self.assertIn('id', standardized)
        self.assertIn('question', standardized)
        self.assertIn('topic', standardized)
        self.assertIn('difficulty', standardized)
        self.assertIn('type', standardized)
        self.assertIn('keywords', standardized)
    
    def test_validate_questions(self):
        """Test question validation"""
        valid_questions = self.parser.validate_questions(self.sample_data)
        self.assertEqual(len(valid_questions), 2)
        
        # Test with invalid question
        invalid_data = [{'id': 3, 'topic': 'test'}]  # Missing question
        valid_questions = self.parser.validate_questions(invalid_data)
        self.assertEqual(len(valid_questions), 0)


class TestCriteriaParser(unittest.TestCase):
    """Test criteria parser functionality"""
    
    def setUp(self):
        self.parser = CriteriaParser()
    
    def test_parse_difficulty(self):
        """Test difficulty parsing"""
        # Test single difficulty
        result = self.parser._parse_difficulty('easy')
        self.assertEqual(result, ['easy'])
        
        # Test multiple difficulties
        result = self.parser._parse_difficulty('easy,medium')
        self.assertEqual(result, ['easy', 'medium'])
        
        # Test invalid difficulty
        result = self.parser._parse_difficulty('invalid')
        self.assertEqual(result, ['medium'])  # Should default to medium
    
    def test_parse_count(self):
        """Test count parsing"""
        # Test valid count
        result = self.parser._parse_count('25')
        self.assertEqual(result, 25)
        
        # Test invalid count
        result = self.parser._parse_count('invalid')
        self.assertEqual(result, 20)  # Should default to 20
        
        # Test negative count
        result = self.parser._parse_count('-5')
        self.assertEqual(result, 20)  # Should default to 20
    
    def test_parse_keywords(self):
        """Test keyword parsing"""
        # Test comma-separated keywords
        result = self.parser._parse_keywords('math,science,programming')
        self.assertEqual(result, ['math', 'science', 'programming'])
        
        # Test single keyword
        result = self.parser._parse_keywords('mathematics')
        self.assertEqual(result, ['mathematics'])


class TestFilterManager(unittest.TestCase):
    """Test filter manager functionality"""
    
    def setUp(self):
        self.filter_manager = FilterManager()
        self.sample_questions = [
            {
                'id': 1,
                'question': 'What is 2+2?',
                'topic': 'mathematics',
                'difficulty': 'easy',
                'type': 'numeric',
                'keywords': ['math', 'addition']
            },
            {
                'id': 2,
                'question': 'What is the capital of France?',
                'topic': 'geography',
                'difficulty': 'easy',
                'type': 'text',
                'keywords': ['geography', 'capitals']
            },
            {
                'id': 3,
                'question': 'Explain quantum mechanics',
                'topic': 'physics',
                'difficulty': 'hard',
                'type': 'essay',
                'keywords': ['physics', 'quantum']
            }
        ]
    
    def test_filter_by_topic(self):
        """Test topic filtering"""
        filtered = self.filter_manager.filter_by_topic(
            self.sample_questions, ['mathematics']
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['topic'], 'mathematics')
    
    def test_filter_by_difficulty(self):
        """Test difficulty filtering"""
        filtered = self.filter_manager.filter_by_difficulty(
            self.sample_questions, ['easy']
        )
        self.assertEqual(len(filtered), 2)
        
        filtered = self.filter_manager.filter_by_difficulty(
            self.sample_questions, ['hard']
        )
        self.assertEqual(len(filtered), 1)
    
    def test_filter_by_keywords(self):
        """Test keyword filtering"""
        filtered = self.filter_manager.filter_by_keywords(
            self.sample_questions, ['math']
        )
        self.assertEqual(len(filtered), 1)
        
        filtered = self.filter_manager.filter_by_keywords(
            self.sample_questions, ['geography']
        )
        self.assertEqual(len(filtered), 1)
    
    def test_filter_by_length(self):
        """Test length filtering"""
        filtered = self.filter_manager.filter_by_min_length(
            self.sample_questions, 20
        )
        self.assertTrue(len(filtered) <= len(self.sample_questions))
        
        filtered = self.filter_manager.filter_by_max_length(
            self.sample_questions, 15
        )
        self.assertTrue(len(filtered) <= len(self.sample_questions))


class TestQuestionSelector(unittest.TestCase):
    """Test question selector functionality"""
    
    def setUp(self):
        self.selector = QuestionSelector()
        self.sample_questions = [
            {
                'id': 1,
                'question': 'What is 2+2?',
                'topic': 'mathematics',
                'difficulty': 'easy',
                'type': 'numeric',
                'keywords': ['math', 'addition']
            },
            {
                'id': 2,
                'question': 'What is the capital of France?',
                'topic': 'geography',
                'difficulty': 'easy',
                'type': 'text',
                'keywords': ['geography', 'capitals']
            },
            {
                'id': 3,
                'question': 'Explain quantum mechanics',
                'topic': 'physics',
                'difficulty': 'hard',
                'type': 'essay',
                'keywords': ['physics', 'quantum']
            }
        ]
        self.selector.load_questions(self.sample_questions)
    
    def test_load_questions(self):
        """Test question loading"""
        self.assertEqual(len(self.selector.questions), 3)
        self.assertEqual(len(self.selector.question_index), 3)
    
    def test_select_questions_by_topic(self):
        """Test question selection by topic"""
        selected = self.selector.select_questions(topic='mathematics')
        self.assertTrue(len(selected) > 0)
        self.assertEqual(selected[0]['topic'], 'mathematics')
    
    def test_select_questions_by_difficulty(self):
        """Test question selection by difficulty"""
        selected = self.selector.select_questions(difficulty='easy')
        self.assertTrue(len(selected) > 0)
        for q in selected:
            self.assertEqual(q['difficulty'], 'easy')
    
    def test_select_questions_with_count(self):
        """Test question selection with count limit"""
        selected = self.selector.select_questions(count=2)
        self.assertEqual(len(selected), 2)
    
    def test_get_statistics(self):
        """Test statistics generation"""
        stats = self.selector.get_statistics()
        self.assertIn('total_questions', stats)
        self.assertIn('topics', stats)
        self.assertIn('difficulties', stats)
        self.assertIn('types', stats)
        self.assertEqual(stats['total_questions'], 3)


class TestSpreadsheetGenerator(unittest.TestCase):
    """Test spreadsheet generator functionality"""
    
    def setUp(self):
        self.generator = SpreadsheetGenerator()
        self.sample_questions = [
            {
                'id': 1,
                'question': 'What is 2+2?',
                'topic': 'mathematics',
                'difficulty': 'easy',
                'type': 'numeric',
                'keywords': ['math', 'addition'],
                'answer': '4'
            },
            {
                'id': 2,
                'question': 'What is the capital of France?',
                'topic': 'geography',
                'difficulty': 'easy',
                'type': 'text',
                'keywords': ['geography', 'capitals'],
                'answer': 'Paris'
            }
        ]
    
    def test_prepare_dataframe(self):
        """Test DataFrame preparation"""
        df = self.generator._prepare_dataframe(self.sample_questions)
        self.assertEqual(len(df), 2)
        self.assertIn('question', df.columns)
        self.assertIn('topic', df.columns)
        self.assertIn('difficulty', df.columns)
    
    def test_calculate_statistics(self):
        """Test statistics calculation"""
        stats = self.generator._calculate_statistics(self.sample_questions)
        self.assertIn('Total Questions', stats)
        self.assertIn('Topics', stats)
        self.assertIn('Difficulties', stats)
        self.assertEqual(stats['Total Questions'], 2)


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestQuestionParser,
        TestCriteriaParser,
        TestFilterManager,
        TestQuestionSelector,
        TestSpreadsheetGenerator
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
