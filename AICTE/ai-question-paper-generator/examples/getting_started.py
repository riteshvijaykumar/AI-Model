#!/usr/bin/env python3
"""
Getting Started Demo - AI Question Bank Selection System

This script demonstrates all major features of the system:
- CLI interface
- Direct command processing  
- PDF generation with marks configuration
- Excel and CSV export
- Question filtering and selection
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a step description"""
    print(f"\n📍 Step {step_num}: {description}")
    print("-" * 40)

def run_command(command, description):
    """Run a command and show the description"""
    print(f"Running: {command}")
    print(f"Purpose: {description}\n")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Command completed successfully")
            if result.stdout:
                # Show first few lines of output
                lines = result.stdout.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"   {line}")
                if len(result.stdout.split('\n')) > 5:
                    print("   ...")
        else:
            print("❌ Command failed")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}...")
    except subprocess.TimeoutExpired:
        print("⏱️ Command timed out (this is normal for GUI launches)")
    except Exception as e:
        print(f"❌ Error running command: {e}")

def main():
    """Main demo function"""
    print_header("AI Question Bank Selection System - Getting Started Demo")
    
    print("""
This demo will show you how to use all features of the system:

1. 📊 Basic system test
2. 📝 Excel export  
3. 📄 PDF question paper generation
4. 💻 CLI interface demo
5. 🌐 GUI interface launch
6. ⚙️ Advanced configuration examples

Let's get started! 🚀
    """)
    
    input("Press Enter to continue...")
    
    # Step 1: Basic system test
    print_step(1, "Testing Basic System Functionality")
    run_command(
        "python demo.py",
        "Load sample data, select questions, and export to Excel"
    )
    
    # Step 2: Excel export with criteria
    print_step(2, "Excel Export with Filtering")
    run_command(
        'python main.py --input data/sample_questions.csv --output demo_excel.xlsx --criteria "difficulty:medium,count:10"',
        "Export 10 medium difficulty questions to Excel format"
    )
    
    # Step 3: CSV export
    print_step(3, "CSV Export")
    run_command(
        'python main.py --input data/sample_questions.csv --output demo_data.csv --format csv --criteria "topic:mathematics,count:5"',
        "Export 5 mathematics questions to CSV format"
    )
    
    # Step 4: PDF generation - basic
    print_step(4, "Basic PDF Question Paper")
    run_command(
        'python main.py --input data/sample_questions.csv --output basic_exam.pdf --format pdf --criteria "count:15"',
        "Generate a basic PDF question paper with 15 questions"
    )
    
    # Step 5: PDF generation - advanced
    print_step(5, "Advanced PDF with Custom Configuration")
    run_command(
        'python main.py --input data/sample_questions.csv --output advanced_exam.pdf --format pdf --criteria "count:20" --marks-config "2marks:12,16marks:4,choices:3" --title "Advanced Mathematics Exam" --subject "Mathematics"',
        "Generate advanced PDF with custom marks distribution and metadata"
    )
    
    # Step 6: Show generated files
    print_step(6, "Checking Generated Files")
    
    files_to_check = [
        "demo_excel.xlsx",
        "demo_data.csv", 
        "basic_exam.pdf",
        "advanced_exam.pdf"
    ]
    
    print("Generated files:")
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} ({size:,} bytes)")
        else:
            print(f"❌ {filename} (not found)")
    
    # Step 7: CLI Demo
    print_step(7, "CLI Interface Demo")
    print("""
To try the interactive CLI interface, run:
    python main.py --cli

Available commands in CLI:
- load data/sample_questions.csv
- select (then follow prompts)
- show
- export
- stats
- help
- exit
    """)
    
    choice = input("Launch CLI now? (y/n): ").lower()
    if choice == 'y':
        print("Launching CLI interface...")
        run_command(
            "python main.py --cli",
            "Interactive command-line interface"
        )
    
    # Step 8: GUI Demo
    print_step(8, "GUI Interface Demo")
    print("""
To try the web-based GUI interface, run:
    streamlit run streamlit_app.py

The GUI will open in your web browser with features:
- File upload interface
- Visual question filtering
- Interactive charts and statistics
- Point-and-click export options
    """)
    
    choice = input("Launch GUI now? (y/n): ").lower()
    if choice == 'y':
        print("Launching GUI interface...")
        print("This will open in your web browser...")
        run_command(
            "streamlit run streamlit_app.py",
            "Web-based graphical user interface"
        )
    
    # Step 9: Advanced Examples
    print_step(9, "Advanced Usage Examples")
    
    print("""
📚 Advanced Command Examples:

1. Filter by multiple topics:
   python main.py -i data.csv -o multi_topic.xlsx -c "topic:math|science,count:20"

2. Difficulty-based selection:
   python main.py -i data.csv -o easy_questions.pdf -f pdf -c "difficulty:easy,count:15"

3. Question type filtering:
   python main.py -i data.csv -o code_questions.xlsx -c "type:code,count:10"

4. Complex PDF configuration:
   python main.py -i data.csv -o complex_exam.pdf -f pdf \\
                  --marks-config "2marks:20,16marks:8,choices:4" \\
                  --title "Comprehensive Final" --subject "Computer Science"

5. Keyword-based selection:
   python main.py -i data.csv -o keyword_filtered.csv -f csv \\
                  -c "keywords:python,count:15"
    """)
    
    # Final summary
    print_header("Demo Complete! 🎉")
    
    print("""
✅ System successfully tested!

📁 Files Created:
- Excel exports with filtering
- CSV data files  
- PDF question papers (basic and advanced)
- Demo outputs

🔗 Next Steps:
1. Read the USER_GUIDE.md for detailed instructions
2. Check QUICK_REFERENCE.md for command shortcuts
3. Explore PDF_FEATURES.md for PDF-specific options
4. Try the CLI with: python main.py --cli
5. Try the GUI with: streamlit run streamlit_app.py

📊 Your question bank system is ready to use!

💡 Tips:
- Use your own CSV files by replacing data/sample_questions.csv
- Customize PDF layouts with different marks configurations
- Combine multiple criteria for precise question selection
- Use the GUI for visual question bank management

Happy question banking! 🎓📚
    """)

if __name__ == "__main__":
    main()
