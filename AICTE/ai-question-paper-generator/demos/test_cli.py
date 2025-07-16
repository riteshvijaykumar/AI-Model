#!/usr/bin/env python3
"""
Test CLI interface with enhanced features
"""

import sys
import os
from pathlib import Path

# Add src to path (go up one level from demos to project root)
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent.parent / "src"))

def test_cli_integration():
    print("🎮 Testing CLI Integration")
    print("=" * 40)
    
    try:
        from src.ui.cli_interface import CLIInterface
        
        # Initialize CLI
        cli = CLIInterface()
        
        # Test loading enhanced sample questions
        print("1. Loading enhanced sample questions...")
        cli.current_questions = []
        
        from src.data_processing.question_parser import QuestionParser
        parser = QuestionParser()
        # Use absolute path from project root
        project_root = Path(__file__).parent.parent
        sample_file = project_root / "data" / "enhanced_sample_questions.csv"
        questions = parser.parse_file(str(sample_file))
        
        cli.current_questions = questions
        cli.selector.load_questions(questions)
        
        if hasattr(cli, 'enhanced_selector') and cli.enhanced_selector:
            cli.enhanced_selector.load_questions(questions)
            print("✅ Enhanced selector loaded")
        
        print(f"✅ Loaded {len(questions)} questions")
        
        # Test getting units
        if cli.enhanced_selector:
            units = cli.enhanced_selector.get_available_units()
            print(f"✅ Found {len(units)} units: {units}")
        
        print("\n🎉 CLI integration test passed!")
        print("\n💡 To use interactively:")
        print("   python main.py --cli")
        print("   > load")
        print("   > unitselect")
        print("   > export")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_cli_integration()
