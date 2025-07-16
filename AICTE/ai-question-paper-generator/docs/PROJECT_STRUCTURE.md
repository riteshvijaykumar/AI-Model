# 📁 Project Structure

## AI Question Bank Selection System

```
ritesh_project/
├── 📄 main.py                    # Main entry point
├── 🌐 streamlit_app.py          # GUI application
├── 📋 requirements.txt          # Python dependencies
│
├── 📂 src/                      # Source code
│   ├── 📂 data_processing/      # Question parsing modules
│   │   ├── question_parser.py   # Multi-format file parser
│   │   └── __init__.py
│   ├── 📂 selection_engine/     # AI selection logic
│   │   ├── question_selector.py # Question selection algorithms
│   │   ├── filter_manager.py    # Filter management
│   │   ├── criteria_parser.py   # Criteria parsing
│   │   └── __init__.py
│   ├── 📂 export/               # Export functionality
│   │   ├── spreadsheet_generator.py # Multi-format export
│   │   ├── pdf_generator.py     # PDF generation
│   │   └── __init__.py
│   ├── 📂 ui/                   # User interfaces
│   │   ├── cli_interface.py     # Command-line interface
│   │   └── __init__.py
│   └── 📂 utils/                # Utility functions
│       └── __init__.py
│
├── 📂 data/                     # Question bank data
│   └── sample_questions.csv     # Sample question database
│
├── 📂 config/                   # Configuration files
│   └── settings.yaml           # System settings
│
├── 📂 docs/                     # Documentation
│   ├── README.md               # Project overview
│   ├── USER_GUIDE.md           # User manual
│   ├── QUICK_REFERENCE.md      # Quick reference
│   ├── PDF_FEATURES.md         # PDF capabilities
│   ├── USAGE.md                # Usage examples
│   ├── GUI_GUIDE.md            # GUI documentation
│   └── PROJECT_STATUS.md       # Project status
│
├── 📂 examples/                 # Example scripts
│   ├── demo.py                 # Basic demo
│   ├── pdf_demo.py             # PDF demo
│   └── getting_started.py      # Quick start guide
│
├── 📂 exports/                  # Export output directory
│   └── (generated files)       # Excel, PDF, CSV, JSON, TXT outputs
│
└── 📂 tests/                    # Test suite
    └── (test files)             # Unit and integration tests
```

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Demo**:
   ```bash
   python examples/demo.py
   ```

3. **Launch CLI**:
   ```bash
   python main.py
   ```

4. **Launch GUI**:
   ```bash
   streamlit run streamlit_app.py
   ```

## 📋 Supported Formats

### Input Formats
- ✅ CSV (.csv)
- ✅ Excel (.xlsx, .xls)
- ✅ JSON (.json)
- ✅ Plain Text (.txt)
- ✅ PDF (.pdf) - Requires PyPDF2 and pdfplumber

### Output Formats
- ✅ Excel (.xlsx) - Formatted spreadsheets
- ✅ CSV (.csv) - Comma-separated values
- ✅ PDF (.pdf) - Professional question papers
- ✅ JSON (.json) - Structured data with metadata
- ✅ Plain Text (.txt) - Simple, detailed, or exam format

## 🎯 Features

- 🤖 **AI-Powered Selection**: Intelligent question filtering and selection
- 📄 **PDF Question Papers**: Professional exam-style documents
- 🎨 **Multiple Interfaces**: CLI, GUI, and direct script execution
- 📊 **Rich Analytics**: Question distribution and statistics
- 🔧 **Configurable**: Flexible marks distribution and formatting
- 📱 **Cross-Platform**: Windows, macOS, and Linux support

---
*Generated automatically by project organization script*
