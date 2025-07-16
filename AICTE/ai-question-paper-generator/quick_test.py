#!/usr/bin/env python3
"""
Quick test to verify the organized project is working
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def quick_test():
    print("🚀 Quick Project Test")
    print("=" * 30)
    
    try:
        # Test 1: Import core modules
        print("1. Testing core imports...")
        from src.data_processing.question_parser import QuestionParser
        from src.selection_engine.question_selector import QuestionSelector
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        print("✅ Core modules imported")
        
        # Test 2: Import enhanced features
        print("2. Testing enhanced features...")
        from src.enhanced_features import EnhancedQuestionSelector
        print("✅ Enhanced features imported")
        
        # Test 3: Load sample data
        print("3. Testing sample data...")
        parser = QuestionParser()
        sample_file = "data/enhanced_sample_questions.csv"
        
        if not Path(sample_file).exists():
            print("❌ Sample file not found")
            return False
            
        questions = parser.parse_file(sample_file)
        print(f"✅ Loaded {len(questions)} questions")
        
        # Test 4: Enhanced selector
        print("4. Testing enhanced selector...")
        enhanced_selector = EnhancedQuestionSelector()
        enhanced_selector.load_questions(questions)
        units = enhanced_selector.get_available_units()
        print(f"✅ Found {len(units)} units")
        
        print("\n🎉 All tests passed! Project is working correctly.")
        print("\nTo use the system:")
        print("  python main.py --cli")
        print("  > unitselect")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    quick_test()
