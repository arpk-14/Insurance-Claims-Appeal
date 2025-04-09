# Developer Documentation
## AI Insurance Claims Denial Appeal Writer

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Code Structure](#code-structure)
3. [Module Documentation](#module-documentation)
4. [Template System](#template-system)
5. [Extending the System](#extending-the-system)
6. [Testing](#testing)
7. [Deployment](#deployment)
8. [Future Development](#future-development)

## System Architecture

The AI Insurance Claims Denial Appeal Writer is built with a modular architecture that separates concerns into distinct components:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  User Input     │────▶│  Appeal Writer  │────▶│  Letter         │
│  Processor      │     │  Core           │     │  Generator      │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        ▲                       ▲                       ▲
        │                       │                       │
        │                       │                       │
        │                       │                       │
┌───────┴───────────────────────┴───────────────────────┴───────┐
│                                                               │
│                       Main Application                        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
        ▲                       ▲                       ▲
        │                       │                       │
┌───────┴───────────┐   ┌───────┴───────────┐   ┌───────┴───────────┐
│                   │   │                   │   │                   │
│  Templates        │   │  Test Cases       │   │  Output Files     │
│                   │   │                   │   │                   │
└───────────────────┘   └───────────────────┘   └───────────────────┘
```

### Component Responsibilities

1. **User Input Processor**: Validates and processes user inputs, ensuring all required fields are present and correctly formatted.

2. **Appeal Writer Core**: Selects the appropriate template based on insurance type and denial reason, then customizes it with user data.

3. **Letter Generator**: Converts the customized appeal letter into various output formats (Markdown, HTML, PDF, Word).

4. **Main Application**: Coordinates the overall workflow and provides the command-line interface.

5. **Templates**: Markdown files containing the base appeal letter templates for different insurance types and denial reasons.

6. **Test Cases**: JSON files containing sample data for testing the system.

7. **Output Files**: Generated appeal letters in various formats.

## Code Structure

The codebase is organized as follows:

```
ai_insurance_appeal_writer/
├── src/
│   ├── appeal_writer.py       # Core template customization logic
│   ├── user_input_processor.py # Input validation and processing
│   ├── letter_generator.py    # Output format generation
│   └── main.py               # Main application and CLI
├── templates/
│   ├── health_medical_necessity_template.md
│   ├── health_experimental_treatment_template.md
│   ├── health_mental_health_parity_template.md
│   ├── auto_insurance_denial_template.md
│   ├── home_insurance_denial_template.md
│   └── ...
├── tests/
│   ├── run_tests.py          # Test runner
│   ├── test_case_health_medical_necessity.json
│   ├── test_case_auto_driver_not_on_policy.json
│   └── ...
├── output/                   # Generated appeal letters
├── docs/
│   ├── user_guide.md         # User documentation
│   └── developer_docs.md     # Developer documentation
└── README.md                 # Project overview
```

## Module Documentation

### appeal_writer.py

The `AppealWriter` class is responsible for selecting and customizing templates based on user inputs.

#### Key Methods:

- `__init__(templates_dir)`: Initialize with templates directory
- `select_template(insurance_type, denial_reason)`: Select appropriate template
- `customize_template(template_name, user_inputs, ...)`: Customize template with user data
- `generate_appeal_letter(user_data)`: Main method to generate an appeal letter

### user_input_processor.py

The `UserInputProcessor` class validates and processes user inputs.

#### Key Methods:

- `validate_inputs(user_data)`: Check if all required fields are present
- `process_form_data(form_data)`: Process raw form data into expected format
- `suggest_additional_information(user_data)`: Generate suggestions for improving the appeal

### letter_generator.py

The `LetterGenerator` class converts appeal letters into various output formats.

#### Key Methods:

- `generate_markdown(appeal_letter, filename)`: Save as Markdown
- `generate_html(appeal_letter, filename)`: Convert to HTML
- `generate_pdf(appeal_letter, filename)`: Convert to PDF
- `generate_docx(appeal_letter, filename)`: Convert to Word
- `create_submission_package(appeal_letter, supporting_docs, user_data)`: Create complete package

### main.py

The `AppealWriterApp` class coordinates the overall workflow.

#### Key Methods:

- `process_user_input(input_data)`: Process and validate user input
- `generate_appeal_letter(user_data, output_format)`: Generate appeal letter
- `create_submission_package(user_data)`: Create submission package
- `run_cli()`: Run command-line interface

## Template System

The template system uses Markdown files with placeholders that are replaced with user data.

### Placeholder Format

Placeholders are enclosed in square brackets, e.g., `[Policyholder Name]`.

### Template Selection Logic

Templates are selected based on insurance type and denial reason:

```python
if insurance_type == "health":
    if denial_reason == "medical_necessity":
        template = "health_medical_necessity_template"
    elif denial_reason == "experimental_treatment":
        template = "health_experimental_treatment_template"
    # ...
elif insurance_type == "auto":
    template = "auto_insurance_denial_template"
elif insurance_type == "home":
    template = "home_insurance_denial_template"
```

### Conditional Sections

Templates include conditional sections that can be included or excluded based on user inputs.

## Extending the System

### Adding New Templates

To add a new template:

1. Create a new Markdown file in the `templates` directory
2. Use the established placeholder format
3. Update the `select_template` method in `appeal_writer.py`

### Adding New Insurance Types

To add a new insurance type:

1. Create templates for the new insurance type
2. Update the `select_template` method in `appeal_writer.py`
3. Update the `required_fields` dictionary in `user_input_processor.py`
4. Update the `denial_reasons` dictionary in `user_input_processor.py`

### Adding New Output Formats

To add a new output format:

1. Add a new method to `LetterGenerator` class
2. Update the `generate_all_formats` method
3. Update the command-line interface in `main.py`

## Testing

The system includes a test framework for verifying functionality.

### Running Tests

```
cd tests
python run_tests.py
```

To run a specific test:

```
python run_tests.py --test-file test_case_health_medical_necessity.json
```

### Adding Test Cases

To add a new test case:

1. Create a JSON file in the `tests` directory
2. Include all required fields for the insurance type
3. Run the test to verify functionality

## Deployment

The system is designed to be run locally, but can be deployed as a service.

### Dependencies

- Python 3.8+
- markdown
- pdfkit
- jinja2
- wkhtmltopdf (for PDF generation)

### Installation

```
pip install markdown pdfkit jinja2
```

For PDF generation, install wkhtmltopdf:
- Ubuntu/Debian: `sudo apt-get install wkhtmltopdf`
- macOS: `brew install wkhtmltopdf`
- Windows: Download from wkhtmltopdf.org

## Future Development

Potential areas for future development:

1. **Web Interface**: Create a web-based UI for easier user interaction
2. **API Service**: Expose functionality as a REST API
3. **Additional Insurance Types**: Add support for more insurance types (e.g., life, disability)
4. **Machine Learning Integration**: Use ML to improve template selection and customization
5. **Document Analysis**: Automatically extract information from denial letters
6. **Legal Review Integration**: Partner with legal services for review of generated appeals
7. **Multi-language Support**: Add templates in multiple languages
8. **Mobile App**: Create a mobile application for on-the-go appeal generation
