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

# Optional import for tabulate
try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

from ..data_processing.question_parser import QuestionParser
from ..selection_engine.question_selector import QuestionSelector
from ..export.spreadsheet_generator import SpreadsheetGenerator


class CLIInterface:
    """Command-line interface for question selection"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.parser = QuestionParser()
        self.selector = QuestionSelector()
        self.generator = SpreadsheetGenerator()
        
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
load     - Load questions from a file
select   - Select questions based on criteria
show     - Show selected questions
export   - Export selected questions to spreadsheet
stats    - Show question bank statistics
clear    - Clear current selection
criteria - Show last used criteria
train    - Train AI models on current question bank
help     - Show this help message
exit     - Exit the program

Examples:
---------
load data/questions.csv
select topic:math difficulty:medium count:20
export output.xlsx
        """
        print(help_text)
    
    def _load_questions(self):
        """Load questions from file"""
        file_path = input("Enter path to question bank file: ").strip()
        
        if not file_path:
            print("No file path provided.")
            return
        
        try:
            print(f"Loading questions from: {file_path}")
            questions = self.parser.parse_file(file_path)
            
            if not questions:
                print("No questions found in file.")
                return
            
            self.current_questions = questions
            self.selector.load_questions(questions)
            
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
        headers = ['ID', 'Topic', 'Difficulty', 'Type', 'Length']
        rows = []
        
        for q in self.selected_questions:
            rows.append([
                q.get('id', 'N/A'),
                q.get('topic', 'N/A'),
                q.get('difficulty', 'N/A'),
                q.get('type', 'N/A'),
                len(q.get('question', ''))
            ])
        
        print(tabulate(rows, headers=headers, tablefmt='grid'))
    
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
        
        output_path = input("Enter output file path (e.g., output.xlsx): ").strip()
        
        if not output_path:
            print("No output path provided.")
            return
        
        try:
            print(f"Exporting {len(self.selected_questions)} questions to: {output_path}")
            success = self.generator.generate_spreadsheet(self.selected_questions, output_path)
            
            if success:
                print("✅ Questions exported successfully!")
            else:
                print("❌ Export failed. Check the logs for details.")
                
        except Exception as e:
            print(f"Error exporting questions: {str(e)}")
    
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


def main():
    """Main entry point for CLI"""
    cli = CLIInterface()
    cli.run()


if __name__ == "__main__":
    main()
