# 📖 AI Question Bank Selection System - Complete User Guide

## 🎯 Overview
The AI Question Bank Selection System is a powerful tool that helps educators and content creators intelligently select relevant questions from large question banks and generate professional question papers in multiple formats (Excel, CSV, PDF).

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ installed
- All dependencies installed (see Installation section)

### Installation
```bash
# Clone or download the project
cd e:\PROJECTS\Python_AI\ritesh_project

# Install dependencies
pip install -r requirements.txt

# Or use the install script (Windows)
install.bat
```

### Test the System
```bash
# Run demo
python demo.py

# Test PDF generation
python pdf_demo.py
```

---

## 🖥️ Command Line Interface (CLI)

### 1. Interactive CLI Mode
Launch the interactive command-line interface:
```bash
python main.py --cli
```

#### Available Commands:

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all available commands | `help` |
| `load` | Load questions from a file | `load data/questions.csv` |
| `select` | Select questions based on criteria | `select topic:math count:20` |
| `show` | Display selected questions | `show` |
| `export` | Export questions to file | `export` |
| `stats` | Show question bank statistics | `stats` |
| `clear` | Clear current selection | `clear` |
| `criteria` | Show last used criteria | `criteria` |
| `train` | Train AI models | `train` |
| `exit` | Exit the program | `exit` |

#### Step-by-Step CLI Workflow:

1. **Load Questions:**
   ```
   > load data/sample_questions.csv
   ✅ Successfully loaded 50 questions.
   ```

2. **Select Questions:**
   ```
   > select
   Enter selection criteria (press Enter to skip):
   Topic (e.g., math, science): mathematics
   Difficulty (easy, medium, hard): medium
   Question type (text, multiple_choice, etc.): 
   Keywords (comma-separated): 
   Number of questions (default 20): 10
   Enable diversity selection? (y/n, default y): y
   ✅ Selected 10 questions.
   ```

3. **Show Selected Questions:**
   ```
   > show
   Display options:
   1. Show all questions
   2. Show summary table
   3. Show first 10 questions
   4. Show by page
   Choose option (1-4): 2
   ```

4. **Export Questions:**
   ```
   > export
   Export Options:
   1. Excel (.xlsx)
   2. CSV (.csv)
   3. PDF Question Paper
   Choose export format (1-3): 3
   ```

### 2. Direct Command Line Mode
Process questions directly without interactive mode:

```bash
# Basic export to Excel
python main.py --input data/sample_questions.csv --output selected.xlsx --criteria "count:20"

# Export to CSV with filtering
python main.py --input data/sample_questions.csv --output filtered.csv \
               --format csv --criteria "difficulty:medium,topic:math,count:15"

# Generate PDF question paper
python main.py --input data/sample_questions.csv --output exam.pdf \
               --format pdf --criteria "count:25" \
               --marks-config "2marks:15,16marks:5,choices:2" \
               --title "Mathematics Exam" --subject "Advanced Mathematics"
```

#### Command Line Arguments:

| Argument | Description | Example |
|----------|-------------|---------|
| `--input`, `-i` | Input question bank file | `--input questions.csv` |
| `--output`, `-o` | Output file path | `--output exam.pdf` |
| `--format`, `-f` | Output format (excel/csv/pdf) | `--format pdf` |
| `--criteria`, `-c` | Selection criteria | `--criteria "topic:math,count:20"` |
| `--marks-config` | PDF marks configuration | `--marks-config "2marks:10,16marks:4"` |
| `--title` | PDF question paper title | `--title "Final Exam"` |
| `--subject` | PDF subject name | `--subject "Mathematics"` |
| `--gui` | Launch GUI interface | `--gui` |
| `--cli` | Launch CLI interface | `--cli` |
| `--verbose`, `-v` | Enable verbose output | `--verbose` |

---

## 🌐 Graphical User Interface (GUI)

### Launch GUI
```bash
# Method 1: Direct Streamlit
streamlit run streamlit_app.py

# Method 2: Through main script
python main.py --gui

# Method 3: Using launcher
python launch_gui.py
```

### GUI Features Overview

#### 1. **Sidebar Navigation**
- **File Upload**: Upload your question bank files
- **Quick Actions**: Load sample data, clear data
- **Settings**: Configure export options

#### 2. **Main Dashboard**
- **Question Bank Statistics**: Visual charts and metrics
- **Data Preview**: Table view of loaded questions
- **Selection Status**: Current selection summary

#### 3. **Question Selection Page**
- **Filter Options**: 
  - Topic selection (dropdown)
  - Difficulty level (radio buttons)
  - Question type (multiselect)
  - Keywords (text input)
  - Number of questions (slider)
