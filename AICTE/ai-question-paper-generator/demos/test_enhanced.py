#!/usr/bin/env python3
"""
Simple test for enhanced features
"""

import sys
import os
from pathlib import Path

# Add src to path (go up one level from demos to project root)
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_enhanced_features():
    print("🧪 Testing Enhanced Features")
    print("=" * 40)
    
    try:
        # Test importing enhanced features
        print("1. Testing imports...")
        from src.enhanced_features import EnhancedQuestionSelector
        from src.data_processing.question_parser import QuestionParser
        print("✅ Imports successful")
        
        # Test loading sample questions
        print("\n2. Loading sample questions...")
        parser = QuestionParser()
        # Use absolute path from project root
        project_root = Path(__file__).parent.parent
        sample_file = project_root / "data" / "enhanced_sample_questions.csv"
        questions = parser.parse_file(str(sample_file))
        print(f"✅ Loaded {len(questions)} questions")
        
        # Test enhanced selector
        print("\n3. Testing enhanced selector...")
        enhanced_selector = EnhancedQuestionSelector()
        enhanced_selector.load_questions(questions)
        
        # Get available units
        units = enhanced_selector.get_available_units()
        print(f"✅ Found {len(units)} units: {units}")
        
        # Test unit-based selection
        print("\n4. Testing unit-based selection...")
        selected_units = units[:2]  # Select first 2 units
        result = enhanced_selector.select_questions_by_units_and_marks(
            selected_units, 
            total_marks=60
        )
        
        print(f"✅ Selected {len(result['questions'])} questions")
        print(f"   Total marks: {result['total_marks']}")
        print(f"   Distribution: {result['distribution']}")
        print(f"   Units: {result['units_covered']}")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_enhanced_features()
