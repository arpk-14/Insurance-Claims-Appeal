// Update server.js to include authentication routes
const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const { marked } = require('marked');
const puppeteer = require('puppeteer');
const docx = require('docx');
const { Document, Paragraph, TextRun, HeadingLevel, AlignmentType, Packer } = docx;
const { router: authRouter, auth } = require('./auth');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// Auth routes
app.use('/api/auth', authRouter);

// Template storage
const templates = {
  health: {
    medical_necessity: fs.readFileSync(path.join(__dirname, 'templates/health_medical_necessity_template.md'), 'utf8'),
    experimental_treatment: fs.readFileSync(path.join(__dirname, 'templates/health_experimental_treatment_template.md'), 'utf8'),
    out_of_network: fs.readFileSync(path.join(__dirname, 'templates/out_of_network_denial_template.md'), 'utf8'),
    pre_existing_condition: fs.readFileSync(path.join(__dirname, 'templates/pre_existing_condition_template.md'), 'utf8'),
    prior_authorization: fs.readFileSync(path.join(__dirname, 'templates/prior_authorization_denial_template.md'), 'utf8'),
    billing_coding_error: fs.readFileSync(path.join(__dirname, 'templates/billing_coding_error_template.md'), 'utf8'),
    mental_health_parity: fs.readFileSync(path.join(__dirname, 'templates/health_mental_health_parity_template.md'), 'utf8')
  },
  auto: {
    driver_not_on_policy: fs.readFileSync(path.join(__dirname, 'templates/auto_insurance_denial_template.md'), 'utf8'),
    coverage_limits: fs.readFileSync(path.join(__dirname, 'templates/auto_insurance_denial_template.md'), 'utf8'),
    lapsed_coverage: fs.readFileSync(path.join(__dirname, 'templates/auto_insurance_denial_template.md'), 'utf8'),
    business_use: fs.readFileSync(path.join(__dirname, 'templates/auto_insurance_denial_template.md'), 'utf8'),
    excluded_driver: fs.readFileSync(path.join(__dirname, 'templates/auto_insurance_denial_template.md'), 'utf8')
  },
  home: {
    maintenance_wear_tear: fs.readFileSync(path.join(__dirname, 'templates/home_insurance_denial_template.md'), 'utf8'),
    excluded_peril: fs.readFileSync(path.join(__dirname, 'templates/home_insurance_denial_template.md'), 'utf8'),
    policy_exclusion: fs.readFileSync(path.join(__dirname, 'templates/home_insurance_denial_template.md'), 'utf8'),
    insufficient_documentation: fs.readFileSync(path.join(__dirname, 'templates/home_insurance_denial_template.md'), 'utf8'),
    late_reporting: fs.readFileSync(path.join(__dirname, 'templates/home_insurance_denial_template.md'), 'utf8')
  }
};

// Helper function to format date
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Helper function to get current date
function getCurrentDate() {
  return new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Generate appeal letter from template
function generateAppealLetter(userData) {
  const { insuranceType, denialReason } = userData;
  
  // Get the appropriate template
  let template = templates[insuranceType][denialReason];
  
  if (!template) {
    throw new Error(`Template not found for ${insuranceType} insurance with denial reason: ${denialReason}`);
  }
  
  // Replace placeholders with user data
  let letter = template;
  
  // Common replacements
  letter = letter.replace(/\[Current Date\]/g, getCurrentDate());
  letter = letter.replace(/\[Policyholder Name\]/g, userData.policyholderName || '');
  letter = letter.replace(/\[Policyholder Address\]/g, userData.policyholderAddress || '');
  letter = letter.replace(/\[City, State ZIP\]/g, `${userData.city || ''}, ${userData.state || ''} ${userData.zipCode || ''}`);
  letter = letter.replace(/\[Insurance Company Name\]/g, userData.insuranceCompanyName || '');
  letter = letter.replace(/\[Insurance Company Address\]/g, userData.insuranceCompanyAddress || 'Claims Review Department');
  letter = letter.replace(/\[Policy Number\]/g, userData.policyNumber || '');
  letter = letter.replace(/\[Claim Number\]/g, userData.claimNumber || '');
  letter = letter.replace(/\[Denial Date\]/g, formatDate(userData.denialDate) || '');
  
  // Insurance-specific replacements
  if (insuranceType === 'health') {
    letter = letter.replace(/\[Date of Service\]/g, formatDate(userData.dateOfService) || '');
    letter = letter.replace(/\[Provider Name\]/g, userData.providerName || '');
    letter = letter.replace(/\[Treatment\]/g, userData.treatment || '');
    letter = letter.replace(/\[Diagnosis\]/g, userData.diagnosis || '');
  } else if (insuranceType === 'auto') {
    letter = letter.replace(/\[Date of Incident\]/g, formatDate(userData.dateOfIncident) || '');
    letter = letter.replace(/\[Vehicle Information\]/g, userData.vehicleInfo || '');
    letter = letter.replace(/\[Accident Description\]/g, userData.accidentDescription || '');
  } else if (insuranceType === 'home') {
    letter = letter.replace(/\[Date of Incident\]/g, formatDate(userData.dateOfIncidentHome) || '');
    letter = letter.replace(/\[Property Address\]/g, userData.propertyAddress || userData.policyholderAddress || '');
    letter = letter.replace(/\[Damage Description\]/g, userData.damageDescription || '');
    letter = letter.replace(/\[Damage Cause\]/g, userData.damageCause || '');
  }
  
  // Supporting documents
  if (userData.supportingDocs && userData.supportingDocs.length > 0) {
    const docsListItems = userData.supportingDocs.map(doc => `- ${doc}`).join('\n');
    letter = letter.replace(/\[Supporting Documents List\]/g, docsListItems);
  } else {
    letter = letter.replace(/\[Supporting Documents List\]/g, '- Copy of Denial Letter\n- Copy of Insurance Policy');
  }
  
  return letter;
}

// Convert markdown to HTML
function markdownToHtml(markdown) {
  return marked(markdown);
}

// Generate PDF from HTML
async function htmlToPdf(html, outputPath) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(html);
  await page.pdf({ path: outputPath, format: 'A4', margin: { top: '1cm', right: '1cm', bottom: '1cm', left: '1cm' } });
  await browser.close();
}