- **Advanced Options**:
  - Diversity selection toggle
  - AI-powered recommendations
  - Custom criteria input

#### 4. **Results & Export Page**
- **Selected Questions Preview**: Table with pagination
- **Export Options**:
  - Excel format with styling
  - CSV format for data processing
  - PDF question paper with formatting
- **Download Buttons**: Direct file downloads

#### 5. **Analytics Page**
- **Question Distribution Charts**:
  - Topics distribution (pie chart)
  - Difficulty levels (bar chart)
  - Question types (donut chart)
- **Selection Analytics**:
  - Criteria effectiveness
  - Diversity metrics
  - Quality scores

### GUI Step-by-Step Workflow:

1. **Upload Data:**
   - Click "Upload Question Bank File" in sidebar
   - Select CSV, Excel, JSON, or TXT file
   - Preview loaded data in main area

2. **Configure Selection:**
   - Navigate to "Question Selection" page
   - Set your criteria using the form controls
   - Click "Select Questions" button

3. **Review Selection:**
   - View selected questions in results table
   - Check selection statistics
   - Preview questions before export

4. **Export Results:**
   - Choose export format (Excel/CSV/PDF)
   - Configure PDF settings if applicable
   - Download generated file

---

## 📄 PDF Question Paper Features

### Marks Configuration

#### Standard Exam Format:
- **2-mark questions**: Short answer, objective type
- **16-mark questions**: Long answer, analytical type
- **Choice options**: Multiple questions to choose from

#### Configuration Examples:

```bash
# Standard exam (84 marks total)
--marks-config "2marks:10,16marks:4,choices:2"

# Extended exam (110 marks total)  
--marks-config "2marks:15,16marks:5,choices:3"

# Short exam (64 marks total)
--marks-config "2marks:8,16marks:3,choices:2"
```

### PDF Structure:

1. **Header Section**:
   - Question paper title
   - Subject and duration
   - Maximum marks and date
   - Professional formatting

2. **Section A - Short Answer (2 marks each)**:
   ```
   Q1. What is the capital of France? [2 marks]
   [Answer space]
   
   Q2. Calculate 15 * 23 [2 marks]
   [Answer space]
   ```

3. **Section B - Long Answer (16 marks each)**:
   ```
   Question 1: (Choose any one)
   a) Write a Python function to find maximum [16 marks]
   b) Explain the causes of World War I [16 marks]
   [Answer space for chosen option]
   ```

### PDF CLI Configuration (Interactive):
```
> export
Choose export format (1-3): 3

PDF Question Paper Configuration
================================
Question Paper Title (default: 'Question Paper'): Mathematics Final Exam
Subject Name (default: 'General Knowledge'): Advanced Mathematics  
Exam Duration (default: '3 Hours'): 2.5 Hours

Marks Configuration:
Number of 2-mark questions (default: 10): 12
Number of 16-mark questions (default: 4): 5
Choice options for 16-mark questions (default: 2): 3

Output PDF path: math_final_exam.pdf
```

---

## 📊 Question Bank Format

### Supported Input Formats:
- **CSV**: Comma-separated values
- **Excel**: .xlsx/.xls files
- **JSON**: JavaScript Object Notation
- **TXT**: Plain text with delimiters

### Required Columns:
| Column | Description | Example |
|--------|-------------|---------|
| `id` | Unique question identifier | 1, 2, 3... |
| `question` | Question text | "What is the capital of France?" |
| `topic` | Subject/topic category | mathematics, science, history |
| `difficulty` | Difficulty level | easy, medium, hard |
| `type` | Question type | text, numeric, code, essay |
| `keywords` | Related keywords | "geography,capitals,france" |
| `answer` | Correct answer | Paris |
| `marks` | Question marks value | 2, 5, 16 |

### Sample CSV Format:
```csv
id,question,topic,difficulty,type,keywords,answer,marks
1,What is the capital of France?,geography,easy,text,"geography,capitals,france",Paris,2
2,Calculate 15 * 23,mathematics,easy,numeric,"math,multiplication",345,2
3,Write a Python function to find maximum,programming,medium,code,"python,programming","def max_two(a,b): return a if a > b else b",16
```

---

## 🎯 Selection Criteria

### Basic Criteria:
- **Topic**: Filter by subject/topic
- **Difficulty**: easy, medium, hard
- **Type**: text, numeric, code, essay
- **Count**: Number of questions to select
- **Keywords**: Keyword-based filtering

### Advanced Criteria:
- **Diversity**: Ensure variety in selection
- **AI Scoring**: Use machine learning for relevance
- **Custom Weights**: Prioritize certain criteria

