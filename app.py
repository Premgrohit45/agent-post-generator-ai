"""
LINKEDIN POST AGENT 9000
AI-Powered Professional Post Creator
A clean, modern Streamlit frontend for LinkedIn post generation
"""

import streamlit as st
import sys
import os
from datetime import datetime
import json
import time
from typing import Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.advanced_agent_orchestrator import LinkedInAgentOrchestrator
    from src.langchain_post_agent import LangChainPostAgent
    from src.email_sender import EmailSender
except ImportError as e:
    st.error(f"🚨 Module Error: {e}")
    st.stop()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="LinkedIn Post Agent 9000",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS & STYLING
# ============================================================================

def load_custom_css():
    """Load custom CSS for futuristic design"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* ==================== GLOBAL STYLES ==================== */
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #0f1b35 50%, #0a0e27 100%);
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Space Grotesk', sans-serif;
        overflow-x: hidden;
    }
    
    /* Animated background particles */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(0, 255, 136, 0.3), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(56, 152, 236, 0.2), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.1), transparent);
        background-size: 200px 200px, 300px 300px, 150px 150px;
        animation: particleFloat 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleFloat {
        from { transform: translateY(0px); }
        to { transform: translateY(-1000px); }
    }
    
    /* ==================== TITLE STYLES ==================== */
    
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 900;
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #00ff88, #00ffff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 255, 136, 0.5);
        letter-spacing: 3px;
        margin: 2rem 0 0.5rem 0;
        animation: titleGlow 3s ease-in-out infinite;
    }
    
    @keyframes titleGlow {
        0%, 100% { filter: drop-shadow(0 0 15px rgba(0, 255, 136, 0.5)); }
        50% { filter: drop-shadow(0 0 30px rgba(0, 255, 255, 0.8)); }
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #b0b8c1;
        letter-spacing: 2px;
        margin-bottom: 2rem;
    }
    
    /* ==================== GLOWING CARDS ==================== */
    
    .glow-card {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.05) 0%, rgba(56, 152, 236, 0.05) 100%);
        border: 2px solid rgba(0, 255, 136, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.1);
    }
    
    .glow-card:hover {
        border-color: #00ff88;
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.3);
        transform: translateY(-5px);
    }
    
    .glow-card-title {
        color: #00ff88;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    /* ==================== STAT BOXES ==================== */
    
    .stat-box {
        background: linear-gradient(135deg, rgba(10, 102, 194, 0.1) 0%, rgba(0, 255, 136, 0.05) 100%);
        border: 1px solid rgba(0, 255, 136, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }
    
    .stat-box:hover {
        border-color: #00ff88;
        box-shadow: 0 0 30px rgba(0, 255, 136, 0.2);
    }
    
    .stat-value {
        font-size: 2.5rem;
        color: #00ff88;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #b0b8c1;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* ==================== FORM ELEMENTS ==================== */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background-color: rgba(15, 27, 53, 0.8) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #00ff88 !important;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.3) !important;
    }
    
    /* ==================== BUTTONS ==================== */
    
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00cccc 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 1rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.3) !important;
        text-transform: uppercase !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 0 40px rgba(0, 255, 136, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) !important;
    }
    
    /* ==================== SIDEBAR STYLES ==================== */
    
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(10, 20, 40, 0.95) 0%, rgba(13, 31, 45, 0.95) 100%) !important;
        border-right: 2px solid rgba(0, 255, 136, 0.3) !important;
    }
    
    [data-testid="stSidebar"] > div {
        background-color: transparent !important;
    }
    
    .sidebar-section {
        background: rgba(0, 255, 136, 0.05);
        border-left: 3px solid #00ff88;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .sidebar-title {
        color: #00ff88;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    
    .sidebar-stat {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        color: #b0b8c1;
        font-size: 0.9rem;
    }
    
    .sidebar-stat-value {
        color: #00ff88;
        font-weight: bold;
    }
    
    /* ==================== LOADING ANIMATION ==================== */
    
    .loading-bar {
        height: 4px;
        background: linear-gradient(90deg, #00ff88, #00ffff, #00ff88);
        border-radius: 2px;
        animation: loading 2s ease-in-out infinite;
        margin: 1rem 0;
    }
    
    @keyframes loading {
        0%, 100% { width: 0%; }
        50% { width: 100%; }
    }
    
    /* ==================== TYPING ANIMATION ==================== */
    
    .typing-text {
        animation: typing 0.05s steps(1, end);
        white-space: pre-wrap;
        word-wrap: break-word;
    }
    
    @keyframes typing {
        from { width: 0; }
    }
    
    /* ==================== STATUS INDICATOR ==================== */
    
    .status-online {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #00ff88;
        border-radius: 50%;
        margin-right: 0.5rem;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 136, 0.8); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 136, 1); }
    }
    
    /* ==================== SUCCESS MESSAGE ==================== */
    
    .success-message {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(56, 152, 236, 0.1) 100%);
        border-left: 4px solid #00ff88;
        padding: 1rem;
        border-radius: 8px;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* ==================== RESPONSIVE ==================== */
    
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .stat-value {
            font-size: 1.8rem;
        }
    }
    
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'posts_generated': 0,
        'emails_sent': 0,
        'current_model': 'Gemini 2.5-Flash',
        'system_status': '🟢 Online',
        'generated_post': None,
        'post_history': [],
        'generation_params': {},
        'sidebar_expanded': True,
        'show_workflow_popup': False,
        'show_email_form': False,
        'default_email': '',
        'auto_send_enabled': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================================
# SIDEBAR COMPONENTS
# ============================================================================

def render_sidebar():
    """Render the working sidebar with stats and controls"""
    
    with st.sidebar:
        st.markdown("### 💼 LINKEDIN POST AGENT")
        st.markdown("---")
        
        # System Status Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">⚙️ System Status</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>Status</span><span class="sidebar-stat-value"><span class="status-online"></span>Online</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>Model</span><span class="sidebar-stat-value">{st.session_state.current_model}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("")
        
        # Statistics Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">📊 Statistics</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>Posts Generated</span><span class="sidebar-stat-value">{st.session_state.posts_generated}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>Emails Sent</span><span class="sidebar-stat-value">{st.session_state.emails_sent}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("")
        
        # Services Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">🔗 Connected Services</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>Web Search</span><span class="sidebar-stat-value">✓</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>Email API</span><span class="sidebar-stat-value">✓</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sidebar-stat"><span>AI Engine</span><span class="sidebar-stat-value">✓</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("---")
        
        # Control Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Stats"):
                st.session_state.posts_generated = 0
                st.session_state.emails_sent = 0
                st.success("✓ Stats reset!")
                st.rerun()
        
        with col2:
            if st.button("📋 View Logs"):
                st.info("System logs would appear here")

# ============================================================================
# MAIN HEADER
# ============================================================================

def render_header():
    """Render the main header with title and subtitle"""
    st.markdown('<h1 class="main-title">LINKEDIN POST AGENT 9000</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">🚀 AI-Powered Professional Post Creator</p>', unsafe_allow_html=True)
    st.markdown("---")

# ============================================================================
# STATISTICS DASHBOARD
# ============================================================================

def render_stats_dashboard():
    """Render the statistics dashboard"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">📝 Posts Generated</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{st.session_state.posts_generated}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">📧 Emails Sent</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{st.session_state.emails_sent}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">🤖 AI Model</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">Gemini</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stat-box">', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">🔌 API Status</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">✓ Active</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# POST GENERATOR FORM
