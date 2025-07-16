# 🎓 AI Question Paper Generator

An intelligent question paper generation system that creates professional exam papers from question banks with unit-based selection and customizable marks distribution.

## ✨ Features

### 🎯 Core Functionality
- **Unit-Based Selection**: Choose questions from specific units/topics
- **Smart Distribution**: Automatic 2-mark and 16-mark question allocation
- **Random Selection**: Intelligent random question selection from chosen units
- **Choice Options**: Automatic choice generation for 16-mark questions

### 📄 Export Formats
- **PDF**: Professional exam-ready question papers
- **Word Document (.docx)**: Editable question papers
- **Excel (.xlsx)**: Structured question data
- **CSV**: Plain text data format
- **JSON**: Structured data with metadata

### 📥 Input Formats
- **CSV**: Comma-separated values (recommended)
- **Excel**: .xlsx and .xls files
- **JSON**: Structured question data
- **Text**: Plain text files
- **PDF**: Parse existing question banks *(experimental)*
- **Word**: Parse .docx question banks *(experimental)*

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Interactive CLI (Recommended)
```bash
python main.py --cli
```

### 3. Unit-Based Question Paper Generation
```
> load
Enter path: data/enhanced_sample_questions.csv

> unitselect
Available Units: Unit 1, Unit 2, Unit 3, Unit 4
Select units: 1,2,3
Total marks: 100
✅ Generated question paper with optimal distribution

> export
Choose format: 6 (Word Document)
✅ Question paper saved as exam.docx
```

### 4. GUI Interface
```bash
streamlit run streamlit_app.py
```

## 📊 Sample Question Bank Format

Your question bank should include these columns:

```csv
id,question,unit,topic,difficulty,type,marks
1,"What is 2+2?",Unit 1,mathematics,easy,numeric,2
2,"Explain calculus principles",Unit 1,mathematics,hard,essay,16
3,"Define photosynthesis",Unit 2,biology,medium,text,16
```

**Required Columns**: `id`, `question`, `unit`, `marks`  
**Recommended Columns**: `topic`, `difficulty`, `type`

## 🎮 Usage Examples

### Example 1: Mathematics Mid-term (80 marks)
```bash
python main.py --cli
> load data/math_questions.csv
> unitselect
Units: 1,2 (Algebra, Calculus)
Marks: 80
Result: 8×2-mark + 4×16-mark questions
```

### Example 2: Comprehensive Final (120 marks)
```bash
> unitselect  
Units: 1,2,3,4 (All units)
Marks: 120
Result: 12×2-mark + 6×16-mark questions
```

### Example 3: Quick Quiz (40 marks)
```bash
> unitselect
Units: 1 (Basic concepts)
Marks: 40
Result: 20×2-mark questions
```

## 📁 Project Structure

```
ritesh_project/
├── 📄 main.py                    # Main CLI application
├── 📄 streamlit_app.py           # Web GUI interface
├── 📄 requirements.txt           # Dependencies
├── 📄 README.md                  # This file
├── 
├── 📁 src/                       # Core source code
│   ├── 📁 data_processing/       # Question parsing
│   ├── 📁 selection_engine/      # AI selection logic
│   ├── 📁 export/               # Export functionality
│   ├── 📁 ui/                   # User interfaces
│   ├── 📁 ai_model/             # ML components
│   ├── 📁 utils/                # Utilities
│   └── 📄 enhanced_features.py   # Enhanced functionality
├── 
├── 📁 data/                      # Sample question banks
│   ├── 📄 sample_questions.csv
│   └── 📄 enhanced_sample_questions.csv
├── 
├── 📁 config/                    # Configuration files
├── 📁 docs/                      # Documentation
├── 📁 demos/                     # Demo scripts
├── 📁 examples/                  # Usage examples
├── 📁 tests/                     # Test files
├── 📁 exports/                   # Generated outputs
└── 📁 archive/                   # Archived files
```

## 🎯 Key Commands

| Command | Description |
|---------|-------------|
| `load` | Load question bank from file |
| `unitselect` | **NEW**: Unit-based selection with marks |
| `select` | Traditional criteria-based selection |
| `show` | Display selected questions |
| `export` | Export to various formats |
| `stats` | Show question bank statistics |
| `help` | Show all commands |

## 📄 Generated Question Paper Structure

### Word Document (.docx) / PDF Format:
```
QUESTION PAPER
Subject: [Subject Name]          Duration: [Duration]
Maximum Marks: [Total]          Date: ___________

INSTRUCTIONS:
1. Read all questions carefully
2. All questions are compulsory
3. Write answers in the space provided

SECTION A - Short Answer Questions (2 Marks Each)
Answer any 10 questions. Each carries 2 marks.

Q1. What is the capital of France? [2 marks]
_________________________________________________

SECTION B - Long Answer Questions (16 Marks Each)
Answer any 5 questions. Each carries 16 marks.

Question 1: (Choose any one)
a) Explain object-oriented programming [16 marks]
b) Describe photosynthesis process [16 marks]

[Answer space for chosen option]
```

## 🔧 Advanced Features

### Smart Distribution Algorithm
- **Small exams (≤50 marks)**: Mostly 2-mark questions
- **Standard exams (51-100 marks)**: Balanced distribution
- **Large exams (>100 marks)**: More 16-mark questions

### Choice Generation
- Automatically generates choice options for 16-mark questions
- "Choose any one" format
- Additional questions selected randomly for choices

## 🆘 Troubleshooting

### Common Issues:
1. **Missing dependencies**: Run `pip install -r requirements.txt`
2. **No questions found**: Check CSV format and file path
3. **Import errors**: Ensure all required packages are installed

### Sample Data:
Use `data/enhanced_sample_questions.csv` to test the system

## 📞 Support

For issues or questions:
1. Check the sample files in `/data/` folder
2. Run demo scripts in `/demos/` folder
3. Review documentation in `/docs/` folder

## 🎉 Ready to Use!

Your AI Question Paper Generator is ready to create professional exam papers with intelligent question selection and multiple export formats.

**Start with**: `python main.py --cli` and use `unitselect` for the enhanced features!