### Criteria Examples:

```bash
# Basic filtering
"topic:mathematics,difficulty:medium,count:20"

# Multiple topics
"topic:math|science,difficulty:easy|medium,count:15"

# Keyword-based
"keywords:python,type:code,count:10"

# Complex criteria
"topic:mathematics,difficulty:medium,type:text|numeric,count:25,diversity:true"
```

---

## 📈 Analytics & Statistics

### Available Metrics:

#### Question Bank Statistics:
- Total questions count
- Topics distribution
- Difficulty levels breakdown  
- Question types analysis
- Average marks distribution

#### Selection Analytics:
- Criteria effectiveness
- Diversity scores
- Quality metrics
- AI confidence levels

### CLI Statistics:
```bash
> stats
Question Bank Statistics
========================
Total Questions: 50
Topics (8):
  mathematics: 12
  science: 8
  geography: 6
  programming: 7
  ...
```

### GUI Analytics:
- Interactive charts and visualizations
- Downloadable reports
- Historical selection tracking
- Performance metrics

---

## 🔧 Advanced Features

### 1. AI Model Training
Train custom models on your question bank:

```bash
# CLI mode
> train
Training AI models...
This may take a few minutes...
✅ Models trained successfully!

# Command line
python main.py --input large_dataset.csv --train-models
```

### 2. Batch Processing
Process multiple files:

```bash
# Process all CSV files in a directory
python batch_process.py --input-dir data/ --output-dir results/
```

### 3. Custom Configurations
Create custom criteria templates:

```yaml
# config/criteria_templates.yaml
standard_exam:
  two_marks: 10
  sixteen_marks: 4
  choices: 2
  
advanced_exam:
  two_marks: 15
  sixteen_marks: 6
  choices: 3
```

### 4. Integration APIs
Use as a Python library:

```python
from src.selection_engine.question_selector import QuestionSelector
from src.export.spreadsheet_generator import SpreadsheetGenerator

# Initialize
selector = QuestionSelector()
generator = SpreadsheetGenerator()

# Load and select
questions = selector.load_from_file('questions.csv')
selected = selector.select_questions(topic='math', count=20)

# Export
generator.generate_output(selected, 'output.pdf', format_type='pdf')
```

---

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Import Errors
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.7+
```

#### 2. File Not Found
```bash
# Verify file path
ls data/sample_questions.csv

# Use absolute path
python main.py --input "C:\full\path\to\questions.csv"
```

#### 3. PDF Generation Fails
```bash
# Install PDF dependencies
pip install reportlab fpdf2

# Check file permissions
# Ensure output directory exists
```

#### 4. GUI Won't Start
```bash
# Install Streamlit
pip install streamlit

# Run directly
streamlit run streamlit_app.py

# Check port availability (default 8501)
```

### Getting Help:
- Run `python main.py --help` for command options
- Use `help` command in CLI mode
- Check log files in `logs/` directory
- Run demo scripts to verify installation

---

## 📝 Examples & Use Cases

### Use Case 1: Teacher Creating Weekly Quiz
```bash
# Load question bank
python main.py --cli
> load data/science_questions.csv
> select topic:biology difficulty:easy count:10
> export quiz_week1.pdf
```

### Use Case 2: Automated Exam Generation
```bash
# Generate final exam with specific format
python main.py --input questions.csv --output final_exam.pdf \
               --format pdf --criteria "count:30" \
               --marks-config "2marks:20,16marks:5,choices:2" \
               --title "Biology Final Exam" --subject "Advanced Biology"
```

### Use Case 3: Research Data Export
```bash
# Export filtered data for analysis
python main.py --input large_dataset.csv --output analysis_data.csv \
               --format csv --criteria "difficulty:hard,type:analytical"
```

### Use Case 4: Interactive Question Review
```bash
# Use GUI for visual question review
streamlit run streamlit_app.py
# Upload file → Filter questions → Review selection → Export
```

---

## 🎉 Conclusion

The AI Question Bank Selection System provides a comprehensive solution for intelligent question selection and professional question paper generation. With support for multiple input/output formats, advanced AI-powered filtering, and both CLI and GUI interfaces, it serves the needs of educators, content creators, and assessment professionals.

### Key Benefits:
- ✅ **Intelligent Selection**: AI-powered question filtering
- ✅ **Multiple Formats**: Excel, CSV, PDF export options
- ✅ **Professional PDFs**: Exam-ready question papers
- ✅ **Flexible Interface**: Both CLI and GUI options
- ✅ **Customizable**: Configurable marks and criteria
- ✅ **Scalable**: Handle large question banks efficiently

**Happy Question Banking! 🎓📚**
