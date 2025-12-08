import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import json
import time
from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Try importing custom modules
try:
    from src.agent_tools import AgentTools
except ImportError:
    st.warning("⚠️ Agent Tools module not fully loaded - running in demo mode")
    AgentTools = None

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="🚀 LinkedIn Post Generator | AI-Powered",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - MODERN & ATTRACTIVE DESIGN
# ============================================================================
def load_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        /* Main App Background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #e2e8f0;
        }
        
        /* Header Styling */
        .header-container {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            padding: 2.5rem 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 20px 60px rgba(6, 182, 212, 0.2);
            text-align: center;
            animation: slideDown 0.6s ease-out;
        }
        
        .header-container h1 {
            color: #ffffff;
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            font-family: 'Poppins', sans-serif;
        }
        
        .header-container p {
            color: #e0f2fe;
            font-size: 1.1rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            border-right: 2px solid #0ea5e9;
        }
        
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 2rem;
        }
        
        .sidebar-header {
            color: #0ea5e9;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #0ea5e9;
            font-family: 'Poppins', sans-serif;
        }
        
        /* Card Styling */
        .stat-card {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #0ea5e9;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(14, 165, 233, 0.2);
            border-left: 4px solid #06b6d4;
        }
        
        .stat-label {
            color: #94a3b8;
            font-size: 0.9rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        
        .stat-value {
            color: #ffffff;
            font-size: 2rem;
            font-weight: 700;
            font-family: 'Poppins', sans-serif;
        }
        
        .stat-subtext {
            color: #64748b;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        /* Input Sections */
        .input-section {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #0ea5e9;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        .input-section h3 {
            color: #0ea5e9;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Poppins', sans-serif;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 25px rgba(14, 165, 233, 0.3);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
            box-shadow: 0 15px 35px rgba(14, 165, 233, 0.4);
            transform: translateY(-2px);
        }
        
        .stButton > button:active {
            transform: translateY(0px);
        }
        
        /* Text Area Styling */
        .stTextArea textarea {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #0ea5e9 !important;
            border-radius: 8px !important;
            font-family: 'Inter', sans-serif;
        }
        
        .stTextArea textarea:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
        }
        
        /* Text Input Styling */
        .stTextInput input {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #0ea5e9 !important;
            border-radius: 8px !important;
        }
        
        .stTextInput input:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.1) !important;
        }
        
        /* Select Box Styling */
        .stSelectbox > div > div {
            background-color: #0f172a !important;
            color: #e2e8f0 !important;
            border: 1px solid #0ea5e9 !important;
            border-radius: 8px !important;
        }
        
        /* Success/Info Messages */
        .stSuccess {
            background-color: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid #10b981 !important;
            border-radius: 8px !important;
        }
        
        .stInfo {
            background-color: rgba(14, 165, 233, 0.1) !important;
            border: 1px solid #0ea5e9 !important;
            border-radius: 8px !important;
        }
        
        .stWarning {
            background-color: rgba(245, 158, 11, 0.1) !important;
            border: 1px solid #f59e0b !important;
            border-radius: 8px !important;
        }
        
        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0px;
            background-color: #1e293b;
            border-bottom: 2px solid #0ea5e9;
            border-radius: 0px;
            padding: 0px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding: 0px 20px;
            background-color: #1e293b;
            border-radius: 0px;
            color: #94a3b8;
            font-weight: 600;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #0ea5e9;
            color: white;
        }
        
        /* Generated Post Container */
        .post-container {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border: 2px solid #0ea5e9;
            border-radius: 12px;
            padding: 2rem;
            margin-top: 1.5rem;
            box-shadow: 0 15px 40px rgba(14, 165, 233, 0.15);
        }
        
        .post-container h4 {
            color: #0ea5e9;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 700;
        }
        
        .post-content {
            background-color: #0f172a;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #06b6d4;
            color: #e2e8f0;
            line-height: 1.8;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }
        
        /* Animations */
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .header-container h1 {
                font-size: 1.8rem;
            }
            
            .stat-card {
                padding: 1rem;
            }
            
            .stat-value {
                font-size: 1.5rem;
            }
        }
        
        /* Divider */
        .divider {
            border-top: 2px solid #0ea5e9;
            margin: 2rem 0;
            opacity: 0.3;
        }
    </style>
    """, unsafe_allow_html=True)

# Load CSS
load_custom_css()

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'generated_posts' not in st.session_state:
    st.session_state.generated_posts = []

if 'total_posts_generated' not in st.session_state:
    st.session_state.total_posts_generated = 0

if 'post_stats' not in st.session_state:
    st.session_state.post_stats = {
        'beginner': 0,
        'intermediate': 0,
        'expert': 0
    }

if 'email_sender' not in st.session_state:
    st.session_state.email_sender = ""

if 'email_password' not in st.session_state:
    st.session_state.email_password = ""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def generate_comprehensive_post(topic: str, expertise_level: str, tone: str, num_paragraphs: int, hashtags: int) -> str:
    """Generate a comprehensive, multi-paragraph LinkedIn post"""
    
    # Extensive paragraph templates for different expertise levels
    opening_paragraphs = {
        'beginner': [
            f"Just started exploring {topic} and I'm genuinely impressed! 🚀\n\nI've been diving deep into understanding how {topic} is reshaping the way we work and think. What started as curiosity has turned into a genuine passion for this space.",
            f"Never thought I'd say this, but {topic} has completely changed my perspective. 💡\n\nAfter spending the last few weeks learning about {topic}, I realize how crucial it is for anyone in tech to understand its fundamentals.",
        ],
        'intermediate': [
            f"After months of working with {topic}, I've discovered some game-changing insights. 🔥\n\nMy journey with {topic} has been transformative, and I want to share what I've learned with everyone in this community.",
            f"{topic} is not just a buzzword - it's a fundamental shift in how we approach problems. 📊\n\nHaving implemented {topic} in several projects, I can confidently say that understanding its core principles is essential for modern professionals.",
        ],
        'expert': [
            f"After years of working in {topic}, I can tell you with certainty that we're at an inflection point. 🎯\n\nThe evolution of {topic} over the past decade has been remarkable, and we're only scratching the surface of its potential.",
            f"As someone who's been deep in the {topic} space for years, I've witnessed both the hype and the reality. 💼\n\nToday, I want to share my perspective on where {topic} is headed and why it matters for your career.",
        ]
    }
    
    insight_paragraphs = {
        'beginner': [
            f"What makes {topic} so important right now? Here's my take:\n\n✅ First, it's solving real-world problems that were previously unsolvable\n✅ Second, it's creating new opportunities for innovation across industries\n✅ Third, the learning curve is becoming more accessible than ever before\n\nEveryone can benefit from understanding {topic}, regardless of their background.",
            f"Key things I've learned about {topic}:\n\n🔑 It's not as complicated as it seems at first\n🔑 The fundamentals matter more than you think\n🔑 Hands-on practice is crucial for mastery\n🔑 Community support is invaluable\n\nThe {topic} ecosystem is growing rapidly, and now is the perfect time to jump in.",
            f"The impact of {topic} is undeniable:\n\n📈 Industry adoption is accelerating\n📈 Job opportunities are skyrocketing\n📈 Innovation is happening at an unprecedented pace\n📈 Skills in {topic} are becoming highly valuable\n\nIf you haven't started learning {topic} yet, what are you waiting for?",
        ],
        'intermediate': [
            f"The practical applications of {topic} are expanding rapidly:\n\n💪 Enterprise-level implementations are becoming mainstream\n💪 Startups are using it to gain competitive advantages\n💪 Cross-industry collaboration is opening new possibilities\n💪 The ROI is becoming increasingly measurable\n\nFrom my experience, the key to success with {topic} is strategic implementation.",
            f"What I've learned from implementing {topic}:\n\n🎯 Planning and strategy are critical before diving in\n🎯 Integration with existing systems requires careful consideration\n🎯 Training and change management are often overlooked\n🎯 Continuous improvement is essential\n\nThe teams that succeed with {topic} are those that treat it as a long-term investment.",
            f"Current trends in {topic}:\n\n📊 Automation is reaching new levels of sophistication\n📊 Integration with AI is becoming standard\n📊 Security and compliance are top priorities\n📊 Scalability solutions are improving significantly\n\nThese trends are shaping the future of how {topic} will be used across organizations.",
        ],
        'expert': [
            f"The evolution of {topic} has been fascinating to witness:\n\n🔬 Early adoption challenges have been largely overcome\n🔬 Standardization efforts are creating better interoperability\n🔬 Advanced use cases are pushing the boundaries of what's possible\n🔬 The talent pool is finally catching up to demand\n\nWe're entering a maturity phase where {topic} is becoming as essential as electricity in many industries.",
            f"My predictions for the {topic} landscape:\n\n🚀 Consolidation among vendors will accelerate\n🚀 New regulations will emerge to ensure responsible use\n🚀 Integration with emerging technologies will create new paradigms\n🚀 Ethical considerations will take center stage\n\nOrganizations that adapt quickly will have significant competitive advantages.",
            f"The technical depth required for {topic}:\n\n🔧 Deep understanding of underlying principles is crucial\n🔧 Cross-disciplinary knowledge becomes increasingly valuable\n🔧 Practical experience with edge cases is essential\n🔧 Continuous learning is non-negotiable\n\nThe future belongs to those who master both the art and science of {topic}.",
        ]
    }
    
    reflection_paragraphs = {
        'beginner': [
            f"What excites me most about {topic} is the potential it holds:\n\nImagine a world where {topic} has solved major challenges in our society. That's not far-fetched. We're already seeing glimpses of this future in forward-thinking organizations.\n\nIf you're on the fence about learning {topic}, I'd encourage you to take the first step today. The learning journey is rewarding, and the community is incredibly supportive.",
            f"The beauty of {topic} is that it's still early:\n\nWhile it may seem like everyone is talking about {topic}, most people still don't truly understand it. This is an incredible opportunity for those willing to invest the time to learn.\n\nThe people who act now and become proficient in {topic} will have significant advantages in the coming years.",
        ],
        'intermediate': [
            f"Looking ahead, {topic} will continue to evolve:\n\nThe next generation of {topic} applications will be more intuitive, more powerful, and more accessible than what exists today. Organizations that build expertise now will lead this transformation.\n\nMy advice? Don't just learn about {topic} - actively participate in shaping its future. Share your insights, collaborate with others, and push the boundaries of what's possible.",
            f"The competitive advantage goes to those who embrace {topic} early:\n\nHistory shows us that early adopters of transformative technologies gain disproportionate benefits. The {topic} revolution is happening now, and the window of opportunity won't remain open forever.\n\nInvest in your {topic} expertise, build networks within the community, and position yourself for the future.",
        ],
        'expert': [
            f"As we look toward the future of {topic}:\n\nWe stand at a unique moment where the theoretical foundations are well-established, and practical applications are being refined daily. The next frontier is not whether {topic} will succeed, but how it will reshape entire industries.\n\nFor those of us who've been in this space, our responsibility is to guide the next generation, ensure ethical implementation, and push for responsible innovation.",
            f"The maturation of {topic} brings new challenges and opportunities:\n\nWe must address questions of governance, sustainability, and societal impact. The technical challenges are largely solved; now we face strategic and ethical ones. Those who can navigate this complexity will define the future of {topic}.\n\nMy commitment is to continue exploring, learning, and sharing insights as this field evolves. I hope you'll join this journey.",
        ]
    }
    
    closing_paragraphs = {
        'beginner': [
            f"This is just the beginning of my {topic} journey, and I can't wait to see where it takes me. If you're interested in {topic}, let's connect and learn together!",
            f"Whether you're a complete beginner or have some {topic} experience, there's always more to discover. I'd love to hear your thoughts on {topic} in the comments below.",
            f"The {topic} community is amazing, and I'm grateful to be part of it. If this resonated with you, share your own {topic} journey in the comments!",
        ],
        'intermediate': [
            f"I'm genuinely excited about where {topic} is heading, and I'd love to collaborate with others who share this passion. Let's build something great together!",
            f"Your experience with {topic} might be different from mine, and that's valuable. Let's discuss in the comments - what aspects of {topic} excite you the most?",
            f"If you're working on {{topic}} projects or have insights to share, please reach out. I'm always eager to learn from others in this space.",
        ],
        'expert': [
            f"The future of {{topic}} is being written by all of us. I'm excited to see where the community takes this technology. What are your predictions for {{topic}}?",
            f"For those diving deep into {{topic}}, let's connect and share knowledge. The best innovations come from collaborative effort within our community.",
            f"My mission is to advance {{topic}} knowledge and foster responsible innovation. If you share this vision, let's connect and make an impact together.",
        ]
    }
    
    # Build the post
    post_parts = []
    
    # Opening paragraph
    post_parts.append(random.choice(opening_paragraphs[expertise_level]))
    
    # Add insight paragraphs based on number requested
    available_insights = insight_paragraphs[expertise_level]
    num_insights = min(num_paragraphs - 1, len(available_insights))
    
    if num_insights > 0:
        selected_insights = random.sample(available_insights, num_insights)
        post_parts.extend(selected_insights)
    
    # Add reflection paragraph if there's room
    if num_paragraphs > 2:
        post_parts.append("\n" + random.choice(reflection_paragraphs[expertise_level]))
    
    # Closing paragraph
    post_parts.append("\n" + random.choice(closing_paragraphs[expertise_level]))
    
    # Join all paragraphs
    full_post = "\n\n".join(post_parts)
    
    # Add hashtags
    if hashtags > 0:
        hashtag_list = [
            f"#{topic.replace(' ', '')}", "#LinkedIn", "#CareerGrowth", "#Innovation", 
            "#Leadership", "#TechTrends", "#FutureOfWork", "#Learning", "#Success",
            "#Inspiration", "#Entrepreneurship", "#Networking", "#ProfessionalDevelopment",
            "#SkillBuilding", "#MindsetMatters"
        ]
        selected_hashtags = random.sample(hashtag_list, min(hashtags, len(hashtag_list)))
        full_post += "\n\n" + " ".join(selected_hashtags)
    
    return full_post


def send_email(recipient_email: str, post_content: str, topic: str, sender_email: str = None, sender_password: str = None) -> tuple:
    """Send the generated post via email"""
    try:
        # Email configuration (you can customize these)
        SENDER_EMAIL = sender_email or st.session_state.get('email_sender', '')
        SENDER_PASSWORD = sender_password or st.session_state.get('email_password', '')
        RECEIVER_EMAIL = recipient_email
        
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            return False, "Email credentials not configured. Please set them in Advanced settings."
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"LinkedIn Post: {topic}"
        message["From"] = SENDER_EMAIL
        message["To"] = RECEIVER_EMAIL
        
        # Create HTML version
        html = f"""\
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
              <h2 style="color: #0ea5e9; margin-bottom: 20px;">Your Generated LinkedIn Post</h2>
              <div style="background-color: #f9fafb; padding: 20px; border-left: 4px solid #0ea5e9; border-radius: 5px; margin-bottom: 20px;">
                <p style="color: #1f2937; line-height: 1.8; white-space: pre-wrap;">{post_content}</p>
              </div>
              <p style="color: #6b7280; font-size: 12px; margin-top: 30px;">
                Generated by LinkedIn Post Generator | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
              </p>
            </div>
          </body>
        </html>
        """
        
        # Create plain text version
        text = f"LinkedIn Post: {topic}\n\n{post_content}"
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
        
        # Send email (Gmail example)
        import smtplib
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message.as_string())
        
        return True, "✅ Email sent successfully!"
    
    except Exception as e:
        return False, f"❌ Failed to send email: {str(e)}"

def get_stats_data():
    """Generate mock statistics data"""
    return {
        'impressions': random.randint(1000, 50000),
        'engagements': random.randint(100, 5000),
        'shares': random.randint(10, 500),
        'comments': random.randint(20, 1000)
    }

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="header-container">
    <h1>🚀 LinkedIn Post Generator</h1>
    <p>Create AI-Powered, Engaging LinkedIn Posts Instantly</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - STATISTICS & QUICK ACTIONS
# ============================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-header">📊 Statistics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Posts Generated</div>
            <div class="stat-value">{st.session_state.total_posts_generated}</div>
            <div class="stat-subtext">This session</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_by_style = sum(st.session_state.post_stats.values())
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Expertise Levels</div>
            <div class="stat-value">{len([v for v in st.session_state.post_stats.values() if v > 0])}</div>
            <div class="stat-subtext">Used levels</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">📈 Expertise Level Breakdown</div>', unsafe_allow_html=True)
    
    for level, count in st.session_state.post_stats.items():
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">{level.capitalize()}</div>
            <div class="stat-value">{count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">🔧 Settings</div>', unsafe_allow_html=True)
    
    api_key_status = st.selectbox(
        "🔐 API Configuration",
        ["✅ Configured", "⚠️ Pending Setup", "❌ Not Available"]
    )
    
    theme_option = st.selectbox(
        "🎨 Theme",
        ["Dark Mode (Default)", "Light Mode", "High Contrast"]
    )
    
    auto_save = st.checkbox("💾 Auto-save generated posts", value=True)

# ============================================================================
# MAIN CONTENT AREA
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs(["✨ Generate Post", "📚 Previous Posts", "📊 Analytics", "⚙️ Advanced"])

# ============================================================================
# TAB 1: GENERATE POST
# ============================================================================
with tab1:
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        topic = st.text_input(
            "📝 Post Topic",
            placeholder="e.g., Artificial Intelligence, Cloud Computing, Leadership...",
            help="What would you like your post to be about?"
        )
    
    with col2:
        expertise_level = st.selectbox(
            "🎓 Your Expertise Level",
            ["Beginner", "Intermediate", "Expert"],
            help="This affects the tone and depth of your post"
        )
    
    col3, col4 = st.columns(2)
    
    with col3:
        tone = st.selectbox(
            "💬 Tone",
            ["Informative", "Conversational", "Bold", "Thoughtful", "Motivational"],
            help="How should the post sound?"
        )
    
    with col4:
        num_paragraphs = st.slider(
            "📄 Number of Paragraphs",
            min_value=2,
            max_value=7,
            value=4,
            help="How many paragraphs should your post have?"
        )
    
    col5, col6 = st.columns(2)
    
    with col5:
        hashtags = st.slider(
            "#️⃣ Number of Hashtags",
            min_value=0,
            max_value=15,
            value=8,
            help="How many hashtags to include?"
        )
    
    with col6:
        add_cta = st.checkbox("🎯 Add Call-to-Action", value=True)
    
    # Email sending option
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.write("📧 **Email Options**")
    
    send_email_option = st.checkbox("📤 Send post via email after generation", value=False)
    
    if send_email_option:
        email_cols = st.columns(2)
        with email_cols[0]:
            recipient_email = st.text_input(
                "📨 Recipient Email",
                placeholder="recipient@example.com",
                help="Where should the post be sent?"
            )
        with email_cols[1]:
            email_note = st.info("💡 Email credentials can be set in Advanced tab")
    
    col_button1, col_button2, col_button3 = st.columns([2, 1, 1])
    
    with col_button1:
        generate_btn = st.button("🚀 Generate Post", use_container_width=True)
    
    with col_button2:
        refresh_btn = st.button("🔄 Refresh", use_container_width=True)
    
    with col_button3:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate Post Logic
    if generate_btn and topic:
        # Progress animation
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Simulate generation with progress
        progress_bar = progress_placeholder.progress(0)
        
        steps = [
            "Analyzing topic...",
            "Crafting opening hook...",
            "Developing insights...",
            "Adding reflections...",
            "Polishing conclusion...",
            "Adding hashtags...",
            "Finalizing post..."
        ]
        
        for i, step in enumerate(steps):
            status_placeholder.info(f"✨ {step}")
            progress = int((i + 1) / len(steps) * 100)
            progress_bar.progress(progress)
            time.sleep(0.4)
        
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()
        
        st.session_state.total_posts_generated += 1
        expertise_lower = expertise_level.lower()
        st.session_state.post_stats[expertise_lower] += 1
        
        # Generate the post
        generated_post = generate_comprehensive_post(
            topic=topic,
            expertise_level=expertise_lower,
            tone=tone.lower(),
            num_paragraphs=num_paragraphs,
            hashtags=hashtags
        )
        
        if add_cta:
            cta_options = [
                "\n\n👉 What are your thoughts? Drop a comment below!",
                "\n\n👉 Let's continue this conversation in the comments!",
                "\n\n👉 Interested? Let's connect and discuss further!",
                "\n\n👉 Share your insights - I'd love to hear your perspective!",
                "\n\n👉 Your feedback helps me grow. Please share your thoughts below!"
            ]
            generated_post += random.choice(cta_options)
        
        st.session_state.generated_posts.append({
            'post': generated_post,
            'topic': topic,
            'expertise_level': expertise_level,
            'tone': tone,
            'paragraphs': num_paragraphs,
            'timestamp': datetime.now(),
            'stats': get_stats_data()
        })
        
        # Success message
        st.success("✅ Post generated successfully!")
        
        # Display the generated post in an enlarged container
        st.markdown(f"""
        <div class="post-container fade-in">
            <h4>📄 Your Generated LinkedIn Post</h4>
            <div class="post-content" style="font-size: 1.05rem; line-height: 1.9;">{generated_post}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col_copy, col_share, col_email = st.columns(3)
        
        with col_copy:
            st.button(
                "📋 Copy to Clipboard",
                key=f"copy_{st.session_state.total_posts_generated}",
                help="Copy this post to paste in LinkedIn"
            )
        
        with col_share:
            st.button(
                "🔗 Share Post",
                key=f"share_{st.session_state.total_posts_generated}",
                help="Share to social media"
            )
        
        with col_email:
            if send_email_option and recipient_email:
                if st.button("📧 Send via Email", key=f"email_{st.session_state.total_posts_generated}"):
                    success, message = send_email(recipient_email, generated_post, topic)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
    
    elif generate_btn and not topic:
        st.warning("⚠️ Please enter a topic to generate a post!")
    
    if clear_btn:
        st.rerun()