# ============================================================================

def render_generator_form():
    """Render the post generator form"""
    st.markdown('<div class="glow-card">', unsafe_allow_html=True)
    st.markdown('<div class="glow-card-title">✍️ Generate LinkedIn Post</div>', unsafe_allow_html=True)
    
    # Email input at top
    st.markdown("**📧 Default Email (Auto-send after generation)**")
    default_email = st.text_input(
        "Email address for automatic sending",
        placeholder="your@email.com",
        key="default_email_input",
        value=st.session_state.get('default_email', '')
    )
    st.session_state.default_email = default_email
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input(
            "Topic for your post",
            placeholder="e.g., AI in business, productivity tips...",
            key="topic_input"
        )
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            tone = st.selectbox(
                "Tone",
                ["Professional", "Motivational", "Personal", "Educational"],
                key="tone_select"
            )
        
        with col_b:
            length = st.selectbox(
                "Length",
                ["Short", "Medium", "Long"],
                key="length_select"
            )
        
        with col_c:
            audience = st.text_input(
                "Target Audience",
                value="Professionals",
                key="audience_input"
            )
        
        col_x, col_y = st.columns(2)
        
        with col_x:
            add_emojis = st.checkbox("✨ Add emojis", value=True)
        
        with col_y:
            auto_send = st.checkbox("🔄 Auto-send to email", value=True)
            st.session_state.auto_send_enabled = auto_send
    
    with col2:
        st.markdown("### 🎯 Actions")
        
        if st.button("🚀 GENERATE POST", use_container_width=True):
            if not topic:
                st.error("⚠️ Please enter a topic")
            elif auto_send and not default_email:
                st.error("⚠️ Please enter email for auto-send")
            else:
                generate_post(topic, tone, length, audience, add_emojis)
        
        if st.button("💡 AI Suggest Topic", use_container_width=True):
            suggest_topic()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# POST GENERATION LOGIC
