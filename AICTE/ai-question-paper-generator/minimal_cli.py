#!/usr/bin/env python3
"""
Minimal CLI test for the question paper generator
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def minimal_cli():
    print("🎓 AI Question Paper Generator - Minimal CLI")
    print("=" * 50)
    
    try:
        # Test basic functionality
        from src.data_processing.question_parser import QuestionParser
        from src.enhanced_features import EnhancedQuestionSelector
        
        print("✅ Core modules loaded successfully!")
        
        # Load sample data
        parser = QuestionParser()
        sample_file = "data/enhanced_sample_questions.csv"
        
        if not Path(sample_file).exists():
            print(f"❌ Sample file not found: {sample_file}")
            return
        
        questions = parser.parse_file(sample_file)
        print(f"✅ Loaded {len(questions)} questions")
        
        # Initialize enhanced selector
        enhanced_selector = EnhancedQuestionSelector()
        enhanced_selector.load_questions(questions)
        
        # Show available units
        units = enhanced_selector.get_available_units()
        print(f"✅ Found {len(units)} units: {units}")
        
        # Demo unit selection
        print("\n🎯 Demo: Unit-based Selection")
        selected_units = units[:2]  # Select first 2 units
        total_marks = 60
        
        print(f"Selected units: {selected_units}")
        print(f"Total marks: {total_marks}")
        
        result = enhanced_selector.select_questions_by_units_and_marks(
            selected_units, total_marks
        )
        
        print(f"\n✅ Selection completed!")
        print(f"   Questions selected: {len(result['questions'])}")
        print(f"   Actual total marks: {result['total_marks']}")
        print(f"   Distribution: {result['distribution']}")
        
        print(f"\n🎉 Your enhanced AI Question Paper Generator is working!")
        print(f"📄 Sample questions from units {selected_units}:")
        
        for i, q in enumerate(result['questions'][:3], 1):
            marks = q.get('marks', 'N/A')
            question_text = q.get('question', 'N/A')[:50] + "..."
            print(f"   {i}. [{marks} marks] {question_text}")
        
        if len(result['questions']) > 3:
            print(f"   ... and {len(result['questions']) - 3} more questions")
        
        print(f"\n💡 To use the full CLI: python main.py --cli")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    minimal_cli()
