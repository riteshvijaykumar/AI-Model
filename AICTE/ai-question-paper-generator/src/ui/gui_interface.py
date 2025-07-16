"""
GUI Interface Module

Provides a user-friendly graphical interface using Streamlit for the question selection system.
Supports file upload, interactive criteria selection, and question preview.
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

from ..data_processing.question_parser import QuestionParser
from ..selection_engine.question_selector import QuestionSelector
from ..export.spreadsheet_generator import SpreadsheetGenerator


def launch_gui():
    """Launch the Streamlit GUI"""
    st.set_page_config(
        page_title="AI Question Bank Selection",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    gui = QuestionSelectionGUI()
    gui.run()


class QuestionSelectionGUI:
    """Streamlit-based GUI for question selection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = QuestionParser()
        self.selector = QuestionSelector()
        self.generator = SpreadsheetGenerator()
        
        # Initialize session state
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize Streamlit session state"""
        if 'questions_loaded' not in st.session_state:
            st.session_state.questions_loaded = False
        if 'current_questions' not in st.session_state:
            st.session_state.current_questions = []
        if 'selected_questions' not in st.session_state:
            st.session_state.selected_questions = []
        if 'last_criteria' not in st.session_state:
            st.session_state.last_criteria = {}
        if 'statistics' not in st.session_state:
            st.session_state.statistics = {}
    
    def run(self):
        """Run the GUI application"""
        st.title("🤖 AI Question Bank Selection System")
        st.markdown("---")
        
        # Sidebar for navigation
        with st.sidebar:
            st.header("Navigation")
            page = st.selectbox(
                "Select Page",
                ["Upload Questions", "Select Questions", "View Results", "Statistics", "Settings"]
            )
        
        # Main content based on selected page
        if page == "Upload Questions":
            self._upload_page()
        elif page == "Select Questions":
            self._selection_page()
        elif page == "View Results":
            self._results_page()
        elif page == "Statistics":
            self._statistics_page()
        elif page == "Settings":
            self._settings_page()
    
    def _upload_page(self):
        """Question upload and loading page"""
        st.header("📁 Upload Question Bank")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Upload File")
            
            uploaded_file = st.file_uploader(
                "Choose a question bank file",
                type=['csv', 'xlsx', 'xls', 'json', 'txt'],
                help="Supported formats: CSV, Excel, JSON, TXT"
            )
            
            if uploaded_file is not None:
                try:
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Parse questions
                    with st.spinner("Loading questions..."):
                        questions = self.parser.parse_file(temp_path)
                    
                    # Clean up temp file
                    Path(temp_path).unlink()
                    
                    if questions:
                        st.session_state.current_questions = questions
                        st.session_state.questions_loaded = True
                        self.selector.load_questions(questions)
                        
                        # Update statistics
                        st.session_state.statistics = self.selector.get_statistics()
                        
                        st.success(f"✅ Successfully loaded {len(questions)} questions!")
                        
                        # Show preview
                        st.subheader("Preview")
                        preview_df = self._create_preview_dataframe(questions[:10])
                        st.dataframe(preview_df, use_container_width=True)
                        
                    else:
                        st.error("No questions found in the uploaded file.")
                        
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        with col2:
            st.subheader("File Format Guide")
            st.markdown("""
            **CSV/Excel Format:**
            - `question`: Question text
            - `topic`: Subject/category
            - `difficulty`: easy/medium/hard
            - `type`: question type
            - `keywords`: comma-separated
            - `answer`: correct answer
            
            **JSON Format:**
            ```json
            {
                "questions": [
                    {
                        "question": "What is 2+2?",
                        "topic": "math",
                        "difficulty": "easy",
                        "answer": "4"
                    }
                ]
            }
            ```
            """)
    
    def _selection_page(self):
        """Question selection page"""
        st.header("🎯 Select Questions")
        
        if not st.session_state.questions_loaded:
            st.warning("Please upload questions first!")
            return
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Selection Criteria")
            
            # Topic selection
            available_topics = list(st.session_state.statistics.get('topics', {}).keys())
            if available_topics:
                selected_topics = st.multiselect(
                    "Topics",
                    available_topics,
                    help="Select one or more topics"
                )
            else:
                selected_topics = []
            
            # Difficulty selection
            available_difficulties = list(st.session_state.statistics.get('difficulties', {}).keys())
            if available_difficulties:
                selected_difficulties = st.multiselect(
                    "Difficulties",
                    available_difficulties,
                    help="Select difficulty levels"
                )
            else:
                selected_difficulties = []
            
            # Type selection
            available_types = list(st.session_state.statistics.get('types', {}).keys())
            if available_types:
                selected_types = st.multiselect(
                    "Question Types",
                    available_types,
                    help="Select question types"
                )
            else:
                selected_types = []
            
            # Keyword input
            keywords = st.text_input(
                "Keywords (comma-separated)",
                help="Enter keywords to search for"
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                count = st.number_input(
                    "Number of questions",
                    min_value=1,
                    max_value=1000,
                    value=20,
                    help="Maximum number of questions to select"
                )
                
                diversity = st.checkbox(
                    "Enable diversity selection",
                    value=True,
                    help="Ensure diverse selection across topics and difficulties"
                )
                
                min_length = st.number_input(
                    "Minimum question length",
                    min_value=0,
                    value=0,
                    help="Minimum number of characters"
                )
                
                max_length = st.number_input(
                    "Maximum question length",
                    min_value=0,
                    value=0,
                    help="Maximum number of characters (0 = no limit)"
                )
        
        with col2:
            st.subheader("Selection Summary")
            
            # Build criteria
            criteria = {}
            if selected_topics:
                criteria['topic'] = selected_topics
            if selected_difficulties:
                criteria['difficulty'] = selected_difficulties
            if selected_types:
                criteria['type'] = selected_types
            if keywords:
                criteria['keywords'] = keywords
            criteria['count'] = count
            criteria['diversity'] = diversity
            if min_length > 0:
                criteria['min_length'] = min_length
            if max_length > 0:
                criteria['max_length'] = max_length
            
            # Display criteria
            st.json(criteria)
            
            # Selection button
            if st.button("🎯 Select Questions", type="primary"):
                if criteria:
                    with st.spinner("Selecting questions..."):
                        try:
                            selected = self.selector.select_questions(**criteria)
                            
                            if selected:
                                st.session_state.selected_questions = selected
                                st.session_state.last_criteria = criteria
                                st.success(f"✅ Selected {len(selected)} questions!")
                            else:
                                st.warning("No questions match the specified criteria.")
                                
                        except Exception as e:
                            st.error(f"Error selecting questions: {str(e)}")
                else:
                    st.warning("Please specify at least one selection criterion.")
    
    def _results_page(self):
        """Results viewing page"""
        st.header("📊 Selection Results")
        
        if not st.session_state.selected_questions:
            st.warning("No questions selected. Please select questions first!")
            return
        
        selected_questions = st.session_state.selected_questions
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Questions", len(selected_questions))
        
        with col2:
            topics = set(q.get('topic', '') for q in selected_questions)
            st.metric("Topics", len(topics))
        
        with col3:
            difficulties = set(q.get('difficulty', '') for q in selected_questions)
            st.metric("Difficulties", len(difficulties))
        
        with col4:
            avg_length = sum(len(q.get('question', '')) for q in selected_questions) / len(selected_questions)
            st.metric("Avg Length", f"{avg_length:.0f}")
        
        # Visualization
        st.subheader("Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Topic distribution
            topic_counts = {}
            for q in selected_questions:
                topic = q.get('topic', 'Unknown')
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            if topic_counts:
                fig = px.pie(
                    values=list(topic_counts.values()),
                    names=list(topic_counts.keys()),
                    title="Topic Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Difficulty distribution
            difficulty_counts = {}
            for q in selected_questions:
                difficulty = q.get('difficulty', 'Unknown')
                difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
            
            if difficulty_counts:
                fig = px.bar(
                    x=list(difficulty_counts.keys()),
                    y=list(difficulty_counts.values()),
                    title="Difficulty Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Questions table
        st.subheader("Selected Questions")
        
        # Create DataFrame
        df = pd.DataFrame(selected_questions)
        
        # Display options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_columns = st.multiselect(
                "Columns to display",
                df.columns.tolist(),
                default=['question', 'topic', 'difficulty', 'type']
            )
        
        with col2:
            page_size = st.number_input(
                "Questions per page",
                min_value=5,
                max_value=100,
                value=10
            )
        
        with col3:
            search_term = st.text_input("Search questions")
        
        # Filter and display
        filtered_df = df[show_columns] if show_columns else df
        
        if search_term:
            mask = filtered_df.astype(str).apply(
                lambda x: x.str.contains(search_term, case=False, na=False)
            ).any(axis=1)
            filtered_df = filtered_df[mask]
        
        # Pagination
        total_pages = (len(filtered_df) + page_size - 1) // page_size
        if total_pages > 1:
            page = st.selectbox(
                "Page",
                range(1, total_pages + 1),
                format_func=lambda x: f"Page {x} of {total_pages}"
            )
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            filtered_df = filtered_df.iloc[start_idx:end_idx]
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # Export options
        st.subheader("Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download Excel"):
                self._download_excel(selected_questions)
        
        with col2:
            if st.button("📥 Download CSV"):
                self._download_csv(selected_questions)
        
        with col3:
            if st.button("📥 Download JSON"):
                self._download_json(selected_questions)
    
    def _statistics_page(self):
        """Statistics page"""
        st.header("📈 Question Bank Statistics")
        
        if not st.session_state.questions_loaded:
            st.warning("Please upload questions first!")
            return
        
        stats = st.session_state.statistics
        questions = st.session_state.current_questions
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Questions", stats.get('total_questions', 0))
        
        with col2:
            st.metric("Topics", len(stats.get('topics', {})))
        
        with col3:
            st.metric("Difficulties", len(stats.get('difficulties', {})))
        
        with col4:
            st.metric("Types", len(stats.get('types', {})))
        
        # Detailed statistics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Topic Distribution")
            topic_stats = stats.get('topics', {})
            if topic_stats:
                fig = px.bar(
                    x=list(topic_stats.keys()),
                    y=list(topic_stats.values()),
                    title="Questions by Topic"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Difficulty Distribution")
            difficulty_stats = stats.get('difficulties', {})
            if difficulty_stats:
                fig = px.pie(
                    values=list(difficulty_stats.values()),
                    names=list(difficulty_stats.keys()),
                    title="Questions by Difficulty"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Question length analysis
        if questions:
            st.subheader("Question Length Analysis")
            lengths = [len(q.get('question', '')) for q in questions]
            
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=lengths, nbinsx=20))
            fig.update_layout(
                title="Question Length Distribution",
                xaxis_title="Question Length (characters)",
                yaxis_title="Number of Questions"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def _settings_page(self):
        """Settings page"""
        st.header("⚙️ Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Selection Settings")
            
            default_count = st.number_input(
                "Default question count",
                min_value=1,
                max_value=1000,
                value=20
            )
            
            diversity_factor = st.slider(
                "Diversity factor",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                help="Higher values increase diversity"
            )
            
            relevance_threshold = st.slider(
                "Relevance threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                help="Minimum relevance score for selection"
            )
        
        with col2:
            st.subheader("Model Training")
            
            if st.session_state.questions_loaded:
                question_count = len(st.session_state.current_questions)
                
                if question_count >= 50:
                    if st.button("🤖 Train AI Models"):
                        with st.spinner("Training models..."):
                            try:
                                results = self.selector.train_models()
                                st.success("Models trained successfully!")
                                
                                for model, accuracy in results.items():
                                    st.metric(f"{model} Accuracy", f"{accuracy:.3f}")
                            except Exception as e:
                                st.error(f"Training error: {str(e)}")
                else:
                    st.warning(f"Need at least 50 questions to train models. Currently have {question_count}.")
            else:
                st.info("Upload questions to enable model training.")
    
    def _create_preview_dataframe(self, questions: List[Dict[str, Any]]) -> pd.DataFrame:
        """Create preview DataFrame from questions"""
        preview_data = []
        for q in questions:
            preview_data.append({
                'ID': q.get('id', 'N/A'),
                'Question': q.get('question', 'N/A')[:100] + '...' if len(q.get('question', '')) > 100 else q.get('question', 'N/A'),
                'Topic': q.get('topic', 'N/A'),
                'Difficulty': q.get('difficulty', 'N/A'),
                'Type': q.get('type', 'N/A')
            })
        return pd.DataFrame(preview_data)
    
    def _download_excel(self, questions: List[Dict[str, Any]]):
        """Generate Excel download"""
        try:
            output = io.BytesIO()
            success = self.generator.generate_spreadsheet(questions, output, format_type='excel')
            
            if success:
                output.seek(0)
                st.download_button(
                    label="Download Excel File",
                    data=output,
                    file_name="selected_questions.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Failed to generate Excel file")
        except Exception as e:
            st.error(f"Error generating Excel: {str(e)}")
    
    def _download_csv(self, questions: List[Dict[str, Any]]):
        """Generate CSV download"""
        try:
            df = pd.DataFrame(questions)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV File",
                data=csv,
                file_name="selected_questions.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error generating CSV: {str(e)}")
    
    def _download_json(self, questions: List[Dict[str, Any]]):
        """Generate JSON download"""
        try:
            import json
            
            export_data = {
                'metadata': {
                    'total_questions': len(questions),
                    'criteria': st.session_state.last_criteria
                },
                'questions': questions
            }
            
            json_str = json.dumps(export_data, indent=2)
            
            st.download_button(
                label="Download JSON File",
                data=json_str,
                file_name="selected_questions.json",
                mime="application/json"
            )
        except Exception as e:
            st.error(f"Error generating JSON: {str(e)}")


if __name__ == "__main__":
    launch_gui()
