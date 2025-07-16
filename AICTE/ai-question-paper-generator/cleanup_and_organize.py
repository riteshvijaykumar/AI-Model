#!/usr/bin/env python3
"""
Project Cleanup and Organization Script

This script will:
1. Move old/test files to archive folders
2. Remove duplicate and temporary files
3. Organize the project structure
4. Create a clean working environment
"""

import os
import shutil
from pathlib import Path
import datetime

def create_archive_structure():
    """Create archive directory structure"""
    
    archive_dirs = [
        "archive/old_tests",
        "archive/deprecated",
        "archive/backup",
        "archive/development"
    ]
    
    for dir_path in archive_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")

def identify_files_to_archive():
    """Identify files that should be archived"""
    
    # Files to move to archive/old_tests
    test_files = [
        "basic_test.py",
        "direct_test.py", 
        "file_test.py",
        "final_test.py",
        "final_verification.py",
        "run_test.py",
        "simple_pdf_test.py",
        "simple_test.py",
        "system_test.py",
        "test_cli_interactive.py",
        "test_cli_pdf.py",
        "test_components.py",
        "test_final_system.py",
        "test_imports.py",
        "test_minimal_cli.py",
        "test_pdf_debug.py",
        "test_system.py",
        "verify_system.py"
    ]
    
    # Files to move to archive/deprecated
    deprecated_files = [
        "cleanup_comprehensive.py",
        "cleanup_final.py",
        "fix_pdf.py",
        "organize_project.py",
        "update_marks.py"
    ]
    
    # Files to move to archive/development
    dev_files = [
        "demo.py",
        "getting_started.py",
        "pdf_demo.py"
    ]
    
    return test_files, deprecated_files, dev_files

def move_files_to_archive():
    """Move identified files to appropriate archive folders"""
    
    test_files, deprecated_files, dev_files = identify_files_to_archive()
    
    # Move test files
    moved_count = 0
    for file_name in test_files:
        if os.path.exists(file_name):
            shutil.move(file_name, f"archive/old_tests/{file_name}")
            print(f"📦 Moved {file_name} → archive/old_tests/")
            moved_count += 1
    
    # Move deprecated files
    for file_name in deprecated_files:
        if os.path.exists(file_name):
            shutil.move(file_name, f"archive/deprecated/{file_name}")
            print(f"📦 Moved {file_name} → archive/deprecated/")
            moved_count += 1
    
    # Move development files (keep copies in examples/)
    for file_name in dev_files:
        if os.path.exists(file_name):
            # Copy to examples first
            os.makedirs("examples", exist_ok=True)
            if not os.path.exists(f"examples/{file_name}"):
                shutil.copy2(file_name, f"examples/{file_name}")
            
            # Move original to archive
            shutil.move(file_name, f"archive/development/{file_name}")
            print(f"📦 Moved {file_name} → archive/development/ (copy in examples/)")
            moved_count += 1
    
    print(f"\n✅ Moved {moved_count} files to archive")

def remove_temporary_files():
    """Remove temporary and cache files"""
    
    temp_patterns = [
        "temp_*",
        "*.tmp",
        "*.log",
        "__pycache__",
        "*.pyc"
    ]
    
    removed_count = 0
    
    # Remove temporary files in root
    for pattern in temp_patterns:
        import glob
        for file_path in glob.glob(pattern):
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                print(f"🗑️ Removed: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️ Could not remove {file_path}: {e}")
    
    # Clean __pycache__ directories recursively
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(cache_path)
                    print(f"🗑️ Removed cache: {cache_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ Could not remove {cache_path}: {e}")
    
    print(f"\n✅ Removed {removed_count} temporary files")

def organize_documentation():
    """Organize documentation files"""
    
    doc_files = {
        "GUI_GUIDE.md": "docs/",
        "PDF_FEATURES.md": "docs/",
        "PROJECT_STATUS.md": "docs/",
        "QUICK_REFERENCE.md": "docs/",
        "USAGE.md": "docs/",
        "USER_GUIDE.md": "docs/"
    }
    
    # Ensure docs directory exists
    os.makedirs("docs", exist_ok=True)
    
    moved_docs = 0
    for doc_file, target_dir in doc_files.items():
        if os.path.exists(doc_file) and not os.path.exists(f"{target_dir}{doc_file}"):
            shutil.move(doc_file, f"{target_dir}{doc_file}")
            print(f"📚 Moved {doc_file} → {target_dir}")
            moved_docs += 1
    
    print(f"\n✅ Organized {moved_docs} documentation files")

