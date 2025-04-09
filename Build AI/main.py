#!/usr/bin/env python3
"""
AI Insurance Claims Denial Appeal Writer
Main application module
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

from appeal_writer import AppealWriter
from user_input_processor import UserInputProcessor
from letter_generator import LetterGenerator

class AppealWriterApp:
    """Main application class for the Insurance Claims Denial Appeal Writer"""
    
    def __init__(self, templates_dir: str = "../templates", output_dir: str = "../output"):
        """Initialize the AppealWriterApp with component modules"""
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize component modules
        self.appeal_writer = AppealWriter(templates_dir=templates_dir)
        self.input_processor = UserInputProcessor()
        self.letter_generator = LetterGenerator(output_dir=output_dir)
    
    def process_user_input(self, input_data: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str]]:
        """
        Process and validate user input data
        
        Args:
            input_data: Raw user input data
            
        Returns:
            Tuple of (is_valid, processed_data, error_messages)
        """
        # Process form data
        processed_data = self.input_processor.process_form_data(input_data)
        
        # Validate inputs
        is_valid, missing_fields = self.input_processor.validate_inputs(processed_data)
        
        return is_valid, processed_data, missing_fields
    
    def generate_appeal_letter(self, user_data: Dict[str, Any], output_format: str = "all") -> Dict[str, str]:
        """
        Generate an appeal letter based on user data
        
        Args:
            user_data: Processed user data
            output_format: Desired output format (markdown, html, pdf, docx, or all)
            
        Returns:
            Dictionary mapping format names to file paths
        """
        # Generate the appeal letter content
        appeal_letter = self.appeal_writer.generate_appeal_letter(user_data)
        
        # Generate the output file(s)
        base_filename = f"appeal_{user_data.get('claim_number', 'letter')}"
        
        if output_format == "markdown" or output_format == "md":
            return {"markdown": self.letter_generator.generate_markdown(appeal_letter, base_filename)}
        elif output_format == "html":
            return {"html": self.letter_generator.generate_html(appeal_letter, base_filename)}
        elif output_format == "pdf":
            return {"pdf": self.letter_generator.generate_pdf(appeal_letter, base_filename)}
        elif output_format == "docx":
            return {"docx": self.letter_generator.generate_docx(appeal_letter, base_filename)}
        else:  # Default to all formats
            return self.letter_generator.generate_all_formats(appeal_letter, base_filename)
    
    def create_submission_package(self, user_data: Dict[str, Any]) -> str:
        """
        Create a complete submission package with appeal letter and supporting documents
        
        Args:
            user_data: Processed user data
            
        Returns:
            Path to the submission package directory
        """
        # Generate the appeal letter
        appeal_letter = self.appeal_writer.generate_appeal_letter(user_data)
        
        # Get supporting documents
        supporting_docs = user_data.get('supporting_docs', [])
        
        # Create the submission package
        return self.letter_generator.create_submission_package(appeal_letter, supporting_docs, user_data)
    
    def get_suggestions(self, user_data: Dict[str, Any]) -> List[str]:
        """
        Get suggestions for improving the appeal
        
        Args:
            user_data: Processed user data
            
        Returns:
            List of suggestions
        """
        return self.input_processor.suggest_additional_information(user_data)
    
    def run_cli(self):
        """Run the application in command-line interface mode"""
        parser = argparse.ArgumentParser(description='Insurance Claims Denial Appeal Writer')
        parser.add_argument('--input', '-i', type=str, help='Input JSON file with user data')
        parser.add_argument('--output-format', '-f', type=str, default='all', 
                           choices=['markdown', 'md', 'html', 'pdf', 'docx', 'all'],
                           help='Output format for the appeal letter')
        parser.add_argument('--package', '-p', action='store_true',
                           help='Create a complete submission package')
        
        args = parser.parse_args()
        
        # Check if input file is provided
        if not args.input:
            print("Error: Input file is required")
            parser.print_help()
            sys.exit(1)
        
        # Load user data from input file
        try:
            with open(args.input, 'r') as file:
                input_data = json.load(file)
        except Exception as e:
            print(f"Error loading input file: {e}")
            sys.exit(1)
        
        # Process and validate user input
        is_valid, processed_data, missing_fields = self.process_user_input(input_data)
        
        if not is_valid:
            print("Error: Invalid input data")
            print("Missing or incorrect fields:")
            for field in missing_fields:
                print(f"- {field}")
            sys.exit(1)
        
        # Get suggestions
        suggestions = self.get_suggestions(processed_data)
        if suggestions:
            print("Suggestions for strengthening your appeal:")
            for suggestion in suggestions:
                print(f"- {suggestion}")
            print()
        
        # Generate the appeal letter
        if args.package:
            # Create a complete submission package
            package_path = self.create_submission_package(processed_data)
            print(f"Submission package created at: {package_path}")
        else:
            # Generate the appeal letter in the requested format(s)
            output_files = self.generate_appeal_letter(processed_data, args.output_format)
            print("Appeal letter generated successfully!")
            for format_name, file_path in output_files.items():
                print(f"{format_name.upper()} version saved to: {file_path}")


def main():
    """Main entry point for the application"""
    app = AppealWriterApp()
    app.run_cli()


if __name__ == "__main__":
    main()
