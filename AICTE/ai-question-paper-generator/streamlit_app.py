#!/usr/bin/env python3
"""
Streamlit GUI Application for AI Question Bank Selection System

Run this with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import io
import base64
import sys
import os

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.data_processing.question_parser import QuestionParser
from src.selection_engine.question_selector import QuestionSelector
from src.export.spreadsheet_generator import SpreadsheetGenerator

# Try to import enhanced features
try:
    from src.enhanced_features import EnhancedQuestionSelector, WordDocumentGenerator, EnhancedInputParser
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)

# Page config
st.set_page_config(
    page_title="🤖 AI Question Bank Selection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

class QuestionSelectionApp:
    """Streamlit application for question selection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = QuestionParser()
        self.selector = QuestionSelector()
        self.generator = SpreadsheetGenerator()
        
        # Initialize enhanced components if available
        if ENHANCED_FEATURES_AVAILABLE:
            self.enhanced_selector = EnhancedQuestionSelector()
            self.word_generator = WordDocumentGenerator()
            self.enhanced_parser = EnhancedInputParser()
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize Streamlit session state variables"""
        if 'questions_loaded' not in st.session_state:
            st.session_state.questions_loaded = False
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        if 'selected_questions' not in st.session_state:
            st.session_state.selected_questions = []
        if 'current_file' not in st.session_state:
            st.session_state.current_file = None
    
    def run(self):
        """Main application interface"""
        
        # Header
        st.title("🤖 AI Question Bank Selection System")
        st.markdown("---")
        
        # Sidebar
        self._render_sidebar()
        
        # Main content
        tab1, tab2, tab3, tab4 = st.tabs(["📂 Load Data", "🎯 Select Questions", "📊 Analytics", "📥 Export"])
        
        with tab1:
            self._render_data_loader()
        
        with tab2:
            self._render_question_selector()
        
        with tab3:
            self._render_analytics()
        
        with tab4:
            self._render_export()
    
    def _render_sidebar(self):
        """Render the sidebar with system info and quick actions"""
        with st.sidebar:
            st.header("📋 System Status")
            
            if st.session_state.questions_loaded:
                st.success(f"✅ {len(st.session_state.questions)} questions loaded")
                if st.session_state.selected_questions:
                    st.info(f"🎯 {len(st.session_state.selected_questions)} questions selected")
            else:
                st.warning("⚠️ No questions loaded")
            
            st.markdown("---")
            
            # Quick load sample data
            st.subheader("🚀 Quick Start")
            if st.button("Load Sample Data", type="primary"):
                self._load_sample_data()
            
            # System info
            st.markdown("---")
            st.subheader("ℹ️ About")
            st.write("AI-powered question selection system")
            st.write("Version: 1.0.0")
    
    def _load_sample_data(self):
        """Load sample question data"""
        try:
            sample_file = "data/sample_questions.csv"
            if os.path.exists(sample_file):
                questions = self.parser.parse_file(sample_file)
                self.selector.load_questions(questions)
                
                st.session_state.questions = questions
                st.session_state.questions_loaded = True
                st.session_state.current_file = sample_file
                
                st.success(f"✅ Loaded {len(questions)} sample questions!")
                st.rerun()
            else:
                st.error(f"❌ Sample file not found: {sample_file}")
        except Exception as e:
            st.error(f"❌ Error loading sample data: {str(e)}")
    
    def _render_data_loader(self):
        """Render the data loading interface"""
        st.header("📂 Load Question Bank")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload your question bank file",
            type=['csv', 'xlsx', 'json', 'txt', 'pdf', 'docx'],
            help="Supported formats: CSV, Excel, JSON, TXT, PDF, Word"
        )
        
        if uploaded_file is not None:
            try:
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Parse the file based on extension
                file_extension = uploaded_file.name.lower().split('.')[-1]
                
                if file_extension == 'pdf':
                    # Parse PDF file
                    if ENHANCED_FEATURES_AVAILABLE and hasattr(self, 'enhanced_parser'):
                        questions = self.enhanced_parser.parse_pdf_questions(temp_path)
                    else:
                        st.error("❌ PDF parsing not available. Install requirements: pip install PyPDF2 pdfplumber")
                        questions = []
                
                elif file_extension == 'docx':
                    # Parse Word file
                    if ENHANCED_FEATURES_AVAILABLE and hasattr(self, 'enhanced_parser'):
                        questions = self.enhanced_parser.parse_docx_questions(temp_path)
                    else:
                        st.error("❌ Word document parsing not available. Install requirements: pip install python-docx")
                        questions = []
                
                else:
                    # Use standard parser for other formats
                    questions = self.parser.parse_file(temp_path)
                
                if questions:
                    # Load questions into selectors
                    self.selector.load_questions(questions)
                    if ENHANCED_FEATURES_AVAILABLE and hasattr(self, 'enhanced_selector'):
                        self.enhanced_selector.load_questions(questions)
                    
                    # Update session state
                    st.session_state.questions = questions
                    st.session_state.questions_loaded = True
                    st.session_state.current_file = uploaded_file.name
                    
                    st.success(f"✅ Successfully loaded {len(questions)} questions from {file_extension.upper()} file!")
                    
                    # Show preview
                    st.subheader("📋 Data Preview")
                    df = pd.DataFrame(questions[:10])  # Show first 10
                    st.dataframe(df, use_container_width=True)
                
                else:
                    st.warning("⚠️ No questions found in the uploaded file.")
                
                # Clean up temp file
                os.remove(temp_path)
                
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                # Clean up temp file on error
                try:
                    os.remove(temp_path)
                except:
                    pass
        
        # Or load sample data
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Load Sample Data", type="secondary"):
                self._load_sample_data()
        
        with col2:
            if st.session_state.questions_loaded:
                st.metric("Questions Loaded", len(st.session_state.questions))
    
    def _render_question_selector(self):
        """Render the question selection interface"""
        st.header("🎯 Select Questions")
        
        if not st.session_state.questions_loaded:
            st.warning("⚠️ Please load question data first")
            return
        
        # Selection mode tabs
        if ENHANCED_FEATURES_AVAILABLE:
            mode_tab1, mode_tab2 = st.tabs(["🎯 Standard Selection", "📝 Unit-Based Question Paper"])
            
            with mode_tab1:
                self._render_standard_selection()
            
            with mode_tab2:
                self._render_enhanced_selection()
        else:
            st.info("💡 Enhanced features not available. Install requirements: pip install python-docx PyPDF2 pdfplumber")
            self._render_standard_selection()
    
    def _render_standard_selection(self):
        """Render standard question selection interface"""
        
        # Selection criteria
        st.subheader("🔧 Selection Criteria")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Get unique topics
            topics = list(set(q.get('topic', 'unknown') for q in st.session_state.questions))
            selected_topics = st.multiselect("Topics", topics, help="Select specific topics")
        
        with col2:
            # Get unique difficulties
            difficulties = list(set(q.get('difficulty', 'unknown') for q in st.session_state.questions))
            selected_difficulties = st.multiselect("Difficulty", difficulties, help="Select difficulty levels")
        
        with col3:
            # Question count
            max_questions = len(st.session_state.questions)
            question_count = st.slider("Number of Questions", 1, min(max_questions, 100), 10)
        
        # Advanced criteria
        with st.expander("🔍 Advanced Filters"):
            col1, col2 = st.columns(2)
            with col1:
                # Question types
                types = list(set(q.get('type', 'unknown') for q in st.session_state.questions))
                selected_types = st.multiselect("Question Types", types)
            
            with col2:
                # Keywords
                keywords_input = st.text_input("Keywords (comma-separated)", 
                                             help="Enter keywords to search for")
                keywords = [k.strip() for k in keywords_input.split(',') if k.strip()] if keywords_input else []
        
        # Selection button
        if st.button("🎯 Select Questions", type="primary", key="standard_select"):
            try:
                # Build criteria
                criteria = {'count': question_count}
                if selected_topics:
                    criteria['topics'] = selected_topics
                if selected_difficulties:
                    criteria['difficulties'] = selected_difficulties
                if selected_types:
                    criteria['types'] = selected_types
                if keywords:
                    criteria['keywords'] = keywords
                
                # Select questions
                selected = self.selector.select_questions(**criteria)
                st.session_state.selected_questions = selected
                
                st.success(f"✅ Selected {len(selected)} questions!")
                
            except Exception as e:
                st.error(f"❌ Selection failed: {str(e)}")
        
        # Display selected questions
        if st.session_state.selected_questions:
            st.subheader("📋 Selected Questions")
            
            # Create DataFrame for display
            display_data = []
            for i, q in enumerate(st.session_state.selected_questions, 1):
                display_data.append({
                    '#': i,
                    'Question': q.get('question', q.get('text', 'N/A'))[:100] + '...',
                    'Topic': q.get('topic', 'N/A'),
                    'Difficulty': q.get('difficulty', 'N/A'),
                    'Type': q.get('type', 'N/A')
                })
            
            df = pd.DataFrame(display_data)
            st.dataframe(df, use_container_width=True)
    
    def _render_analytics(self):
        """Render analytics and visualizations"""
        st.header("📊 Question Bank Analytics")
        
        if not st.session_state.questions_loaded:
            st.warning("⚠️ Please load question data first")
            return
        
        questions = st.session_state.questions
        
        # Basic statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Questions", len(questions))
        
        with col2:
            topics = set(q.get('topic', 'unknown') for q in questions)
            st.metric("Topics", len(topics))
        
        with col3:
            difficulties = set(q.get('difficulty', 'unknown') for q in questions)
            st.metric("Difficulty Levels", len(difficulties))
        
        with col4:
            types = set(q.get('type', 'unknown') for q in questions)
            st.metric("Question Types", len(types))
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Topic distribution
            topic_counts = {}
            for q in questions:
                topic = q.get('topic', 'unknown')
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            fig_topics = px.pie(
                values=list(topic_counts.values()),
                names=list(topic_counts.keys()),
                title="Distribution by Topic"
            )
            st.plotly_chart(fig_topics, use_container_width=True)
        
        with col2:
            # Difficulty distribution
            diff_counts = {}
            for q in questions:
                diff = q.get('difficulty', 'unknown')
                diff_counts[diff] = diff_counts.get(diff, 0) + 1
            
            fig_diff = px.bar(
                x=list(diff_counts.keys()),
                y=list(diff_counts.values()),
                title="Distribution by Difficulty"
            )
            st.plotly_chart(fig_diff, use_container_width=True)
    
    def _render_export(self):
        """Render export interface"""
        st.header("📥 Export Selected Questions")
        
        if not st.session_state.selected_questions:
            st.warning("⚠️ Please select questions first")
            return
        
        st.info(f"Ready to export {len(st.session_state.selected_questions)} questions")
        
        # Export options
        col1, col2 = st.columns(2)
        
        with col1:
            filename = st.text_input("Output filename", value="selected_questions.xlsx")
        
        with col2:
            export_format = st.selectbox("Format", [
                "Excel (.xlsx)", 
                "CSV (.csv)", 
                "PDF Question Paper (.pdf)",
                "Word Document (.docx)",
                "JSON (.json)",
                "Plain Text (.txt)"
            ])
        
        # Additional options for specific formats
        format_options = {}
        
        if export_format.startswith("PDF"):
            st.subheader("📄 PDF Configuration")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                two_marks = st.number_input("2-mark questions", min_value=0, max_value=50, value=10)
            with col2:
                sixteen_marks = st.number_input("16-mark questions", min_value=0, max_value=20, value=4)
            with col3:
                choice_options = st.number_input("Choice options for 16-mark", min_value=1, max_value=10, value=2)
            
            title = st.text_input("Paper Title", value="Question Paper")
            subject = st.text_input("Subject", value="General")
            
            format_options = {
                'marks_config': {
                    'two_marks_count': two_marks,
                    'sixteen_marks_count': sixteen_marks,
                    'choice_options': choice_options,
                    'title': title,
                    'subject': subject
                }
            }
        
        elif export_format.startswith("Plain Text"):
            st.subheader("📝 Text Format Options")
            txt_style = st.selectbox("Style", ["Simple", "Detailed", "Exam Format"])
            format_options = {'format_style': txt_style.lower().replace(' format', '').replace(' ', '_')}
        
        # Export button
        if st.button("📥 Export Questions", type="primary"):
            try:
                if export_format.startswith("Excel"):
                    self.generator.generate_output(
                        st.session_state.selected_questions, 
                        filename, 
                        format_type='excel'
                    )
                    st.success(f"✅ Questions exported to {filename}")
                
                elif export_format.startswith("CSV"):
                    csv_filename = filename.replace('.xlsx', '.csv')
                    self.generator.generate_output(
                        st.session_state.selected_questions, 
                        csv_filename, 
                        format_type='csv'
                    )
                    st.success(f"✅ Questions exported to {csv_filename}")
                
                elif export_format.startswith("PDF"):
                    pdf_filename = filename.replace('.xlsx', '.pdf')
                    success = self.generator.generate_output(
                        st.session_state.selected_questions, 
                        pdf_filename, 
                        format_type='pdf',
                        **format_options
                    )
                    if success:
                        st.success(f"✅ PDF question paper exported to {pdf_filename}")
                    else:
                        st.error("❌ PDF export failed")
                
                elif export_format.startswith("JSON"):
                    json_filename = filename.replace('.xlsx', '.json')
                    self.generator.generate_output(
                        st.session_state.selected_questions, 
                        json_filename, 
                        format_type='json'
                    )
                    st.success(f"✅ Questions exported to {json_filename}")
                
                elif export_format.startswith("Plain Text"):
                    txt_filename = filename.replace('.xlsx', '.txt')
                    self.generator.generate_output(
                        st.session_state.selected_questions, 
                        txt_filename, 
                        format_type='txt',
                        **format_options
                    )
                    st.success(f"✅ Questions exported to {txt_filename}")
                
                elif export_format.startswith("Word Document"):
                    if ENHANCED_FEATURES_AVAILABLE and hasattr(self, 'word_generator'):
                        # Generate Word document
                        word_filename = filename.replace('.xlsx', '.docx')
                        try:
                            # Create exports directory if it doesn't exist
                            import os
                            os.makedirs("exports", exist_ok=True)
                            
                            output_path = self.word_generator.generate_question_paper(
                                questions=st.session_state.selected_questions,
                                title="Question Paper",
                                instructions="Answer all questions as per instructions.",
                                output_path=f"exports/{word_filename}"
                            )
                            
                            st.success(f"✅ Word document exported to {output_path}")
                            
                            # Provide download link
                            try:
                                with open(output_path, "rb") as file:
                                    st.download_button(
                                        label="⬇️ Download Word Document",
                                        data=file.read(),
                                        file_name=word_filename,
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                            except Exception as download_error:
                                st.warning(f"File created but download failed: {download_error}")
                        except Exception as word_error:
                            st.error(f"Word export failed: {word_error}")
                    else:
                        st.error("❌ Word export not available. Install python-docx: pip install python-docx")
        
            except Exception as e:
                st.error(f"❌ Export failed: {str(e)}")
        
        # Download options
        if st.session_state.selected_questions:
            st.subheader("⬇️ Quick Downloads")
            col1, col2, col3 = st.columns(3)
            
            try:
                # CSV download
                with col1:
                    df = pd.DataFrame(st.session_state.selected_questions)
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📄 Download CSV",
                        data=csv_data,
                        file_name="selected_questions.csv",
                        mime="text/csv"
                    )
                
                # JSON download
                with col2:
                    import json
                    json_data = json.dumps({
                        'metadata': {
                            'total_questions': len(st.session_state.selected_questions),
                            'export_timestamp': pd.Timestamp.now().isoformat()
                        },
                        'questions': st.session_state.selected_questions
                    }, indent=2)
                    st.download_button(
                        label="📋 Download JSON",
                        data=json_data,
                        file_name="selected_questions.json",
                        mime="application/json"
                    )
                
                # TXT download
                with col3:
                    txt_content = "AI Question Bank - Selected Questions\n"
                    txt_content += "=" * 50 + "\n\n"
                    for i, q in enumerate(st.session_state.selected_questions, 1):
                        txt_content += f"{i}. {q.get('question', 'N/A')}\n"
                        txt_content += f"   Topic: {q.get('topic', 'N/A')}\n"
                        txt_content += f"   Difficulty: {q.get('difficulty', 'N/A')}\n\n"
                    
                    st.download_button(
                        label="📝 Download TXT",
                        data=txt_content,
                        file_name="selected_questions.txt",
                        mime="text/plain"
                    )
            
            except Exception as e:
                st.error(f"❌ Download preparation failed: {str(e)}")

    def _render_enhanced_selection(self):
        """Render enhanced unit-based question paper selection"""
        
        st.subheader("📝 Unit-Based Question Paper Generator")
        st.info("Generate question papers with specific unit selection and total marks distribution")
        
        # Load questions into enhanced selector
        if hasattr(self, 'enhanced_selector'):
            self.enhanced_selector.load_questions(st.session_state.questions)
            available_units = self.enhanced_selector.get_available_units()
        else:
            available_units = list(set(q.get('unit', q.get('topic', 'Unknown')) for q in st.session_state.questions))
        
        if not available_units:
            st.warning("⚠️ No units found in the question bank. Make sure your questions have 'unit' or 'topic' fields.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏷️ Unit Selection")
            
            # Unit selection
            selected_units = st.multiselect(
                "Select Units for Question Paper",
                available_units,
                help="Choose the units from which questions should be selected"
            )
            
            # Total marks input
            total_marks = st.number_input(
                "Total Marks for Question Paper",
                min_value=10,
                max_value=500,
                value=60,
                step=2,
                help="Total marks for the entire question paper"
            )
            
            # Marks distribution mode
            distribution_mode = st.radio(
                "Marks Distribution",
                ["Auto (Recommended)", "Custom"],
                help="Choose how to distribute marks across question types"
            )
            
            marks_distribution = None
            if distribution_mode == "Custom":
                st.subheader("🎯 Custom Distribution")
                
                col_2mark, col_16mark = st.columns(2)
                with col_2mark:
                    marks_2 = st.number_input("2-mark questions (count)", min_value=0, max_value=50, value=10)
                with col_16mark:
                    marks_16 = st.number_input("16-mark questions (count)", min_value=0, max_value=20, value=3)
                
                marks_distribution = {
                    '2': marks_2,
                    '16': marks_16
                }
                
                calculated_total = (marks_2 * 2) + (marks_16 * 16)
                if calculated_total != total_marks:
                    st.warning(f"⚠️ Calculated total ({calculated_total}) doesn't match target ({total_marks})")
        
        with col2:
            st.subheader("⚙️ Question Paper Options")
            
            # Choice options for 16-mark questions
            add_choices = st.checkbox(
                "Add Choice Options for 16-mark Questions",
                value=True,
                help="Each 16-mark question will have an additional choice option"
            )
            
            # Export format
            export_format = st.selectbox(
                "Export Format",
                ["PDF", "Word Document (.docx)", "Both"],
                help="Choose the output format for the question paper"
            )
            
            # Paper title
            paper_title = st.text_input(
                "Question Paper Title",
                value="Sample Question Paper",
                help="Title for the generated question paper"
            )
            
            # Instructions
            instructions = st.text_area(
                "Instructions for Students",
                value="1. Answer all questions.\n2. Each question carries marks as indicated.\n3. Choose one from the choice questions.",
                help="Instructions that will appear on the question paper"
            )
        
        # Generate button
        st.markdown("---")
        
        if st.button("📝 Generate Question Paper", type="primary", key="enhanced_select"):
            if not selected_units:
                st.error("❌ Please select at least one unit")
                return
            
            try:
                with st.spinner("🔄 Generating question paper..."):
                    # Generate questions using enhanced selector
                    if hasattr(self, 'enhanced_selector'):
                        result = self.enhanced_selector.select_questions_by_units_and_marks(
                            selected_units=selected_units,
                            total_marks=total_marks,
                            marks_distribution=marks_distribution
                        )
                        
                        selected_questions = result['questions']
                        paper_config = result['paper_config']
                        
                        # Add choice options for 16-mark questions if requested
                        if add_choices:
                            selected_questions = self._add_choice_options(selected_questions, selected_units)
                        
                        # Store in session state
                        st.session_state.selected_questions = selected_questions
                        st.session_state.paper_config = {
                            'title': paper_title,
                            'instructions': instructions,
                            'total_marks': total_marks,
                            'units': selected_units,
                            'distribution': paper_config.get('distribution', {}),
                            'export_format': export_format
                        }
                        
                        st.success(f"✅ Generated question paper with {len(selected_questions)} questions!")
                        st.success(f"📊 Total marks: {paper_config['actual_marks']}")
                        
                        # Display distribution
                        if 'distribution' in paper_config:
                            st.info(f"📈 Distribution: {paper_config['distribution']}")
                        
                        # Display preview
                        self._display_question_paper_preview()
                        
                    else:
                        st.error("❌ Enhanced features not available")
                        
            except Exception as e:
                st.error(f"❌ Failed to generate question paper: {str(e)}")
    
    def _add_choice_options(self, questions: List[Dict], selected_units: List[str]) -> List[Dict]:
        """Add choice options for 16-mark questions"""
        enhanced_questions = []
        
        for question in questions:
            enhanced_question = question.copy()
            
            # Add choice option for 16-mark questions
            if int(question.get('marks', 2)) == 16:
                # Find another 16-mark question from the same units as choice
                choice_candidates = [
                    q for q in st.session_state.questions 
                    if (int(q.get('marks', 2)) == 16 and 
                        str(q.get('unit', q.get('topic', ''))) in selected_units and
                        q.get('question', '') != question.get('question', ''))
                ]
                
                if choice_candidates:
                    import random
                    choice_question = random.choice(choice_candidates)
                    enhanced_question['choice_option'] = choice_question.get('question', '')
                    enhanced_question['choice_answer'] = choice_question.get('answer', '')
            
            enhanced_questions.append(enhanced_question)
        
        return enhanced_questions
    
    def _display_question_paper_preview(self):
        """Display a preview of the generated question paper"""
        if not st.session_state.selected_questions:
            return
        
        st.subheader("📋 Question Paper Preview")
        
        paper_config = st.session_state.get('paper_config', {})
        
        # Paper header
        st.markdown(f"### {paper_config.get('title', 'Question Paper')}")
        st.markdown(f"**Total Marks: {paper_config.get('total_marks', 'N/A')}**")
        st.markdown(f"**Units: {', '.join(paper_config.get('units', []))}**")
        
        # Instructions
        if paper_config.get('instructions'):
            st.markdown("**Instructions:**")
            st.markdown(paper_config['instructions'])
        
        st.markdown("---")
        
        # Group questions by marks
        questions_by_marks = {}
        for q in st.session_state.selected_questions:
            marks = int(q.get('marks', 2))
            if marks not in questions_by_marks:
                questions_by_marks[marks] = []
            questions_by_marks[marks].append(q)
        
        # Display questions
        question_number = 1
        for marks in sorted(questions_by_marks.keys()):
            st.markdown(f"#### Section: {marks}-Mark Questions")
            
            for question in questions_by_marks[marks]:
                st.markdown(f"**{question_number}. {question.get('question', 'N/A')}** ({marks} marks)")
                
                # Show choice option if available
                if 'choice_option' in question:
                    st.markdown(f"**OR**")
                    st.markdown(f"**{question_number}. {question['choice_option']}** ({marks} marks)")
                
                st.markdown("")  # Add spacing
                question_number += 1
        
        # Export buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export as PDF", key="export_pdf"):
                self._export_question_paper("PDF")
        
        with col2:
            if st.button("📝 Export as Word", key="export_word"):
                self._export_question_paper("Word")
        
        with col3:
            if st.button("📊 Export as Excel", key="export_excel"):
                self._export_question_paper("Excel")
    
    def _export_question_paper(self, format_type: str):
        """Export the question paper in the specified format"""
        try:
            if format_type == "Word" and hasattr(self, 'word_generator'):
                # Generate Word document
                paper_config = st.session_state.get('paper_config', {})
                output_path = self.word_generator.generate_question_paper(
                    questions=st.session_state.selected_questions,
                    title=paper_config.get('title', 'Question Paper'),
                    instructions=paper_config.get('instructions', ''),
                    output_path="exports/question_paper.docx"
                )
                
                st.success(f"✅ Word document exported: {output_path}")
                
                # Provide download link
                with open(output_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Download Word Document",
                        data=file.read(),
                        file_name="question_paper.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            
            elif format_type == "PDF":
                # For now, create a simple text version
                paper_content = self._generate_paper_text()
                st.download_button(
                    label="⬇️ Download PDF (Text)",
                    data=paper_content,
                    file_name="question_paper.txt",
                    mime="text/plain"
                )
                st.info("💡 Full PDF generation coming soon!")
            
            elif format_type == "Excel":
                # Create Excel export
                df = pd.DataFrame(st.session_state.selected_questions)
                excel_buffer = io.BytesIO()
                df.to_excel(excel_buffer, index=False)
                excel_buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_buffer.getvalue(),
                    file_name="question_paper.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")
    
    def _generate_paper_text(self) -> str:
        """Generate plain text version of the question paper"""
        paper_config = st.session_state.get('paper_config', {})
        
        content = f"{paper_config.get('title', 'Question Paper')}\n"
        content += f"Total Marks: {paper_config.get('total_marks', 'N/A')}\n"
        content += f"Units: {', '.join(paper_config.get('units', []))}\n\n"
        
        if paper_config.get('instructions'):
            content += "Instructions:\n"
            content += paper_config['instructions'] + "\n\n"
        
        content += "=" * 50 + "\n\n"
        
        # Add questions
        question_number = 1
        for question in st.session_state.selected_questions:
            marks = question.get('marks', 2)
            content += f"{question_number}. {question.get('question', 'N/A')} ({marks} marks)\n"
            
            if 'choice_option' in question:
                content += f"OR\n"
                content += f"{question_number}. {question['choice_option']} ({marks} marks)\n"
            
            content += "\n"
            question_number += 1
        
        return content

def main():
    """Main function to run the Streamlit app"""
    app = QuestionSelectionApp()
    app.run()

if __name__ == "__main__":
    main()
