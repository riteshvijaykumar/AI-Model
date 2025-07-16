#!/usr/bin/env python3
"""
AI Question Bank Selection Model - Main Entry Point

This script provides the main interface for the AI-powered question selection system.
Users can select relevant questions from a question bank and generate tailored 
question sets in spreadsheet format.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

# Import core modules
try:
    from src.selection_engine.question_selector import QuestionSelector
    from src.data_processing.question_parser import QuestionParser
    from src.export.spreadsheet_generator import SpreadsheetGenerator
    CORE_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Error importing core modules: {e}")
    print("Please install required dependencies: pip install -r requirements.txt")
    sys.exit(1)

# Import UI modules (optional)
try:
    from src.ui.cli_interface import CLIInterface
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False

try:
    from src.ui.gui_interface import launch_gui
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        description="AI Question Bank Selection Model",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --input questions.csv --output selected.xlsx
  python main.py --gui
  python main.py --cli
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Path to input question bank file (CSV, Excel, JSON, TXT, or PDF)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Path to output spreadsheet file'
    )
    
    parser.add_argument(
        '--criteria', '-c',
        type=str,
        help='Selection criteria (e.g., "difficulty:medium,topic:math,count:20")'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['excel', 'csv', 'pdf', 'json', 'txt'],
        default='excel',
        help='Output format: excel, csv, pdf, json, or txt (default: excel)'
    )
    
    parser.add_argument(
        '--marks-config',
        type=str,
        help='Marks configuration for PDF format (e.g., "2marks:10,16marks:4,choices:2")'
    )
    
    parser.add_argument(
        '--title',
        type=str,
        help='Title for PDF question paper'
    )
    
    parser.add_argument(
        '--subject',
        type=str,
        help='Subject name for PDF question paper'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch graphical user interface'
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Launch command-line interface'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/settings.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # If no specific mode is chosen, determine based on arguments
    if not args.gui and not args.cli:
        if args.input and args.output:
            # Direct processing mode
            process_direct(args)
        else:
            # Default to CLI
            args.cli = True
    
    # Launch appropriate interface
    if args.gui:
        print("Launching GUI interface...")
        print("Please use: streamlit run streamlit_app.py")
        import subprocess
        import sys
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    elif args.cli:
        if not CLI_AVAILABLE:
            print("❌ CLI interface not available due to missing dependencies.")
            print("Please install missing packages or use the minimal CLI:")
            print("   python minimal_cli.py")
            return 1
        
        print("Launching CLI interface...")
        cli = CLIInterface(config_path=args.config)
        cli.run()
    
    return 0


def process_direct(args):
    """Process questions directly from command line arguments"""
    try:
        print(f"Loading question bank from: {args.input}")
        
        # Initialize components
        parser = QuestionParser()
        selector = QuestionSelector()
        exporter = SpreadsheetGenerator()
        
        # Load and parse question bank
        questions = parser.parse_file(args.input)
        selector.load_questions(questions)
        
        # Parse criteria if provided
        criteria = {}
        if args.criteria:
            for criterion in args.criteria.split(','):
                key, value = criterion.split(':')
                criteria[key.strip()] = value.strip()
        
        # Select questions
        print("Selecting questions based on criteria...")
        selected_questions = selector.select_questions(**criteria)
        
        # Prepare export parameters
        export_kwargs = {'format_type': args.format}
        
        # Handle PDF-specific configuration
        if args.format == 'pdf':
            marks_config = {}
            
            # Parse marks configuration
            if args.marks_config:
                for config_item in args.marks_config.split(','):
                    key, value = config_item.split(':')
                    key = key.strip()
                    if key == '2marks':
                        marks_config['two_marks_count'] = int(value)
                    elif key == '16marks':
                        marks_config['sixteen_marks_count'] = int(value)
                    elif key == 'choices':
                        marks_config['choice_options'] = int(value)
            
            # Set defaults if not provided
            marks_config.setdefault('two_marks_count', 10)
            marks_config.setdefault('sixteen_marks_count', 4)
            marks_config.setdefault('choice_options', 2)
            
            # Add title and subject if provided
            if args.title:
                marks_config['title'] = args.title
            if args.subject:
                marks_config['subject'] = args.subject
            
            export_kwargs['marks_config'] = marks_config
            
            print(f"PDF Configuration:")
            print(f"  2-mark questions: {marks_config['two_marks_count']}")
            print(f"  16-mark questions: {marks_config['sixteen_marks_count']}")
            print(f"  Choice options: {marks_config['choice_options']}")
        
        # Export questions
        print(f"Exporting {len(selected_questions)} questions to: {args.output}")
        success = exporter.generate_output(selected_questions, args.output, **export_kwargs)
        
        if success:
            print("✅ Process completed successfully!")
        else:
            print("❌ Export failed. Check the logs for details.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    sys.exit(main())
