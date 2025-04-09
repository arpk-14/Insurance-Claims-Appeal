#!/usr/bin/env python3
"""
AI Insurance Claims Denial Appeal Writer
Core functionality for generating customized appeal letters
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

class AppealWriter:
    """Main class for the Insurance Claims Denial Appeal Writer"""
    
    def __init__(self, templates_dir: str = "../templates"):
        """Initialize the AppealWriter with templates directory"""
        self.templates_dir = Path(templates_dir)
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, str]:
        """Load all template files from the templates directory"""
        templates = {}
        for template_file in self.templates_dir.glob("*.md"):
            template_name = template_file.stem
            with open(template_file, 'r') as file:
                templates[template_name] = file.read()
        return templates
    
    def select_template(self, insurance_type: str, denial_reason: str) -> str:
        """Select the appropriate template based on insurance type and denial reason"""
        if insurance_type == "health":
            if denial_reason == "medical_necessity":
                return "health_medical_necessity_template"
            elif denial_reason == "experimental_treatment":
                return "health_experimental_treatment_template"
            elif denial_reason == "mental_health_parity":
                return "health_mental_health_parity_template"
            elif denial_reason == "out_of_network":
                return "out_of_network_denial_template"
            elif denial_reason == "prior_authorization":
                return "prior_authorization_denial_template"
            elif denial_reason == "billing_coding_error":
                return "billing_coding_error_template"
            elif denial_reason == "pre_existing_condition":
                return "pre_existing_condition_template"
            else:
                # Default to medical necessity if specific reason not found
                return "health_medical_necessity_template"
        elif insurance_type == "auto":
            return "auto_insurance_denial_template"
        elif insurance_type == "home":
            return "home_insurance_denial_template"
        else:
            # Default to medical necessity if insurance type not found
            return "health_medical_necessity_template"
    
    def customize_template(self, template_name: str, user_inputs: Dict[str, Any],
                          conditional_sections: Dict[str, bool] = None,
                          supporting_docs: List[str] = None,
                          tone_preferences: Dict[str, Any] = None,
                          urgency_level: int = 0) -> str:
        """
        Customize a template with user inputs and conditional sections
        
        Args:
            template_name: Name of the template to customize
            user_inputs: Dictionary of user inputs to replace placeholders
            conditional_sections: Dictionary of conditional sections to include/exclude
            supporting_docs: List of supporting documents available
            tone_preferences: Dictionary of tone preferences (formality, assertiveness)
            urgency_level: Urgency level (0-5, with 5 being most urgent)
            
        Returns:
            Customized appeal letter text
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        # Get the template text
        template_text = self.templates[template_name]
        
        # Replace common placeholders
        letter_text = self._replace_common_placeholders(template_text, user_inputs)
        
        # Handle conditional sections
        if conditional_sections:
            letter_text = self._handle_conditional_sections(letter_text, conditional_sections)
        
        # Customize supporting documentation section
        if supporting_docs:
            letter_text = self._customize_supporting_docs(letter_text, supporting_docs)
        
        # Adjust tone if preferences provided
        if tone_preferences:
            letter_text = self._adjust_tone(letter_text, tone_preferences)
        
        # Add urgency language if needed
        if urgency_level > 3:  # Only add for higher urgency levels
            letter_text = self._add_urgency_language(letter_text, urgency_level)
        
        return letter_text
    
    def _replace_common_placeholders(self, text: str, user_inputs: Dict[str, Any]) -> str:
        """Replace common placeholders in the template with user inputs"""
        # Set current date if not provided
        if 'date' not in user_inputs:
            user_inputs['date'] = datetime.datetime.now().strftime("%B %d, %Y")
        
        # Common placeholders across all templates
        common_placeholders = {
            "[Policyholder Name]": user_inputs.get('policyholder_name', ''),
            "[Policyholder Address]": user_inputs.get('policyholder_address', ''),
            "[City, State ZIP]": user_inputs.get('city_state_zip', ''),
            "[Date]": user_inputs.get('date', ''),
            "[Insurance Company Name]": user_inputs.get('insurance_company_name', ''),
            "[Insurance Company Address]": user_inputs.get('insurance_company_address', ''),
            "[Policy Number]": user_inputs.get('policy_number', ''),
            "[Claim Number]": user_inputs.get('claim_number', ''),
            "[Date of Service]": user_inputs.get('date_of_service', ''),
            "[Date of Incident]": user_inputs.get('date_of_incident', ''),
            "[Patient Name]": user_inputs.get('patient_name', user_inputs.get('policyholder_name', '')),
            "[denial date]": user_inputs.get('denial_date', '')
        }
        
        # Replace common placeholders
        result = text
        for placeholder, value in common_placeholders.items():
            result = result.replace(placeholder, value)
        
        # Replace insurance-type specific placeholders
        if user_inputs.get('insurance_type') == 'health':
            health_placeholders = {
                "[Provider Name]": user_inputs.get('provider_name', ''),
                "[physician name]": user_inputs.get('physician_name', ''),
                "[treatment/procedure/service]": user_inputs.get('treatment', ''),
                "[diagnosis]": user_inputs.get('diagnosis', '')
            }
            for placeholder, value in health_placeholders.items():
                result = result.replace(placeholder, value)
                
        elif user_inputs.get('insurance_type') == 'auto':
            auto_placeholders = {
                "[Vehicle Information]": user_inputs.get('vehicle_info', ''),
                "[Accident Description]": user_inputs.get('accident_description', '')
            }
            for placeholder, value in auto_placeholders.items():
                result = result.replace(placeholder, value)
                
        elif user_inputs.get('insurance_type') == 'home':
            home_placeholders = {
                "[Property Address]": user_inputs.get('property_address', ''),
                "[Damage Description]": user_inputs.get('damage_description', ''),
                "[Cause of Damage]": user_inputs.get('damage_cause', '')
            }
            for placeholder, value in home_placeholders.items():
                result = result.replace(placeholder, value)
        
        return result
    
    def _handle_conditional_sections(self, text: str, conditional_sections: Dict[str, bool]) -> str:
        """Include or exclude conditional sections based on user inputs"""
        # This is a simplified implementation
        # In a real system, you would have more sophisticated section handling
        
        lines = text.split('\n')
        result_lines = []
        
        skip_section = False
        current_section = None
        
        for line in lines:
            # Check for section markers (simplified approach)
            if line.startswith("### "):
                section_name = line[4:].strip()
                if section_name in conditional_sections:
                    current_section = section_name
                    skip_section = not conditional_sections[section_name]
                else:
                    current_section = None
                    skip_section = False
            
            # If we're not skipping the current section, add the line
            if not skip_section:
                result_lines.append(line)
            
            # Check for end of section (simplified - assumes a new section or blank line ends the previous)
            if current_section and (line.strip() == "" or line.startswith("### ")):
                current_section = None
                skip_section = False
        
        return '\n'.join(result_lines)
    
    def _customize_supporting_docs(self, text: str, supporting_docs: List[str]) -> str:
        """Customize the supporting documentation section based on available docs"""
        # Find the enclosures section
        enclosures_start = text.find("Enclosures:")
        if enclosures_start == -1:
            return text
        
        # Find the end of the enclosures section (next section or end of text)
        enclosures_end = text.find("\n\n", enclosures_start)
        if enclosures_end == -1:
            enclosures_end = len(text)
        
        # Build new enclosures section
        new_enclosures = "Enclosures:\n"
        new_enclosures += "1. Copy of Denial Letter\n"
        
        # Add each supporting document
        for i, doc in enumerate(supporting_docs, 2):
            new_enclosures += f"{i}. {doc}\n"
        
        # Replace the old enclosures section with the new one
        return text[:enclosures_start] + new_enclosures + text[enclosures_end:]
    
    def _adjust_tone(self, text: str, tone_preferences: Dict[str, Any]) -> str:
        """Adjust the tone of the letter based on user preferences"""
        # This would be more sophisticated in a real implementation
        # For now, we'll just make simple adjustments
        
        formality = tone_preferences.get('formality', 'neutral')  # formal, neutral, casual
        assertiveness = tone_preferences.get('assertiveness', 'neutral')  # strong, neutral, gentle
        
        # This is a placeholder for more sophisticated tone adjustment
        # In a real implementation, you would use NLP techniques
        
        return text
    
    def _add_urgency_language(self, text: str, urgency_level: int) -> str:
        """Add urgency language based on the urgency level"""
        # Find the request for review section
        request_start = text.find("## Request for Review")
        if request_start == -1:
            return text
        
        # Add urgency paragraph after the first paragraph in the request section
        first_para_end = text.find("\n\n", request_start)
        if first_para_end == -1:
            return text
        
        urgency_text = "\nThis matter requires urgent attention as "
        
        if urgency_level == 4:
            urgency_text += "delay in treatment could result in worsening of my condition."
        elif urgency_level == 5:
            urgency_text += "this is a time-sensitive medical situation that could result in serious harm if not addressed promptly."
        
        urgency_text += " I respectfully request an expedited review of this appeal.\n"
        
        # Insert the urgency text
        return text[:first_para_end] + urgency_text + text[first_para_end:]
    
    def generate_appeal_letter(self, user_data: Dict[str, Any]) -> str:
        """
        Main method to generate an appeal letter based on user data
        
        Args:
            user_data: Dictionary containing all user inputs and preferences
            
        Returns:
            Fully customized appeal letter text
        """
        # Extract key information
        insurance_type = user_data.get('insurance_type', 'health')
        denial_reason = user_data.get('denial_reason', 'medical_necessity')
        
        # Select appropriate template
        template_name = self.select_template(insurance_type, denial_reason)
        
        # Extract conditional sections, supporting docs, and preferences
        conditional_sections = user_data.get('conditional_sections', {})
        supporting_docs = user_data.get('supporting_docs', [])
        tone_preferences = user_data.get('tone_preferences', {})
        urgency_level = user_data.get('urgency_level', 0)
        
        # Customize the template
        appeal_letter = self.customize_template(
            template_name,
            user_data,
            conditional_sections,
            supporting_docs,
            tone_preferences,
            urgency_level
        )
        
        return appeal_letter
    
    def save_appeal_letter(self, appeal_letter: str, output_file: str) -> None:
        """Save the appeal letter to a file"""
        with open(output_file, 'w') as file:
            file.write(appeal_letter)
        print(f"Appeal letter saved to {output_file}")


