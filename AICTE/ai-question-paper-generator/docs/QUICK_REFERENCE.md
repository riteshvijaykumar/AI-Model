# 🚀 Quick Reference Card - AI Question Bank Selection System

## ⚡ Quick Start Commands

### Launch Interfaces
```bash
# Interactive CLI
python main.py

# Web GUI  
streamlit run streamlit_app.py

# Direct processing - ALL FORMATS SUPPORTED
python main.py --input data.csv --output result.xlsx --format excel
python main.py --input data.pdf --output result.json --format json
python main.py --input data.xlsx --output exam.pdf --format pdf
```

## 📋 CLI Commands Cheat Sheet

| Command | What it does | Example |
|---------|--------------|---------|
| `load` | Load question bank | `load data/questions.csv` |
| `select` | Filter questions | Interactive prompts |
| `show` | Display results | Choose display format |
| `export` | Save to file | Choose from 5 formats (Excel/CSV/PDF/JSON/TXT) |
| `stats` | Show statistics | View question distribution |
| `clear` | Reset selection | Clear current results |
| `help` | Show commands | List all options |
| `exit` | Quit program | Close CLI |

## 🎯 Selection Criteria Quick Format

```bash
# Basic criteria format
"topic:VALUE,difficulty:VALUE,count:NUMBER"

# Examples
"topic:math,difficulty:medium,count:20"
"topic:science,type:text,count:15"
"difficulty:easy,count:10"
```

## 📄 PDF Export Quick Config

```bash
# Standard exam (84 marks)
--marks-config "2marks:10,16marks:4,choices:2"

# Extended exam (110 marks)
--marks-config "2marks:15,16marks:5,choices:3"

# Custom title and subject
--title "Final Exam" --subject "Mathematics"
```

## 🔧 One-Line Examples

```bash
# Generate Excel with 20 math questions
python main.py -i data.csv -o math.xlsx -f excel -c "topic:math,count:20"

# Create PDF exam paper
python main.py -i data.csv -o exam.pdf -f pdf -c "count:25" --title "Midterm"

# Export filtered CSV
python main.py -i data.csv -o filtered.csv -f csv -c "difficulty:hard"

# Generate JSON with metadata  
python main.py -i data.xlsx -o questions.json -f json -c "topic:science,count:15"

# Create detailed text file
python main.py -i data.pdf -o summary.txt -f txt -c "count:10"
```

## 📊 File Format Support

| Format | Input | Output | Notes |
|--------|-------|--------|-------|
| CSV | ✅ | ✅ | Comma-separated values |
| Excel | ✅ | ✅ | .xlsx/.xls files |
| JSON | ✅ | ✅ | JavaScript Object Notation with metadata |
| TXT | ✅ | ✅ | Plain text with multiple styles |
| PDF | ❌ | ✅ | Professional question papers (output only) |

## 🎮 GUI Navigation

1. **Upload** → Load your question bank file (CSV, Excel, JSON, TXT)
2. **Filter** → Set selection criteria 
3. **Select** → Apply filters and AI selection
4. **Preview** → Review selected questions
5. **Export** → Download in any of 5 formats (Excel, CSV, PDF, JSON, TXT)

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| File not found | Check file path and permissions |
| PDF parsing fails | `pip install PyPDF2 pdfplumber` |
| PDF export fails | `pip install reportlab` |
| GUI won't start | `pip install streamlit` |
| No output | Check criteria - might be too restrictive |
| Empty export | Ensure questions have proper format and marks column |

## 📁 Required CSV Columns

```csv
id,question,topic,difficulty,type,keywords,answer,marks
1,"Question text",subject,easy,text,"keyword1,keyword2",answer,2
```

**Minimum required**: `id`, `question`, `topic`, `difficulty`  
**Recommended**: All columns for best functionality

## 🎯 Marks Distribution Examples

| Configuration | 2-marks | 16-marks | Total | Use Case |
|---------------|---------|----------|-------|----------|
| Standard | 10 | 4 | 84 | Regular exam |
| Extended | 15 | 5 | 110 | Final exam |
| Short | 8 | 3 | 64 | Quiz/Test |
| Custom | 12 | 6 | 120 | Comprehensive |

## 📞 Help Resources

- **CLI Help**: Type `help` in interactive mode
- **Command Help**: `python main.py --help`
- **Demo Scripts**: `python examples/demo.py` or `python examples/pdf_demo.py`
- **User Guide**: See `USER_GUIDE.md` for detailed instructions
- **Feature Overview**: See `PDF_FEATURES.md` for PDF capabilities

## 🔧 All Format Examples

### Input Format Examples
```bash
# CSV input
python main.py -i questions.csv -o output.pdf -f pdf

# Excel input  
python main.py -i questions.xlsx -o output.json -f json

# JSON input
python main.py -i questions.json -o output.txt -f txt

# Text input
python main.py -i questions.txt -o output.xlsx -f excel

# PDF input (extract questions)
python main.py -i questions.pdf -o output.csv -f csv
```

### Output Format Examples
```bash
# Excel output with formatting
python main.py -i data.csv -o formatted.xlsx -f excel

# CSV for data processing
python main.py -i data.csv -o export.csv -f csv  

# Professional PDF question paper
python main.py -i data.csv -o exam.pdf -f pdf --title "Final Exam"

# JSON with metadata
python main.py -i data.csv -o structured.json -f json

# Text in different styles
python main.py -i data.csv -o simple.txt -f txt    # Detailed style (default)
```

## 📝 Text Format Styles

The TXT export supports 3 different styles:

### Simple Style
```
1. What is the capital of France?
2. Calculate 15 * 23
3. What is the chemical symbol for gold?
```

### Detailed Style (Default)
```
Question 1:
  Text: What is the capital of France?
  Topic: geography
  Difficulty: easy
  Type: text
  Marks: 2
```

### Exam Style
```
Q1. What is the capital of France? (2 marks)
    Answer: Paris

Q2. Calculate 15 * 23 (2 marks)
    Answer: 345
```

---
**Remember**: Start with `python examples/demo.py` to test the system! 🎓

✨ **UPDATED**: Now supports all major formats for both input and output!
📁 **ORGANIZED**: Clean project structure with examples in `/examples` folder!
