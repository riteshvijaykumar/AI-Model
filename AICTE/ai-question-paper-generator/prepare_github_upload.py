#!/usr/bin/env python3
"""
GitHub Release Preparation Script

This script prepares your project for GitHub upload by:
1. Checking project structure
2. Validating files
3. Creating release notes
4. Providing Git commands
"""

import os
import subprocess
from pathlib import Path

def check_git_installed():
    """Check if Git is installed"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        print(f"✅ Git installed: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first:")
        print("   https://git-scm.com/downloads")
        return False

def check_essential_files():
    """Check if essential files exist"""
    essential_files = [
        'README_GITHUB.md',
        'LICENSE',
        '.gitignore',
        'requirements.txt',
        'streamlit_app.py',
        'minimal_cli.py'
    ]
    
    missing_files = []
    for file_name in essential_files:
        if not os.path.exists(file_name):
            missing_files.append(file_name)
        else:
            print(f"✅ {file_name}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def create_release_notes():
    """Create release notes"""
    release_notes = """# Release Notes - Enhanced AI Question Paper Generator v1.0

## 🎉 Major Features

### ✨ New in v1.0
- **Unit-Based Question Selection**: Select questions from specific units
- **PDF Input Support**: Upload and parse PDF question banks
- **Word Document Support**: Import .docx files and export professional papers
- **Choice Options**: Automatic choice questions for 16-mark questions
- **Enhanced GUI**: Modern Streamlit interface with advanced features
- **Multiple Export Formats**: Word, PDF, Excel, CSV, JSON support

### 🔧 Technical Improvements
- Clean, organized project structure
- Comprehensive error handling
- Dependency checking and validation
- Professional documentation
- Example data and demonstrations

### 📚 Documentation
- Complete user guides
- API documentation
- Usage examples
- Installation instructions

## 🚀 Quick Start
```bash
git clone https://github.com/yourusername/ai-question-paper-generator.git
cd ai-question-paper-generator
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 💡 Use Cases
- Educational institutions creating exam papers
- Teachers generating practice questions
- Training organizations developing assessments
- Automated question paper generation systems

## 🎯 Highlights
- **Smart Distribution**: Automatic marks calculation and distribution
- **Multi-Format Support**: Handle various input and output formats
- **User-Friendly**: Both GUI and CLI interfaces available
- **Extensible**: Modular architecture for easy enhancement
- **Professional**: Export publication-ready question papers

Ready for production use! 🚀
"""
    
    with open("RELEASE_NOTES.md", "w", encoding="utf-8") as f:
        f.write(release_notes)
    
    print("📝 Created RELEASE_NOTES.md")

def generate_git_commands():
    """Generate Git commands for upload"""
    
    commands = """
# 🚀 GitHub Upload Commands

## Step 1: Initialize Git Repository
cd path/to/your/project
git init

## Step 2: Add all files
git add .

## Step 3: Create initial commit
git commit -m "Initial commit: Enhanced AI Question Paper Generator v1.0

Features:
- Unit-based question selection
- PDF and Word document support
- Professional export formats
- Enhanced GUI with Streamlit
- Complete project organization"

## Step 4: Create GitHub Repository
# Go to https://github.com/new
# Create a new repository named: ai-question-paper-generator
# Choose public or private
# DO NOT initialize with README (we have our own)

## Step 5: Connect to GitHub
git branch -M main
git remote add origin https://github.com/YOURUSERNAME/ai-question-paper-generator.git

## Step 6: Push to GitHub
git push -u origin main

## Step 7: Create Release (Optional)
# Go to your GitHub repository
# Click "Releases" -> "Create a new release"
# Tag version: v1.0.0
# Release title: "Enhanced AI Question Paper Generator v1.0"
# Copy content from RELEASE_NOTES.md

## Step 8: Additional Setup (Optional)
# Add topics/tags for discoverability:
# - python
# - streamlit
# - education
# - question-paper
# - ai
# - pdf-processing
# - exam-generator

# Enable GitHub Pages for documentation (if desired)
# Settings -> Pages -> Source: Deploy from branch -> main -> /docs
"""
    
    with open("GITHUB_UPLOAD_COMMANDS.md", "w", encoding="utf-8") as f:
        f.write(commands)
    
    print("📋 Created GITHUB_UPLOAD_COMMANDS.md")

def main():
    """Run GitHub preparation"""
    print("🚀 Preparing Project for GitHub Upload")
    print("=" * 50)
    
    # Check Git
    if not check_git_installed():
        return
    
    # Check files
    print("\n📁 Checking essential files...")
    if not check_essential_files():
        print("❌ Please ensure all essential files are present")
        return
    
    # Create release notes
    print("\n📝 Creating release documentation...")
    create_release_notes()
    
    # Generate commands
    print("\n📋 Generating Git commands...")
    generate_git_commands()
    
    print("\n" + "=" * 50)
    print("✅ Project ready for GitHub upload!")
    
    print("\n🎯 Next Steps:")
    print("1. Read GITHUB_UPLOAD_COMMANDS.md")
    print("2. Create GitHub repository at https://github.com/new")
    print("3. Run the Git commands")
    print("4. Upload completed!")
    
    print("\n💡 Tips:")
    print("- Use descriptive repository name: ai-question-paper-generator")
    print("- Add topics: python, streamlit, education, ai")
    print("- Consider making it public to share with community")
    print("- Add a good repository description")

if __name__ == "__main__":
    main()
