// Frontend-Backend Integration for AI Insurance Claims Denial Appeal Writer

// Update the form submission to send data to the backend API
document.addEventListener('DOMContentLoaded', function() {
    // Keep all existing code from script.js
    
    // Update the Generate button click handler
    document.getElementById('generateButton').addEventListener('click', function() {
        // Show loading indicator
        showLoadingIndicator();
        
        // Collect form data
        const formData = collectFormData();
        
        // Send data to backend API
        fetch('/api/generate-appeal', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hideLoadingIndicator();
            
            if (data.success) {
                // Update download links with actual file paths
                updateDownloadLinksWithPaths(data.files);
                
                // Set letter preview HTML
                document.getElementById('letterPreview').innerHTML = data.preview;
                
                // Show results section
                document.getElementById('step4').classList.add('hidden');
                document.getElementById('results').classList.remove('hidden');
            } else {
                showValidationError(data.error || 'An error occurred while generating your appeal letter.');
            }
        })
        .catch(error => {
            hideLoadingIndicator();
            showValidationError('An error occurred: ' + error.message);
        });
    });
    
    // Function to collect all form data
    function collectFormData() {
        const insuranceType = document.querySelector('input[name="insuranceType"]:checked').value;
        const denialReasonId = `${insuranceType}DenialReason`;
        const denialReason = document.getElementById(denialReasonId).value;
        
        // Common fields
        const formData = {
            insuranceType: insuranceType,
            denialReason: denialReason,
            policyholderName: document.getElementById('policyholderName').value,
            policyholderAddress: document.getElementById('policyholderAddress').value,
            city: document.getElementById('city').value,
            state: document.getElementById('state').value,
            zipCode: document.getElementById('zipCode').value,
            insuranceCompanyName: document.getElementById('insuranceCompanyName').value,
            insuranceCompanyAddress: document.getElementById('insuranceCompanyAddress').value,
            policyNumber: document.getElementById('policyNumber').value,
            claimNumber: document.getElementById('claimNumber').value,
            denialDate: document.getElementById('denialDate').value,
            supportingDocs: Array.from(document.querySelectorAll('input[name="supportingDocs"]:checked'))
                .map(checkbox => checkbox.value),
            urgencyLevel: document.getElementById('urgencyLevel').value,
            additionalInfo: document.getElementById('additionalInfo').value,
            outputFormats: Array.from(document.querySelectorAll('input[name="outputFormat"]:checked'))
                .map(checkbox => checkbox.value),
            createPackage: document.getElementById('createPackage').checked
        };
        
        // Insurance-specific fields
        if (insuranceType === 'health') {
            formData.dateOfService = document.getElementById('dateOfService').value;
            formData.providerName = document.getElementById('providerName').value;
            formData.treatment = document.getElementById('treatment').value;
            formData.diagnosis = document.getElementById('diagnosis').value;
            
            // Previous treatments
            const treatmentNames = Array.from(document.querySelectorAll('input[name="treatmentName[]"]'))
                .map(input => input.value)
                .filter(value => value.trim() !== '');
            
            const treatmentDates = Array.from(document.querySelectorAll('input[name="treatmentDates[]"]'))
                .map(input => input.value)
                .filter(value => value.trim() !== '');
            
            const treatmentOutcomes = Array.from(document.querySelectorAll('input[name="treatmentOutcome[]"]'))
                .map(input => input.value)
                .filter(value => value.trim() !== '');
            
            formData.previousTreatments = treatmentNames.map((name, index) => ({
                name: name,
                dates: treatmentDates[index] || '',
                outcome: treatmentOutcomes[index] || ''
            }));
        } else if (insuranceType === 'auto') {
            formData.dateOfIncident = document.getElementById('dateOfIncident').value;
            formData.vehicleInfo = document.getElementById('vehicleInfo').value;
            formData.accidentDescription = document.getElementById('accidentDescription').value;
        } else if (insuranceType === 'home') {
            formData.dateOfIncidentHome = document.getElementById('dateOfIncidentHome').value;
            formData.propertyAddress = document.getElementById('propertyAddress').value;
            formData.damageDescription = document.getElementById('damageDescription').value;
            formData.damageCause = document.getElementById('damageCause').value;
        }
        
        return formData;
    }
    
    // Function to update download links with actual file paths
    function updateDownloadLinksWithPaths(files) {
        document.getElementById('downloadMarkdown').href = files.markdown;
        document.getElementById('downloadHTML').href = files.html;
        document.getElementById('downloadPDF').href = files.pdf;
        document.getElementById('downloadDOCX').href = files.docx;
        
        // If package is available
        if (files.package) {
            document.getElementById('downloadPackage').href = files.package;
            document.getElementById('packageDownloadSection').classList.remove('hidden');
        } else {
            document.getElementById('packageDownloadSection').classList.add('hidden');
        }
    }
    
    // Get suggestions for strengthening appeal
    function getSuggestions() {
        const insuranceType = document.querySelector('input[name="insuranceType"]:checked').value;
        const denialReasonId = `${insuranceType}DenialReason`;
        const denialReason = document.getElementById(denialReasonId).value;
        
        // Only proceed if both values are available
        if (!insuranceType || !denialReason) return;
        
        fetch('/api/get-suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ insuranceType, denialReason })
        })
        .then(response => response.json())
        .then(data => {
            if (data.suggestions && data.suggestions.length > 0) {
                // Create or update suggestions section
                let suggestionsSection = document.getElementById('suggestionsList');
                if (!suggestionsSection) {
                    // Create new suggestions section if it doesn't exist
                    const container = document.createElement('div');
                    container.className = 'alert alert-info mt-3';
                    container.innerHTML = `
                        <h5>Suggestions for Strengthening Your Appeal</h5>
                        <ul id="suggestionsList"></ul>
                    `;
                    
                    // Find the appropriate place to insert it (after the supporting docs section)
                    const supportingDocsSection = document.querySelector('.form-check').closest('.mb-4');
                    supportingDocsSection.parentNode.insertBefore(container, supportingDocsSection.nextSibling);
                    
                    suggestionsSection = document.getElementById('suggestionsList');
                }
                
                // Clear existing suggestions
                suggestionsSection.innerHTML = '';
                
                // Add new suggestions
                data.suggestions.forEach(suggestion => {
                    const li = document.createElement('li');
                    li.textContent = suggestion;
                    suggestionsSection.appendChild(li);
                });
            }
        })
        .catch(error => {
            console.error('Error getting suggestions:', error);
        });
    }
    
    // Add event listeners for getting suggestions
    document.querySelectorAll('input[name="insuranceType"]').forEach(radio => {
        radio.addEventListener('change', getSuggestions);
    });
    
    document.querySelectorAll('#healthDenialReason, #autoDenialReason, #homeDenialReason').forEach(select => {
        select.addEventListener('change', getSuggestions);
    });
});
