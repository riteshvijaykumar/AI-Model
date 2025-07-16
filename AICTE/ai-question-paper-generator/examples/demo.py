#!/usr/bin/env python3
"""
Demo script for AI Question Bank Selection System
"""

import sys
import os
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def main():
    print("🤖 AI Question Bank Selection System - Demo")
    print("=" * 50)
    
    try:
        # 1. Load and display sample data
        print("1. Loading sample question bank...")
        sample_file = "data/sample_questions.csv"
        
        if os.path.exists(sample_file):
            df = pd.read_csv(sample_file)
            print(f"✅ Loaded {len(df)} questions from {sample_file}")
            print("\nSample questions:")
            print(df[['question', 'topic', 'difficulty']].head())
            
            # 2. Import and test basic functionality
            print("\n2. Testing system components...")
            from src.data_processing.question_parser import QuestionParser
            from src.selection_engine.question_selector import QuestionSelector
            from src.export.spreadsheet_generator import SpreadsheetGenerator
            
            # Initialize
            parser = QuestionParser()
            selector = QuestionSelector()
            generator = SpreadsheetGenerator()
            print("✅ Components initialized successfully")
            
            # 3. Parse questions
            print("\n3. Parsing questions...")
            questions = parser.parse_file(sample_file)
            print(f"✅ Parsed {len(questions)} questions")
            
            # 4. Load into selector
            print("\n4. Loading into selection engine...")
            selector.load_questions(questions)
            print("✅ Questions loaded into selector")
            
            # 5. Select some questions
            print("\n5. Selecting questions...")
            # Simple selection without complex criteria
            if hasattr(selector, 'questions') and selector.questions:
                # Get first 3 questions as a simple demo
                selected = selector.questions[:3]
                print(f"✅ Selected {len(selected)} questions for demo")
                
                print("\nSelected questions:")
                for i, q in enumerate(selected, 1):
                    text = q.get('question', q.get('text', 'N/A'))[:60]
                    topic = q.get('topic', 'N/A')
                    print(f"  {i}. {text}... (Topic: {topic})")
                
                # 6. Export to Excel
                print("\n6. Exporting to Excel...")
                output_file = "demo_output.xlsx"
                try:
                    generator.generate_spreadsheet(selected, output_file)
                    if os.path.exists(output_file):
                        print(f"✅ Successfully exported to {output_file}")
                        print(f"   File size: {os.path.getsize(output_file)} bytes")
                    else:
                        print("❌ Output file was not created")
                except Exception as e:
                    print(f"❌ Export failed: {e}")
            else:
                print("❌ No questions available for selection")
                
        else:
            print(f"❌ Sample file not found: {sample_file}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎉 Demo completed!")

if __name__ == "__main__":
    main()
