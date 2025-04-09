#!/bin/bash

# Deployment script for AI Insurance Claims Denial Appeal Writer website
# This script deploys the application to production environments

echo "Starting deployment process for AI Insurance Claims Denial Appeal Writer..."

# Check if Netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "Netlify CLI not found. Installing..."
    npm install -g netlify-cli
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "Heroku CLI not found. Installing..."
    curl https://cli-assets.heroku.com/install.sh | sh
fi

# Deploy backend to Heroku
echo "Deploying backend to Heroku..."
echo "Note: This script assumes you have already logged in to Heroku CLI"
echo "If not, please run 'heroku login' before continuing"

# Create Heroku app if it doesn't exist
heroku_app_name="ai-insurance-appeal-writer"
if ! heroku apps:info --app $heroku_app_name &> /dev/null; then
    echo "Creating Heroku app: $heroku_app_name"
    heroku create $heroku_app_name
else
    echo "Using existing Heroku app: $heroku_app_name"
fi

# Set environment variables
echo "Setting environment variables..."
heroku config:set JWT_SECRET="your-secure-jwt-secret" --app $heroku_app_name
heroku config:set NODE_ENV="production" --app $heroku_app_name

# Deploy to Heroku
echo "Pushing code to Heroku..."
git init
git add .
git commit -m "Deploy to Heroku"
git push heroku master

# Deploy frontend to Netlify
echo "Deploying frontend to Netlify..."
echo "Note: This script assumes you have already logged in to Netlify CLI"
echo "If not, please run 'netlify login' before continuing"

# Create Netlify site if it doesn't exist
netlify_site_name="ai-insurance-appeal-writer"
if ! netlify sites:list | grep -q $netlify_site_name; then
    echo "Creating Netlify site: $netlify_site_name"
    netlify sites:create --name $netlify_site_name
else
    echo "Using existing Netlify site: $netlify_site_name"
fi

# Deploy to Netlify
echo "Deploying to Netlify..."
netlify deploy --prod

echo "Deployment complete!"
echo "Backend URL: https://$heroku_app_name.herokuapp.com"
echo "Frontend URL: https://$netlify_site_name.netlify.app"
