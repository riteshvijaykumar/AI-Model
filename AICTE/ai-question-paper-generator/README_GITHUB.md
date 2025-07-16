# 🤖 Enhanced AI Question Paper Generator

An intelligent question paper generation system with advanced unit-based selection, marks distribution, and multi-format support including PDF input processing.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.25+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Key Features

### 🎯 Advanced Question Selection
- **Unit-Based Selection**: Choose questions from specific units/topics
- **Marks Distribution**: Automatic distribution of 2-mark and 16-mark questions
- **Random Selection**: Intelligent random selection maintaining requirements
- **Choice Options**: Automatic choice questions for 16-mark questions

### 📄 Multi-Format Input Support
- ✅ CSV files
- ✅ Excel spreadsheets (.xlsx, .xls)
- ✅ **PDF documents** (automatic text extraction)
- ✅ **Word documents** (.docx)
- ✅ JSON format
- ✅ Plain text files

### 📤 Professional Export Formats
- ✅ **Professional Word documents** (.docx) with formatting
- ✅ PDF question papers
- ✅ Excel spreadsheets
- ✅ CSV files
- ✅ JSON format

### 🖥️ Multiple Interfaces
- **Enhanced GUI**: Modern Streamlit web interface with PDF support
- **CLI Interface**: Command-line tool for automation
- **Interactive Launcher**: Dependency checking and setup

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-question-paper-generator.git
cd ai-question-paper-generator

# Install dependencies
pip install -r requirements.txt
```

### Launch Options

```bash
# Option 1: Enhanced GUI (Recommended)
streamlit run streamlit_app.py

# Option 2: CLI Interface
python minimal_cli.py

# Option 3: GUI Launcher with checks
python launch_enhanced_gui.py
```

## 📖 Usage Guide

### 🖥️ GUI Interface

1. **Upload Question Bank**
   - Drag & drop CSV, Excel, PDF, or Word files
   - Use sample data: `data/enhanced_sample_questions.csv`

2. **Select Generation Mode**
   - **Standard Selection**: Traditional criteria-based selection
   - **Unit-Based Paper**: Advanced unit and marks-based generation

3. **Configure Paper**
   - Select units (e.g., Unit 1, Unit 2)
   - Set total marks (e.g., 60 marks)
   - Choose export format

4. **Generate & Export**
   - Preview question paper with choice options
   - Export as Word document, PDF, or Excel

### 💻 CLI Interface

```bash
# Interactive CLI
python minimal_cli.py

# Follow prompts:
# 1. Load question bank
# 2. Select units
# 3. Specify total marks
# 4. Export format selection
```

## 📊 Sample Question Bank Format

```csv
question,unit,marks,topic,difficulty,type,answer
"What is Python?","Unit 1",2,"Programming","easy","mcq","A programming language"
"Explain OOP concepts","Unit 1",16,"Programming","medium","long","Object-oriented programming refers to..."
"Define variables","Unit 1",2,"Programming","easy","short","Variables store data values"
"Compare lists and tuples","Unit 2",16,"Data Structures","medium","long","Lists are mutable while tuples..."
```

### Required Columns
- `question`: Question text
- `unit`: Unit identifier (Unit 1, Unit 2, etc.)
- `marks`: Question marks (2 or 16)
- `topic`: Subject area
- `difficulty`: easy/medium/hard
- `type`: Question type
- `answer`: Expected answer

## 🏗️ Project Structure

```
├── streamlit_app.py              # Main GUI application
├── minimal_cli.py                # CLI interface
├── launch_enhanced_gui.py        # GUI launcher
├── requirements.txt              # Dependencies
├── src/
│   ├── enhanced_features.py      # Core enhanced functionality
│   ├── ai_model/                 # AI classification
│   ├── data_processing/          # Question parsing (PDF/Word support)
│   ├── selection_engine/         # Selection algorithms
│   ├── export/                   # Export generators
│   └── ui/                       # Interface components
├── data/
│   └── enhanced_sample_questions.csv
├── config/                       # Configuration
├── examples/                     # Demo scripts
├── docs/                         # Documentation
└── exports/                      # Generated papers
```

## 🎯 Example: Unit-Based Generation

```python
from src.enhanced_features import EnhancedQuestionSelector

# Initialize selector
selector = EnhancedQuestionSelector()
selector.load_questions(questions)

# Generate question paper
result = selector.select_questions_by_units_and_marks(
    selected_units=["Unit 1", "Unit 2", "Unit 3"],
    total_marks=100
)

# Output:
# - 10 questions × 2 marks = 20 marks
# - 5 questions × 16 marks = 80 marks
# - Total: 100 marks
# - Choice options added for 16-mark questions
```

## 📝 Requirements

```
streamlit>=1.25.0      # Web interface
pandas>=2.0.3          # Data processing
python-docx>=0.8.11    # Word documents
PyPDF2>=3.0.1          # PDF processing
pdfplumber>=0.10.3     # Enhanced PDF extraction
plotly>=5.15.0         # Visualizations
openpyxl>=3.1.2        # Excel files
scikit-learn>=1.3.0    # ML components
transformers>=4.30.2   # NLP models
```

## 🔧 Advanced Configuration

### PDF Processing
- Automatic text extraction from uploaded PDFs
- Question parsing using pattern recognition
- Support for various PDF formats

### Word Document Handling
- Parse .docx question banks
- Generate professional formatted question papers
- Customizable templates and styling

### AI-Powered Features
- Question classification and tagging
- Relevance scoring for better selection
- Smart distribution algorithms

## 🎉 Features in Action

### Unit Selection
![Unit Selection](docs/images/unit-selection.png)

### Marks Distribution
- Specify total marks: **60**
- Auto-distribution: **6 × 2-marks + 3 × 16-marks = 60 marks**

### Choice Options
```
5. Explain object-oriented programming concepts. (16 marks)
OR
5. Describe inheritance and polymorphism in Python. (16 marks)
```

### Export Formats
- **Word**: Professional formatting with headers, instructions, answer spaces
- **PDF**: Print-ready question papers
- **Excel**: Structured data for analysis

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- 📖 Check [Documentation](docs/)
- 💻 Review [Examples](examples/)
- 🐛 Report issues on GitHub
- 💬 Discussions and questions welcome

## 🏆 Acknowledgments

- Built with modern Python ecosystem
- Streamlit for beautiful web interfaces
- Contributors and testers

---

**🎓 Made for educators, by developers who care about education**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/ai-question-paper-generator?style=social)](https://github.com/yourusername/ai-question-paper-generator/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/ai-question-paper-generator?style=social)](https://github.com/yourusername/ai-question-paper-generator/network/members)
