"""
Command Line Interface Module

Provides an interactive command-line interface for the question selection system.
Supports various commands and interactive question selection.
"""

import sys
import os
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import click

from ..data_processing.question_parser import QuestionParser
from ..selection_engine.question_selector import QuestionSelector
from ..export.spreadsheet_generator import SpreadsheetGenerator

# Import enhanced features
try:
    from ..enhanced_features import EnhancedQuestionSelector, WordDocumentGenerator, EnhancedInputParser
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError:
    ENHANCED_FEATURES_AVAILABLE = False


class CLIInterface:
    """Command-line interface for question selection"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
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
        else:
            self.enhanced_selector = None
            self.word_generator = None
            self.enhanced_parser = None
        
        # Current state
        self.current_questions = []
        self.selected_questions = []
        self.last_criteria = {}
        
    def run(self):
        """Run the CLI interface"""
        self._print_welcome()
        
        while True:
            try:
                command = input("\nEnter command (type 'help' for options): ").strip().lower()
                
                if command in ['exit', 'quit', 'q']:
                    self._print_goodbye()
                    break
                elif command == 'help':
                    self._show_help()
                elif command == 'load':
                    self._load_questions()
                elif command == 'select':
                    self._select_questions()
                elif command == 'unitselect':
                    self._unit_based_selection()
                elif command == 'show':
                    self._show_questions()
                elif command == 'export':
                    self._export_questions()
                elif command == 'stats':
                    self._show_statistics()
                elif command == 'clear':
                    self._clear_selection()
                elif command == 'criteria':
                    self._show_criteria()
                elif command == 'train':
                    self._train_models()
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
            except EOFError:
                self._print_goodbye()
                break
            except Exception as e:
                print(f"Error: {str(e)}")
                self.logger.error(f"CLI error: {str(e)}")
    
    def _print_welcome(self):
        """Print welcome message"""
        print("=" * 60)
        print("🤖 AI Question Bank Selection System")
        print("=" * 60)
        print("Welcome! This tool helps you select relevant questions")
        print("from your question bank using AI-powered filtering.")
        print("\nType 'help' to see available commands.")
    
    def _print_goodbye(self):
        """Print goodbye message"""
        print("\n" + "=" * 60)
        print("Thank you for using the AI Question Bank Selection System!")
        print("=" * 60)
    
    def _show_help(self):
        """Show available commands"""
        help_text = """
Available Commands:
==================
load       - Load questions from a file (CSV, Excel, JSON, TXT, PDF, Word)
select     - Select questions based on criteria
unitselect - NEW: Select questions by units and total marks
show       - Show selected questions
export     - Export selected questions (Excel, CSV, PDF, Word)
stats      - Show question bank statistics
clear      - Clear current selection
criteria   - Show last used criteria
train      - Train AI models on current question bank
help       - Show this help message
exit       - Exit the program

