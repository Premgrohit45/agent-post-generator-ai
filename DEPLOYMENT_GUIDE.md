# 🚀 Deployment Guide - LinkedGenius AI Post Generator

## ✅ GitHub Push Status
- **Repository**: `https://github.com/Premgrohit45/linkedin-agent-post-generator-ai`
- **Owner**: Premgrohit45
- **Status**: ✅ All code committed and pushed to master branch
- **Latest Commit**: `a4683b1` - Update agent logic and UI: sidebar + enhancements

---

## 📋 Prerequisites for Deployment

### 1. **System Requirements**
- Python 3.9 or higher
- Git (version control)
- pip (Python package manager)
- Internet connection for API calls

### 2. **Required API Keys**
You'll need to obtain:
- **Google Gemini API Key** (for AI post generation)
- **Gmail App Password** (for email sending)
- **Web Search API Key** (optional, for web research)

---

## 🔧 Local Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/Premgrohit45/linkedin-agent-post-generator-ai.git
cd linkedin-agent-post-generator-ai
```

### Step 2: Create Virtual Environment
```bash
# For Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
EMAIL_SENDER=your_gmail_address@gmail.com
EMAIL_PASSWORD=your_gmail_app_password_here
SEARCH_API_KEY=your_search_api_key_here (optional)
```

**How to get Gmail App Password:**
1. Go to Google Account Settings: https://myaccount.google.com/
2. Navigate to Security > App passwords
3. Select Mail and Windows Computer
4. Copy the generated 16-character password
5. Paste it in `.env` as `EMAIL_PASSWORD`

### Step 5: Run the Application Locally
```bash
streamlit run streamlit_app_modern.py
```

The app will open at `http://localhost:8501`

---

## 🌐 Cloud Deployment Options

### **Option 1: Streamlit Cloud (Recommended - FREE & Easy)**

#### Steps:
1. **Push code to GitHub** (Already done! ✅)

2. **Go to Streamlit Cloud**: https://streamlit.io/cloud

3. **Sign in with GitHub**
   - Click "New app"
   - Select your repository: `Premgrohit45/linkedin-agent-post-generator-ai`
   - Select branch: `master`
   - Set main file path: `streamlit_app_modern.py`

4. **Add Secrets** (Environment Variables)
   - In Streamlit Cloud, go to your app settings
   - Click "Secrets"
   - Add the following:
   ```
   GOOGLE_API_KEY = "your_api_key"
   EMAIL_SENDER = "your_email@gmail.com"
   EMAIL_PASSWORD = "your_app_password"
   ```

5. **Deploy**
   - Click "Deploy" and wait for the app to build
   - Your app will be live at: `https://your-username-appname.streamlit.app`

---

### **Option 2: Heroku (Requires Credit Card)**

#### Steps:
1. **Create Procfile** (create in project root):
```
web: streamlit run streamlit_app_modern.py --server.port=$PORT --server.address=0.0.0.0
```

2. **Create runtime.txt** (create in project root):
```
python-3.11.0
```

3. **Deploy to Heroku**:
```bash
heroku login
heroku create your-app-name
heroku config:set GOOGLE_API_KEY="your_key"
heroku config:set EMAIL_SENDER="your_email"
heroku config:set EMAIL_PASSWORD="your_password"
git push heroku master
```

---

### **Option 3: Azure App Service (Enterprise)**

#### Steps:
1. **Create Azure App Service**
2. **Configure deployment from GitHub**
3. **Set environment variables** in Azure portal
4. **Deploy**

---

### **Option 4: AWS Lambda + API Gateway (Advanced)**

1. **Package application** with serverless framework
2. **Deploy** using AWS CLI or AWS Console

---

## 🧪 Testing After Deployment

1. **Visit your deployed URL**
2. **Test Features**:
   - Generate a sample post
   - Send test email
   - Verify sidebar opens (click ☰ icon)
   - Check statistics update

---

## 📊 Project Features

✅ **AI-Powered Post Generation**
- Uses Google Gemini 2.5-Flash LLM
- LangChain framework with ReAct agent
- Supports multiple AI tools: Web search, statistics, trending topics

✅ **Email Distribution**
- SMTP email sending via Gmail
- Batch email sending support
- Error handling and validation

✅ **Beautiful UI**
- Futuristic Streamlit interface
- Neon-themed popup sidebar with statistics
- Real-time stats tracking
- Animated elements and glassmorphic design

✅ **Session Management**
- Auto-updating statistics
- Post history tracking
- Multi-page navigation

---

## 🐛 Troubleshooting

### Issue: "AttributeError: st.session_state has no attribute..."
**Solution**: Clear Streamlit cache
```bash
rm -rf ~/.streamlit/
streamlit run streamlit_app_modern.py
```

### Issue: "ModuleNotFoundError: No module named 'langchain_core'"
**Solution**: Reinstall dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Gmail authentication fails
**Solution**:
1. Verify email and password in `.env`
2. Ensure Gmail App Password is used (not regular password)
3. Check if 2-factor authentication is enabled

### Issue: API Key errors
**Solution**:
1. Verify API key is correct in `.env`
2. Check API quota in Google Cloud Console
3. Ensure API is enabled in Cloud Console

---

## 📝 File Structure

```
linkedin-agent-post-generator-ai/
├── streamlit_app_modern.py       # Main UI application
├── requirements.txt              # Python dependencies
├── .env.example                  # Example env variables
├── .gitignore                    # Git ignore rules
├── src/
│   ├── langchain_post_agent.py   # LangChain agent for post generation
│   ├── email_sender.py           # Email sending module
│   ├── advanced_agent_orchestrator.py  # Agent coordinator
│   ├── agent_tools.py            # Tool definitions for LLM
│   └── config.py                 # Configuration management
├── output/                       # Generated posts storage
├── docs/                         # Documentation
└── DEPLOYMENT_GUIDE.md          # This file
```

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** (already in .gitignore)
2. **Use environment variables** for all secrets
3. **Rotate API keys** regularly
4. **Monitor API usage** to prevent unexpected charges
5. **Enable GitHub secret scanning**

---

## 📞 Support & Resources

- **Google Gemini API Docs**: https://ai.google.dev/
- **Streamlit Docs**: https://docs.streamlit.io/
- **LangChain Docs**: https://python.langchain.com/
- **GitHub Pages**: https://github.com/Premgrohit45/linkedin-agent-post-generator-ai

---

## ✨ Latest Updates

### Recent Changes:
✅ Futuristic popup slide-in sidebar with statistics
✅ Paragraph-based post length (1-10 paragraphs)
✅ Real-time stats tracking in sidebar
✅ Glassmorphic UI design
✅ Fixed KeyError in post generation
✅ Added session state initialization

---

**Last Updated**: December 9, 2025
**Status**: Ready for Production ✅
