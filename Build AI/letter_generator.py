#!/usr/bin/env python3
"""
AI Insurance Claims Denial Appeal Writer
Letter generation and output module
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import markdown
import pdfkit
from jinja2 import Template

class LetterGenerator:
    """Generate and format appeal letters in various output formats"""
    
    def __init__(self, output_dir: str = "../output"):
        """Initialize the LetterGenerator with output directory"""
        self.output_dir = Path(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_markdown(self, appeal_letter: str, filename: str) -> str:
        """
        Save the appeal letter as a Markdown file
        
        Args:
            appeal_letter: The appeal letter text
            filename: Base filename (without extension)
            
        Returns:
            Path to the saved file
        """
        output_path = self.output_dir / f"{filename}.md"
        with open(output_path, 'w') as file:
            file.write(appeal_letter)
        return str(output_path)
    
    def generate_html(self, appeal_letter: str, filename: str) -> str:
        """
        Convert the appeal letter to HTML and save
        
        Args:
            appeal_letter: The appeal letter text in Markdown format
            filename: Base filename (without extension)
            
        Returns:
            Path to the saved HTML file
        """
        # Convert Markdown to HTML
        html_content = markdown.markdown(appeal_letter)
        
        # Wrap in a basic HTML template with styling
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Insurance Appeal Letter</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                h1, h2, h3 {
                    color: #333;
                }
                .header {
                    margin-bottom: 30px;
                }
                .footer {
                    margin-top: 30px;
                    border-top: 1px solid #ccc;
                    padding-top: 10px;
                }
                .enclosures {
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <div class="content">
                {{ content }}
            </div>
        </body>
        </html>
        """
        
        # Render the template
        template = Template(html_template)
        html_output = template.render(content=html_content)
        
        # Save the HTML file
        output_path = self.output_dir / f"{filename}.html"
        with open(output_path, 'w') as file:
            file.write(html_output)
        
        return str(output_path)
    
    def generate_pdf(self, appeal_letter: str, filename: str) -> str:
        """
        Convert the appeal letter to PDF and save
        
        Args:
            appeal_letter: The appeal letter text in Markdown format
            filename: Base filename (without extension)
            
        Returns:
            Path to the saved PDF file
        """
        # First generate HTML
        html_path = self.generate_html(appeal_letter, f"{filename}_temp")
        
        # Convert HTML to PDF
        output_path = self.output_dir / f"{filename}.pdf"
        
        try:
            # Use pdfkit (wrapper for wkhtmltopdf) to convert HTML to PDF
            pdfkit.from_file(html_path, str(output_path))
            
            # Remove temporary HTML file
            os.remove(html_path)
            
            return str(output_path)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            print("Falling back to HTML output only")
            return html_path
    
    def generate_docx(self, appeal_letter: str, filename: str) -> str:
        """
        Convert the appeal letter to DOCX and save
        
        Args:
            appeal_letter: The appeal letter text in Markdown format
            filename: Base filename (without extension)
            
        Returns:
            Path to the saved DOCX file
        """
        try:
            # This would use a library like python-docx in a real implementation
            # For this example, we'll just note that it would be implemented
            output_path = self.output_dir / f"{filename}.docx"
            
            # Placeholder for actual DOCX generation
            with open(output_path, 'w') as file:
                file.write("This would be a DOCX file in a real implementation.\n\n")
                file.write(appeal_letter)
            
            return str(output_path)
        except Exception as e:
            print(f"Error generating DOCX: {e}")
            print("Falling back to Markdown output")
            return self.generate_markdown(appeal_letter, filename)
    
    def generate_all_formats(self, appeal_letter: str, base_filename: str) -> Dict[str, str]:
        """
        Generate the appeal letter in all available formats
        
        Args:
            appeal_letter: The appeal letter text in Markdown format
            base_filename: Base filename (without extension)
            
        Returns:
            Dictionary mapping format names to file paths
        """
        outputs = {}
        
        # Generate each format
        outputs['markdown'] = self.generate_markdown(appeal_letter, base_filename)
        outputs['html'] = self.generate_html(appeal_letter, base_filename)
        
        try:
            outputs['pdf'] = self.generate_pdf(appeal_letter, base_filename)
        except Exception as e:
            print(f"PDF generation failed: {e}")
        
        try:
            outputs['docx'] = self.generate_docx(appeal_letter, base_filename)
        except Exception as e:
            print(f"DOCX generation failed: {e}")
        
        return outputs
    
    def create_submission_package(self, appeal_letter: str, supporting_docs: List[str], 
                                 user_data: Dict[str, Any]) -> str:
        """
        Create a complete submission package with appeal letter and supporting documents
        
        Args:
            appeal_letter: The appeal letter text
            supporting_docs: List of paths to supporting documents
            user_data: User data dictionary
            
        Returns:
            Path to the submission package directory
        """
        # Create a unique directory for this submission package
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        package_dir = self.output_dir / f"appeal_package_{timestamp}"
        os.makedirs(package_dir, exist_ok=True)
        
        # Generate the appeal letter in multiple formats
        base_filename = "appeal_letter"
        self.generate_all_formats(appeal_letter, str(package_dir / base_filename))
        
        # Create a cover sheet for the package
        cover_sheet = self._create_cover_sheet(user_data)
        with open(package_dir / "cover_sheet.md", 'w') as file:
            file.write(cover_sheet)
        
        # Create a checklist for submission
        checklist = self._create_submission_checklist(user_data, supporting_docs)
        with open(package_dir / "submission_checklist.md", 'w') as file:
            file.write(checklist)
        
        # In a real implementation, this would also copy the supporting documents
        # to the package directory
        
        return str(package_dir)
    
    def _create_cover_sheet(self, user_data: Dict[str, Any]) -> str:
        """Create a cover sheet for the appeal package"""
        cover_sheet = f"""# Insurance Appeal Submission Package

## Claimant Information
- **Name:** {user_data.get('policyholder_name', '')}
- **Policy Number:** {user_data.get('policy_number', '')}
- **Claim Number:** {user_data.get('claim_number', '')}
- **Date of Service/Incident:** {user_data.get('date_of_service', user_data.get('date_of_incident', ''))}
- **Date of Denial:** {user_data.get('denial_date', '')}

## Appeal Information
- **Insurance Company:** {user_data.get('insurance_company_name', '')}
- **Type of Insurance:** {user_data.get('insurance_type', '').capitalize()}
- **Reason for Denial:** {user_data.get('denial_reason', '').replace('_', ' ').capitalize()}
- **Date of Appeal:** {datetime.datetime.now().strftime("%B %d, %Y")}

## Package Contents
1. This Cover Sheet
2. Appeal Letter
3. Copy of Denial Letter
4. [Additional contents listed in the Submission Checklist]

## Contact Information
If you have any questions regarding this appeal, please contact:

{user_data.get('policyholder_name', '')}
{user_data.get('policyholder_address', '')}
{user_data.get('city_state_zip', '')}
Phone: {user_data.get('phone', 'Not provided')}
Email: {user_data.get('email', 'Not provided')}
"""
        return cover_sheet
    
    def _create_submission_checklist(self, user_data: Dict[str, Any], 
                                    supporting_docs: List[str]) -> str:
        """Create a checklist for appeal submission"""
        checklist = f"""# Appeal Submission Checklist

## Required Items
- [ ] Signed and dated appeal letter
- [ ] Copy of denial letter from insurance company
- [ ] Copy of relevant medical records or documentation

## Supporting Documentation
"""
        # Add each supporting document to the checklist
        for doc in supporting_docs:
            checklist += f"- [ ] {doc}\n"
        
        checklist += """
## Submission Instructions
1. Make copies of all documents for your records
2. Send the appeal package via certified mail with return receipt requested
3. If submitting electronically, keep confirmation of submission
4. Follow up with the insurance company if you don't receive a response within the timeframe specified in your policy

## Important Deadlines
"""
        # Add deadline information if available
        if 'appeal_deadline' in user_data:
            checklist += f"- Appeal must be submitted by: {user_data.get('appeal_deadline')}\n"
        else:
            checklist += "- Check your denial letter or policy for the appeal deadline\n"
        
        checklist += """
## After Submission
- Mark your calendar to follow up if no response within 30 days
- Prepare for possible second-level appeal if first appeal is denied
- Consider contacting your state insurance department if appeal is denied
"""
        return checklist


