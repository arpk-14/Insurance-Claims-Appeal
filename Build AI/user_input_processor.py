#!/usr/bin/env python3
"""
AI Insurance Claims Denial Appeal Writer
User input processing module
"""

import json
import re
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class UserInputProcessor:
    """Process and validate user inputs for the appeal writer"""
    
    def __init__(self):
        """Initialize the UserInputProcessor"""
        self.required_fields = {
            'common': [
                'policyholder_name',
                'insurance_company_name',
                'policy_number',
                'claim_number',
                'denial_date'
            ],
            'health': [
                'date_of_service',
                'provider_name',
                'treatment',
                'diagnosis'
            ],
            'auto': [
                'date_of_incident',
                'vehicle_info',
                'accident_description'
            ],
            'home': [
                'date_of_incident',
                'property_address',
                'damage_description',
                'damage_cause'
            ]
        }
        
        self.denial_reasons = {
            'health': [
                'medical_necessity',
                'experimental_treatment',
                'mental_health_parity',
                'out_of_network',
                'prior_authorization',
                'billing_coding_error',
                'pre_existing_condition'
            ],
            'auto': [
                'driver_not_on_policy',
                'coverage_limits',
                'lapsed_coverage',
                'business_use',
                'excluded_driver'
            ],
            'home': [
                'maintenance_wear_tear',
                'excluded_peril',
                'policy_exclusion',
                'insufficient_documentation',
                'late_reporting'
            ]
        }
    
    def validate_inputs(self, user_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate user inputs for completeness and correctness
        
        Args:
            user_data: Dictionary containing user inputs
            
        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        
        # Check insurance type
        insurance_type = user_data.get('insurance_type')
        if not insurance_type or insurance_type not in ['health', 'auto', 'home']:
            missing_fields.append('insurance_type (must be health, auto, or home)')
            return False, missing_fields
        
        # Check denial reason
        denial_reason = user_data.get('denial_reason')
        if not denial_reason:
            missing_fields.append('denial_reason')
        elif denial_reason not in self.denial_reasons.get(insurance_type, []):
            valid_reasons = ', '.join(self.denial_reasons.get(insurance_type, []))
            missing_fields.append(f'denial_reason (must be one of: {valid_reasons})')
        
        # Check common required fields
        for field in self.required_fields['common']:
            if not user_data.get(field):
                missing_fields.append(field)
        
        # Check insurance-type specific required fields
        for field in self.required_fields.get(insurance_type, []):
            if not user_data.get(field):
                missing_fields.append(field)
        
        # Validate date formats (simplified)
        date_fields = ['date_of_service', 'date_of_incident', 'denial_date']
        for field in date_fields:
            if field in user_data and user_data[field]:
                if not self._is_valid_date_format(user_data[field]):
                    missing_fields.append(f"{field} (invalid date format)")
        
        return len(missing_fields) == 0, missing_fields
    
    def _is_valid_date_format(self, date_str: str) -> bool:
        """
        Check if a string is in a valid date format
        This is a simplified implementation - a real one would be more robust
        """
        # Accept formats like "April 8, 2025" or "04/08/2025"
        date_patterns = [
            r'\w+ \d{1,2}, \d{4}',  # Month Day, Year
            r'\d{1,2}/\d{1,2}/\d{4}'  # MM/DD/YYYY
        ]
        
        for pattern in date_patterns:
            if re.match(pattern, date_str):
                return True
        
        return False
    
    def process_form_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process form data into the format expected by the appeal writer
        
        Args:
            form_data: Raw form data from user interface
            
        Returns:
            Processed data ready for the appeal writer
        """
        processed_data = {}
        
        # Copy basic fields
        for key, value in form_data.items():
            if key not in ['supporting_documents', 'previous_treatments', 'conditional_sections']:
                processed_data[key] = value
        
        # Process supporting documents
        if 'supporting_documents' in form_data:
            processed_data['supporting_docs'] = []
            for doc in form_data['supporting_documents']:
                if doc.get('available', False):
                    processed_data['supporting_docs'].append(doc['name'])
        
        # Process conditional sections
        if 'conditional_sections' in form_data:
            processed_data['conditional_sections'] = {}
            for section in form_data['conditional_sections']:
                processed_data['conditional_sections'][section['name']] = section.get('include', False)
        
        # Process previous treatments
        if 'previous_treatments' in form_data and form_data['previous_treatments']:
            treatments = []
            for treatment in form_data['previous_treatments']:
                if treatment.get('name') and treatment.get('dates') and treatment.get('outcome'):
                    treatments.append(f"{treatment['name']} from {treatment['dates']}, which resulted in {treatment['outcome']}")
            
            if treatments:
                processed_data['previous_treatments'] = treatments
                processed_data['conditional_sections'] = processed_data.get('conditional_sections', {})
                processed_data['conditional_sections']['Previous Treatments'] = True
        
        return processed_data
    
    def extract_data_from_documents(self, documents: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract relevant data from uploaded documents
        
        Args:
            documents: Dictionary mapping document types to file paths
            
        Returns:
            Dictionary of extracted data
        """
        extracted_data = {}
        
        # This would use OCR and NLP in a real implementation
        # For now, we'll return a placeholder
        
        if 'denial_letter' in documents:
            # In a real implementation, this would extract:
            # - Denial reason
            # - Denial date
            # - Claim number
            # - Insurance company details
            extracted_data['has_denial_letter'] = True
        
        if 'policy_document' in documents:
            # In a real implementation, this would extract:
            # - Policy number
            # - Coverage details
            # - Relevant policy language
            extracted_data['has_policy_document'] = True
        
        if 'medical_records' in documents:
            # In a real implementation, this would extract:
            # - Diagnosis
            # - Treatment history
            # - Provider information
            extracted_data['has_medical_records'] = True
        
        return extracted_data
    
    def suggest_additional_information(self, user_data: Dict[str, Any]) -> List[str]:
        """
        Suggest additional information that would strengthen the appeal
        
        Args:
            user_data: Current user data
            
        Returns:
            List of suggestions for additional information
        """
        suggestions = []
        insurance_type = user_data.get('insurance_type')
        denial_reason = user_data.get('denial_reason')
        
        # Common suggestions
        if 'denial_letter' not in user_data.get('documents', {}):
            suggestions.append("Include a copy of the denial letter to ensure your appeal addresses the specific reasons for denial.")
        
        if 'policy_document' not in user_data.get('documents', {}):
            suggestions.append("Include a copy of your policy document to reference specific coverage provisions.")
        
        # Insurance-type specific suggestions
        if insurance_type == 'health':
            if denial_reason == 'medical_necessity' and 'physician_letter' not in user_data.get('documents', {}):
                suggestions.append("A letter from your physician explaining why the treatment is medically necessary would significantly strengthen your appeal.")
            
            if denial_reason == 'experimental_treatment' and not user_data.get('clinical_studies'):
                suggestions.append("Including clinical studies or medical literature supporting the treatment would help demonstrate it's not experimental.")
        
        elif insurance_type == 'auto':
            if 'accident_photos' not in user_data.get('documents', {}):
                suggestions.append("Photos of the accident scene and vehicle damage would provide visual evidence to support your claim.")
            
            if 'police_report' not in user_data.get('documents', {}):
                suggestions.append("A copy of the police report would provide an official account of the accident.")
        
        elif insurance_type == 'home':
            if 'damage_photos' not in user_data.get('documents', {}):
                suggestions.append("Photos of the property damage would provide visual evidence to support your claim.")
            
            if 'repair_estimates' not in user_data.get('documents', {}):
                suggestions.append("Professional repair estimates would help document the extent and cost of the damage.")
        
        return suggestions


def main():
    """Example usage of the UserInputProcessor class"""
    processor = UserInputProcessor()
    
    # Example form data
    form_data = {
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
        'supporting_documents': [
            {'name': 'Denial Letter', 'available': True},
            {'name': 'Medical Records', 'available': True},
            {'name': 'Physician Letter', 'available': False}
        ],
        'previous_treatments': [
            {'name': 'Physical Therapy', 'dates': 'January-February 2025', 'outcome': 'minimal improvement'},
            {'name': 'Pain Medication', 'dates': 'December 2024-March 2025', 'outcome': 'temporary relief only'}
        ],
        'conditional_sections': [
            {'name': 'Clinical Evidence', 'include': True}
        ]
    }
    
    # Process the form data
    processed_data = processor.process_form_data(form_data)
    
    # Validate the processed data
    is_valid, missing_fields = processor.validate_inputs(processed_data)
    
    if is_valid:
        print("User data is valid!")
        print(json.dumps(processed_data, indent=2))
    else:
        print("User data is invalid. Missing or incorrect fields:")
        for field in missing_fields:
            print(f"- {field}")
    
    # Get suggestions for additional information
    suggestions = processor.suggest_additional_information(processed_data)
    if suggestions:
        print("\nSuggestions for strengthening your appeal:")
        for suggestion in suggestions:
            print(f"- {suggestion}")


if __name__ == "__main__":
    main()