# ============================================================================

def generate_post(topic: str, tone: str, length: str, audience: str, add_emojis: bool):
    """Generate a LinkedIn post"""
    
    # Show loading animation
    st.markdown('<div class="loading-bar"></div>', unsafe_allow_html=True)
    
    with st.spinner("🤖 AI Agent is generating your post..."):
        try:
            # Validate inputs
            if not topic or len(topic.strip()) == 0:
                st.error("❌ Please enter a valid topic")
                return
            
            # Map parameters
            tone_lower = tone.lower()
            length_map = {"Short": 1, "Medium": 3, "Long": 5}
            length_paragraphs = length_map.get(length, 3)
            
            # Initialize orchestrator
            try:
                orchestrator = LinkedInAgentOrchestrator()
            except ValueError as e:
                st.error(f"🔑 Configuration Error: {str(e)}")
                st.info("💡 Make sure your .env file has GOOGLE_API_KEY configured")
                return
            except Exception as e:
                st.error(f"⚙️ Initialization Error: {str(e)}")
                return
            
            # Generate post
            try:
                result = orchestrator.orchestrate_post_creation(
                    topic=topic,
                    tone=tone_lower,
                    length=length_paragraphs,
                    target_audience=audience
                )
            except Exception as e:
                st.error(f"🤖 Agent Generation Error: {str(e)}")
                st.info("💡 The AI agent encountered an issue. Please try again or use a different topic.")
                return
            
            # Check result
            if result is None:
                st.error("❌ No result returned from agent")
                return
            
            # Check for success - the orchestrator now always returns the post data
            post_content = result
            
            # Update session state
            st.session_state.posts_generated += 1
            st.session_state.generated_post = post_content
            st.session_state.post_history.append({
                'topic': topic,
                'content': post_content,
                'timestamp': datetime.now().isoformat(),
                'params': {
                    'tone': tone,
                    'length': length,
                    'audience': audience
                }
            })
            st.session_state.generation_params = {
                'topic': topic,
                'tone': tone,
                'length': length,
                'audience': audience
            }
            
            st.success("✓ Post generated successfully!")
            
            # Show workflow popup
            st.session_state.show_workflow_popup = True
            
            # Auto-send email as default process
            if st.session_state.get('auto_send_enabled', True):
                email_to_send = st.session_state.get('default_email', '')
                if email_to_send and '@' in email_to_send:
                    send_email_post(email_to_send, is_auto=True)
                    if st.session_state.emails_sent > 0:
                        st.success(f"📧 Email automatically sent to {email_to_send}")
            
            st.rerun()
        
        except Exception as e:
            st.error(f"🚨 Unexpected Error: {str(e)}")
            st.info(f"📋 Debug info: {type(e).__name__}")

# ============================================================================
# DISPLAY GENERATED POST
# ============================================================================

