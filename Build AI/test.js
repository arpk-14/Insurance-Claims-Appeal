// Test script for AI Insurance Claims Denial Appeal Writer web application
const assert = require('assert');
const axios = require('axios');
const fs = require('fs');
const path = require('path');

// Base URL for API
const API_URL = 'http://localhost:3000/api';

// Test user credentials
const testUser = {
  name: 'Test User',
  email: 'test@example.com',
  password: 'password123'
};

// Test appeal data
const testAppeal = {
  insuranceType: 'health',
  denialReason: 'medical_necessity',
  policyholderName: 'John Doe',
  policyholderAddress: '123 Main St',
  city: 'Anytown',
  state: 'CA',
  zipCode: '12345',
  insuranceCompanyName: 'Health Insurance Co',
  insuranceCompanyAddress: '456 Corporate Ave, Suite 789',
  policyNumber: 'POL123456',
  claimNumber: 'CLM789012',
  denialDate: '2025-03-15',
  dateOfService: '2025-02-28',
  providerName: 'Dr. Jane Smith',
  treatment: 'Physical Therapy',
  diagnosis: 'Lower Back Pain',
  supportingDocs: ['Medical Records', 'Letter from Doctor'],
  urgencyLevel: 'medium',
  additionalInfo: 'I have been experiencing severe pain and this treatment is necessary for my recovery.'
};

// Store auth token
let authToken = '';

// Run tests
async function runTests() {
  console.log('Starting tests for AI Insurance Claims Denial Appeal Writer...');
  
  try {
    // Test 1: Register new user
    console.log('\nTest 1: Register new user');
    await testRegister();
    
    // Test 2: Login
    console.log('\nTest 2: Login');
    await testLogin();
    
    // Test 3: Get user data
    console.log('\nTest 3: Get user data');
    await testGetUser();
    
    // Test 4: Generate appeal letter
    console.log('\nTest 4: Generate appeal letter');
    await testGenerateAppeal();
    
    // Test 5: Get suggestions
    console.log('\nTest 5: Get suggestions');
    await testGetSuggestions();
    
    // Test 6: Save appeal
    console.log('\nTest 6: Save appeal');
    await testSaveAppeal();
    
    // Test 7: Get saved appeals
    console.log('\nTest 7: Get saved appeals');
    await testGetAppeals();
    
    console.log('\nAll tests passed successfully!');
  } catch (error) {
    console.error('\nTest failed:', error.message);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
  }
}

// Test user registration
async function testRegister() {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, testUser);
    assert(response.status === 200, 'Registration failed');
    assert(response.data.token, 'No token returned');
    console.log('✓ User registration successful');
    authToken = response.data.token;
  } catch (error) {
    // If user already exists, this is fine for testing
    if (error.response && error.response.status === 400 && 
        error.response.data.errors && 
        error.response.data.errors[0].msg === 'User already exists') {
      console.log('✓ User already exists, proceeding with login test');
    } else {
      throw error;
    }
  }
}

// Test user login
async function testLogin() {
  const response = await axios.post(`${API_URL}/auth/login`, {
    email: testUser.email,
    password: testUser.password
  });
  
  assert(response.status === 200, 'Login failed');
  assert(response.data.token, 'No token returned');
  console.log('✓ User login successful');
  authToken = response.data.token;
}

// Test getting user data
async function testGetUser() {
  const response = await axios.get(`${API_URL}/auth/user`, {
    headers: {
      'x-auth-token': authToken
    }
  });
  
  assert(response.status === 200, 'Failed to get user data');
  assert(response.data.name === testUser.name, 'User name does not match');
  assert(response.data.email === testUser.email, 'User email does not match');
  console.log('✓ Get user data successful');
}

// Test generating appeal letter
async function testGenerateAppeal() {
  const response = await axios.post(`${API_URL}/generate-appeal`, testAppeal, {
    headers: {
      'x-auth-token': authToken,
      'Content-Type': 'application/json'
    }
  });
  
  assert(response.status === 200, 'Failed to generate appeal letter');
  assert(response.data.success, 'Appeal generation not successful');
  assert(response.data.files.markdown, 'No markdown file path returned');
  assert(response.data.files.html, 'No HTML file path returned');
  assert(response.data.files.pdf, 'No PDF file path returned');
  assert(response.data.files.docx, 'No DOCX file path returned');
  assert(response.data.preview, 'No preview HTML returned');
  
  // Check if preview contains expected content
  assert(response.data.preview.includes(testAppeal.policyholderName), 'Preview does not contain policyholder name');
  assert(response.data.preview.includes(testAppeal.insuranceCompanyName), 'Preview does not contain insurance company name');
  
  console.log('✓ Appeal letter generation successful');
}

// Test getting suggestions
async function testGetSuggestions() {
  const response = await axios.post(`${API_URL}/get-suggestions`, {
    insuranceType: testAppeal.insuranceType,
    denialReason: testAppeal.denialReason
  });
  
  assert(response.status === 200, 'Failed to get suggestions');
  assert(Array.isArray(response.data.suggestions), 'Suggestions is not an array');
  assert(response.data.suggestions.length > 0, 'No suggestions returned');
  console.log('✓ Get suggestions successful');
}

// Test saving appeal
async function testSaveAppeal() {
  const response = await axios.post(`${API_URL}/auth/save-appeal`, testAppeal, {
    headers: {
      'x-auth-token': authToken,
      'Content-Type': 'application/json'
    }
  });
  
  assert(response.status === 200, 'Failed to save appeal');
  assert(response.data.success, 'Appeal save not successful');
  assert(response.data.appealId, 'No appeal ID returned');
  console.log('✓ Save appeal successful');
}

// Test getting saved appeals
async function testGetAppeals() {
  const response = await axios.get(`${API_URL}/auth/appeals`, {
    headers: {
      'x-auth-token': authToken
    }
  });
  
  assert(response.status === 200, 'Failed to get appeals');
  assert(Array.isArray(response.data), 'Appeals is not an array');
  assert(response.data.length > 0, 'No appeals returned');
  
  // Check if the saved appeal is in the list
  const savedAppeal = response.data.find(appeal => 
    appeal.insuranceType === testAppeal.insuranceType &&
    appeal.denialReason === testAppeal.denialReason &&
    appeal.policyholderName === testAppeal.policyholderName
  );
  
  assert(savedAppeal, 'Saved appeal not found in appeals list');
  console.log('✓ Get appeals successful');
}

// Run the tests
runTests().catch(console.error);
