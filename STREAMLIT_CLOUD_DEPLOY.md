# 🚀 Streamlit Cloud Deployment Guide

## Quick Deploy Steps

### 1. Push Code to GitHub ✅
Your code is already on GitHub at: `https://github.com/Premgrohit45/agent-post-generator-ai`

### 2. Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account (Premgrohit45)

2. **Create New App**
   - Click "New app"
   - Repository: `Premgrohit45/agent-post-generator-ai`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

### 3. Configure Secrets

After deployment, go to **App Settings > Secrets** and add:

```toml
GOOGLE_API_KEY = "AIzaSyDu-xL3V34L7Q42yzRkd-kln_LwxOfzotM"
EMAIL_SENDER = "prem.golhar2005@gmail.com"
EMAIL_PASSWORD = "tuey tcyn wszn nsbs"
EMAIL_RECIPIENT = "prem.golhar2005@gmail.com"
```

### 4. Get Your Google AI API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and paste into Streamlit secrets

### 5. Gmail App Password

1. Enable 2-Factor Authentication on your Gmail
2. Go to: https://myaccount.google.com/apppasswords
3. Create app password for "Mail"
4. Copy the 16-character password into Streamlit secrets

## Your App Will Be Live! 🎉

Your app will be accessible at:
`https://[your-app-name].streamlit.app/`

## Troubleshooting

- If deployment fails, check the logs in Streamlit Cloud
- Make sure all secrets are properly configured
- Verify your Google AI API key is active
- Ensure Gmail app password is correct

## Features
✅ AI-Powered LinkedIn Post Generation
✅ Email Distribution
✅ Modern Dark UI
✅ Customizable Settings