def main():
    """Example usage of the LetterGenerator class"""
    generator = LetterGenerator()
    
    # Example appeal letter (simplified)
    appeal_letter = """# Appeal of Insurance Claim Denial

[Date]

[Insurance Company]
[Address]
[City, State ZIP]

**Re: Appeal of Claim Denial**
Policy Number: ABC123456
Claim Number: CLM987654321
Date of Service: March 15, 2025

Dear Claims Review Department:

I am writing to appeal your decision to deny my claim for an MRI of the lumbar spine that was provided on March 15, 2025.

## Medical Necessity

The MRI was ordered by Dr. Smith due to persistent lower back pain that did not respond to conservative treatment.

## Supporting Documentation

I have enclosed the following documentation:
1. Copy of the denial letter
2. Letter from Dr. Smith explaining medical necessity
3. Medical records documenting my condition

Thank you for your prompt attention to this matter.

Sincerely,

Jane Doe
"""
    
    # Example user data
    user_data = {
        'policyholder_name': 'Jane Doe',
        'policy_number': 'ABC123456',
        'claim_number': 'CLM987654321',
        'insurance_company_name': 'XYZ Insurance',
        'insurance_type': 'health',
        'denial_reason': 'medical_necessity',
        'date_of_service': 'March 15, 2025',
        'denial_date': 'March 30, 2025',
        'email': 'jane.doe@example.com',
        'phone': '555-123-4567'
    }
    
    # Example supporting documents
    supporting_docs = [
        'Denial Letter.pdf',
        'Medical Necessity Letter from Dr. Smith.pdf',
        'Medical Records.pdf',
        'MRI Report.pdf'
    ]
    
    # Generate the letter in different formats
    print("Generating appeal letter in multiple formats...")
    output_files = generator.generate_all_formats(appeal_letter, "example_appeal")
    
    for format_name, file_path in output_files.items():
        print(f"{format_name.upper()} version saved to: {file_path}")
    
    # Create a complete submission package
    print("\nCreating submission package...")
    package_path = generator.create_submission_package(appeal_letter, supporting_docs, user_data)
    print(f"Submission package created at: {package_path}")


if __name__ == "__main__":
    main()
