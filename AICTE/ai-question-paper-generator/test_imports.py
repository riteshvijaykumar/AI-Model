#!/usr/bin/env python3
"""
Test CLI import step by step
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    print("Testing imports step by step...")
    
    try:
        print("1. Testing basic imports...")
        import sys, os, logging
        from pathlib import Path
        print("✅ Basic imports OK")
        
        print("2. Testing click...")
        import click
        print("✅ Click OK")
        
        print("3. Testing data processing...")
        from src.data_processing.question_parser import QuestionParser
        print("✅ Question parser OK")
        
        print("4. Testing selection engine...")
        from src.selection_engine.question_selector import QuestionSelector
        print("✅ Question selector OK")
        
        print("5. Testing export...")
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        print("✅ Spreadsheet generator OK")
        
        print("6. Testing CLI interface...")
        from src.ui.cli_interface import CLIInterface
        print("✅ CLI interface OK")
        
        print("\n🎉 All imports successful!")
        print("CLI should work now. Try: python main.py --cli")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_imports()
