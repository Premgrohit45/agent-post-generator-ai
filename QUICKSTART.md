# 🚀 Quick Start Guide - LinkedIn Post Agent

## ⚡ Get Started in 5 Minutes!

### Step 1: Get Your Google AI API Key (FREE)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")

### Step 2: Set Up Gmail for Email Sending
1. Enable 2-Factor Authentication on Gmail
2. Go to: https://myaccount.google.com/apppasswords
3. Generate App Password for "Mail"
4. Copy the 16-character password

### Step 3: Configure Your Agent
1. Open `.env` file in this folder
2. Replace the placeholders:
   ```
   GOOGLE_API_KEY=AIza_your_actual_key_here
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=your_16_char_app_password
   EMAIL_RECIPIENT=recipient@gmail.com
   ```

### Step 4: Test Your Setup
```bash
python test_setup.py
```

### Step 5: Start Generating Blogs!

#### Option A: Interactive Mode (Beginner Friendly)
```bash
python main.py --interactive
```

#### Option B: Command Line
```bash
# Generate a post about AI
python main.py --topic "The Future of AI in Business"

# Generate with custom settings
python main.py --topic "Remote Work Tips" --tone casual --length short
```

## 🎯 What You Get

- **AI-Generated LinkedIn Posts** using Google's latest AI
- **Professional Email Distribution** to any recipient
- **Multiple Content Formats** (JSON, TXT, HTML email)
- **Batch Processing** for multiple topics
- **Topic Suggestions** powered by AI
- **Complete FREE Usage** with generous limits

## 💡 Example Commands

```bash
# Generate single post interactively
python main.py --interactive

# Generate specific topic
python main.py --topic "5 Leadership Tips for 2024"

# Generate with custom tone
python main.py --topic "Digital Marketing Trends" --tone inspirational

# Generate short content
python main.py --topic "Quick Productivity Hacks" --length short
```

## 📊 Usage Limits (FREE)

- **15 posts per minute**
- **1,500 posts per day**
- **Zero cost** for typical usage
- **No credit card** required

## 🆘 Need Help?

1. **Setup Issues**: Check `README.md` for detailed instructions
2. **API Problems**: Ensure your Google API key is valid
3. **Email Issues**: Verify Gmail App Password setup
4. **General Questions**: Review the documentation in `docs/`

## 🎉 That's It!

You now have a fully functional AI-powered LinkedIn post agent that can:
- Generate professional content in seconds
- Send beautifully formatted emails
- Save posts for later use
- Suggest trending topics
- Scale to multiple posts automatically

**Happy Blogging! 🚀**