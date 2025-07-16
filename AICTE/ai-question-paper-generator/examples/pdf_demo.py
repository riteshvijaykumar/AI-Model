#!/usr/bin/env python3
"""
Demo script for PDF Question Paper Generation
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    print("🎓 AI Question Bank - PDF Question Paper Demo")
    print("=" * 55)
    
    try:
        # Import modules
        from src.data_processing.question_parser import QuestionParser
        from src.selection_engine.question_selector import QuestionSelector
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        
        # Initialize components
        print("1. Initializing components...")
        parser = QuestionParser()
        selector = QuestionSelector()
        generator = SpreadsheetGenerator()
        
        # Load sample questions
        print("2. Loading sample questions...")
        sample_file = "data/sample_questions.csv"
        
        if not os.path.exists(sample_file):
            print(f"❌ Sample file not found: {sample_file}")
            return
        
        questions = parser.parse_file(sample_file)
        selector.load_questions(questions)
        print(f"✅ Loaded {len(questions)} questions")
        
        # Show marks distribution
        marks_dist = {}
        for q in questions:
            marks = q.get('marks', 'Unknown')
            marks_dist[marks] = marks_dist.get(marks, 0) + 1
        
        print("3. Marks distribution:")
        for marks, count in sorted(marks_dist.items()):
            print(f"   {marks} marks: {count} questions")
        
        # Demo 1: Basic PDF export
        print("\n4. Generating basic PDF question paper...")
        
        # Select questions for a balanced paper
        selected_2_marks = selector.select_questions(count=12)
        selected_16_marks = selector.select_questions(count=8)
        
        all_selected = selected_2_marks + selected_16_marks
        
        # Basic marks configuration
        marks_config = {
            'title': 'Sample Question Paper',
            'subject': 'General Knowledge',
            'duration': '3 Hours',
            'two_marks_count': 10,
            'sixteen_marks_count': 4,
            'choice_options': 2
        }
        
        output_file = "demo_question_paper.pdf"
        
        success = generator.generate_output(
            all_selected,
            output_file,
            format_type='pdf',
            marks_config=marks_config
        )
        
        if success:
            print(f"✅ PDF generated: {output_file}")
            if os.path.exists(output_file):
                size = os.path.getsize(output_file)
                print(f"   File size: {size:,} bytes")
        else:
            print("❌ PDF generation failed")
        
        # Demo 2: Custom configuration PDF
        print("\n5. Generating custom configuration PDF...")
        
        custom_config = {
            'title': 'Mathematics Question Paper',
            'subject': 'Advanced Mathematics',
            'duration': '2.5 Hours',
            'two_marks_count': 8,
            'sixteen_marks_count': 3,
            'choice_options': 3
        }
        
        # Select math-focused questions if available
        math_questions = [q for q in questions if 'math' in q.get('topic', '').lower()]
        if len(math_questions) < 15:
            math_questions = all_selected[:15]  # Fallback
        
        custom_output = "math_question_paper.pdf"
        
        success = generator.generate_output(
            math_questions,
            custom_output,
            format_type='pdf',
            marks_config=custom_config
        )
        
        if success:
            print(f"✅ Custom PDF generated: {custom_output}")
            if os.path.exists(custom_output):
                size = os.path.getsize(custom_output)
                print(f"   File size: {size:,} bytes")
        
        # Demo 3: Command line usage examples
        print("\n6. Command line usage examples:")
        print("   # Basic PDF export")
        print("   python main.py --input data/sample_questions.csv --output exam.pdf --format pdf")
        print()
        print("   # Custom marks configuration")
        print("   python main.py --input data/sample_questions.csv --output custom_exam.pdf \\")
        print("                  --format pdf --marks-config '2marks:15,16marks:5,choices:3' \\")
        print("                  --title 'Final Exam' --subject 'Computer Science'")
        print()
        print("   # With selection criteria")
        print("   python main.py --input data/sample_questions.csv --output filtered_exam.pdf \\")
        print("                  --format pdf --criteria 'difficulty:medium,count:20'")
        
        print("\n🎉 PDF Demo completed!")
        print("\nGenerated files:")
        for filename in [output_file, custom_output]:
            if os.path.exists(filename):
                print(f"  ✅ {filename}")
            else:
                print(f"  ❌ {filename} (not found)")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install reportlab fpdf2")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
