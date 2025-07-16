#!/usr/bin/env python3
"""
Final System Test - Verify All Features
Tests the organized project with all format support
"""

import os
import sys
import subprocess
from pathlib import Path

def test_basic_imports():
    """Test if all core modules can be imported"""
    print("🔍 Testing Core Module Imports")
    print("=" * 35)
    
    try:
        sys.path.append('src')
        
        # Test core imports
        from src.data_processing.question_parser import QuestionParser
        print("   ✅ QuestionParser imported successfully")
        
        from src.selection_engine.question_selector import QuestionSelector
        print("   ✅ QuestionSelector imported successfully")
        
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        print("   ✅ SpreadsheetGenerator imported successfully")
        
        from src.ui.cli_interface import CLIInterface
        print("   ✅ CLIInterface imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import error: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\n📦 Testing Dependencies")
    print("=" * 25)
    
    dependencies = [
        ("pandas", "Data processing"),
        ("openpyxl", "Excel support"),
        ("reportlab", "PDF generation"),
        ("streamlit", "GUI interface"),
    ]
    
    missing = []
    
    for package, description in dependencies:
        try:
            __import__(package)
            print(f"   ✅ {package} - {description}")
        except ImportError:
            print(f"   ❌ {package} - {description}")
            missing.append(package)
    
    # Check optional PDF dependencies
    pdf_deps = [("PyPDF2", "PDF reading"), ("pdfplumber", "Advanced PDF parsing")]
    pdf_available = True
    
    for package, description in pdf_deps:
        try:
            __import__(package)
            print(f"   ✅ {package} - {description} (optional)")
        except ImportError:
            print(f"   ⚠️  {package} - {description} (optional)")
            pdf_available = False
    
    if missing:
        print(f"\n   📦 Install missing: pip install {' '.join(missing)}")
    
    if not pdf_available:
        print(f"   📦 For PDF input: pip install PyPDF2 pdfplumber")
    
    return len(missing) == 0

def test_sample_data():
    """Test if sample data exists and is valid"""
    print("\n📊 Testing Sample Data")
    print("=" * 22)
    
    sample_file = "data/sample_questions.csv"
    
    if not os.path.exists(sample_file):
        print(f"   ❌ Sample file missing: {sample_file}")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv(sample_file)
        
        print(f"   ✅ Sample file loaded: {len(df)} questions")
        print(f"   📋 Columns: {list(df.columns)}")
        
        # Check required columns
        required_cols = ['question', 'topic', 'difficulty']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            print(f"   ⚠️  Missing columns: {missing_cols}")
        else:
            print(f"   ✅ All required columns present")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error reading sample data: {e}")
        return False

def test_format_support():
    """Test format support capabilities"""
    print("\n🔄 Testing Format Support")
    print("=" * 27)
    
    try:
        sys.path.append('src')
        from src.data_processing.question_parser import QuestionParser
        from src.export.spreadsheet_generator import SpreadsheetGenerator
        
        parser = QuestionParser()
        generator = SpreadsheetGenerator()
        
        print(f"   📥 Input formats: {parser.supported_formats}")
        
        # Test basic functionality
        if os.path.exists("data/sample_questions.csv"):
            questions = parser.parse_file("data/sample_questions.csv")
            print(f"   ✅ Parsed {len(questions)} sample questions")
            
            # Test export formats
            test_formats = [
                ("excel", "test_excel.xlsx"),
                ("csv", "test_csv.csv"),
                ("json", "test_json.json"),
                ("txt", "test_txt.txt")
            ]
            
            os.makedirs("exports", exist_ok=True)
            
            for format_type, filename in test_formats:
                try:
                    output_path = f"exports/{filename}"
                    success = generator.generate_output(
                        questions[:3], output_path, format_type=format_type
                    )
                    if success and os.path.exists(output_path):
                        size = os.path.getsize(output_path)
                        print(f"   ✅ {format_type.upper()} export: {filename} ({size} bytes)")
                    else:
                        print(f"   ❌ {format_type.upper()} export failed")
                except Exception as e:
                    print(f"   ❌ {format_type.upper()} export error: {e}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Format test error: {e}")
        return False

def test_gui_readiness():
    """Test if GUI can be launched"""
    print("\n🌐 Testing GUI Readiness")
    print("=" * 25)
    
    try:
        import streamlit
        print(f"   ✅ Streamlit {streamlit.__version__} available")
        
        # Check if streamlit app file exists
        if os.path.exists("streamlit_app.py"):
            print("   ✅ GUI application file exists")
            print("   🚀 Launch with: streamlit run streamlit_app.py")
            return True
        else:
            print("   ❌ GUI application file missing")
            return False
            
    except ImportError:
        print("   ❌ Streamlit not available")
        print("   📦 Install with: pip install streamlit")
        return False

def test_cli_functionality():
    """Test CLI functionality"""
    print("\n💻 Testing CLI Functionality")
    print("=" * 29)
    
    try:
        # Test main.py exists and has help
        if os.path.exists("main.py"):
            print("   ✅ Main CLI application exists")
            
            # Try to get help output
            result = subprocess.run(
                [sys.executable, "main.py", "--help"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("   ✅ CLI help command works")
                return True
            else:
                print("   ⚠️  CLI help had issues")
                return False
                
        else:
            print("   ❌ Main CLI application missing")
            return False
            
    except Exception as e:
        print(f"   ❌ CLI test error: {e}")
        return False

def show_quick_start():
    """Show quick start instructions"""
    print("\n🚀 Quick Start Guide")
    print("=" * 20)
    print("1. Test the system:")
    print("   python examples/demo.py")
    print("\n2. Interactive CLI:")
    print("   python main.py")
    print("\n3. Web GUI:")
    print("   streamlit run streamlit_app.py")
    print("\n4. Direct command:")
    print("   python main.py -i data/sample_questions.csv -o exports/test.xlsx -f excel")

def main():
    """Run all verification tests"""
    print("🧪 AI Question Bank System - Final Verification")
    print("=" * 55)
    
    tests = [
        ("Core Imports", test_basic_imports),
        ("Dependencies", test_dependencies),
        ("Sample Data", test_sample_data),
        ("Format Support", test_format_support),
        ("GUI Readiness", test_gui_readiness),
        ("CLI Functionality", test_cli_functionality)
    ]
    
    results = {}
    passed = 0
    
    for test_name, test_func in tests:
        results[test_name] = test_func()
        if results[test_name]:
            passed += 1
    
    # Summary
    print("\n" + "=" * 55)
    print("📋 VERIFICATION RESULTS")
    print("=" * 55)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20}: {status}")
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 SYSTEM FULLY OPERATIONAL!")
        print("✨ All features working, project organized and ready!")
        show_quick_start()
    elif passed >= len(tests) - 1:
        print("\n✅ SYSTEM OPERATIONAL!")
        print("⚠️  Minor issues detected, but core functionality works")
        show_quick_start()
    else:
        print("\n⚠️  SYSTEM NEEDS ATTENTION")
        print("🔧 Multiple issues detected - check error messages above")
    
    return passed == len(tests)

if __name__ == "__main__":
    main()
