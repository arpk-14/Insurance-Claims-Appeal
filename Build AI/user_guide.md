# AI Insurance Claims Denial Appeal Writer
## User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Using the Appeal Writer](#using-the-appeal-writer)
5. [Input Requirements](#input-requirements)
6. [Output Formats](#output-formats)
7. [Tips for Successful Appeals](#tips-for-successful-appeals)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

## Introduction

The AI Insurance Claims Denial Appeal Writer is a powerful tool designed to help policyholders create effective appeal letters when their insurance claims are denied. The system supports multiple insurance types (health, auto, and home) and various denial reasons, generating customized appeal letters based on your specific situation.

### Key Features

- **Multi-insurance support**: Generate appeals for health, auto, and home insurance denials
- **Customized templates**: Tailored appeal letters for different denial reasons
- **Multiple output formats**: Generate letters in Markdown, HTML, PDF, and Word formats
- **Supporting documentation guidance**: Recommendations for strengthening your appeal
- **Complete submission packages**: Create organized appeal packages with all necessary components

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Dependencies

The following Python packages are required:
- markdown
- pdfkit
- jinja2

### Installation Steps

1. Clone the repository or download the source code:
   ```
   git clone https://github.com/yourusername/ai-insurance-appeal-writer.git
   cd ai-insurance-appeal-writer
   ```

2. Install the required dependencies:
   ```
   pip install markdown pdfkit jinja2
   ```

3. For PDF generation (optional), install wkhtmltopdf:
   - On Ubuntu/Debian: `sudo apt-get install wkhtmltopdf`
   - On macOS: `brew install wkhtmltopdf`
   - On Windows: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

## Getting Started

The appeal writer can be used in two ways:
1. Command-line interface (CLI)
2. Preparing a JSON input file

### Quick Start Example

1. Create a JSON file with your appeal information (see [Input Requirements](#input-requirements) for details)
2. Run the appeal writer:
   ```
   python src/main.py --input your_appeal_data.json
   ```
3. Find your generated appeal letter in the `output` directory

## Using the Appeal Writer

### Command-Line Interface

The main script provides several options:

```
python src/main.py --input INPUT_FILE [--output-format FORMAT] [--package]
```

Options:
- `--input`, `-i`: Path to JSON file containing appeal information (required)
- `--output-format`, `-f`: Output format (markdown, html, pdf, docx, or all)
- `--package`, `-p`: Create a complete submission package with cover sheet and checklist

Examples:
```
# Generate appeal letter in all formats
python src/main.py --input my_appeal.json

# Generate only PDF version
python src/main.py --input my_appeal.json --output-format pdf

# Create a complete submission package
python src/main.py --input my_appeal.json --package
```

### JSON Input File

The appeal writer requires a JSON file with information about your insurance claim denial. Here's a basic template:

```json
{
    "insurance_type": "health",
    "denial_reason": "medical_necessity",
    "policyholder_name": "Jane Doe",
    "policyholder_address": "123 Main Street",
    "city_state_zip": "Anytown, CA 12345",
    "insurance_company_name": "ABC Health Insurance",
    "policy_number": "POL123456789",
    "claim_number": "CLM987654321",
    "date_of_service": "March 15, 2025",
    "denial_date": "March 30, 2025",
    "provider_name": "Dr. John Smith",
    "treatment": "MRI of the lumbar spine",
    "diagnosis": "chronic lower back pain"
}
```

See the [Input Requirements](#input-requirements) section for detailed field descriptions.

## Input Requirements

### Common Fields (All Insurance Types)

| Field | Description | Required |
|-------|-------------|----------|
| insurance_type | Type of insurance (health, auto, home) | Yes |
| denial_reason | Reason for claim denial | Yes |
| policyholder_name | Full name of policyholder | Yes |
| policyholder_address | Street address | Yes |
| city_state_zip | City, state, and ZIP code | Yes |
| insurance_company_name | Name of insurance company | Yes |
| insurance_company_address | Address of insurance company | No |
| policy_number | Insurance policy number | Yes |
| claim_number | Claim identification number | Yes |
| denial_date | Date of denial letter | Yes |
| email | Policyholder email address | No |
| phone | Policyholder phone number | No |

### Health Insurance Fields

| Field | Description | Required |
|-------|-------------|----------|
| date_of_service | Date medical service was provided | Yes |
| provider_name | Name of healthcare provider | Yes |
| physician_name | Name of ordering/referring physician | Yes |
| treatment | Description of treatment/procedure/service | Yes |
| diagnosis | Medical diagnosis | Yes |
| previous_treatments | List of previous treatments and outcomes | No |

### Auto Insurance Fields

| Field | Description | Required |
|-------|-------------|----------|
| date_of_incident | Date of accident/incident | Yes |
| vehicle_info | Year, make, model, and VIN | Yes |
| accident_description | Description of what happened | Yes |
| driver_name | Name of driver (if not policyholder) | No |
| driver_relationship | Relationship to policyholder | No |

### Home Insurance Fields

| Field | Description | Required |
|-------|-------------|----------|
| date_of_incident | Date of damage/loss | Yes |
| property_address | Address of insured property | Yes |
| damage_description | Description of damage/loss | Yes |
| damage_cause | Cause of damage/loss | Yes |
| denial_reason_stated | Specific reason stated in denial letter | No |

### Supporting Documents

You can specify available supporting documents:

```json
"supporting_documents": [
    {"name": "Denial Letter", "available": true},
    {"name": "Medical Records", "available": true},
    {"name": "Physician Letter", "available": false}
]
```

### Conditional Sections

You can control which sections appear in your appeal letter:

```json
"conditional_sections": [
    {"name": "Previous Treatments", "include": true},
    {"name": "Clinical Evidence", "include": true}
]
```

### Tone Preferences

You can adjust the tone of your appeal letter:

```json
"tone_preferences": {
    "formality": "formal",
    "assertiveness": "moderate"
}
```

### Urgency Level

You can indicate the urgency of your appeal (0-5, with 5 being most urgent):

```json
"urgency_level": 3
```

## Output Formats

The appeal writer can generate letters in the following formats:

### Markdown (.md)
- Plain text format with simple formatting
- Easily editable in any text editor
- Good for further customization

### HTML (.html)
- Web page format with styling
- Can be viewed in any web browser
- Printable from browser

### PDF (.pdf)
- Portable Document Format
- Professional appearance
- Requires wkhtmltopdf to be installed

### Word (.docx)
- Microsoft Word format
- Easily editable in Word or compatible applications
- Good for further customization

## Tips for Successful Appeals

1. **Be timely**: Submit your appeal within the timeframe specified in your denial letter (typically 30-180 days).

2. **Be specific**: Clearly identify the denied claim, including dates of service and claim numbers.

3. **Address the specific reason for denial**: Focus your appeal on directly addressing the reason given for denial.

4. **Include supporting documentation**: Attach all relevant documentation that supports your case.

5. **Reference your policy**: Quote specific sections of your policy that support coverage for your claim.

6. **Be professional**: Maintain a respectful, professional tone throughout your appeal letter.

7. **Follow up**: If you don't receive a response within 30 days, follow up with your insurance company.

8. **Consider external review**: If your internal appeal is denied, you may have the right to an external review.

## Troubleshooting

### Common Issues

#### PDF Generation Fails
- Ensure wkhtmltopdf is installed on your system
- Check that the path to wkhtmltopdf is in your system PATH

#### Missing Fields Error
- Check that your JSON input file includes all required fields for your insurance type
- Verify that field names match exactly as specified in the documentation

#### Template Not Found
- Ensure you're running the script from the correct directory
- Check that the templates directory exists and contains the necessary template files

## FAQ

### How long should I wait for a response to my appeal?
Insurance companies typically have 30-60 days to respond to appeals, depending on state regulations and the type of insurance.

### Can I submit multiple appeals for the same claim?
Yes, if your first appeal is denied, you can usually submit a second-level appeal or request an external review.

### Do I need a lawyer to appeal an insurance claim denial?
While not required, legal assistance can be beneficial for complex cases or high-value claims.

### Can this tool help with Medicare or Medicaid appeals?
Yes, the health insurance templates can be used for Medicare or Medicaid appeals, though these programs may have specific requirements not fully addressed by the templates.

### How do I know which denial reason to select?
Review your denial letter carefully. The reason for denial should be clearly stated. If unclear, contact your insurance company for clarification.

### Can I edit the generated appeal letter?
Yes, all output formats are designed to be editable. We recommend reviewing and customizing the letter to your specific situation before submission.
