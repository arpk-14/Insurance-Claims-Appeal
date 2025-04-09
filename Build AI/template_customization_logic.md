# Template Customization Logic

This document outlines the logic for customizing appeal letter templates based on user inputs and specific denial scenarios.

## Template Selection Logic

The system will select the appropriate base template using the following decision tree:

```
if insurance_type == "health":
    if denial_reason == "medical_necessity":
        template = "health_medical_necessity_template.md"
    elif denial_reason == "experimental_treatment":
        template = "health_experimental_treatment_template.md"
    elif denial_reason == "mental_health_parity":
        template = "health_mental_health_parity_template.md"
    elif denial_reason == "out_of_network":
        template = "out_of_network_denial_template.md"
    elif denial_reason == "prior_authorization":
        template = "prior_authorization_denial_template.md"
    elif denial_reason == "billing_coding_error":
        template = "billing_coding_error_template.md"
    elif denial_reason == "pre_existing_condition":
        template = "pre_existing_condition_template.md"
    else:
        template = "health_general_template.md"
        
elif insurance_type == "auto":
    template = "auto_insurance_denial_template.md"
    
elif insurance_type == "home":
    template = "home_insurance_denial_template.md"
    
else:
    template = "general_appeal_template.md"
```

## Variable Substitution

Each template contains placeholder variables that will be replaced with user-provided information:

### Common Variables (All Templates)
- `[Policyholder Name]`
- `[Policyholder Address]`
- `[City, State ZIP]`
- `[Date]` (current date or user-specified date)
- `[Insurance Company Name]`
- `[Insurance Company Address]`
- `[Policy Number]`
- `[Claim Number]`
- `[Date of Service/Incident]`

### Health Insurance Specific Variables
- `[Provider Name]`
- `[Diagnosis]`
- `[Treatment/Procedure/Service]`
- `[Physician Name]`
- `[Previous Treatments]`

### Auto Insurance Specific Variables
- `[Vehicle Information]`
- `[Accident Description]`
- `[Driver Name]`

### Home Insurance Specific Variables
- `[Property Address]`
- `[Damage Description]`
- `[Cause of Damage]`

## Conditional Content Blocks

Templates include conditional sections that will be included or excluded based on specific user inputs:

### Medical Necessity Template
- Include "Previous Treatments" section only if user indicates prior treatments
- Include "Clinical Evidence" section only if user has supporting studies/guidelines

### Experimental Treatment Template
- Include "FDA Approval" section only if treatment has FDA approval
- Include "Other Insurance Coverage" section only if user indicates other insurers cover this treatment

### Out-of-Network Template
- Include only the relevant "Circumstances" section based on user's reason for out-of-network care

### Auto Insurance Template
- Include only the relevant denial reason section based on specific denial reason

### Home Insurance Template
- Include only the relevant denial reason section based on specific denial reason

## Customization Process

1. **Template Selection**: System selects base template based on insurance type and denial reason
2. **Variable Replacement**: System replaces all placeholders with user-provided information
3. **Conditional Content**: System includes or excludes conditional sections based on user inputs
4. **Supporting Documentation**: System customizes the "Enclosures" section based on documents user has available
5. **Tone Adjustment**: System adjusts language formality and assertiveness based on user preference
6. **Length Adjustment**: System expands or contracts sections based on complexity of case and user preference

## Special Handling

### Medical Records
- If user has detailed medical records, system will extract and incorporate specific relevant details
- If user lacks medical records, system will provide guidance on obtaining necessary documentation

### Policy Language
- If user provides specific policy language, system will incorporate direct quotes
- If policy language is unavailable, system will use standard industry terminology

### Urgency Factors
- System will add "Request for Expedited Review" section if user indicates time-sensitive situation
- System will adjust submission instructions based on urgency

## Template Versioning

Templates will be versioned to accommodate:
- Regulatory changes
- Insurance industry practice updates
- User feedback and success rates
- Regional variations in insurance law

## Template Customization API

The template customization engine will expose the following API for the frontend:

```
customize_template(
    template_id: str,
    user_inputs: dict,
    conditional_sections: dict,
    supporting_docs: list,
    tone_preferences: dict,
    urgency_level: int
) -> str
```

This API will return the fully customized appeal letter text based on the provided parameters.
