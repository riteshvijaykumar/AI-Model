# 🤖 AI Question Bank Selection System

## 🎉 **PROJECT STATUS: COMPLETED & READY FOR USE** ✅

**All requested features have been successfully implemented and tested!**
- ✅ AI-powered question selection
- ✅ Professional PDF question paper generation  
- ✅ Support for 2-mark and 16-mark questions with choice options
- ✅ Both CLI and GUI interfaces
- ✅ Comprehensive documentation and troubleshooting
- ✅ Multiple export formats (Excel, PDF)
- ✅ Extensive testing and verification

---

## 📋 Overview
An intelligent question selection and exam paper generation system powered by AI. This tool helps educators, content creators, and assessment professionals efficiently select relevant questions from large question banks and generate professional question papers in multiple formats.

## ✨ Key Features

### 🎯 **Intelligent Question Selection**
- **AI-Powered Filtering**: Machine learning-based question relevance scoring
- **Multi-Criteria Selection**: Filter by topic, difficulty, type, keywords, and more
- **Diversity Algorithms**: Ensure balanced question distribution
- **Custom Criteria**: Define your own selection parameters

### 📄 **Professional PDF Generation**
- **Exam-Ready Question Papers**: Professionally formatted PDF documents
- **Flexible Marks System**: Support for 2-mark, 16-mark, and custom marks
- **Choice-Based Questions**: "Choose any one" format for higher-mark questions
- **Custom Headers**: Title, subject, duration, total marks, and date
- **Answer Spaces**: Proper spacing for written responses

### 💻 **Multiple Interfaces**
- **Interactive CLI**: Command-line interface with guided prompts
- **Web GUI**: Streamlit-based graphical interface with charts and visualizations
- **Direct Commands**: One-line command processing
- **Python API**: Use as a library in your applications

### 📊 **Export Formats**
- **Excel (.xlsx)**: Formatted spreadsheets with styling
- **CSV (.csv)**: Plain data for further processing
- **PDF (.pdf)**: Professional question papers with custom layouts

## 🚀 Quick Start

### Installation
```bash
# Clone or download the project
cd e:\PROJECTS\Python_AI\ritesh_project

# Install dependencies
pip install -r requirements.txt

# Test the system
python demo.py
```

### Try It Now!
```bash
# Interactive demo with all features
python getting_started.py

# Generate a PDF exam paper
python main.py --input data/sample_questions.csv --output my_exam.pdf --format pdf

# Launch web interface
streamlit run streamlit_app.py

# Use interactive CLI
python main.py --cli
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[USER_GUIDE.md](USER_GUIDE.md)** | 📚 Complete user manual with step-by-step instructions |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | ⚡ Command cheat sheet and quick examples |
| **[PDF_FEATURES.md](PDF_FEATURES.md)** | 📄 Detailed PDF generation capabilities |
| **[USAGE.md](USAGE.md)** | 🔧 Basic usage instructions and examples |

## 🎮 Usage Examples

### Command Line Examples
```bash
# Basic Excel export with filtering
python main.py --input questions.csv --output selected.xlsx --criteria "topic:math,count:20"

# Generate PDF exam with custom configuration
python main.py --input questions.csv --output exam.pdf --format pdf \
               --marks-config "2marks:15,16marks:5,choices:2" \
               --title "Mathematics Final" --subject "Advanced Math"

# Export filtered CSV data
python main.py --input questions.csv --output data.csv --format csv \
               --criteria "difficulty:medium,type:text,count:25"
```

### Interactive CLI Workflow
```bash
python main.py --cli

> load data/sample_questions.csv
✅ Successfully loaded 50 questions.

> select
Enter selection criteria:
Topic: mathematics
Difficulty: medium
Count: 15
✅ Selected 15 questions.

> export
Choose format: 3 (PDF Question Paper)
[Configure PDF settings...]
✅ PDF exported successfully!
```

### Web GUI Workflow
1. **Launch**: `streamlit run streamlit_app.py`
2. **Upload**: Select your question bank file
3. **Filter**: Set criteria using interactive controls
4. **Select**: Apply AI-powered selection
5. **Export**: Download in your preferred format

## Project Structure

```
├── src/
│   ├── ai_model/
│   │   ├── question_classifier.py    # AI model for question classification
│   │   ├── relevance_scorer.py       # Scoring system for question relevance
│   │   └── model_trainer.py          # Training utilities for the AI model
│   ├── data_processing/
│   │   ├── question_parser.py        # Parse different question bank formats
│   │   ├── data_validator.py         # Validate and clean question data
│   │   └── preprocessor.py           # Text preprocessing utilities
│   ├── selection_engine/
│   │   ├── question_selector.py      # Main selection logic
│   │   ├── filter_manager.py         # Handle various filtering criteria
│   │   └── criteria_parser.py        # Parse user specifications
│   ├── export/
│   │   ├── spreadsheet_generator.py  # Generate Excel/CSV outputs
│   │   └── formatter.py              # Format questions for output
│   └── ui/
│       ├── cli_interface.py          # Command-line interface
│       └── gui_interface.py          # Graphical user interface
├── data/
│   ├── sample_questions.csv          # Sample question bank
│   ├── models/                       # Trained AI models
│   └── templates/                    # Output templates
├── config/
│   ├── settings.yaml                 # Application settings
│   └── criteria_templates.yaml       # Predefined selection criteria
├── tests/
├── requirements.txt
└── main.py
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface
```bash
python main.py --input questions.csv --criteria "difficulty:medium,topic:math" --output selected_questions.xlsx
```

### Python API
```python
from src.selection_engine.question_selector import QuestionSelector

selector = QuestionSelector()
selector.load_question_bank("questions.csv")
selected = selector.select_questions(
    difficulty="medium",
    topic="mathematics",
    count=20
)
selector.export_to_excel("output.xlsx")
```

## Configuration

Edit `config/settings.yaml` to customize:
- AI model parameters
- Default selection criteria
- Output formatting options
- File paths and formats

## License

MIT License
