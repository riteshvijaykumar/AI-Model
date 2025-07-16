#!/usr/bin/env python3
"""
Enhanced GUI Demo
Demonstrates the new unit-based question paper generation features
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def demo_enhanced_features():
    """Demonstrate enhanced features"""
    
    print("🚀 Enhanced GUI Features Demo")
    print("=" * 50)
    
    # Check enhanced features availability
    try:
        from src.enhanced_features import EnhancedQuestionSelector, WordDocumentGenerator
        print("✅ Enhanced features available!")
        
        # Load sample questions
        import pandas as pd
        sample_file = "data/enhanced_sample_questions.csv"
        
        if Path(sample_file).exists():
            df = pd.read_csv(sample_file)
            questions = df.to_dict('records')
            
            print(f"📊 Loaded {len(questions)} sample questions")
            
            # Demonstrate enhanced selector
            selector = EnhancedQuestionSelector()
            selector.load_questions(questions)
            
            available_units = selector.get_available_units()
            print(f"🏷️ Available units: {available_units}")
            
            # Demonstrate selection
            if available_units:
                selected_units = available_units[:2]  # Select first 2 units
                total_marks = 60
                
                print(f"🎯 Selecting questions from units: {selected_units}")
                print(f"📝 Target total marks: {total_marks}")
                
                result = selector.select_questions_by_units_and_marks(
                    selected_units=selected_units,
                    total_marks=total_marks
                )
                
                selected_questions = result['questions']
                config = result['paper_config']
                
                print(f"✅ Selected {len(selected_questions)} questions")
                print(f"📊 Actual marks: {config['actual_marks']}")
                print(f"📈 Distribution: {config['distribution']}")
                
                # Show questions by marks
                questions_by_marks = {}
                for q in selected_questions:
                    marks = int(q.get('marks', 2))
                    if marks not in questions_by_marks:
                        questions_by_marks[marks] = []
                    questions_by_marks[marks].append(q)
                
                print("\\n📋 Question Paper Structure:")
                for marks in sorted(questions_by_marks.keys()):
                    count = len(questions_by_marks[marks])
                    print(f"  • {marks}-mark questions: {count}")
                
                # Demonstrate Word export if available
                try:
                    word_gen = WordDocumentGenerator()
                    
                    import os
                    os.makedirs("exports", exist_ok=True)
                    
                    output_path = word_gen.generate_question_paper(
                        questions=selected_questions,
                        title="Demo Question Paper",
                        instructions="Answer all questions as per instructions.",
                        output_path="exports/demo_paper.docx"
                    )
                    
                    print(f"📄 Word document created: {output_path}")
                    
                except Exception as word_error:
                    print(f"⚠️ Word export not available: {word_error}")
            
            print("\\n🌐 Enhanced GUI Features:")
            print("  • ✅ Unit-based question selection")
            print("  • ✅ Total marks specification")
            print("  • ✅ Automatic marks distribution")
            print("  • ✅ Choice options for 16-mark questions")
            print("  • ✅ Word document export")
            print("  • ✅ Enhanced question paper preview")
            
            print("\\n🚀 Launch the GUI:")
            print("  python launch_enhanced_gui.py")
            print("  OR")
            print("  streamlit run streamlit_app.py")
            
        else:
            print(f"❌ Sample file not found: {sample_file}")
            print("Creating sample data...")
            create_sample_data()
            
    except ImportError as e:
        print(f"❌ Enhanced features not available: {e}")
        print("Install requirements: pip install python-docx PyPDF2 pdfplumber")

def create_sample_data():
    """Create enhanced sample data"""
    
    sample_data = """question,unit,marks,topic,difficulty,type,answer
What is Python?,Unit 1,2,Programming,easy,mcq,A programming language
Explain variables in Python,Unit 1,2,Programming,easy,short,Variables store data values
Define object-oriented programming,Unit 1,16,Programming,medium,long,OOP is a programming paradigm based on objects
What is a function?,Unit 1,2,Programming,easy,short,A reusable block of code
Describe inheritance in Python,Unit 1,16,Programming,medium,long,Inheritance allows classes to inherit properties from other classes
What is a list in Python?,Unit 2,2,Data Structures,easy,mcq,An ordered collection of items
How do you sort a list?,Unit 2,2,Data Structures,easy,short,Using the sort() method
Explain different data structures in Python,Unit 2,16,Data Structures,medium,long,Python has lists tuples dictionaries sets etc
What is a dictionary?,Unit 2,2,Data Structures,easy,short,A collection of key-value pairs
Compare lists and tuples,Unit 2,16,Data Structures,medium,long,Lists are mutable tuples are immutable
What is exception handling?,Unit 3,2,Error Handling,medium,short,Managing errors in code
Try-except block usage,Unit 3,2,Error Handling,medium,short,Used to catch and handle exceptions
Implement comprehensive error handling,Unit 3,16,Error Handling,hard,long,Use try-except-else-finally blocks with specific exception types
What is a file operation?,Unit 3,2,File Handling,easy,short,Reading or writing to files
Describe file handling in Python,Unit 3,16,File Handling,medium,long,Python provides built-in functions for file operations
What is a module?,Unit 4,2,Modules,easy,short,A file containing Python code
How to import modules?,Unit 4,2,Modules,easy,short,Using import statement
Create a comprehensive module system,Unit 4,16,Modules,hard,long,Design modules with proper structure imports and documentation
What is pip?,Unit 4,2,Package Management,easy,short,Python package installer
Explain package management best practices,Unit 4,16,Package Management,medium,long,Use virtual environments requirements.txt and proper versioning"""
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs("data", exist_ok=True)
    
    # Write sample data
    with open("data/enhanced_sample_questions.csv", "w", encoding="utf-8") as f:
        f.write(sample_data)
    
    print("✅ Sample data created: data/enhanced_sample_questions.csv")

if __name__ == "__main__":
    demo_enhanced_features()
