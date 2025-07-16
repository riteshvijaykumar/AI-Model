
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
