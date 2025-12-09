# 🚀 Streamlit Cloud Deployment Guide

## Step-by-Step Deployment Instructions

### 📌 **STEP 1: Prepare Your GitHub Repository**
✅ **ALREADY DONE** - Your code is on GitHub at:
```
https://github.com/Premgrohit45/linkedin-agent-post-generator-ai
```

---

### 🔐 **STEP 2: Create Streamlit Cloud Account**

1. Go to: **https://streamlit.io/cloud**
2. Click **"Sign up"** (top right)
3. Select **"Sign up with GitHub"**
4. Authorize Streamlit to access your GitHub account
5. Follow the prompts to complete signup

---

### ⚙️ **STEP 3: Deploy Your App**

1. After logging into Streamlit Cloud, click **"New app"** (top right)

2. You'll see a deployment form with 3 fields:
   ```
   Repository: Premgrohit45/linkedin-agent-post-generator-ai
   Branch: master
   Main file path: streamlit_app_modern.py
   ```

3. **Fill in the fields:**
   - **Repository**: Select `Premgrohit45/linkedin-agent-post-generator-ai`
   - **Branch**: Select `master`
   - **Main file path**: Type `streamlit_app_modern.py`

4. Click **"Deploy!"** button

---

### 🔑 **STEP 4: Add Secrets (API Keys)**

⚠️ **IMPORTANT**: Your app needs API keys to function!

**Method A: Via Streamlit Cloud Dashboard (Recommended)**

1. Wait for your app to finish deploying
2. Once deployed, click the **☰ menu** (top right of your app)
3. Select **"Settings"**
4. Go to **"Secrets"** tab
5. Click **"Edit secrets"**
6. Add your secrets in this format:

```
GOOGLE_API_KEY = "your-actual-google-api-key-here"
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-16-char-app-password"
```

7. Click **"Save"**

**Method B: Via GitHub (Alternative)**

1. Create a file `.streamlit/secrets.toml` in your repo root
2. Add the same content as above
3. Push to GitHub
4. Streamlit will automatically use it

---

### 🔑 **STEP 5: Get Your API Keys**

#### **A. Google Gemini API Key**

1. Go to: https://ai.google.dev/
2. Click **"Get API key"**
3. Create a new project or select existing
4. Copy the API key
5. Add to Streamlit Secrets as `GOOGLE_API_KEY`

#### **B. Gmail App Password**

1. Go to: https://myaccount.google.com/
2. Select **"Security"** (left sidebar)
3. Look for **"App passwords"** (scroll down)
4. Select `Mail` and `Windows Computer`
5. Google will generate a 16-character password
6. Copy and add to Streamlit Secrets as `EMAIL_PASSWORD`
7. Use your full email address as `EMAIL_SENDER`

---

### ✅ **STEP 6: Verify Deployment**

1. Your app should be live at:
   ```
   https://your-app-name.streamlit.app
   ```

2. Click the **☰ menu** in your deployed app to verify sidebar works

3. Try these features:
   - ✓ Click the green **☰** menu button (opens sidebar)
   - ✓ Check statistics in sidebar
   - ✓ Generate a sample post
   - ✓ Test email sending

---

## 🎯 **Quick Checklist**

- [ ] Code is on GitHub (https://github.com/Premgrohit45/linkedin-agent-post-generator-ai)
- [ ] Streamlit Cloud account created
- [ ] App deployed via "New app"
- [ ] GOOGLE_API_KEY added to Secrets
- [ ] EMAIL_SENDER added to Secrets
- [ ] EMAIL_PASSWORD added to Secrets
- [ ] App is live and functional
- [ ] Sidebar opens and displays stats
- [ ] Post generation works
- [ ] Email sending works

---

## 🆘 **Troubleshooting**

### **Issue: "ModuleNotFoundError: No module named..."**
✅ **Solution**: Streamlit automatically installs from `requirements.txt` (already in your repo)

### **Issue: "API Key not found"**
✅ **Solution**: 
- Go to app Settings → Secrets
- Verify keys are added exactly as shown above
- Check for extra spaces or quotes

### **Issue: "Email failed to send"**
✅ **Solution**:
- Verify EMAIL_SENDER is correct Gmail address
- Verify EMAIL_PASSWORD is 16-character app password (not regular password)
- Check Gmail security settings

### **Issue: "App won't load"**
✅ **Solution**:
- Check the logs in Streamlit Cloud dashboard
- Redeploy by clicking "Reboot" in app menu
- Check if all dependencies installed correctly

---

## 📊 **Expected App Features After Deployment**

✅ **Working Features**:
- Beautiful neon-themed UI
- Futuristic popup sidebar (click ☰ button)
- Real-time statistics
- AI-powered post generation (1-10 paragraphs)
- Email distribution system
- Session state management

✅ **Sidebar Features**:
- 🤖 Agent Status display
- 📊 Posts Generated counter
- 📧 Emails Sent counter
- 🔗 Connection Status
- 🔄 Reset Stats button
- 🔍 Diagnostics button
- 💾 Export Logs button
- ⚙️ Settings placeholder

---

## 🔒 **Security Notes**

1. **Never commit `.env` file** to GitHub (it's in .gitignore)
2. **Always use Streamlit Secrets** for API keys on cloud
3. **Rotate API keys regularly** for security
4. **Monitor API usage** to prevent unexpected charges

---

## 📞 **Support Links**

- Streamlit Docs: https://docs.streamlit.io/
- Streamlit Cloud: https://streamlit.io/cloud
- Google Gemini API: https://ai.google.dev/
- Gmail Setup Help: https://support.google.com/accounts

---

## ✨ **You're Ready to Deploy!**

Follow the steps above and your app will be live in minutes! 🎉

**Questions?** Check the troubleshooting section or visit Streamlit docs.

---

**Last Updated**: December 9, 2025
**Repository**: https://github.com/Premgrohit45/linkedin-agent-post-generator-ai
