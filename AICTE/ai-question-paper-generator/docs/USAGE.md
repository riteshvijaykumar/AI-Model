# 🤖 AI Question Bank Selection System - Quick Start Guide

## ✅ System Status: WORKING ✅

The AI Question Bank Selection System is now fully operational! 

## 📁 Generated Output Files
- `selected_questions.xlsx` - Questions selected using the main CLI
- `test_output.xlsx` - Output from system tests
- `demo_output.xlsx` - Output from the demo script

## 🚀 How to Run the System

### 1. Command Line Interface (Interactive)
```bash
python main.py --cli
```
This opens an interactive CLI where you can use commands like:
- `load data/sample_questions.csv` - Load questions
- `select topic:math count:10` - Select questions
- `export output.xlsx` - Export to Excel
- `help` - Show all commands

### 2. Direct Processing
```bash
python main.py --input data/sample_questions.csv --output my_output.xlsx --criteria "count:10"
```

### 3. GUI Interface
```bash
python main.py --gui
# OR
python launch_gui.py
```

### 4. Demo Script
```bash
python demo.py
```

## 📊 Available Sample Data
- `data/sample_questions.csv` - 50 sample questions across various topics
- Topics include: geography, mathematics, chemistry, programming, history, science, astronomy, biology
- Difficulty levels: easy, medium, hard
- Question types: text, numeric, code, essay

## 🔧 Selection Criteria Examples
- `count:20` - Select 20 questions
- `topic:math` - Select math questions  
- `difficulty:medium` - Select medium difficulty
- `topic:science,count:5` - 5 science questions
- `difficulty:easy,topic:geography,count:3` - 3 easy geography questions

## 📈 Key Features Working
✅ Question parsing from CSV files
✅ AI-powered question classification
✅ Multi-criteria selection engine
✅ Excel export functionality
✅ Command-line interface
✅ GUI interface (Streamlit-based)
✅ Interactive CLI with help system
✅ Batch processing capabilities

## 🎯 Next Steps
1. Add your own question bank CSV files to the `data/` folder
2. Customize selection criteria in `config/criteria_templates.yaml`
3. Train custom AI models using `python -c "from src.ai_model.model_trainer import ModelTrainer; trainer = ModelTrainer(); trainer.train_models()"`
4. Explore advanced filtering options

## 🔍 System Architecture
- **Data Processing**: Handles CSV, Excel, JSON, TXT files
- **AI Model**: Uses sklearn, transformers for classification
- **Selection Engine**: Multi-criteria filtering and scoring
- **Export**: Excel generation with formatting
- **UI**: Both CLI and web-based GUI interfaces

## 🛠️ Troubleshooting
If you encounter issues:
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Check that sample data exists: `data/sample_questions.csv`
3. Run the demo script to verify functionality: `python demo.py`
4. Check logs in the `logs/` directory

The system is ready for production use! 🎉
