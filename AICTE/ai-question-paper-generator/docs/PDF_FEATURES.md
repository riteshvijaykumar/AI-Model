# 🎓 AI Question Bank Selection System - Enhanced with PDF Support

## ✅ **NEW FEATURES ADDED:**

### 📄 PDF Question Paper Generation
- **Professional PDF question papers** with proper formatting
- **Customizable marks distribution** (2 marks, 16 marks, etc.)
- **Choice-based questions** for higher mark questions
- **Formatted exam header** with title, subject, duration, and date
- **Answer spaces** and proper sectioning

### 🔢 Marks Configuration
- **2-mark questions**: Short answer questions
- **16-mark questions**: Long answer questions with choice options
- **Flexible choice options**: Choose 1 from 2, 3, or more options
- **Automatic marks calculation**: Total marks computed automatically

## 🚀 **How to Use PDF Export:**

### 1. Command Line (Direct)
```bash
# Basic PDF export
python main.py --input data/sample_questions.csv --output exam.pdf --format pdf

# Custom marks configuration
python main.py --input data/sample_questions.csv --output custom_exam.pdf \
               --format pdf --marks-config "2marks:15,16marks:5,choices:3" \
               --title "Final Exam" --subject "Computer Science"

# With selection criteria
python main.py --input data/sample_questions.csv --output filtered_exam.pdf \
               --format pdf --criteria "difficulty:medium,count:20"
```

### 2. Interactive CLI
```bash
python main.py --cli
# Then use: export -> choose option 3 (PDF Question Paper)
```

### 3. Demo Script
```bash
python pdf_demo.py
```

## 📋 **PDF Configuration Options:**

### Marks Configuration Format:
- `2marks:X` - Number of 2-mark questions (default: 10)
- `16marks:Y` - Number of 16-mark questions (default: 4)  
- `choices:Z` - Choice options for 16-mark questions (default: 2)

### Example Configurations:
```bash
# Standard exam: 10 x 2-marks + 4 x 16-marks with 2 choices = 84 marks
--marks-config "2marks:10,16marks:4,choices:2"

# Extended exam: 15 x 2-marks + 5 x 16-marks with 3 choices = 110 marks
--marks-config "2marks:15,16marks:5,choices:3"

# Short exam: 8 x 2-marks + 3 x 16-marks with 2 choices = 64 marks
--marks-config "2marks:8,16marks:3,choices:2"
```

## 📝 **PDF Features:**

### Question Paper Structure:
1. **Header Section**:
   - Question paper title
   - Subject name and duration
   - Maximum marks and date
   - Professional formatting

2. **Section A - Short Answer Questions (2 marks each)**:
   - Clear question numbering
   - Marks indication for each question
   - Adequate answer spaces

3. **Section B - Long Answer Questions (16 marks each)**:
   - **Choice-based format**: "Question 1: Choose any one"
   - Multiple options (a, b, c, etc.)
   - Clear instructions for choices
   - Extended answer spaces

4. **Instructions**:
   - General exam instructions
   - Section-specific guidelines
   - Time management tips

### Sample PDF Structure:
```
QUESTION PAPER
Subject: Mathematics          Duration: 3 Hours
Max Marks: 84                Date: 11/07/2025

SECTION A - Short Answer Questions (2 Marks Each)
Answer any 10 questions. Each question carries 2 marks.

Q1. What is the capital of France? [2 marks]
[Answer space]

Q2. Calculate 15 * 23 [2 marks]
[Answer space]

SECTION B - Long Answer Questions (16 Marks Each)
Answer any 4 questions. Each question carries 16 marks.

Question 1: (Choose any one)
a) Write a Python function to find maximum of two numbers [16 marks]
b) Explain the causes of World War I [16 marks]
[Answer space for chosen option]
```

## 🎯 **Generated Files:**
- ✅ `demo_question_paper.pdf` (4,628 bytes) - General knowledge paper
- ✅ `math_question_paper.pdf` (4,491 bytes) - Mathematics focused paper  
- ✅ `test_exam.pdf` (3,352 bytes) - Sample exam with 10 questions

## 📊 **Sample Data with Marks:**
The system now includes marks information in the sample data:
- **2-mark questions**: Basic questions (capitals, simple math, definitions)
- **16-mark questions**: Complex questions (programming, essays, analysis)
- **Automatic assignment**: Based on difficulty and question type

## 🔧 **Technical Features:**
- **PDF Library**: ReportLab for professional formatting
- **Flexible Layout**: Adjustable page sizes and margins
- **Custom Styles**: Different fonts and formatting for sections
- **Table Support**: Structured header information
- **Error Handling**: Comprehensive error checking and logging

## 📈 **Supported Export Formats:**
1. **Excel (.xlsx)** - Spreadsheet format with styling
2. **CSV (.csv)** - Plain text comma-separated values
3. **PDF (.pdf)** - **NEW!** Professional question paper format

## 🎉 **System Status:**
- ✅ **Core functionality**: Working
- ✅ **Excel/CSV export**: Working  
- ✅ **PDF export**: **NEW - Working**
- ✅ **CLI interface**: Enhanced with PDF options
- ✅ **Marks configuration**: **NEW - Working**
- ✅ **Choice questions**: **NEW - Working**

The AI Question Bank Selection System is now a complete solution for creating professional question papers in multiple formats! 🎓
