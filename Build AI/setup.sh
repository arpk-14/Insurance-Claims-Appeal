#!/bin/bash

# Setup script for AI Insurance Claims Denial Appeal Writer website
# This script prepares the environment for testing and deployment

echo "Setting up AI Insurance Claims Denial Appeal Writer website..."

# Create public directory for static files
mkdir -p public
cp index.html public/
cp login.html public/
cp register.html public/
cp dashboard.html public/
cp saved-appeals.html public/
cp styles.css public/
cp script.js public/
cp integration.js public/

# Create templates directory and copy templates
mkdir -p templates
cp ../templates/*.md templates/

# Create output directory for generated files
mkdir -p output

# Install dependencies
echo "Installing dependencies..."
npm install

# Install additional dependencies for testing
npm install --save-dev axios mocha chai

# Update package.json to include test script
sed -i 's/"scripts": {/"scripts": {\n    "test": "node test.js",/g' package.json

echo "Setup complete!"
echo "To start the server: npm start"
echo "To run automated tests: npm test"
echo "To run manual tests: node manual_test_checklist.js"
