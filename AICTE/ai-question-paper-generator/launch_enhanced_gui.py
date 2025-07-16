#!/usr/bin/env python3
"""
Enhanced GUI Launcher for AI Question Bank Selection System

This launcher includes enhanced features for unit-based question paper generation.
Run this with: python launch_enhanced_gui.py
"""

import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'python-docx',
        'PyPDF2',
        'pdfplumber'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-docx':
                import docx
            elif package == 'PyPDF2':
                import PyPDF2
            elif package == 'pdfplumber':
                import pdfplumber
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_missing_packages(packages):
    """Install missing packages"""
    if packages:
        print(f"Installing missing packages: {', '.join(packages)}")
        for package in packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
    return True

def launch_gui():
    """Launch the enhanced Streamlit GUI"""
    
    print("🚀 AI Question Bank Selection System - Enhanced GUI")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"⚠️ Missing packages: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ").lower().strip()
        
        if response == 'y':
            if not install_missing_packages(missing):
                print("❌ Failed to install some packages. Please install manually.")
                print(f"Run: pip install {' '.join(missing)}")
                return
        else:
            print("❌ Cannot proceed without required packages.")
            print(f"Please install: pip install {' '.join(missing)}")
            return
    
    print("✅ All dependencies satisfied!")
    
    # Check if enhanced sample data exists
    sample_file = Path("data/enhanced_sample_questions.csv")
    if not sample_file.exists():
        print("⚠️ Enhanced sample data not found. Creating sample data...")
        create_sample_data()
    
    # Launch Streamlit
    print("🌐 Launching enhanced GUI...")
    print("📝 Features available:")
    print("  • Unit-based question selection")
    print("  • Total marks specification")
    print("  • Choice options for 16-mark questions")
    print("  • Word document export")
    print("  • PDF question paper generation")
    print("")
    print("🔗 Opening in your default web browser...")
    print("💡 To stop the server, press Ctrl+C in this terminal")
    print("")
    
    try:
        # Run Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'streamlit_app.py',
            '--server.address', 'localhost',
            '--server.port', '8501',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 GUI stopped by user")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")

def create_sample_data():
    """Create enhanced sample data with units and marks"""
    
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
    os.makedirs("data", exist_ok=True)
    
    # Write sample data
    with open("data/enhanced_sample_questions.csv", "w", encoding="utf-8") as f:
        f.write(sample_data)
    
    print("✅ Sample data created: data/enhanced_sample_questions.csv")

if __name__ == "__main__":
    launch_gui()
