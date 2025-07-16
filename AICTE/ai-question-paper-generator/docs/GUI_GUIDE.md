# 🌐 GUI Interface Guide

## 🚀 How to Launch the GUI

The AI Question Bank Selection System includes a beautiful web-based GUI built with Streamlit.

### Method 1: Using the Launcher Script (Recommended)
```bash
python launch_gui.py
```

### Method 2: Direct Streamlit Command
```bash
streamlit run streamlit_app.py
```

### Method 3: Through Main Application
```bash
python main.py --gui
```

## 🌟 GUI Features

### 📂 **Load Data Tab**
- Upload CSV, Excel, JSON, or TXT files
- Preview loaded question data
- Load sample data with one click
- View data statistics

### 🎯 **Select Questions Tab**
- Interactive criteria selection
- Multi-select filters for:
  - Topics
  - Difficulty levels
  - Question types
  - Keywords
- Advanced filtering options
- Real-time selection preview

### 📊 **Analytics Tab**
- Question bank statistics
- Interactive visualizations
- Topic distribution charts
- Difficulty level analysis
- Question type breakdowns

### 📥 **Export Tab**
- Export selected questions to Excel or CSV
- Download functionality
- Custom filename options
- Multiple format support

## 🎨 User Interface

The GUI provides a modern, intuitive interface with:
- ✅ Responsive design
- 🎨 Clean, professional layout
- 📱 Mobile-friendly interface
- 🔍 Real-time search and filtering
- 📊 Interactive charts and graphs
- 💾 Easy export functionality

## 🌐 Accessing the Interface

1. Run one of the launch commands above
2. Your default web browser will open automatically
3. Navigate to: http://localhost:8501
4. Start using the application!

## 🛠️ Troubleshooting

### If the GUI doesn't start:
1. Ensure Streamlit is installed: `pip install streamlit`
2. Check that port 8501 is available
3. Try the alternative launch methods

### If you see warnings about ScriptRunContext:
- These are normal when running through Python directly
- Use `streamlit run streamlit_app.py` instead

### For best experience:
- Use a modern web browser (Chrome, Firefox, Safari, Edge)
- Ensure JavaScript is enabled
- Clear browser cache if you encounter issues

## 🎯 Quick Start with GUI

1. **Launch**: `python launch_gui.py`
2. **Load Data**: Click "Load Sample Data" in the sidebar
3. **Select Questions**: Go to "Select Questions" tab, set criteria, click "Select Questions"
4. **Export**: Go to "Export" tab, click "Export Questions"

That's it! You now have a selected set of questions exported to Excel format.

## 📸 Screenshots

The GUI includes:
- Modern sidebar with system status
- Tabbed interface for different functions
- Interactive charts and visualizations
- Real-time data preview
- Professional export options

Enjoy using the AI Question Bank Selection System! 🤖✨