def display_generated_post():
    """Display the generated post with actions"""
    
    if st.session_state.generated_post:
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        st.markdown('<div class="glow-card-title">✨ Generated Post</div>', unsafe_allow_html=True)
        
        post = st.session_state.generated_post
        post_text = post.get('content', 'No content')
        
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 136, 0.05);
            border-left: 3px solid #00ff88;
            padding: 1.5rem;
            border-radius: 10px;
            white-space: pre-wrap;
            word-wrap: break-word;
            color: #ffffff;
            font-size: 1rem;
            line-height: 1.6;
        ">{post_text}</div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        
        # Action buttons
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("📋 Copy Post"):
                st.write(post_text)
                st.success("✓ Copy the text above")
        
        with col2:
            if st.button("💾 Save as TXT"):
                download_content(post_text, "post.txt", "text/plain")
                st.success("✓ Download started")
        
        with col3:
            if st.button("📄 Save as MD"):
                download_content(post_text, "post.md", "text/markdown")
                st.success("✓ Download started")
        
        with col4:
            if st.button("🔄 Regenerate"):
                params = st.session_state.generation_params
                generate_post(
                    params['topic'],
                    params['tone'],
                    params['length'],
                    params['audience'],
                    True
                )
        
        with col5:
            if st.button("📧 Send Email"):
                st.session_state.show_email_form = True
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show generation info
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        st.markdown('<div class="glow-card-title">ℹ️ Generation Details</div>', unsafe_allow_html=True)
        
        params = st.session_state.generation_params
        st.markdown(f"""
        - **Topic**: {params.get('topic', 'N/A')}
        - **Tone**: {params.get('tone', 'N/A')}
        - **Length**: {params.get('length', 'N/A')}
        - **Audience**: {params.get('audience', 'N/A')}
        - **Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# WORKFLOW POPUP - Shows Generation Process & Tools
# ============================================================================

def render_workflow_popup():
    """Display workflow and tools used in generation"""
    
    if st.session_state.generated_post and st.session_state.show_workflow_popup:
        with st.container():
            st.markdown("""
            <style>
            .workflow-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 999;
                animation: fadeIn 0.3s ease-in;
            }
            
            .workflow-content {
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                border: 2px solid #00ff88;
                border-radius: 15px;
                padding: 2rem;
                max-width: 600px;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 0 40px rgba(0, 255, 136, 0.5);
                animation: slideUp 0.4s ease-out;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideUp {
                from { 
                    opacity: 0;
                    transform: translateY(50px);
                }
                to { 
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Modal background
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                border: 2px solid #00ff88;
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 0 40px rgba(0, 255, 136, 0.5);
            ">
            """, unsafe_allow_html=True)
            
            # Header
            st.markdown("""
            <div style="
                text-align: center;
                margin-bottom: 1.5rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid rgba(0, 255, 136, 0.3);
            ">
                <h2 style="
                    color: #00ff88;
                    font-size: 1.8rem;
                    margin: 0;
                    text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
                ">🚀 Generation Workflow</h2>
                <p style="color: #888; margin-top: 0.5rem;">AI Agent Process & Technologies Used</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Get workflow details
            post = st.session_state.generated_post
            metadata = post.get('agent_metadata', {})
            orchestration = post.get('orchestration_metadata', {})
            
            # Workflow Steps
            st.markdown("### 📋 Workflow Steps", unsafe_allow_html=True)
            
            steps = [
                ("1️⃣ Input Processing", "Topic, tone, length, and audience validated"),
                ("2️⃣ LangChain Agent Init", "ReAct agent initialized with tools"),
                ("3️⃣ Research Phase", "Web search & trending topics analyzed"),
                ("4️⃣ Content Generation", "AI generates professional post content"),
                ("5️⃣ Quality Check", "Post validated and formatted"),
                ("6️⃣ Email Dispatch", "Post automatically sent to recipient"),
            ]
            
            for step_title, step_desc in steps:
                st.markdown(f"""
                <div style="
                    background: rgba(0, 255, 136, 0.1);
                    border-left: 3px solid #00ff88;
                    padding: 0.8rem;
                    margin-bottom: 0.8rem;
                    border-radius: 5px;
                ">
                    <strong style="color: #00ff88;">{step_title}</strong><br>
                    <span style="color: #ccc; font-size: 0.9rem;">{step_desc}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Technologies Used
            st.markdown("### 🛠️ Technologies & Tools", unsafe_allow_html=True)
            
            tech_items = [
                ("🤖 AI Model", "Google Gemini 2.5-Flash"),
                ("🔗 Agent Framework", "LangChain ReAct Agent"),
                ("📚 Language Library", "LangGraph (v1.0+)"),
                ("🔍 Search Tool", "Web Search Integration"),
                ("📊 Data Analysis", "Statistics & Trending Topics"),
                ("📧 Email Service", "Gmail SMTP Backend"),
            ]
            
            col_a, col_b = st.columns(2)
            for idx, (tech_name, tech_desc) in enumerate(tech_items):
                if idx % 2 == 0:
                    with col_a:
                        st.markdown(f"""
                        <div style="
                            background: rgba(0, 188, 212, 0.15);
                            padding: 1rem;
                            border-radius: 8px;
                            margin-bottom: 0.8rem;
                            border: 1px solid rgba(0, 188, 212, 0.3);
                        ">
                            <strong style="color: #00bcd4;">{tech_name}</strong><br>
                            <span style="color: #aaa; font-size: 0.85rem;">{tech_desc}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    with col_b:
                        st.markdown(f"""
                        <div style="
                            background: rgba(0, 188, 212, 0.15);
                            padding: 1rem;
                            border-radius: 8px;
                            margin-bottom: 0.8rem;
                            border: 1px solid rgba(0, 188, 212, 0.3);
                        ">
                            <strong style="color: #00bcd4;">{tech_name}</strong><br>
                            <span style="color: #aaa; font-size: 0.85rem;">{tech_desc}</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Agent Metadata
            st.markdown("### ⚡ Agent Details", unsafe_allow_html=True)
            
            details = [
                ("Framework", metadata.get('framework', 'LangChain ReAct Agent')),
                ("Model", metadata.get('model', 'Gemini 2.5-Flash')),
                ("Agent Type", metadata.get('agent_type', 'ReAct (Reasoning + Acting)')),
                ("Tools Available", str(len(metadata.get('tools_available', []))),),
            ]
            
            for detail_name, detail_value in details:
                st.markdown(f"""
                <div style="
                    display: flex;
                    justify-content: space-between;
                    padding: 0.6rem 0;
                    border-bottom: 1px solid rgba(0, 255, 136, 0.2);
                ">
                    <span style="color: #888;">{detail_name}:</span>
                    <strong style="color: #00ff88;">{detail_value}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Action Buttons
            st.markdown("### 📌 Actions", unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("✅ Close Popup", use_container_width=True, key="close_workflow"):
                    st.session_state.show_workflow_popup = False
                    st.rerun()
            
            with col_btn2:
                if st.button("📧 Send Email", use_container_width=True, key="send_from_popup"):
                    st.session_state.show_email_form = True
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# EMAIL SENDING SECTION
# ============================================================================

def render_email_section():
    """Render email sending section (only after post generation)"""
    
    if st.session_state.generated_post:
        st.markdown('<div class="glow-card">', unsafe_allow_html=True)
        st.markdown('<div class="glow-card-title">📧 Send via Email</div>', unsafe_allow_html=True)
        
        recipient_email = st.text_input(
            "Recipient Email",
            placeholder="user@example.com",
            key="recipient_email"
        )
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if st.button("Send Email", use_container_width=True, key="send_btn"):
                if not recipient_email or '@' not in recipient_email:
                    st.error("⚠️ Please enter a valid email")
                else:
                    send_email_post(recipient_email)
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_email_form = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def download_content(content: str, filename: str, mime_type: str):
    """Helper to download content"""
    st.download_button(
        label=f"Download {filename.split('.')[-1].upper()}",
        data=content,
        file_name=filename,
        mime=mime_type
    )

def suggest_topic():
    """AI suggest a topic"""
    suggestions = [
        "How AI is transforming the workplace in 2025",
        "5 productivity hacks every professional needs",
        "The future of remote work",
        "Building a personal brand on LinkedIn",
        "Essential skills for the modern workforce"
    ]
    import random
    suggestion = random.choice(suggestions)
    st.info(f"💡 Suggested topic: **{suggestion}**")

def send_email_post(recipient: str, is_auto: bool = False):
    """Send generated post via email"""
    try:
        email_sender = EmailSender()
        post = st.session_state.generated_post
        
        if not recipient or '@' not in recipient:
            if not is_auto:
                st.error("⚠️ Please enter a valid email")
            return False
        
        success, message = email_sender.send_post({
            'content': post.get('content', ''),
            'subject': f"LinkedIn Post: {st.session_state.generation_params.get('topic', 'Generated Post')}"
        }, recipient)
        
        if success:
            st.session_state.emails_sent += 1
            if not is_auto:
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.markdown('### ✅ Email Sent Successfully!')
                st.markdown(f'Post sent to: **{recipient}**')
                st.markdown('</div>', unsafe_allow_html=True)
            return True
        else:
            if not is_auto:
                st.error(f"❌ Failed to send: {message}")
            return False
    
    except Exception as e:
        if not is_auto:
            st.error(f"🚨 Error: {str(e)}")
        return False

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application"""
    load_custom_css()
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render header
    render_header()
    
    # Render stats dashboard
    render_stats_dashboard()
    
    st.markdown("")
    st.markdown("")
    
    # Render generator form
    render_generator_form()
    
    st.markdown("")
    
    # Display generated post if exists
    if st.session_state.generated_post:
        display_generated_post()
        st.markdown("")
        
        # Show workflow popup
        if st.session_state.get('show_workflow_popup', False):
            render_workflow_popup()
        
        # Email section
        if st.session_state.get('show_email_form', False):
            render_email_section()

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
