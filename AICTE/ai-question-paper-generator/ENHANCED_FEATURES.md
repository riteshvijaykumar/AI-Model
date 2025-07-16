# 🚀 Enhanced AI Question Paper Generator

## 🎯 New Features Overview

Your AI Question Paper Generator has been **significantly enhanced** with the exact features you requested:

### ✨ Key Enhancements

1. **🎓 Unit-Based Question Selection**
   - Select questions from specific units/topics
   - User specifies which units to include
   - Balanced distribution across selected units

2. **📊 Total Marks-Based Distribution**
   - User specifies total marks for question paper
   - System automatically calculates optimal 2-mark/16-mark distribution
   - Smart allocation based on exam patterns

3. **📝 Word Document Export (.docx)**
   - Professional Word document question papers
   - Same formatting as PDF but in editable format
   - Headers, sections, choice options, answer spaces

4. **📄 Enhanced Input Support**
   - Parse questions from PDF files
   - Parse questions from Word documents
   - Maintains existing CSV, Excel, JSON, TXT support

5. **🔄 Random Question Selection**
   - Intelligent random selection from specified units
   - Ensures proper marks distribution
   - Avoids duplicates and maintains quality

## 🎮 How to Use the Enhanced Features

### Method 1: Interactive CLI (Recommended)

```bash
python main.py --cli
```

Then use the new `unitselect` command:

```
> unitselect
```

### Method 2: Enhanced Demo Script

```bash
python enhanced_demo.py
```

### Method 3: GUI Interface

```bash
streamlit run streamlit_app.py
```

## 📋 Step-by-Step Workflow

### 1. Load Your Question Bank

**Supported Input Formats:**
- CSV files (recommended)
- Excel files (.xlsx, .xls)
- JSON files
- Text files
- **NEW:** PDF files
- **NEW:** Word documents (.docx)

```
> load
Enter path to question bank file: data/enhanced_sample_questions.csv
```

### 2. Unit-Based Selection

```
> unitselect
```

The system will:
1. Show available units from your question bank
2. Ask you to select which units to include
3. Ask for total marks
4. Automatically calculate optimal distribution
5. Randomly select questions from chosen units

**Example:**
```
Available Units/Topics:
  1. Unit 1 (Mathematics basics)
  2. Unit 2 (Science & Physics)
  3. Unit 3 (Programming)
  4. Unit 4 (History & Literature)

Enter unit numbers (comma-separated): 1,2,3
Enter total marks for the question paper: 100

✅ Selection completed!
Selected 15 questions
Total marks: 100
Distribution: {'2_marks': 10, '16_marks': 5}
Choice options: 2
```

### 3. Export Options

```
> export
```

**Export Formats:**
1. Excel (.xlsx)
2. CSV (.csv)
3. PDF Question Paper
4. JSON (.json)
5. Plain Text (.txt)
6. **NEW:** Word Document (.docx)

## 📊 Sample Question Bank Format

Your question bank should include a `unit` column:

```csv
id,question,unit,topic,difficulty,type,marks
1,"What is 2+2?",Unit 1,math,easy,numeric,2
2,"Explain calculus",Unit 1,math,hard,essay,16
3,"Define photosynthesis",Unit 2,biology,medium,essay,16
```

## 🎯 Example Use Cases

### Use Case 1: Mid-term Exam (80 marks)
- Select Units: 1, 2
- Total Marks: 80
- Result: 8 × 2-mark + 4 × 16-mark questions

### Use Case 2: Final Exam (120 marks)
- Select Units: 1, 2, 3, 4
- Total Marks: 120
- Result: 12 × 2-mark + 6 × 16-mark questions

### Use Case 3: Quick Quiz (40 marks)
- Select Units: 1
- Total Marks: 40
- Result: 20 × 2-mark questions

## 📄 Generated Document Features

### Word Document (.docx) Features:
- **Professional Layout**: Standard A4 format with proper margins
- **Header Section**: Title, subject, duration, total marks
- **Section A**: 2-mark questions with answer spaces
- **Section B**: 16-mark questions with choice options
- **Instructions**: Clear exam instructions
- **Editable Format**: Can be modified in Microsoft Word

### Enhanced PDF Features:
- Same professional formatting as before
- Optimized for the new unit-based selection
- Automatic choice option calculation

## 🔧 Technical Details

### Automatic Distribution Algorithm:

```python
def calculate_distribution(total_marks):
    if total_marks <= 50:
        # Small test: mostly 2-mark questions
        two_marks = min(total_marks // 2, 20)
        sixteen_marks = (total_marks - two_marks * 2) // 16
    elif total_marks <= 100:
        # Standard exam: balanced approach
        sixteen_marks = min(total_marks // 20, 4)
        two_marks = (total_marks - sixteen_marks * 16) // 2
    else:
        # Large exam: more 16-mark questions
        sixteen_marks = min(total_marks // 16, 6)
        two_marks = (total_marks - sixteen_marks * 16) // 2
```

### Choice Options Logic:
- For 16-mark questions, automatically provides 2 choice options
- "Choose any one" format
- Extra questions for choices are randomly selected

## 🚀 Installation & Setup

1. **Install Enhanced Dependencies:**
```bash
pip install python-docx PyPDF2 pdfplumber
```

2. **Run Enhanced Demo:**
```bash
python enhanced_demo.py
```

3. **Use Interactive CLI:**
```bash
python main.py --cli
> unitselect
```

## 🎉 Success Metrics

✅ **Unit Selection**: Choose from any combination of available units
✅ **Marks Distribution**: Automatic optimal distribution for any total marks
✅ **Random Selection**: Intelligent random selection ensuring quality
✅ **Word Export**: Professional .docx question papers
✅ **PDF/Word Input**: Parse existing question banks
✅ **Choice Options**: Automatic choice generation for 16-mark questions

## 🔍 Example Output

**Generated Question Paper Structure:**
```
SAMPLE QUESTION PAPER
Subject: Mixed Topics          Duration: 3 Hours
Maximum Marks: 100            Date: _____________

SECTION A - Short Answer Questions (2 Marks Each)
Answer any 10 questions. Each question carries 2 marks.

Q1. What is the capital of France? [2 marks]
_________________________________________________

SECTION B - Long Answer Questions (16 Marks Each)
Answer any 5 questions. Each question carries 16 marks.

Question 1: (Choose any one)
a) Explain object-oriented programming concepts [16 marks]
b) Describe the photosynthesis process [16 marks]

[Answer space for chosen option]
```

## 📞 Support

If you encounter any issues:

1. **Missing Dependencies:**
   ```bash
   pip install python-docx PyPDF2 pdfplumber
   ```

2. **Question Format Issues:**
   - Ensure your CSV has `unit`, `question`, and `marks` columns
   - Use the provided `enhanced_sample_questions.csv` as reference

3. **Export Problems:**
   - Check file permissions
   - Ensure output directory exists

Your enhanced AI Question Paper Generator is now ready to create professional question papers with exactly the features you requested! 🎓✨
