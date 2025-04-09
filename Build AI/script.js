// Main JavaScript for AI Insurance Claims Denial Appeal Writer

document.addEventListener('DOMContentLoaded', function() {
    // Step navigation
    const steps = ['step1', 'step2', 'step3', 'step4'];
    const indicators = ['step1-indicator', 'step2-indicator', 'step3-indicator', 'step4-indicator'];
    
    function showStep(stepIndex) {
        // Hide all steps
        steps.forEach(step => {
            document.getElementById(step).classList.add('hidden');
        });
        
        // Show the current step
        document.getElementById(steps[stepIndex]).classList.remove('hidden');
        
        // Update indicators
        indicators.forEach((indicator, index) => {
            const indicatorElement = document.getElementById(indicator);
            if (index < stepIndex) {
                indicatorElement.classList.remove('active');
                indicatorElement.classList.add('completed');
            } else if (index === stepIndex) {
                indicatorElement.classList.add('active');
                indicatorElement.classList.remove('completed');
            } else {
                indicatorElement.classList.remove('active');
                indicatorElement.classList.remove('completed');
            }
        });
        
        // Scroll to top of the form
        window.scrollTo({
            top: document.querySelector('.step-indicator').offsetTop - 20,
            behavior: 'smooth'
        });
    }
    
    // Insurance type selection
    const insuranceTypeRadios = document.querySelectorAll('input[name="insuranceType"]');
    insuranceTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            // Hide all insurance-specific sections
            document.querySelectorAll('.health-specific, .auto-specific, .home-specific').forEach(section => {
                section.classList.add('hidden');
            });
            
            // Show the selected insurance-specific sections
            const selectedType = this.value;
            document.querySelectorAll(`.${selectedType}-specific`).forEach(section => {
                section.classList.remove('hidden');
            });
            
            // Add visual selection to cards
            document.querySelectorAll('.card').forEach(card => {
                card.classList.remove('selected');
            });
            this.closest('.card').classList.add('selected');
        });
    });
    
    // Step 1 Next button
    document.getElementById('step1Next').addEventListener('click', function() {
        // Validate insurance type selection
        const insuranceType = document.querySelector('input[name="insuranceType"]:checked');
        if (!insuranceType) {
            showValidationError('Please select an insurance type.');
            return;
        }
        
        // Validate denial reason selection
        const denialReasonId = `${insuranceType.value}DenialReason`;
        const denialReason = document.getElementById(denialReasonId).value;
        if (!denialReason) {
            showValidationError('Please select a denial reason.');
            return;
        }
        
        showStep(1); // Move to step 2
    });
    
    // Step 2 Back button
    document.getElementById('step2Back').addEventListener('click', function() {
        showStep(0); // Back to step 1
    });
    
    // Step 2 Next button
    document.getElementById('step2Next').addEventListener('click', function() {
        // Basic validation for required fields
        const requiredFields = [
            'policyholderName', 'policyNumber', 'claimNumber', 
            'denialDate', 'policyholderAddress', 'city', 'state', 'zipCode',
            'insuranceCompanyName'
        ];
        
        let isValid = true;
        requiredFields.forEach(field => {
            const element = document.getElementById(field);
            if (!element.value) {
                element.classList.add('is-invalid');
                isValid = false;
            } else {
                element.classList.remove('is-invalid');
            }
        });
        
        // Insurance-specific validation
        const insuranceType = document.querySelector('input[name="insuranceType"]:checked').value;
        
        if (insuranceType === 'health') {
            const healthFields = ['dateOfService', 'providerName', 'treatment', 'diagnosis'];
            healthFields.forEach(field => {
                const element = document.getElementById(field);
                if (!element.value) {
                    element.classList.add('is-invalid');
                    isValid = false;
                } else {
                    element.classList.remove('is-invalid');
                }
            });
        } else if (insuranceType === 'auto') {
            const autoFields = ['dateOfIncident', 'vehicleInfo'];
            autoFields.forEach(field => {
                const element = document.getElementById(field);
                if (!element.value) {
                    element.classList.add('is-invalid');
                    isValid = false;
                } else {
                    element.classList.remove('is-invalid');
                }
            });
        } else if (insuranceType === 'home') {
            const homeFields = ['dateOfIncidentHome', 'damageDescription', 'damageCause'];
            homeFields.forEach(field => {
                const element = document.getElementById(field);
                if (!element.value) {
                    element.classList.add('is-invalid');
                    isValid = false;
                } else {
                    element.classList.remove('is-invalid');
                }
            });
        }
        
        if (!isValid) {
            showValidationError('Please fill in all required fields.');
            return;
        }
        
        showStep(2); // Move to step 3
    });
    
    // Step 3 Back button
    document.getElementById('step3Back').addEventListener('click', function() {
        showStep(1); // Back to step 2
    });
    
    // Step 3 Next button
    document.getElementById('step3Next').addEventListener('click', function() {
        // Populate review section
        populateReview();
        showStep(3); // Move to step 4
    });
    
    // Step 4 Back button
    document.getElementById('step4Back').addEventListener('click', function() {
        showStep(2); // Back to step 3
    });
    
    // Add treatment button
    document.getElementById('addTreatment').addEventListener('click', function() {
        const treatmentsContainer = document.getElementById('previousTreatments');
        const newTreatment = document.createElement('div');
        newTreatment.className = 'row mb-3 previous-treatment';
        newTreatment.innerHTML = `
            <div class="col-md-4">
                <input type="text" class="form-control" placeholder="Treatment Name" name="treatmentName[]">
            </div>
            <div class="col-md-4">
                <input type="text" class="form-control" placeholder="Dates (e.g., Jan-Mar 2025)" name="treatmentDates[]">
            </div>
            <div class="col-md-3">
                <input type="text" class="form-control" placeholder="Outcome" name="treatmentOutcome[]">
            </div>
            <div class="col-md-1">
                <button type="button" class="btn btn-outline-danger btn-sm remove-treatment">
                    <i class="bi bi-trash"></i>
                </button>
            </div>
        `;
        treatmentsContainer.appendChild(newTreatment);
        
        // Add event listener to the remove button
        newTreatment.querySelector('.remove-treatment').addEventListener('click', function() {
            treatmentsContainer.removeChild(newTreatment);
        });
    });
    
    // Populate review section
    function populateReview() {
        const insuranceType = document.querySelector('input[name="insuranceType"]:checked').value;
        const denialReasonId = `${insuranceType}DenialReason`;
        const denialReason = document.getElementById(denialReasonId).value;
        
        // Format denial reason for display
        let formattedDenialReason = denialReason.replace(/_/g, ' ');
        formattedDenialReason = formattedDenialReason.split(' ').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
        ).join(' ');
        
        // Format insurance type for display
        const formattedInsuranceType = insuranceType.charAt(0).toUpperCase() + insuranceType.slice(1);
        
        // Common fields
        document.getElementById('reviewInsuranceType').textContent = formattedInsuranceType;
        document.getElementById('reviewDenialReason').textContent = formattedDenialReason;
        document.getElementById('reviewPolicyholder').textContent = document.getElementById('policyholderName').value;
        document.getElementById('reviewPolicyNumber').textContent = document.getElementById('policyNumber').value;
        document.getElementById('reviewClaimNumber').textContent = document.getElementById('claimNumber').value;
        document.getElementById('reviewDenialDate').textContent = formatDate(document.getElementById('denialDate').value);
        document.getElementById('reviewInsuranceCompany').textContent = document.getElementById('insuranceCompanyName').value;
        
        // Hide all insurance-specific review sections
        document.getElementById('healthReviewSection').classList.add('hidden');
        document.getElementById('autoReviewSection').classList.add('hidden');
        document.getElementById('homeReviewSection').classList.add('hidden');
        
        // Show and populate the appropriate insurance-specific review section
        if (insuranceType === 'health') {
            document.getElementById('healthReviewSection').classList.remove('hidden');
            document.getElementById('reviewDateOfService').textContent = formatDate(document.getElementById('dateOfService').value);
            document.getElementById('reviewProvider').textContent = document.getElementById('providerName').value;
            document.getElementById('reviewTreatment').textContent = document.getElementById('treatment').value;
            document.getElementById('reviewDiagnosis').textContent = document.getElementById('diagnosis').value;
        } else if (insuranceType === 'auto') {
            document.getElementById('autoReviewSection').classList.remove('hidden');
            document.getElementById('reviewDateOfIncident').textContent = formatDate(document.getElementById('dateOfIncident').value);
            document.getElementById('reviewVehicleInfo').textContent = document.getElementById('vehicleInfo').value;
            document.getElementById('reviewAccidentDescription').textContent = document.getElementById('accidentDescription').value;
        } else if (insuranceType === 'home') {
            document.getElementById('homeReviewSection').classList.remove('hidden');
            document.getElementById('reviewDateOfIncidentHome').textContent = formatDate(document.getElementById('dateOfIncidentHome').value);
            document.getElementById('reviewPropertyAddress').textContent = document.getElementById('propertyAddress').value || document.getElementById('policyholderAddress').value;
            document.getElementById('reviewDamageDescription').textContent = document.getElementById('damageDescription').value;
            document.getElementById('reviewDamageCause').textContent = document.getElementById('damageCause').value;
        }
        
        // Supporting documents
        const supportingDocs = Array.from(document.querySelectorAll('input[name="supportingDocs"]:checked'))
            .map(checkbox => checkbox.value)
            .join(', ');
        document.getElementById('reviewSupportingDocs').textContent = supportingDocs || 'None specified';
        
        // Urgency level
        const urgencyLevel = document.getElementById('urgencyLevel');
        document.getElementById('reviewUrgencyLevel').textContent = urgencyLevel.options[urgencyLevel.selectedIndex].text;
    }
    
    // Generate button
    document.getElementById('generateButton').addEventListener('click', function() {
        // Show loading indicator
        showLoadingIndicator();
        
        // In a real implementation, this would send the form data to the server
        // For this demo, we'll simulate a server request with setTimeout
        setTimeout(function() {
            hideLoadingIndicator();
            
            document.getElementById('step4').classList.add('hidden');
            document.getElementById('results').classList.remove('hidden');
            
            // Generate a sample letter preview
            generateLetterPreview();
            
            // Update download links with unique IDs
            const uniqueId = generateUniqueId();
            updateDownloadLinks(uniqueId);
        }, 2000);
    });
    
    // Generate letter preview
    function generateLetterPreview() {
        const insuranceType = document.querySelector('input[name="insuranceType"]:checked').value;
        const policyholderName = document.getElementById('policyholderName').value;
        const policyholderAddress = document.getElementById('policyholderAddress').value;
        const cityStateZip = `${document.getElementById('city').value}, ${document.getElementById('state').value} ${document.getElementById('zipCode').value}`;
        const insuranceCompany = document.getElementById('insuranceCompanyName').value;
        const insuranceCompanyAddress = document.getElementById('insuranceCompanyAddress').value || "Claims Review Department";
        const policyNumber = document.getElementById('policyNumber').value;
        const claimNumber = document.getElementById('claimNumber').value;
        const denialDate = document.getElementById('denialDate').value;
        
        // Format the date
        const currentDate = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        // Create a sample letter based on the insurance type
        let letterHTML = '';
        
        if (insuranceType === 'health') {
            const serviceDate = document.getElementById('dateOfService').value;
            const provider = document.getElementById('providerName').value;
            const treatment = document.getElementById('treatment').value;
            const diagnosis = document.getElementById('diagnosis').value;
            
            letterHTML = `
                <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                    <p>${currentDate}</p>
                    <p>${insuranceCompany}<br>
                    ${insuranceCompanyAddress}</p>
                    
                    <p><strong>Re: Appeal of Claim Denial</strong><br>
                    Policy Number: ${policyNumber}<br>
                    Claim Number: ${claimNumber}<br>
                    Date of Service: ${formatDate(serviceDate)}<br>
                    Patient: ${policyholderName}</p>
                    
                    <p>Dear Claims Review Department:</p>
                    
                    <p>I am writing to appeal your decision to deny coverage for ${treatment} that was provided on ${formatDate(serviceDate)}. According to your denial letter dated ${formatDate(denialDate)}, the claim was denied because the service was deemed "not medically necessary." After reviewing my policy benefits and consulting with my healthcare provider, I believe this determination was made in error, and I am requesting a full review of this decision.</p>
                    
                    <h3>Medical Background and Necessity</h3>
                    
                    <p>I was diagnosed with ${diagnosis} and my physician, ${provider}, determined that this trea
(Content truncated due to size limit. Use line ranges to read in chunks)