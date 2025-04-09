# AI Agent Insurance Claims Denial Appeal Writer

## Project Overview

This project implements an AI agent that helps users create effective appeal letters when their insurance claims are denied. The system supports multiple insurance types (health, auto, and home) and various denial reasons, generating customized appeal letters based on specific situations.

## Key Features

- **Multi-insurance support**: Generate appeals for health, auto, and home insurance denials
- **Customized templates**: Tailored appeal letters for different denial reasons
- **Multiple output formats**: Generate letters in Markdown, HTML, PDF, and Word formats
- **Supporting documentation guidance**: Recommendations for strengthening appeals
- **Complete submission packages**: Create organized appeal packages with all necessary components

## Repository Structure

```
ai_insurance_appeal_writer/
├── src/                      # Source code
│   ├── appeal_writer.py      # Core template customization logic
│   ├── user_input_processor.py # Input validation and processing
│   ├── letter_generator.py   # Output format generation
│   └── main.py              # Main application and CLI
├── templates/                # Appeal letter templates
│   ├── health_medical_necessity_template.md
│   ├── health_experimental_treatment_template.md
│   ├── health_mental_health_parity_template.md
│   ├── auto_insurance_denial_template.md
│   ├── home_insurance_denial_template.md
│   └── ...
├── tests/                    # Test cases and test runner
│   ├── run_tests.py
│   ├── test_case_health_medical_necessity.json
│   └── ...
├── output/                   # Generated appeal letters
├── docs/                     # Documentation
│   ├── user_guide.md
│   ├── developer_docs.md
│   └── future_ai_agent_recommendations.md
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Dependencies

```bash
pip install markdown pdfkit jinja2
```

For PDF generation (optional), install wkhtmltopdf:
- On Ubuntu/Debian: `sudo apt-get install wkhtmltopdf`
- On macOS: `brew install wkhtmltopdf`
- On Windows: Download from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)

## Quick Start

1. Create a JSON file with your appeal information:

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

2. Run the appeal writer:

```bash
python src/main.py --input your_appeal_data.json
```

3. Find your generated appeal letter in the `output` directory

## Documentation

For detailed information, please refer to:

- [User Guide](docs/user_guide.md) - Instructions for using the system
- [Developer Documentation](docs/developer_docs.md) - Technical details and extension guidelines
- [Future AI Agent Recommendations](docs/future_ai_agent_recommendations.md) - Ideas for future AI agentic solutions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Insurance industry resources and guidelines
- State insurance departments for appeal process information
- Open source libraries: markdown, pdfkit, jinja2
