"""
PDF Generator Module

Generates formatted PDF question papers with customizable marks distribution
and choice options for questions.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import List, Dict, Any, Optional
import os
from datetime import datetime


class PDFQuestionPaper:
    """Generates formatted PDF question papers"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkred
        )
        
        # Question style
        self.question_style = ParagraphStyle(
            'Question',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=15,
            spaceBefore=10,
            leftIndent=20
        )
        
        # Choice style
        self.choice_style = ParagraphStyle(
            'Choice',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            leftIndent=40
        )
        
        # Instructions style
        self.instruction_style = ParagraphStyle(
            'Instructions',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            alignment=TA_JUSTIFY,
            textColor=colors.darkgreen
        )
    
    def generate_question_paper(
        self,
        questions: List[Dict[str, Any]],
        output_path: str,
        exam_config: Dict[str, Any] = None
    ) -> bool:
        """
        Generate a formatted PDF question paper
        
        Args:
            questions: List of question dictionaries
            output_path: Path for the output PDF file
            exam_config: Configuration for exam format
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Default exam configuration
            config = {
                'title': 'Question Paper',
                'subject': 'General Knowledge',
                'duration': '3 Hours',
                'max_marks': 100,
                'sections': {
                    'section_a': {
                        'title': 'Section A - Short Answer Questions (2 Marks Each)',
                        'marks_per_question': 2,
                        'count': 10,
                        'instructions': 'Answer any 10 questions. Each question carries 2 marks.'
                    },
                    'section_b': {
                        'title': 'Section B - Long Answer Questions (16 Marks Each)',
                        'marks_per_question': 16,
                        'count': 4,
                        'choice_options': 2,
                        'instructions': 'Answer any 4 questions. Each question carries 16 marks. Choose from the given options.'
                    }
                }
            }
            
            # Update with provided config
            if exam_config:
                config.update(exam_config)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Header
            self._add_header(story, config)
            
            # Instructions
            self._add_general_instructions(story, config)
            
            # Questions by section
            self._add_questions_by_section(story, questions, config)
            
            # Build PDF
            doc.build(story)
            
            return True
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return False
    
    def _add_header(self, story: List, config: Dict):
        """Add header section to the PDF"""
        # Title
        title = Paragraph(config['title'], self.title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Exam details table
        exam_data = [
            ['Subject:', config.get('subject', 'N/A'), 'Duration:', config.get('duration', 'N/A')],
            ['Max Marks:', str(config.get('max_marks', 100)), 'Date:', datetime.now().strftime('%d/%m/%Y')]
        ]
        
        exam_table = Table(exam_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
        exam_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(exam_table)
        story.append(Spacer(1, 20))
    
    def _add_general_instructions(self, story: List, config: Dict):
        """Add general instructions"""
        instructions = [
            "1. Read all questions carefully before attempting.",
            "2. All questions are compulsory unless otherwise mentioned.",
            "3. Write your answers clearly and legibly.",
            "4. Use of calculators is not allowed unless specified.",
            "5. Manage your time effectively."
        ]
        
        inst_header = Paragraph("<b>General Instructions:</b>", self.section_style)
        story.append(inst_header)
        
        for instruction in instructions:
            inst_para = Paragraph(instruction, self.instruction_style)
            story.append(inst_para)
        
        story.append(Spacer(1, 20))
    
    def _add_questions_by_section(self, story: List, questions: List[Dict], config: Dict):
        """Add questions organized by sections"""
        sections = config.get('sections', {})
        
        # Separate questions by marks
        questions_2_marks = []
        questions_16_marks = []
        other_questions = []
        
        for q in questions:
            marks = q.get('marks', 0)
            if marks == 2:
                questions_2_marks.append(q)
            elif marks == 16:
                questions_16_marks.append(q)
            else:
                other_questions.append(q)
        
        # Section A - 2 marks questions
        if 'section_a' in sections and questions_2_marks:
            self._add_section(story, 'Section A', sections['section_a'], questions_2_marks[:sections['section_a']['count']])
        
        # Section B - 16 marks questions with choices
        if 'section_b' in sections and questions_16_marks:
            self._add_section_with_choices(story, 'Section B', sections['section_b'], questions_16_marks)
        
        # Add other questions if any
        if other_questions:
            other_section = {
                'title': 'Additional Questions',
                'instructions': 'Answer the following questions as directed.',
                'marks_per_question': 'Variable'
            }
            self._add_section(story, 'Additional', other_section, other_questions)
    
    def _add_section(self, story: List, section_name: str, section_config: Dict, questions: List[Dict]):
        """Add a regular section with questions"""
        # Section header
        section_title = Paragraph(section_config['title'], self.section_style)
        story.append(section_title)
        
        # Section instructions
        if 'instructions' in section_config:
            inst_para = Paragraph(f"<i>{section_config['instructions']}</i>", self.instruction_style)
            story.append(inst_para)
            story.append(Spacer(1, 10))
        
        # Questions
        for i, question in enumerate(questions, 1):
            marks = section_config.get('marks_per_question', question.get('marks', 'N/A'))
            question_text = f"<b>Q{i}.</b> {question.get('question', question.get('text', 'N/A'))} <b>[{marks} marks]</b>"
            
            q_para = Paragraph(question_text, self.question_style)
            story.append(q_para)
            
            # Add answer space
            story.append(Spacer(1, 30))
        
        story.append(Spacer(1, 20))
    
    def _add_section_with_choices(self, story: List, section_name: str, section_config: Dict, questions: List[Dict]):
        """Add a section with choice-based questions"""
        # Section header
        section_title = Paragraph(section_config['title'], self.section_style)
        story.append(section_title)
        
        # Section instructions
        if 'instructions' in section_config:
            inst_para = Paragraph(f"<i>{section_config['instructions']}</i>", self.instruction_style)
            story.append(inst_para)
            story.append(Spacer(1, 10))
        
        # Questions with choices
        choice_options = section_config.get('choice_options', 2)
        questions_per_choice = section_config.get('count', 4)
        
        question_num = 1
        choice_group = 1
        
        i = 0
        while i < len(questions) and choice_group <= questions_per_choice:
            # Choice group header
            choice_header = Paragraph(f"<b>Question {question_num}: (Choose any one)</b>", self.section_style)
            story.append(choice_header)
            
            # Add choice options
            for choice_option in range(choice_options):
                if i < len(questions):
                    question = questions[i]
                    marks = section_config.get('marks_per_question', question.get('marks', 16))
                    
                    option_label = chr(ord('a') + choice_option)  # a, b, c, etc.
                    question_text = f"<b>{option_label})</b> {question.get('question', question.get('text', 'N/A'))} <b>[{marks} marks]</b>"
                    
                    q_para = Paragraph(question_text, self.question_style)
                    story.append(q_para)
                    story.append(Spacer(1, 20))
                    
                    i += 1
            
            # Add answer space for the chosen option
            answer_space = Paragraph("<i>Answer space for chosen option:</i>", self.instruction_style)
            story.append(answer_space)
            story.append(Spacer(1, 60))
            
            question_num += 1
            choice_group += 1
        
        story.append(Spacer(1, 20))


class PDFExportManager:
    """Manages PDF export functionality"""
    
    def __init__(self):
        self.pdf_generator = PDFQuestionPaper()
    
    def export_questions_to_pdf(
        self,
        questions: List[Dict[str, Any]],
        output_path: str,
        marks_config: Dict[str, Any] = None
    ) -> bool:
        """
        Export questions to PDF with specified marks configuration
        
        Args:
            questions: List of questions
            output_path: Output PDF file path
            marks_config: Configuration for marks distribution
        
        Returns:
            bool: Success status
        """
        # Default marks configuration
        default_config = {
            'title': 'Question Paper',
            'subject': 'Subject Name',
            'duration': '3 Hours',
            'max_marks': 100,
            'two_marks_count': 10,
            'sixteen_marks_count': 4,
            'choice_options': 2
        }
        
        if marks_config:
            default_config.update(marks_config)
        
        # Prepare exam configuration
        exam_config = {
            'title': default_config['title'],
            'subject': default_config['subject'],
            'duration': default_config['duration'],
            'max_marks': default_config['max_marks'],
            'sections': {
                'section_a': {
                    'title': f'Section A - Short Answer Questions (2 Marks Each)',
                    'marks_per_question': 2,
                    'count': default_config['two_marks_count'],
                    'instructions': f'Answer any {default_config["two_marks_count"]} questions. Each question carries 2 marks.'
                },
                'section_b': {
                    'title': f'Section B - Long Answer Questions (16 Marks Each)',
                    'marks_per_question': 16,
                    'count': default_config['sixteen_marks_count'],
                    'choice_options': default_config['choice_options'],
                    'instructions': f'Answer any {default_config["sixteen_marks_count"]} questions. Each question carries 16 marks. Choose from the given options.'
                }
            }
        }
        
        # Assign marks to questions if not already assigned
        self._assign_marks_to_questions(questions, default_config)
        
        # Generate PDF
        try:
            print(f"Debug: Calling PDF generator with {len(questions)} questions")
            result = self.pdf_generator.generate_question_paper(
                questions, output_path, exam_config
            )
            print(f"Debug: PDF generator returned: {result}")
            return result
        except Exception as e:
            print(f"Debug: Error in PDF generation: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _assign_marks_to_questions(self, questions: List[Dict], config: Dict):
        """Assign marks to questions based on configuration"""
        two_marks_count = config['two_marks_count']
        sixteen_marks_count = config['sixteen_marks_count']
        
        # Assign 2 marks to first set of questions
        for i in range(min(two_marks_count, len(questions))):
            questions[i]['marks'] = 2
        
        # Assign 16 marks to next set of questions
        start_idx = two_marks_count
        end_idx = min(start_idx + sixteen_marks_count * config['choice_options'], len(questions))
        
        for i in range(start_idx, end_idx):
            questions[i]['marks'] = 16
        
        # Assign default marks to remaining questions
        for i in range(end_idx, len(questions)):
            if 'marks' not in questions[i]:
                questions[i]['marks'] = 5  # Default marks