Examples:
---------
load data/questions.csv
select topic:math difficulty:medium count:20
unitselect                   # NEW: Unit-based selection
export output.xlsx
export exam.pdf              # Export as PDF question paper
export exam.docx             # NEW: Export as Word document
        """
        print(help_text)
        
        if ENHANCED_FEATURES_AVAILABLE:
            print("\n✨ Enhanced Features Available:")
            print("- Unit-based question selection")
            print("- Word document (.docx) export")
            print("- PDF/Word input file parsing")
        else:
            print("\n⚠️  Enhanced features not available. Install dependencies:")
            print("   pip install python-docx PyPDF2 pdfplumber")
    
    def _load_questions(self):
        """Load questions from file"""
        file_path = input("Enter path to question bank file: ").strip()
        
        if not file_path:
            print("No file path provided.")
            return
        
        try:
            print(f"Loading questions from: {file_path}")
            
            # Check if it's a PDF or Word file and use enhanced parser
            file_ext = Path(file_path).suffix.lower()
            if ENHANCED_FEATURES_AVAILABLE and file_ext in ['.pdf', '.docx']:
                if file_ext == '.pdf':
                    questions = self.enhanced_parser.parse_pdf_questions(file_path)
                elif file_ext == '.docx':
                    questions = self.enhanced_parser.parse_docx_questions(file_path)
                
                if questions:
                    print(f"✨ Parsed {len(questions)} questions from {file_ext.upper()} file")
                    print("⚠️  Note: Parsed questions may need manual review for accuracy")
            else:
                # Use regular parser for standard formats
                questions = self.parser.parse_file(file_path)
            
            if not questions:
                print("No questions found in file.")
                return
            
            self.current_questions = questions
            self.selector.load_questions(questions)
            
            # Also load into enhanced selector if available
            if ENHANCED_FEATURES_AVAILABLE:
                self.enhanced_selector.load_questions(questions)
            
            print(f"✅ Successfully loaded {len(questions)} questions.")
            
            # Show basic statistics
            stats = self.selector.get_statistics()
            print(f"Topics: {len(stats['topics'])}")
            print(f"Difficulties: {len(stats['difficulties'])}")
            print(f"Types: {len(stats['types'])}")
            
        except Exception as e:
            print(f"Error loading questions: {str(e)}")
    
    def _select_questions(self):
        """Select questions based on criteria"""
        if not self.current_questions:
            print("No questions loaded. Please load questions first.")
            return
        
        print("\nQuestion Selection")
        print("=" * 20)
        print("Enter selection criteria (press Enter to skip):")
        
        criteria = {}
        
        # Get criteria from user
        topic = input("Topic (e.g., math, science): ").strip()
        if topic:
            criteria['topic'] = topic
        
        difficulty = input("Difficulty (easy, medium, hard): ").strip()
        if difficulty:
            criteria['difficulty'] = difficulty
        
        q_type = input("Question type (text, multiple_choice, etc.): ").strip()
        if q_type:
            criteria['type'] = q_type
        
        keywords = input("Keywords (comma-separated): ").strip()
        if keywords:
            criteria['keywords'] = keywords
        
        count = input("Number of questions (default 20): ").strip()
        if count:
            try:
                criteria['count'] = int(count)
            except ValueError:
                print("Invalid count, using default (20)")
                criteria['count'] = 20
        
        diversity = input("Enable diversity selection? (y/n, default y): ").strip().lower()
        criteria['diversity'] = diversity != 'n'
        
        if not criteria:
            print("No criteria specified.")
            return
        
        try:
            print("\nSelecting questions...")
            selected = self.selector.select_questions(**criteria)
            
            if not selected:
                print("No questions match the specified criteria.")
                return
            
            self.selected_questions = selected
            self.last_criteria = criteria
            
            print(f"✅ Selected {len(selected)} questions.")
            
            # Show preview
            preview = input("Show preview of selected questions? (y/n): ").strip().lower()
            if preview == 'y':
                self._show_questions_preview(selected[:5])
            
        except Exception as e:
            print(f"Error selecting questions: {str(e)}")
    
    def _show_questions(self):
        """Show selected questions"""
        if not self.selected_questions:
            print("No questions selected. Please select questions first.")
            return
        
        print(f"\nSelected Questions ({len(self.selected_questions)})")
        print("=" * 50)
        
        # Show options
        print("Display options:")
        print("1. Show all questions")
        print("2. Show summary table")
        print("3. Show first 10 questions")
        print("4. Show by page")
        
        choice = input("Choose option (1-4): ").strip()
        
        if choice == '1':
            self._show_all_questions()
        elif choice == '2':
            self._show_summary_table()
        elif choice == '3':
            self._show_questions_preview(self.selected_questions[:10])
        elif choice == '4':
            self._show_questions_paged()
        else:
            print("Invalid choice.")
    
    def _show_all_questions(self):
        """Show all selected questions"""
        for i, question in enumerate(self.selected_questions, 1):
            print(f"\n{i}. {question.get('question', 'N/A')}")
            print(f"   Topic: {question.get('topic', 'N/A')}")
            print(f"   Difficulty: {question.get('difficulty', 'N/A')}")
            print(f"   Type: {question.get('type', 'N/A')}")
            if question.get('keywords'):
                print(f"   Keywords: {', '.join(question['keywords'])}")
    
    def _show_summary_table(self):
        """Show summary table of selected questions"""
        print(f"{'ID':<5} {'Topic':<15} {'Difficulty':<10} {'Type':<15} {'Length':<8}")
        print("-" * 60)
        
        for q in self.selected_questions:
            print(f"{str(q.get('id', 'N/A')):<5} "
                  f"{q.get('topic', 'N/A')[:14]:<15} "
                  f"{q.get('difficulty', 'N/A'):<10} "
                  f"{q.get('type', 'N/A')[:14]:<15} "
                  f"{len(q.get('question', '')):<8}")
    
    def _show_questions_preview(self, questions: List[Dict[str, Any]]):
        """Show preview of questions"""
        for i, question in enumerate(questions, 1):
            print(f"\n{i}. {question.get('question', 'N/A')[:100]}...")
            print(f"   Topic: {question.get('topic', 'N/A')} | "
                  f"Difficulty: {question.get('difficulty', 'N/A')} | "
                  f"Type: {question.get('type', 'N/A')}")
    
    def _show_questions_paged(self):
        """Show questions with pagination"""
        page_size = 5
        total_pages = (len(self.selected_questions) + page_size - 1) // page_size
        current_page = 1
        
        while True:
            start_idx = (current_page - 1) * page_size
            end_idx = start_idx + page_size
            page_questions = self.selected_questions[start_idx:end_idx]
            
            print(f"\nPage {current_page} of {total_pages}")
            print("-" * 40)
            self._show_questions_preview(page_questions)
            
            if total_pages > 1:
                print(f"\nNavigation: [p]revious, [n]ext, [q]uit")
                choice = input("Enter choice: ").strip().lower()
                
                if choice == 'n' and current_page < total_pages:
                    current_page += 1
                elif choice == 'p' and current_page > 1:
                    current_page -= 1
                elif choice == 'q':
                    break
                else:
                    print("Invalid choice or at boundary.")
            else:
                break
    
    def _export_questions(self):
        """Export selected questions"""
        if not self.selected_questions:
            print("No questions selected. Please select questions first.")
            return
        
        print("\nExport Options:")
        print("1. Excel (.xlsx)")
        print("2. CSV (.csv)")
        print("3. PDF Question Paper")
        print("4. JSON (.json)")
        print("5. Plain Text (.txt)")
        if ENHANCED_FEATURES_AVAILABLE:
            print("6. Word Document (.docx)")  # NEW option
        
        max_choice = 6 if ENHANCED_FEATURES_AVAILABLE else 5
        choice = input(f"Choose export format (1-{max_choice}): ").strip()
        
        if choice == '3':
            self._export_pdf_question_paper()
        elif choice == '6' and ENHANCED_FEATURES_AVAILABLE:
            # Word document export
            output_path = input("Enter output file path (e.g., exam.docx): ").strip()
            if not output_path:
                print("No output path provided.")
                return
            if not output_path.endswith('.docx'):
                output_path += '.docx'
            self._enhanced_export('docx', output_path)
        elif choice in ['4', '5']:
            output_path = input("Enter output file path (e.g., output.json or output.txt): ").strip()
            
            if not output_path:
                print("No output path provided.")
                return
            
            if choice == '4':
                format_type = 'json'
            else:  # choice == '5'
                format_type = 'txt'
                # Ask for TXT format style
                print("\nTXT Format Options:")
                print("1. Simple (questions only)")
                print("2. Detailed (with metadata)")
                print("3. Exam format (with marks)")
                style_choice = input("Choose format style (1-3, default: 2): ").strip() or '2'
                
                style_map = {'1': 'simple', '2': 'detailed', '3': 'exam'}
                format_style = style_map.get(style_choice, 'detailed')
            
            try:
                print(f"Exporting {len(self.selected_questions)} questions to: {output_path}")
                
                if format_type == 'txt':
                    success = self.generator.generate_output(
                        self.selected_questions, 
                        output_path, 
                        format_type=format_type,
                        format_style=format_style
                    )
                else:
                    success = self.generator.generate_output(
                        self.selected_questions, 
                        output_path, 
                        format_type=format_type
                    )
                
                if success:
                    print("✅ Questions exported successfully!")
                else:
                    print("❌ Export failed. Check the logs for details.")
                    
            except Exception as e:
                print(f"Error exporting questions: {str(e)}")
        else:
            output_path = input("Enter output file path (e.g., output.xlsx): ").strip()
            
            if not output_path:
                print("No output path provided.")
                return
            
            format_type = 'excel' if choice == '1' else 'csv'
            
            try:
                print(f"Exporting {len(self.selected_questions)} questions to: {output_path}")
                success = self.generator.generate_output(
                    self.selected_questions, 
                    output_path, 
                    format_type=format_type
                )
                
                if success:
                    print("✅ Questions exported successfully!")
                else:
                    print("❌ Export failed. Check the logs for details.")
                    
            except Exception as e:
                print(f"Error exporting questions: {str(e)}")
    
    def _export_pdf_question_paper(self):
        """Export questions as a formatted PDF question paper"""
        print("\nPDF Question Paper Configuration")
        print("=" * 40)
        
        # Get exam details
        title = input("Question Paper Title (default: 'Question Paper'): ").strip()
        if not title:
            title = "Question Paper"
        
        subject = input("Subject Name (default: 'General Knowledge'): ").strip()
        if not subject:
            subject = "General Knowledge"
        
        duration = input("Exam Duration (default: '3 Hours'): ").strip()
        if not duration:
            duration = "3 Hours"
        
        # Get marks configuration
        print("\nMarks Configuration:")
        two_marks_count = input("Number of 2-mark questions (default: 10): ").strip()
        try:
            two_marks_count = int(two_marks_count) if two_marks_count else 10
        except ValueError:
            two_marks_count = 10
        
        sixteen_marks_count = input("Number of 16-mark questions (default: 4): ").strip()
        try:
            sixteen_marks_count = int(sixteen_marks_count) if sixteen_marks_count else 4
        except ValueError:
            sixteen_marks_count = 4
        
        choice_options = input("Choice options for 16-mark questions (default: 2): ").strip()
        try:
            choice_options = int(choice_options) if choice_options else 2
        except ValueError:
            choice_options = 2
        
        # Calculate total marks
        total_marks = (two_marks_count * 2) + (sixteen_marks_count * 16)
        
        output_path = input(f"Output PDF path (default: '{subject.lower().replace(' ', '_')}_question_paper.pdf'): ").strip()
        if not output_path:
            output_path = f"{subject.lower().replace(' ', '_')}_question_paper.pdf"
        
        # Prepare marks configuration
        marks_config = {
            'title': title,
            'subject': subject,
            'duration': duration,
            'max_marks': total_marks,
            'two_marks_count': two_marks_count,
            'sixteen_marks_count': sixteen_marks_count,
            'choice_options': choice_options
        }
        
        print(f"\nGenerating PDF question paper...")
        print(f"Title: {title}")
        print(f"Subject: {subject}")
        print(f"Duration: {duration}")
        print(f"Total Marks: {total_marks}")
        print(f"2-mark questions: {two_marks_count}")
        print(f"16-mark questions: {sixteen_marks_count} (with {choice_options} choices each)")
        
        try:
            success = self.generator.generate_output(
                self.selected_questions,
                output_path,
                format_type='pdf',
                marks_config=marks_config
            )
            
            if success:
                print(f"✅ PDF question paper exported successfully to: {output_path}")
            else:
                print("❌ PDF export failed. Check the logs for details.")
                
        except Exception as e:
            print(f"Error exporting PDF: {str(e)}")

    def _show_statistics(self):
        """Show question bank statistics"""
        if not self.current_questions:
            print("No questions loaded. Please load questions first.")
            return
        
        stats = self.selector.get_statistics()
        
        print(f"\nQuestion Bank Statistics")
        print("=" * 30)
        print(f"Total Questions: {stats['total_questions']}")
        
        print(f"\nTopics ({len(stats['topics'])}):")
        for topic, count in stats['topics'].items():
            print(f"  {topic}: {count}")
        
        print(f"\nDifficulties ({len(stats['difficulties'])}):")
        for difficulty, count in stats['difficulties'].items():
            print(f"  {difficulty}: {count}")
        
        print(f"\nTypes ({len(stats['types'])}):")
        for q_type, count in stats['types'].items():
            print(f"  {q_type}: {count}")
    
    def _clear_selection(self):
        """Clear current selection"""
        self.selected_questions = []
        self.last_criteria = {}
        print("✅ Selection cleared.")
    
    def _show_criteria(self):
        """Show last used criteria"""
        if not self.last_criteria:
            print("No criteria used yet.")
            return
        
        print("\nLast Used Criteria:")
        print("=" * 20)
        for key, value in self.last_criteria.items():
            print(f"{key}: {value}")
    
    def _train_models(self):
        """Train AI models"""
        if not self.current_questions:
            print("No questions loaded. Please load questions first.")
            return
        
        if len(self.current_questions) < 50:
            print("Need at least 50 questions to train models effectively.")
            return
        
        print("Training AI models...")
        print("This may take a few minutes...")
        
        try:
            results = self.selector.train_models()
            
            print("\n✅ Training completed!")
            print("Model Performance:")
            for model, accuracy in results.items():
                print(f"  {model}: {accuracy:.3f}")
                
        except Exception as e:
            print(f"Error training models: {str(e)}")
    
    def _unit_based_selection(self):
        """Enhanced unit-based question selection"""
        if not ENHANCED_FEATURES_AVAILABLE:
            print("❌ Enhanced features not available. Please install dependencies:")
            print("   pip install python-docx PyPDF2 pdfplumber")
            return
            
        if not self.current_questions:
            print("No questions loaded. Please load questions first.")
            return
        
        # Load questions into enhanced selector
        self.enhanced_selector.load_questions(self.current_questions)
        
        print("\n🎯 Unit-Based Question Selection")
        print("=" * 40)
        
        # Show available units
        available_units = self.enhanced_selector.get_available_units()
        if not available_units:
            print("No units/topics found in the question bank.")
            return
        
        print("Available Units/Topics:")
        for i, unit in enumerate(available_units, 1):
            print(f"  {i}. {unit}")
        
        # Get user selection
        try:
            unit_input = input("\nEnter unit numbers (comma-separated, e.g., 1,3,5): ").strip()
            if not unit_input:
                print("No units selected.")
                return
            
            unit_indices = [int(x.strip()) - 1 for x in unit_input.split(',')]
            selected_units = [available_units[i] for i in unit_indices if 0 <= i < len(available_units)]
            
            if not selected_units:
                print("Invalid unit selection.")
                return
            
            print(f"Selected units: {', '.join(selected_units)}")
            
            # Get total marks
            total_marks = input("Enter total marks for the question paper (e.g., 100): ").strip()
            total_marks = int(total_marks) if total_marks else 100
            
            # Perform selection
            print("\nSelecting questions...")
            result = self.enhanced_selector.select_questions_by_units_and_marks(
                selected_units, total_marks
            )
            
            self.selected_questions = result['questions']
            
            print(f"\n✅ Selection completed!")
            print(f"Selected {len(self.selected_questions)} questions")
            print(f"Total marks: {result['total_marks']}")
            print(f"Distribution: {result['distribution']}")
            print(f"Units covered: {', '.join(result['units_covered'])}")
            
            if result['choice_options'] > 0:
                print(f"16-mark questions will have {result['choice_options']} choice options")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error during selection: {e}")
    
    def _enhanced_export(self, format_type: str, output_path: str):
        """Enhanced export with Word document support"""
        if not ENHANCED_FEATURES_AVAILABLE:
            print("❌ Enhanced features not available.")
            return False
        
        if not self.selected_questions:
            print("No questions selected. Please select questions first.")
            return False
        
        if format_type == 'docx':
            print("\nWord Document Configuration:")
            title = input("Question Paper Title (default: 'Question Paper'): ").strip()
            if not title:
                title = "Question Paper"
            
            subject = input("Subject Name (default: 'General Knowledge'): ").strip()
            if not subject:
                subject = "General Knowledge"
            
            duration = input("Exam Duration (default: '3 Hours'): ").strip()
            if not duration:
                duration = "3 Hours"
            
            # Calculate total marks
            total_marks = sum(int(q.get('marks', 2)) for q in self.selected_questions)
            
            # Count 16-mark questions for choice options
            sixteen_mark_count = len([q for q in self.selected_questions if int(q.get('marks', 2)) == 16])
            choice_options = 2 if sixteen_mark_count > 0 else 0
            
            paper_config = {
                'title': title,
                'subject': subject,
                'duration': duration,
                'total_marks': total_marks,
                'choice_options': choice_options
            }
            
            try:
                success = self.word_generator.generate_question_paper(
                    self.selected_questions,
                    output_path,
                    paper_config
                )
                
                if success:
                    print(f"✅ Word document exported successfully to: {output_path}")
                    return True
                else:
                    print("❌ Word document export failed.")
                    return False
                    
            except Exception as e:
                print(f"Error exporting Word document: {e}")
                return False
        
        return False


def main():
    """Main entry point for CLI"""
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()
