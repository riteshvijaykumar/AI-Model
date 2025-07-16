#!/usr/bin/env python3
"""
Final system test script - Tests all components after cleanup
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_system():
    """Test all system components"""
    print("🧪 Testing AI Question Bank Selection System")
    print("=" * 50)
    
    # Test 1: Import all modules
    print("\n1. Testing module imports...")
    try:
        from src.data_processing.question_parser import QuestionParser
        from src.selection_engine.question_selector import QuestionSelector
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        from src.ui.cli_interface import CLIInterface
        print("✅ All core modules imported successfully")
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False
    
    # Test 2: Check critical dependencies
    print("\n2. Testing critical dependencies...")
    critical_deps = [
        'pandas', 'numpy', 'openpyxl', 'streamlit', 
        'plotly', 'reportlab', 'PyPDF2', 'transformers'
    ]
    
    for dep in critical_deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - Missing!")
    
    # Test 3: Check sample data
    print("\n3. Testing sample data...")
    sample_file = "data/sample_questions.csv"
    if os.path.exists(sample_file):
        try:
            parser = QuestionParser()
            questions = parser.parse_file(sample_file)
            print(f"✅ Sample data loaded: {len(questions)} questions")
        except Exception as e:
            print(f"❌ Sample data loading failed: {e}")
    else:
        print("❌ Sample data file not found")
    
    # Test 4: Test question selection
    print("\n4. Testing question selection...")
    try:
        selector = QuestionSelector()
        if os.path.exists(sample_file):
            questions = parser.parse_file(sample_file)
            selector.load_questions(questions)
            selected = selector.select_questions(count=5)
            print(f"✅ Question selection works: Selected {len(selected)} questions")
        else:
            print("⚠️ Skipped - no sample data")
    except Exception as e:
        print(f"❌ Question selection failed: {e}")
    
    # Test 5: Test export formats
    print("\n5. Testing export capabilities...")
    formats_to_test = ['csv', 'excel', 'json', 'txt', 'pdf']
    
    try:
        generator = SpreadsheetGenerator()
        
        # Create sample questions for testing
        sample_questions = [
            {
                'id': 1,
                'question': 'What is 2+2?',
                'topic': 'math',
                'difficulty': 'easy',
                'type': 'text',
                'marks': 2
            },
            {
                'id': 2,
                'question': 'Explain photosynthesis.',
                'topic': 'science',
                'difficulty': 'medium',
                'type': 'text',
                'marks': 16
            }
        ]
        
        for fmt in formats_to_test:
            try:
                output_file = f"exports/test_output.{fmt if fmt != 'excel' else 'xlsx'}"
                
                # Remove existing file if any
                if os.path.exists(output_file):
                    os.remove(output_file)
                
                # Test export
                if fmt == 'pdf':
                    success = generator.generate_output(
                        sample_questions, 
                        output_file, 
                        format_type=fmt,
                        marks_config={
                            'two_marks_count': 1,
                            'sixteen_marks_count': 1,
                            'choice_options': 1,
                            'title': 'Test Paper',
                            'subject': 'Test'
                        }
                    )
                else:
                    success = generator.generate_output(
                        sample_questions, 
                        output_file, 
                        format_type=fmt
                    )
                
                if success and os.path.exists(output_file):
                    print(f"✅ {fmt.upper()} export works")
                    # Clean up test file
                    os.remove(output_file)
                else:
                    print(f"❌ {fmt.upper()} export failed")
                    
            except Exception as e:
                print(f"❌ {fmt.upper()} export error: {e}")
        
    except Exception as e:
        print(f"❌ Export testing failed: {e}")
    
    # Test 6: GUI readiness check
    print("\n6. Testing GUI readiness...")
    try:
        # Check if streamlit_app.py exists and is valid
        if os.path.exists("streamlit_app.py"):
            print("✅ Streamlit app file exists")
            
            # Try to import the app
            import streamlit_app
            print("✅ Streamlit app imports successfully")
        else:
            print("❌ Streamlit app file not found")
    except Exception as e:
        print(f"❌ GUI readiness check failed: {e}")
    
    # Test 7: CLI readiness check
    print("\n7. Testing CLI readiness...")
    try:
        # Check if main.py exists and is valid
        if os.path.exists("main.py"):
            print("✅ Main CLI file exists")
        else:
            print("❌ Main CLI file not found")
    except Exception as e:
        print(f"❌ CLI readiness check failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 System Test Complete!")
    print("\n📋 Quick Start Commands:")
    print("   Streamlit GUI: streamlit run streamlit_app.py")
    print("   CLI Interface: python main.py --cli")
    print("   Direct Process: python main.py -i data.csv -o result.xlsx")
    print("   PDF Export: python main.py -i data.csv -o result.pdf -f pdf")
    
    return True

if __name__ == "__main__":
    test_system()
