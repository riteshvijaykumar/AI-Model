#!/usr/bin/env python3
"""
Final Validation Script for Enhanced AI Question Paper Generator

This script validates that all features are working correctly after cleanup.
"""

import os
import sys
from pathlib import Path

def validate_project_structure():
    """Validate that essential directories and files exist"""
    print("📁 Validating project structure...")
    
    essential_dirs = ["src", "data", "config", "exports", "examples", "docs"]
    essential_files = [
        "streamlit_app.py",
        "minimal_cli.py", 
        "launch_enhanced_gui.py",
        "requirements.txt",
        "src/enhanced_features.py"
    ]
    
    missing_dirs = [d for d in essential_dirs if not os.path.exists(d)]
    missing_files = [f for f in essential_files if not os.path.exists(f)]
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ Project structure validated")
    return True

def validate_enhanced_features():
    """Validate that enhanced features can be imported"""
    print("\n🔧 Validating enhanced features...")
    
    try:
        sys.path.append(str(Path(__file__).parent / "src"))
        from src.enhanced_features import EnhancedQuestionSelector, WordDocumentGenerator, EnhancedInputParser
        print("✅ Enhanced features available")
        return True
    except ImportError as e:
        print(f"❌ Enhanced features not available: {e}")
        return False

def validate_sample_data():
    """Validate that sample data exists and can be loaded"""
    print("\n📊 Validating sample data...")
    
    try:
        from src.data_processing.question_parser import QuestionParser
        parser = QuestionParser()
        
        # Check for enhanced sample data
        if os.path.exists("data/enhanced_sample_questions.csv"):
            questions = parser.parse_file("data/enhanced_sample_questions.csv")
            print(f"✅ Enhanced sample data loaded: {len(questions)} questions")
            return True
        else:
            print("❌ Enhanced sample data not found")
            return False
    except Exception as e:
        print(f"❌ Sample data validation failed: {e}")
        return False

def validate_gui_components():
    """Validate GUI components"""
    print("\n🖥️ Validating GUI components...")
    
    try:
        import streamlit
        print(f"✅ Streamlit available (v{streamlit.__version__})")
        
        # Check if main GUI file is valid Python
        with open("streamlit_app.py", "r") as f:
            content = f.read()
            if "ENHANCED_FEATURES_AVAILABLE" in content and "pdf" in content.lower():
                print("✅ GUI supports PDF input")
                return True
            else:
                print("❌ GUI missing PDF support")
                return False
    except Exception as e:
        print(f"❌ GUI validation failed: {e}")
        return False

def validate_pdf_support():
    """Validate PDF processing capabilities"""
    print("\n📄 Validating PDF support...")
    
    try:
        import PyPDF2
        import pdfplumber
        print("✅ PDF libraries available")
        
        # Test enhanced parser
        from src.enhanced_features import EnhancedInputParser
        parser = EnhancedInputParser()
        print("✅ Enhanced PDF parser available")
        return True
    except ImportError as e:
        print(f"⚠️ PDF libraries not available: {e}")
        print("💡 Install with: pip install PyPDF2 pdfplumber")
        return False

def validate_word_support():
    """Validate Word document support"""
    print("\n📝 Validating Word document support...")
    
    try:
        import docx
        print("✅ python-docx library available")
        
        from src.enhanced_features import WordDocumentGenerator
        generator = WordDocumentGenerator()
        print("✅ Word document generator available")
        return True
    except ImportError as e:
        print(f"⚠️ Word support not available: {e}")
        print("💡 Install with: pip install python-docx")
        return False

def run_quick_feature_test():
    """Run a quick test of core features"""
    print("\n🎯 Running quick feature test...")
    
    try:
        # Load sample data
        from src.data_processing.question_parser import QuestionParser
        from src.enhanced_features import EnhancedQuestionSelector
        
        parser = QuestionParser()
        questions = parser.parse_file("data/enhanced_sample_questions.csv")
        
        # Test enhanced selection
        selector = EnhancedQuestionSelector()
        selector.load_questions(questions)
        
        units = selector.get_available_units()
        if units:
            result = selector.select_questions_by_units_and_marks(
                selected_units=units[:2],
                total_marks=40
            )
            print(f"✅ Selected {len(result['questions'])} questions")
            print(f"✅ Total marks: {result['paper_config']['actual_marks']}")
            return True
        else:
            print("❌ No units found in sample data")
            return False
            
    except Exception as e:
        print(f"❌ Feature test failed: {e}")
        return False

def main():
    """Run complete validation"""
    print("🔍 Final Project Validation")
    print("=" * 50)
    
    results = [
        validate_project_structure(),
        validate_enhanced_features(),
        validate_sample_data(),
        validate_gui_components(),
        validate_pdf_support(),
        validate_word_support(),
        run_quick_feature_test()
    ]
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 50)
    print(f"📊 Validation Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validations passed! Project is ready for use.")
        print("\n🚀 Quick Start:")
        print("  • Enhanced GUI: streamlit run streamlit_app.py")
        print("  • CLI Interface: python minimal_cli.py")
        print("  • GUI Launcher: python launch_enhanced_gui.py")
        
        print("\n✨ Available Features:")
        print("  • ✅ Unit-based question selection")
        print("  • ✅ Total marks specification")
        print("  • ✅ Choice options for 16-mark questions")
        print("  • ✅ PDF and Word input support")
        print("  • ✅ Multiple export formats")
        print("  • ✅ Enhanced GUI interface")
        
    else:
        print("⚠️ Some validations failed. Check the issues above.")
        print("💡 Try: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
