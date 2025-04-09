#!/usr/bin/env python3
"""
AI Insurance Claims Denial Appeal Writer
Test script for evaluating the appeal writer with sample cases
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from appeal_writer import AppealWriter
from user_input_processor import UserInputProcessor
from letter_generator import LetterGenerator
from main import AppealWriterApp

def run_test(test_file, output_dir="./output"):
    """Run a test case and return the results"""
    print(f"Running test: {test_file}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load test data
    with open(test_file, 'r') as file:
        test_data = json.load(file)
    
    # Initialize the app
    app = AppealWriterApp(output_dir=output_dir)
    
    # Process and validate the test data
    is_valid, processed_data, missing_fields = app.process_user_input(test_data)
    
    if not is_valid:
        print("Test data validation failed:")
        for field in missing_fields:
            print(f"- {field}")
        return False, None
    
    # Get suggestions
    suggestions = app.get_suggestions(processed_data)
    if suggestions:
        print("Suggestions for strengthening the appeal:")
        for suggestion in suggestions:
            print(f"- {suggestion}")
    
    # Generate the appeal letter
    test_name = Path(test_file).stem
    base_filename = f"{test_name}_result"
    
    try:
        # Generate the appeal letter in all formats
        output_files = app.generate_appeal_letter(processed_data, "all")
        
        print("Appeal letter generated successfully!")
        for format_name, file_path in output_files.items():
            print(f"{format_name.upper()} version saved to: {file_path}")
        
        return True, output_files
    except Exception as e:
        print(f"Error generating appeal letter: {e}")
        return False, None

def run_all_tests(test_dir=None, output_dir="./output"):
    """Run all test cases in the test directory"""
    if test_dir is None:
        # Use the directory where this script is located
        test_dir_path = Path(__file__).parent
    else:
        test_dir_path = Path(test_dir)
    
    # Find all JSON test files
    test_files = list(test_dir_path.glob("*.json"))
    
    if not test_files:
        print(f"No test files found in {test_dir}")
        return
    
    print(f"Found {len(test_files)} test files")
    
    # Run each test
    results = {}
    for test_file in test_files:
        success, output_files = run_test(test_file, output_dir)
        results[test_file.name] = {
            "success": success,
            "output_files": output_files
        }
        print()  # Add a blank line between tests
    
    # Print summary
    print("\n=== Test Summary ===")
    success_count = sum(1 for result in results.values() if result["success"])
    print(f"Passed: {success_count}/{len(results)}")
    
    for test_name, result in results.items():
        status = "PASS" if result["success"] else "FAIL"
        print(f"{test_name}: {status}")
    
    return results

def main():
    """Main entry point for the test script"""
    parser = argparse.ArgumentParser(description='Test the Insurance Claims Denial Appeal Writer')
    parser.add_argument('--test-file', '-t', type=str, help='Specific test file to run')
    parser.add_argument('--test-dir', '-d', type=str, help='Directory containing test files')
    parser.add_argument('--output-dir', '-o', type=str, default='../output', help='Directory for output files')
    
    args = parser.parse_args()
    
    if args.test_file:
        # Run a specific test
        run_test(args.test_file, args.output_dir)
    else:
        # Run all tests
        run_all_tests(args.test_dir, args.output_dir)

if __name__ == "__main__":
    main()