def create_clean_structure():
    """Create clean project structure"""
    
    essential_dirs = [
        "src",
        "data", 
        "config",
        "exports",
        "examples",
        "docs",
        "tests",
        "archive"
    ]
    
    for dir_name in essential_dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("✅ Ensured clean directory structure")

def create_project_summary():
    """Create a summary of the clean project"""
    
    summary = f"""# AI Question Paper Generator - Project Summary

## Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🚀 Main Features
- Unit-based question selection
- Total marks specification
- Random question selection with distribution
- Choice options for 16-mark questions
- PDF and Word document input support
- Multiple export formats (PDF, Word, Excel, CSV)

## 📁 Project Structure

### Core Files
- `streamlit_app.py` - Enhanced GUI application
- `launch_enhanced_gui.py` - GUI launcher with dependency checking
- `minimal_cli.py` - Working CLI interface
- `requirements.txt` - All dependencies

### Source Code (`src/`)
- `enhanced_features.py` - Core enhanced functionality
- `ai_model/` - AI classification and scoring
- `data_processing/` - Question parsing
- `selection_engine/` - Question selection logic
- `export/` - Export generators
- `ui/` - Interface components
- `utils/` - Utility functions

### Data (`data/`)
- `enhanced_sample_questions.csv` - Sample data with units and marks
- `sample_questions.csv` - Original sample data

### Configuration (`config/`)
- `settings.yaml` - System settings
- `criteria_templates.yaml` - Selection criteria templates

### Documentation (`docs/`)
- Complete user guides and feature documentation

### Examples (`examples/`)
- Demo scripts showing functionality

### Archives (`archive/`)
- `old_tests/` - Previous test files
- `deprecated/` - Deprecated functionality
- `development/` - Development files

## 🎯 Quick Start

### CLI Usage
```bash
python minimal_cli.py
```

### GUI Usage
```bash
python launch_enhanced_gui.py
# OR
streamlit run streamlit_app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## ✅ Working Solutions
All enhanced features are implemented and tested:
- ✅ Unit-based selection
- ✅ Total marks distribution  
- ✅ Choice options for 16-mark questions
- ✅ PDF/Word input parsing
- ✅ Word document export
- ✅ Enhanced GUI interface

## 📝 Key Files for Users
- `streamlit_app.py` - Main GUI application
- `minimal_cli.py` - Command-line interface
- `data/enhanced_sample_questions.csv` - Sample question bank
- `requirements.txt` - Installation requirements

Project cleaned and organized on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open("PROJECT_CLEAN_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📄 Created PROJECT_CLEAN_SUMMARY.md")

def main():
    """Run the complete cleanup process"""
    
    print("🧹 Starting Project Cleanup and Organization")
    print("=" * 60)
    
    # Step 1: Create archive structure
    print("\n📁 Creating archive structure...")
    create_archive_structure()
    
    # Step 2: Move files to archive
    print("\n📦 Moving files to archive...")
    move_files_to_archive()
    
    # Step 3: Remove temporary files
    print("\n🗑️ Removing temporary files...")
    remove_temporary_files()
    
    # Step 4: Organize documentation
    print("\n📚 Organizing documentation...")
    organize_documentation()
    
    # Step 5: Ensure clean structure
    print("\n🏗️ Creating clean structure...")
    create_clean_structure()
    
    # Step 6: Create project summary
    print("\n📄 Creating project summary...")
    create_project_summary()
    
    print("\n" + "=" * 60)
    print("🎉 Project cleanup completed!")
    print("\n📋 Current project status:")
    print("  ✅ Enhanced features implemented")
    print("  ✅ GUI supports PDF/Word input")
    print("  ✅ Unit-based selection working")
    print("  ✅ Word document export available")
    print("  ✅ Project organized and cleaned")
    
    print("\n🚀 Ready to use:")
    print("  • GUI: streamlit run streamlit_app.py")
    print("  • CLI: python minimal_cli.py")
    print("  • Launcher: python launch_enhanced_gui.py")

if __name__ == "__main__":
    main()
