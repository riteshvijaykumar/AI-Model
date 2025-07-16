#!/usr/bin/env python3
"""
Enhanced AI Question Paper Generator Demo

This demo showcases the new features:
1. Unit-based question selection
2. Total marks-based distribution
3. Word document (.docx) export
4. Enhanced PDF/Word input parsing
"""

import sys
import os
from pathlib import Path

# Add src to path (go up one level from demos to project root)
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))

def main():
    print("🎓 Enhanced AI Question Paper Generator - Demo")
    print("=" * 55)
    
    try:
        # Import enhanced features
        from src.enhanced_features import EnhancedQuestionSelector, WordDocumentGenerator
        from src.data_processing.question_parser import QuestionParser
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        
        print("✅ All enhanced features loaded successfully!")
        
        # Initialize components
        parser = QuestionParser()
        enhanced_selector = EnhancedQuestionSelector()
        word_generator = WordDocumentGenerator()
        pdf_generator = SpreadsheetGenerator()
        
        # Load sample questions
        # Use absolute path from project root
        project_root = Path(__file__).parent.parent
        sample_file = project_root / "data" / "enhanced_sample_questions.csv"
        if not sample_file.exists():
            print(f"❌ Sample file not found: {sample_file}")
            return
        
        print(f"\n1. Loading questions from: {sample_file}")
        questions = parser.parse_file(str(sample_file))
        enhanced_selector.load_questions(questions)
        
        print(f"✅ Loaded {len(questions)} questions")
        
        # Show available units
        units = enhanced_selector.get_available_units()
        print(f"\n2. Available units/topics ({len(units)}):")
        for i, unit in enumerate(units[:10], 1):  # Show first 10
            print(f"   {i}. {unit}")
        if len(units) > 10:
            print(f"   ... and {len(units) - 10} more")
        
        # Demo 1: Unit-based selection for 100 marks
        print(f"\n3. Demo 1: Unit-based Selection (100 marks)")
        print("-" * 45)
        selected_units = units[:3]  # Select first 3 units
        print(f"Selected units: {', '.join(selected_units)}")
        
        result = enhanced_selector.select_questions_by_units_and_marks(
            selected_units, 
            total_marks=100
        )
        
        print(f"✅ Selected {len(result['questions'])} questions")
        print(f"   Total marks: {result['total_marks']}")
        print(f"   Distribution: {result['distribution']}")
        print(f"   Choice options: {result['choice_options']}")
        
        # Demo 2: Export to Word document
        print(f"\n4. Demo 2: Word Document Export")
        print("-" * 35)
        
        word_config = {
            'title': 'Sample Question Paper',
            'subject': 'Mixed Topics',
            'duration': '3 Hours',
            'total_marks': result['total_marks'],
            'choice_options': result['choice_options']
        }
        
        word_output = "demo_enhanced_paper.docx"
        success = word_generator.generate_question_paper(
            result['questions'],
            word_output,
            word_config
        )
        
        if success:
            print(f"✅ Word document created: {word_output}")
        else:
            print("❌ Word document creation failed")
        
        # Demo 3: Export to PDF for comparison
        print(f"\n5. Demo 3: PDF Export (for comparison)")
        print("-" * 40)
        
        pdf_config = {
            'title': word_config['title'],
            'subject': word_config['subject'],
            'duration': word_config['duration'],
            'two_marks_count': result['distribution'].get('2_marks', 0),
            'sixteen_marks_count': result['distribution'].get('16_marks', 0),
            'choice_options': result['choice_options']
        }
        
        pdf_output = "demo_enhanced_paper.pdf"
        success = pdf_generator.generate_output(
            result['questions'],
            pdf_output,
            format_type='pdf',
            marks_config=pdf_config
        )
        
        if success:
            print(f"✅ PDF document created: {pdf_output}")
        else:
            print("❌ PDF document creation failed")
        
        # Demo 4: Different marks configuration
        print(f"\n6. Demo 4: Custom Marks Configuration (150 marks)")
        print("-" * 50)
        
        result2 = enhanced_selector.select_questions_by_units_and_marks(
            selected_units, 
            total_marks=150
        )
        
        print(f"✅ Selected {len(result2['questions'])} questions")
        print(f"   Total marks: {result2['total_marks']}")
        print(f"   Distribution: {result2['distribution']}")
        
        # Summary
        print(f"\n🎉 Demo completed successfully!")
        print("=" * 55)
        print("Enhanced features demonstrated:")
        print("✅ Unit-based question selection")
        print("✅ Automatic marks distribution")
        print("✅ Word document (.docx) export")
        print("✅ Enhanced PDF export")
        print("✅ Flexible marks configuration")
        
        print(f"\nGenerated files:")
        if os.path.exists(word_output):
            print(f"📄 {word_output} ({os.path.getsize(word_output):,} bytes)")
        if os.path.exists(pdf_output):
            print(f"📄 {pdf_output} ({os.path.getsize(pdf_output):,} bytes)")
        
        print(f"\n💡 To use these features interactively:")
        print("   python main.py --cli")
        print("   > unitselect")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install required dependencies:")
        print("   pip install python-docx PyPDF2 pdfplumber")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