def main():
    """Example usage of the AppealWriter class"""
    # Create an instance of the AppealWriter
    writer = AppealWriter()
    
    # Example user data
    user_data = {
        'insurance_type': 'health',
        'denial_reason': 'medical_necessity',
        'policyholder_name': 'Jane Doe',
        'policyholder_address': '123 Main Street',
        'city_state_zip': 'Anytown, CA 12345',
        'insurance_company_name': 'ABC Health Insurance',
        'insurance_company_address': '456 Insurance Way, Insuranceville, CA 67890',
        'policy_number': 'POL123456789',
        'claim_number': 'CLM987654321',
        'date_of_service': 'March 15, 2025',
        'denial_date': 'March 30, 2025',
        'provider_name': 'Dr. John Smith',
        'physician_name': 'Dr. John Smith',
        'treatment': 'MRI of the lumbar spine',
        'diagnosis': 'chronic lower back pain',
        'conditional_sections': {
            'Previous Treatments': True,
            'Clinical Evidence': True
        },
        'supporting_docs': [
            'Letter of Medical Necessity from Dr. John Smith',
            'Medical Records from January-March 2025',
            'Clinical Studies Supporting Treatment'
        ],
        'tone_preferences': {
            'formality': 'formal',
            'assertiveness': 'neutral'
        },
        'urgency_level': 3
    }
    
    # Generate the appeal letter
    appeal_letter = writer.generate_appeal_letter(user_data)
    
    # Save the appeal letter
    writer.save_appeal_letter(appeal_letter, 'example_appeal_letter.md')
    
    # Print confirmation
    print("Appeal letter generated successfully!")


if __name__ == "__main__":
    main()