# ============================================================================
# TAB 2: PREVIOUS POSTS
# ============================================================================
with tab2:
    if st.session_state.generated_posts:
        st.subheader("📚 Your Generated Posts")
        
        for idx, post_item in enumerate(reversed(st.session_state.generated_posts)):
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Topic:** {post_item['topic']} | **Style:** {post_item['style']}")
                
                with col2:
                    st.caption(f"⏰ {post_item['timestamp'].strftime('%H:%M:%S')}")
                
                with col3:
                    if st.button("👁️ View", key=f"view_{idx}"):
                        st.info(post_item['post'])
                
                st.markdown('---')
    else:
        st.info("📭 No posts generated yet. Start creating in the 'Generate Post' tab!")

# ============================================================================
# TAB 3: ANALYTICS
# ============================================================================
with tab3:
    if st.session_state.generated_posts:
        st.subheader("📊 Post Performance Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_impressions = sum(p['stats']['impressions'] for p in st.session_state.generated_posts)
        total_engagements = sum(p['stats']['engagements'] for p in st.session_state.generated_posts)
        avg_engagement_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Impressions</div>
                <div class="stat-value">{total_impressions:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Engagements</div>
                <div class="stat-value">{total_engagements:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Engagement Rate</div>
                <div class="stat-value">{avg_engagement_rate:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            total_shares = sum(p['stats']['shares'] for p in st.session_state.generated_posts)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">Total Shares</div>
                <div class="stat-value">{total_shares:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Analytics Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Expertise Level Distribution
            level_counts = {}
            for post in st.session_state.generated_posts:
                level = post['expertise_level']
                level_counts[level] = level_counts.get(level, 0) + 1
            
            fig_level = px.pie(
                values=list(level_counts.values()),
                names=list(level_counts.keys()),
                title="📊 Posts by Expertise Level",
                color_discrete_sequence=['#0ea5e9', '#06b6d4', '#10b981']
            )
            fig_level.update_layout(
                paper_bgcolor='rgba(30, 41, 59, 0.8)',
                font_color='#e2e8f0',
                font_family='Inter',
            )
            st.plotly_chart(fig_level, use_container_width=True)
        
        with col2:
            # Engagement Metrics
            metrics_names = ['Impressions', 'Engagements', 'Shares', 'Comments']
            metrics_values = [
                sum(p['stats']['impressions'] for p in st.session_state.generated_posts) // 100,
                sum(p['stats']['engagements'] for p in st.session_state.generated_posts) // 10,
                sum(p['stats']['shares'] for p in st.session_state.generated_posts),
                sum(p['stats']['comments'] for p in st.session_state.generated_posts)
            ]
            
            fig_metrics = go.Figure(data=[
                go.Bar(
                    x=metrics_names,
                    y=metrics_values,
                    marker_color=['#0ea5e9', '#06b6d4', '#10b981', '#f59e0b'],
                    text=metrics_values,
                    textposition='outside',
                )
            ])
            fig_metrics.update_layout(
                title="📈 Engagement Metrics",
                paper_bgcolor='rgba(30, 41, 59, 0.8)',
                plot_bgcolor='rgba(15, 23, 42, 0.5)',
                font_color='#e2e8f0',
                font_family='Inter',
                xaxis_title="",
                yaxis_title="Count",
                showlegend=False,
            )
            st.plotly_chart(fig_metrics, use_container_width=True)
    else:
        st.info("📭 No data to display yet. Generate some posts first!")

# ============================================================================
# TAB 4: ADVANCED SETTINGS
# ============================================================================
with tab4:
    st.subheader("⚙️ Advanced Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.write("🔐 **Email Configuration**")
        st.caption("Configure your email to send generated posts via email")
        
        email_provider = st.selectbox(
            "Email Provider",
            ["Gmail", "Outlook", "Yahoo", "Custom SMTP"]
        )
        
        email_address = st.text_input(
            "📧 Email Address",
            placeholder="your.email@gmail.com",
            help="Your email address"
        )
        
        email_password = st.text_input(
            "🔑 Email Password / App Password",
            type="password",
            placeholder="Your app password",
            help="For Gmail, use 16-character App Password (not your regular password). Generate at https://myaccount.google.com/apppasswords"
        )
        
        if st.button("✅ Save Email Settings"):
            st.session_state.email_sender = email_address
            st.session_state.email_password = email_password
            st.success("✅ Email settings saved!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.write("📝 **Content Preferences**")
        
        max_length = st.slider("Maximum post length (characters)", 500, 5000, 2000)
        min_engagement = st.slider("Minimum engagement score", 1, 10, 5)
        
        auto_format = st.checkbox("🎨 Auto-format posts", value=True)
        include_emojis = st.checkbox("😊 Include emojis in posts", value=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Email Test Section
    st.subheader("📧 Email Test")
    
    test_email_col1, test_email_col2 = st.columns(2)
    
    with test_email_col1:
        test_recipient = st.text_input(
            "Test Recipient Email",
            placeholder="test@example.com",
            help="Send a test email to verify your settings"
        )
    
    with test_email_col2:
        if st.button("🧪 Send Test Email", use_container_width=True):
            if st.session_state.email_sender and st.session_state.email_password:
                with st.spinner("Sending test email..."):
                    test_post = f"This is a test email from LinkedIn Post Generator\n\nGenerated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    success, message = send_email(test_recipient, test_post, "Test Email")
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            else:
                st.error("❌ Please configure email settings first!")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    st.subheader("💾 Data Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export Posts (JSON)", use_container_width=True):
            if st.session_state.generated_posts:
                export_data = json.dumps(st.session_state.generated_posts, default=str, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=export_data,
                    file_name=f"posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No posts to export!")
    
    with col2:
        if st.button("📊 Export Stats (JSON)", use_container_width=True):
            if st.session_state.generated_posts:
                stats_data = {
                    "total_posts": st.session_state.total_posts_generated,
                    "expertise_breakdown": st.session_state.post_stats,
                    "generated_at": datetime.now().isoformat()
                }
                st.download_button(
                    label="Download Stats",
                    data=json.dumps(stats_data, indent=2),
                    file_name=f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            else:
                st.warning("No stats to export!")
    
    with col3:
        if st.button("🗑️ Clear All Data", use_container_width=True):
            if st.warning("⚠️ This will delete all generated posts. Click again to confirm."):
                st.session_state.generated_posts = []
                st.session_state.total_posts_generated = 0
                st.session_state.post_stats = {
                    'beginner': 0,
                    'intermediate': 0,
                    'expert': 0
                }
                st.success("✅ All data cleared!")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem; font-size: 0.9rem;">
    <p>🚀 <strong>LinkedIn Post Generator</strong> | AI-Powered Content Creation</p>
    <p>Built with ❤️ | Version 2.0 | <strong>© 2025 All Rights Reserved</strong></p>
    <p style="margin-top: 1rem; font-size: 0.85rem;">
        💡 Tips: Use specific topics for better results | Experiment with different styles | 
        Save your favorite posts for later use
    </p>
</div>
""", unsafe_allow_html=True)