// Generate DOCX from markdown
async function markdownToDocx(markdown, outputPath) {
  const doc = new Document();
  
  // Split markdown into lines
  const lines = markdown.split('\n');
  
  // Process each line
  for (const line of lines) {
    if (line.trim() === '') {
      // Empty line
      doc.addParagraph(new Paragraph({}));
    } else if (line.startsWith('# ')) {
      // Heading 1
      doc.addParagraph(
        new Paragraph({
          text: line.substring(2),
          heading: HeadingLevel.HEADING_1
        })
      );
    } else if (line.startsWith('## ')) {
      // Heading 2
      doc.addParagraph(
        new Paragraph({
          text: line.substring(3),
          heading: HeadingLevel.HEADING_2
        })
      );
    } else if (line.startsWith('### ')) {
      // Heading 3
      doc.addParagraph(
        new Paragraph({
          text: line.substring(4),
          heading: HeadingLevel.HEADING_3
        })
      );
    } else if (line.startsWith('- ')) {
      // Bullet point
      doc.addParagraph(
        new Paragraph({
          text: line.substring(2),
          bullet: {
            level: 0
          }
        })
      );
    } else {
      // Regular paragraph
      doc.addParagraph(
        new Paragraph({
          text: line
        })
      );
    }
  }
  
  // Save document
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
}

// API endpoint to generate appeal letter
app.post('/api/generate-appeal', auth, async (req, res) => {
  try {
    const userData = req.body;
    
    // Validate required fields
    if (!userData.insuranceType || !userData.denialReason || !userData.policyholderName) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    // Generate unique ID for files
    const uniqueId = `appeal_${Date.now()}`;
    const outputDir = path.join(__dirname, 'output');
    
    // Create output directory if it doesn't exist
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Generate markdown appeal letter
    const markdownLetter = generateAppealLetter(userData);
    const markdownPath = path.join(outputDir, `${uniqueId}.md`);
    fs.writeFileSync(markdownPath, markdownLetter);
    
    // Convert to HTML
    const htmlLetter = markdownToHtml(markdownLetter);
    const htmlPath = path.join(outputDir, `${uniqueId}.html`);
    fs.writeFileSync(htmlPath, htmlLetter);
    
    // Convert to PDF
    const pdfPath = path.join(outputDir, `${uniqueId}.pdf`);
    await htmlToPdf(htmlLetter, pdfPath);
    
    // Convert to DOCX
    const docxPath = path.join(outputDir, `${uniqueId}.docx`);
    await markdownToDocx(markdownLetter, docxPath);
    
    // Save to user's appeals if authenticated
    if (req.user) {
      // In a real implementation, this would save to a database
      // For this demo, we'll just return success
    }
    
    // Return file paths
    res.json({
      success: true,
      files: {
        markdown: `/output/${uniqueId}.md`,
        html: `/output/${uniqueId}.html`,
        pdf: `/output/${uniqueId}.pdf`,
        docx: `/output/${uniqueId}.docx`
      },
      preview: htmlLetter
    });
  } catch (error) {
    console.error('Error generating appeal letter:', error);
    res.status(500).json({ error: error.message });
  }
});

// API endpoint to get suggestions for strengthening appeal
app.post('/api/get-suggestions', (req, res) => {
  const userData = req.body;
  const { insuranceType, denialReason } = userData;
  
  let suggestions = [
    'Include a copy of the denial letter to ensure your appeal addresses the specific reasons for denial.',
    'Include a copy of your policy document to reference specific coverage provisions.'
  ];
  
  // Add insurance-specific suggestions
  if (insuranceType === 'health') {
    if (denialReason === 'medical_necessity') {
      suggestions.push('A letter from your physician explaining why the treatment is medically necessary would significantly strengthen your appeal.');
      suggestions.push('Include any relevant medical records or test results that support the need for treatment.');
    } else if (denialReason === 'experimental_treatment') {
      suggestions.push('Include peer-reviewed studies or clinical guidelines that support the treatment\'s effectiveness.');
      suggestions.push('A letter from a specialist familiar with this treatment would strengthen your appeal.');
    }
  } else if (insuranceType === 'auto') {
    suggestions.push('Include photographs of the damage to your vehicle.');
    suggestions.push('If available, include a copy of the police report from the accident.');
  } else if (insuranceType === 'home') {
    suggestions.push('Include photographs of the damage to your property.');
    suggestions.push('A professional assessment from a contractor or inspector can help validate your claim.');
  }
  
  res.json({ suggestions });
});

// Serve static files from the public directory
app.use(express.static('public'));

// Serve HTML files
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'login.html'));
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'register.html'));
});

app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard.html'));
});

app.get('/saved-appeals', (req, res) => {
  res.sendFile(path.join(__dirname, 'saved-appeals.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;
