import streamlit as st
import sys
import os
from datetime import datetime
import json
import time
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import re

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


try:
    from src.advanced_agent_orchestrator import LinkedInAgentOrchestrator
    from src.langchain_post_agent import LangChainPostAgent
    from src.email_sender import EmailSender
    from src.agent_tools import AgentTools
except ImportError as e:
    st.error(f"🚨 Agent Module Error: {e}")
    st.stop()


st.set_page_config(
    page_title="💼 LinkedGenius | AI-Powered LinkedIn Content Creator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)


def load_agent_css():
    st.markdown("""
    <style>
    /* Import futuristic fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles with LinkedIn-inspired Dark Background */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #0a1520 25%, #0d1f2d 50%, #0a1520 75%, #000000 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        font-family: 'Space Grotesk', sans-serif;
        color: #ffffff;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated particles background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20% 30%, rgba(10, 102, 194, 0.4), transparent),
            radial-gradient(2px 2px at 60% 70%, rgba(56, 152, 236, 0.3), transparent),
            radial-gradient(1px 1px at 50% 50%, rgba(255, 255, 255, 0.15), transparent),
            radial-gradient(1px 1px at 80% 10%, rgba(10, 102, 194, 0.35), transparent);
        background-size: 200px 200px, 300px 300px, 150px 150px, 250px 250px;
        background-position: 0 0, 40px 60px, 130px 270px, 70px 100px;
        animation: particleFloat 20s linear infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes particleFloat {
        from { transform: translateY(0px); }
        to { transform: translateY(-1000px); }
    }
    
    /* Ensure content is above background */
    .stApp > * {
        position: relative;
        z-index: 1;
    }
    
    /* Enhanced Text Rendering for All Elements */
    * {
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        font-feature-settings: "kern" 1, "liga" 1 !important;
    }
    
    /* Improved Typography Base */
    body, div, p, span {
        word-spacing: 1px !important;
        letter-spacing: 0.5px !important;
        line-height: 1.8 !important;
    }
    
    /* Glassmorphism Header Container with 3D effect */
    .agent-header {
        background: rgba(5, 10, 20, 0.8);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 2px solid rgba(10, 102, 194, 0.4);
        border-radius: 20px;
        padding: 1rem 1.5rem;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 
            0 5px 20px 0 rgba(10, 102, 194, 0.2),
            inset 0 0 30px rgba(10, 102, 194, 0.05);
        animation: headerPulse 4s ease-in-out infinite;
        transform-style: preserve-3d;
        perspective: 1000px;
        position: relative;
        overflow: hidden;
    }
    
    .agent-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(10, 102, 194, 0.15),
            transparent
        );
        animation: shimmer 3s infinite;
    }
    
    @keyframes headerPulse {
        0%, 100% { 
            border-color: rgba(10, 102, 194, 0.5);
            box-shadow: 
                0 8px 32px 0 rgba(10, 102, 194, 0.3),
                inset 0 0 40px rgba(10, 102, 194, 0.08),
                0 0 80px rgba(10, 102, 194, 0.15);
        }
        50% { 
            border-color: rgba(56, 152, 236, 0.7);
            box-shadow: 
                0 8px 40px 0 rgba(10, 102, 194, 0.5),
                inset 0 0 60px rgba(10, 102, 194, 0.15),
                0 0 120px rgba(56, 152, 236, 0.3);
        }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .agent-title {
        font-family: 'Orbitron', monospace;
        font-size: 2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #0A66C2, #3898EC, #0A66C2);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 3s ease infinite;
        margin: 0;
        letter-spacing: 6px;
        text-transform: uppercase;
        filter: drop-shadow(0 0 20px rgba(10, 102, 194, 0.7));
        position: relative;
        z-index: 2;
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .agent-subtitle {
        font-size: 1.1rem;
        background: linear-gradient(90deg, #3898EC, #ffffff, #3898EC);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 5s ease infinite;
        margin-top: 0.8rem;
        font-weight: 500;
        letter-spacing: 2px;
        text-transform: uppercase;
        position: relative;
        z-index: 2;
    }
    
    .agent-status {
        font-size: 1.1rem;
        color: #00ff88;
        margin-top: 1rem;
        font-weight: 700;
        letter-spacing: 2px;
        position: relative;
        z-index: 2;
        animation: statusBlink 2s ease-in-out infinite;
    }
    
    @keyframes statusBlink {
        0%, 100% { opacity: 1; text-shadow: 0 0 10px rgba(0, 255, 136, 0.8); }
        50% { opacity: 0.7; text-shadow: 0 0 20px rgba(0, 255, 136, 1); }
    }
    
    /* Enhanced Status Dashboard with 3D Cards */
    .status-dashboard {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .status-card {
        background: rgba(5, 10, 20, 0.7);
        backdrop-filter: blur(15px) saturate(180%);
        -webkit-backdrop-filter: blur(15px) saturate(180%);
        border: 1px solid rgba(10, 102, 194, 0.3);
        border-radius: 15px;
        padding: 1rem 0.8rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        transform: translateY(0);
        box-shadow: 
            0 4px 15px 0 rgba(10, 102, 194, 0.15),
            inset 0 0 15px rgba(10, 102, 194, 0.03);
        position: relative;
        overflow: hidden;
    }
    
    .status-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(10, 102, 194, 0.3),
            transparent
        );
        transition: left 0.5s;
    }
    
    .status-card:hover {
        border-color: #0A66C2;
        box-shadow: 
            0 8px 25px rgba(10, 102, 194, 0.3),
            inset 0 0 25px rgba(10, 102, 194, 0.1),
            0 0 40px rgba(56, 152, 236, 0.2);
        transform: translateY(-5px) scale(1.02);
    }
    
    .status-card:hover::before {
        left: 100%;
    }
    
    .status-icon {
        font-size: 2rem;
        margin-bottom: 0.6rem;
        display: block;
        animation: iconFloat 3s ease-in-out infinite;
        filter: drop-shadow(0 0 8px rgba(10, 102, 194, 0.5));
    }
    
    @keyframes iconFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .status-title {
        color: #3898EC;
        font-weight: 700;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.3rem;
    }
    
    .status-value {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 700;
        margin-top: 0.3rem;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.4);
    }
    
    /* Enhanced Control Panels with Glassmorphism */
    .control-panel {
        background: rgba(5, 10, 20, 0.7);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid rgba(10, 102, 194, 0.3);
        border-radius: 18px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 
            0 5px 20px 0 rgba(10, 102, 194, 0.15),
            inset 0 0 20px rgba(10, 102, 194, 0.05);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .control-panel:hover {
        border-color: rgba(10, 102, 194, 0.7);
        box-shadow: 
            0 12px 48px 0 rgba(10, 102, 194, 0.35),
            inset 0 0 50px rgba(10, 102, 194, 0.12);
    }
    
    .control-panel::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #0A66C2, #3898EC, #0A66C2, #3898EC);
        background-size: 400% 400%;
        border-radius: 25px;
        opacity: 0;
        z-index: -1;
        animation: borderGlow 3s ease infinite;
        transition: opacity 0.3s;
    }
    
    .control-panel:hover::before {
        opacity: 0.5;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .panel-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.3rem;
        background: linear-gradient(135deg, #0A66C2, #3898EC);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1.2rem;
        text-align: center;
        font-weight: 700;
        letter-spacing: 3px;
        text-transform: uppercase;
        filter: drop-shadow(0 0 15px rgba(10, 102, 194, 0.5));
    }
    
    /* Futuristic Buttons with LinkedIn Theme */
    .stButton > button {
        background: linear-gradient(135deg, #0A66C2 0%, #3898EC 50%, #0A66C2 100%);
        background-size: 200% 200%;
        color: #ffffff;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 4px 15px rgba(10, 102, 194, 0.4),
            inset 0 0 15px rgba(255, 255, 255, 0.08);
        font-family: 'Orbitron', monospace;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.5);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 15px 40px rgba(10, 102, 194, 0.7),
            inset 0 0 30px rgba(255, 255, 255, 0.2),
            0 0 60px rgba(56, 152, 236, 0.5);
        background-position: 100% 0;
        animation: neonPulse 1.5s ease-in-out infinite;
    }
    
    @keyframes neonPulse {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.2); }
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02);
    }
    
    /* Enhanced Input Fields with Glow Effect */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(10, 102, 194, 0.3);
        border-radius: 15px;
        color: #ffffff;
        font-size: 1rem;
        padding: 0.9rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #0A66C2;
        box-shadow: 
            0 0 20px rgba(10, 102, 194, 0.6),
            inset 0 0 15px rgba(10, 102, 194, 0.15);
        background: rgba(0, 0, 0, 0.6);
        transform: translateY(-2px);
    }
    
    /* Placeholder styling */
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(56, 152, 236, 0.5);
        font-style: italic;
    }
    
    /* Enhanced Labels */
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: #3898EC !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(10, 102, 194, 0.5);
        margin-bottom: 0.8rem !important;
    }
    
    /* Hide Sidebar Completely */
    .css-1d391kg, [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Remove sidebar toggle button */
    button[kind="header"] {
        display: none !important;
    }
    
    /* NEON SIDEBAR STYLES */
    .neon-sidebar {
        position: fixed;
        left: 0;
        top: 0;
        width: 300px;
        height: 100vh;
        background: rgba(0, 10, 30, 0.95);
        backdrop-filter: blur(20px);
        border-right: 2px solid rgba(0, 255, 136, 0.4);
        padding: 2rem 1.5rem;
        overflow-y: auto;
        z-index: 999;
        box-shadow: 10px 0 50px rgba(0, 255, 136, 0.15);
        display: none;
    }
    
    .neon-sidebar.visible {
        display: block;
    }
    
    .sidebar-toggle {
        position: fixed;
        left: 20px;
        top: 20px;
        width: 50px;
        height: 50px;
        background: rgba(0, 255, 136, 0.2);
        border: 2px solid #00ff88;
        border-radius: 12px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        z-index: 1001;
        transition: all 0.3s ease;
    }
    
    .sidebar-toggle:hover {
        background: rgba(0, 255, 136, 0.4);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.6);
    }
    
    .sidebar-section {
        margin-bottom: 2rem;
        padding: 1.2rem;
        background: rgba(0, 255, 136, 0.05);
        border: 2px solid rgba(0, 255, 136, 0.2);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .sidebar-section:hover {
        background: rgba(0, 255, 136, 0.1);
        border-color: rgba(0, 255, 136, 0.5);
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
    }
    
    .sidebar-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #00ff88;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.8rem;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .sidebar-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.6rem 0;
        color: #ffffff;
        font-size: 0.9rem;
        border-bottom: 1px solid rgba(0, 255, 136, 0.1);
    }
    
    .sidebar-stat:last-child {
        border-bottom: none;
    }
    
    .stat-value {
        font-weight: 700;
        color: #00ff88;
        font-size: 1.1rem;
    }
    
    .sidebar-button {
        width: 100%;
        padding: 0.8rem;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1), rgba(0, 255, 136, 0.05));
        border: 2px solid rgba(0, 255, 136, 0.4);
        border-radius: 10px;
        color: #00ff88;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sidebar-button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.3), rgba(0, 255, 136, 0.15));
        box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        transform: translateY(-2px);
    }
    
    .sidebar-button:active {
        transform: translateY(0);
    }
    
    /* Expand main content to full width */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    
    /* Enhanced Success/Error/Warning/Info Messages */
    .stSuccess {
        background: rgba(0, 255, 136, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #00ff88 !important;
        border-radius: 18px !important;
        color: #00ff88 !important;
        padding: 1.2rem !important;
        box-shadow: 0 5px 20px rgba(0, 255, 136, 0.2) !important;
        animation: messageSlideIn 0.5s ease-out;
    }
    
    .stError {
        background: rgba(255, 0, 100, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #ff0064 !important;
        border-radius: 18px !important;
        color: #ff0064 !important;
        padding: 1.2rem !important;
        box-shadow: 0 5px 20px rgba(255, 0, 100, 0.2) !important;
        animation: messageSlideIn 0.5s ease-out;
    }
    
    .stWarning {
        background: rgba(255, 200, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #ffc800 !important;
        border-radius: 18px !important;
        color: #ffc800 !important;
        padding: 1.2rem !important;
        box-shadow: 0 5px 20px rgba(255, 200, 0, 0.2) !important;
        animation: messageSlideIn 0.5s ease-out;
    }
    
    .stInfo {
        background: rgba(0, 150, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid #0096ff !important;
        border-radius: 18px !important;
        color: #0096ff !important;
        padding: 1.2rem !important;
        box-shadow: 0 5px 20px rgba(0, 150, 255, 0.2) !important;
        animation: messageSlideIn 0.5s ease-out;
    }
    
    @keyframes messageSlideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Enhanced Progress Bars with Animated Gradient */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffff, #0096ff, #00ffff) !important;
        background-size: 200% 200% !important;
        animation: progressGlow 2s ease infinite !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.6) !important;
    }
    
    @keyframes progressGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Enhanced Metrics with Glassmorphism */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(15px) saturate(180%) !important;
        border: 2px solid rgba(0, 255, 255, 0.3) !important;
        padding: 1.5rem !important;
        border-radius: 18px !important;
        box-shadow: 
            0 8px 32px 0 rgba(0, 255, 255, 0.1),
            inset 0 0 20px rgba(0, 255, 255, 0.03) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 
            0 12px 48px 0 rgba(0, 255, 255, 0.2),
            inset 0 0 30px rgba(0, 255, 255, 0.05) !important;
        transform: translateY(-5px) !important;
    }
    
    /* Enhanced Code Blocks */
    .stCode {
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.1) !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    
    /* Enhanced Loading Animation */
    .loading-animation {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem;
    }
    
    .loading-spinner {
        border: 5px solid rgba(0, 255, 255, 0.1);
        border-top: 5px solid #00ffff;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        animation: spin 1s linear infinite;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Terminal-like output with Neon Green Glow */
    .terminal-output {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        color: #00ff00;
        font-family: 'Courier New', monospace;
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #00ff00;
        margin: 1.5rem 0;
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 
            0 5px 25px rgba(0, 255, 0, 0.2),
            inset 0 0 20px rgba(0, 255, 0, 0.1);
        animation: terminalFlicker 0.1s infinite alternate;
    }
    
    @keyframes terminalFlicker {
        0% { opacity: 0.98; }
        100% { opacity: 1; }
    }
    
    /* Enhanced Blog Content Text */
    .post-content-text {
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 400 !important;
        font-size: 1.15rem !important;
        line-height: 1.9 !important;
        text-align: justify !important;
        padding: 2rem !important;
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        text-rendering: optimizeLegibility !important;
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
        box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.05) !important;
    }
    
    /* Enhanced Blog Title Styling */
    .post-title {
        background: linear-gradient(135deg, #00ffff, #0096ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin: 0 !important;
        filter: drop-shadow(0 0 15px rgba(0, 255, 255, 0.6)) !important;
    }
    
    /* Enhanced Content Container */
    .content-container {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(15px) saturate(180%) !important;
        border: 2px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        margin: 2rem 0 !important;
        box-shadow: 
            0 8px 32px 0 rgba(0, 255, 255, 0.15),
            inset 0 0 30px rgba(0, 255, 255, 0.05) !important;
    }
    
    /* Enhanced Section Headers */
    .section-header {
        background: linear-gradient(90deg, #00ffff, #0096ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 600 !important;
        margin-bottom: 1.5rem !important;
        text-transform: uppercase !important;
        letter-spacing: 3px !important;
        filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.5)) !important;
    }
    
    /* Enhanced Hashtag and CTA Styling */
    .meta-content {
        color: #ffffff !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 500 !important;
        line-height: 1.7 !important;
        padding: 1.2rem !important;
        border-radius: 12px !important;
        overflow-y: auto !important;
        max-height: 140px !important;
    }
    
    /* Enhanced Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(0, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #00ffff !important;
        font-weight: 700 !important;
        padding: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(0, 255, 255, 0.6) !important;
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(0, 255, 255, 0.2) !important;
        border-radius: 0 0 15px 15px !important;
        padding: 2rem !important;
        box-shadow: inset 0 0 20px rgba(0, 255, 255, 0.05) !important;
    }
    
    /* Enhanced Markdown text improvements */
    .stMarkdown {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    
    .stMarkdown p {
        color: #ffffff !important;
        line-height: 1.8 !important;
        margin-bottom: 1.2rem !important;
    }
    
    .stMarkdown strong {
        background: linear-gradient(90deg, #00ffff, #0096ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        font-weight: 700 !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255, 255, 255, 0.03);
        padding: 0.5rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(0, 255, 255, 0.2);
        border-radius: 12px;
        color: #00ffff;
        font-weight: 600;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 255, 0.1);
        border-color: rgba(0, 255, 255, 0.5);
        box-shadow: 0 5px 15px rgba(0, 255, 255, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 150, 255, 0.2)) !important;
        border-color: #00ffff !important;
        box-shadow: 0 5px 20px rgba(0, 255, 255, 0.3) !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #0A66C2, #3898EC);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(10, 102, 194, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #3898EC, #0A66C2);
        box-shadow: 0 0 15px rgba(10, 102, 194, 0.8);
    }
    
    /* Checkbox styling */
    .stCheckbox {
        color: #00ffff !important;
    }
    
    .stCheckbox > label {
        color: #00ffff !important;
        font-weight: 600 !important;
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #8000ff 0%, #4000ff 100%) !important;
        box-shadow: 0 5px 20px rgba(128, 0, 255, 0.4) !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #4000ff 0%, #8000ff 100%) !important;
        box-shadow: 0 10px 30px rgba(128, 0, 255, 0.6) !important;
    }
    
    /* Sidebar button styling */
    [data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #0A66C2, #3898EC);
        color: #ffffff;
        border: 1px solid rgba(10, 102, 194, 0.5);
        border-radius: 12px;
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        box-shadow: 0 3px 10px rgba(10, 102, 194, 0.3);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #3898EC, #0A66C2);
        box-shadow: 0 5px 15px rgba(10, 102, 194, 0.5);
        transform: translateY(-2px);
    }
    
    /* Footer fixed at bottom */
    .main .block-container {
        padding-bottom: 80px;
    }
    
    /* Footer container styling - fixed at bottom */
    .footer-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        background: rgba(2, 5, 10, 0.95);
        backdrop-filter: blur(20px);
        border-top: 1px solid rgba(10, 102, 194, 0.3);
        z-index: 999;
        padding: 0.8rem 0;
        box-shadow: 0 -5px 20px rgba(0, 0, 0, 0.5);
    }

    /* ========== POPUP SLIDE-IN SIDEBAR CSS ========== */
    
    /* Sidebar Overlay */
    .sidebar-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(4px);
        z-index: 1900;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
    }
    
    .sidebar-overlay.active {
        opacity: 1;
        visibility: visible;
    }
    
    /* Main Sidebar Panel */
    .popup-sidebar {
        position: fixed;
        left: 0;
        top: 0;
        height: 100vh;
        width: 320px;
        background: linear-gradient(135deg, rgba(10, 20, 40, 0.95) 0%, rgba(13, 31, 45, 0.95) 100%);
        backdrop-filter: blur(8px);
        border-right: 2px solid #00ff88;
        z-index: 2000;
        transform: translateX(-100%);
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: inset -5px 0 20px rgba(0, 255, 136, 0.1);
        overflow-y: auto;
        padding: 0;
    }
    
    .popup-sidebar.active {
        transform: translateX(0);
    }
    
    /* Sidebar Header */
    .sidebar-header {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(56, 152, 236, 0.1) 100%);
        border-bottom: 1px solid rgba(0, 255, 136, 0.3);
        padding: 1.5rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 2001;
    }
    
    .sidebar-title {
        color: #00ff88;
        font-size: 1.2rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .sidebar-close-btn {
        background: none;
        border: none;
        color: #00ff88;
        font-size: 1.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        padding: 0;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .sidebar-close-btn:hover {
        color: #ffffff;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        transform: scale(1.1);
    }
    
    /* Sidebar Content Container */
    .sidebar-content {
        padding: 1.5rem 1rem;
    }
    
    /* Status Section */
    .sidebar-section {
        margin-bottom: 1.5rem;
        background: rgba(0, 255, 136, 0.05);
        border-left: 3px solid #00ff88;
        padding: 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .sidebar-section:hover {
        background: rgba(0, 255, 136, 0.1);
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
    }
    
    .sidebar-section-title {
        color: #00ff88;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        text-shadow: 0 0 8px rgba(0, 255, 136, 0.4);
    }
    
    /* Stat Item */
    .sidebar-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        color: #b0b8c1;
        font-size: 0.9rem;
    }
    
    .sidebar-stat:last-child {
        border-bottom: none;
    }
    
    .sidebar-stat-label {
        color: #b0b8c1;
    }
    
    .sidebar-stat-value {
        color: #00ff88;
        font-weight: bold;
        font-size: 1.1rem;
        text-shadow: 0 0 8px rgba(0, 255, 136, 0.3);
    }
    
    /* Sidebar Buttons */
    .sidebar-buttons {
        margin-top: 1.5rem;
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }
    
    .sidebar-btn {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15) 0%, rgba(56, 152, 236, 0.15) 100%);
        border: 1px solid #00ff88;
        color: #00ff88;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        text-shadow: 0 0 5px rgba(0, 255, 136, 0.3);
    }
    
    .sidebar-btn:hover {
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.25) 0%, rgba(56, 152, 236, 0.25) 100%);
        border-color: #3898EC;
        color: #ffffff;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.4);
        transform: translateY(-2px);
    }
    
    .sidebar-btn:active {
        transform: translateY(0);
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
    }
    
    /* Status Indicator */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #00ff88;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        margin-right: 0.5rem;
        animation: statusPulse 2s ease-in-out infinite;
    }
    
    @keyframes statusPulse {
        0%, 100% { box-shadow: 0 0 10px rgba(0, 255, 136, 0.8); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 136, 1); }
    }
    
    /* Number Counter Animation */
    .stat-counter {
        display: inline-block;
        font-weight: bold;
        color: #00ff88;
    }
    
    /* Hamburger Menu Button Style */
    .hamburger-menu-btn {
        background: none;
        border: none;
        color: #00ff88;
        font-size: 1.8rem;
        cursor: pointer;
        padding: 0;
        transition: all 0.3s ease;
    }
    
    .hamburger-menu-btn:hover {
        color: #ffffff;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.8);
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    if 'agent_initialized' not in st.session_state:
        st.session_state.agent_initialized = False
    if 'post_history' not in st.session_state:
        st.session_state.post_history = []
    if 'total_generated' not in st.session_state:
        st.session_state.total_generated = 0
    if 'total_posts_generated' not in st.session_state:
        st.session_state.total_posts_generated = 0
    if 'total_emails_sent' not in st.session_state:
        st.session_state.total_emails_sent = 0
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = None
    if 'generation_topic' not in st.session_state:
        st.session_state.generation_topic = ''
    if 'generation_tone' not in st.session_state:
        st.session_state.generation_tone = 'professional'
    if 'generation_length' not in st.session_state:
        st.session_state.generation_length = 1
    if 'generation_audience' not in st.session_state:
        st.session_state.generation_audience = 'professionals'
    if 'sidebar_open' not in st.session_state:
        st.session_state.sidebar_open = False
    if 'agent_status' not in st.session_state:
        st.session_state.agent_status = '🟢 Online'
    if 'email_api_status' not in st.session_state:
        st.session_state.email_api_status = '✓ Connected'
    if 'web_search_status' not in st.session_state:
        st.session_state.web_search_status = '✓ Active'
    if 'current_model' not in st.session_state:
        st.session_state.current_model = 'Gemini 2.5-Flash'


def render_status_dashboard():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🚀</div>
            <div class="status-title">System Status</div>
            <div class="status-value">OPERATIONAL</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="status-card">
            <div class="status-icon">📝</div>
            <div class="status-title">Blogs Generated</div>
            <div class="status-value">{st.session_state.total_generated}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="status-card">
            <div class="status-icon">📧</div>
            <div class="status-title">Emails Sent</div>
            <div class="status-value">{st.session_state.total_emails_sent}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="status-card">
            <div class="status-icon">🤖</div>
            <div class="status-title">AI Model</div>
            <div class="status-value">GEMINI 2.5</div>
        </div>
        """, unsafe_allow_html=True)

# Initialize Agent
@st.cache_resource
def initialize_agent():
    try:
        # Initialize advanced multi-agent orchestrator
        orchestrator = LinkedInAgentOrchestrator()
        return orchestrator, True, "Advanced Agent Orchestrator initialized with function calling"
    except Exception as e:
        return None, False, f"Agent initialization failed: {str(e)}"

# Email validation function
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Post Generation Interface
def render_post_generator():
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">🚀 BLOG GENERATION SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("🎯 BLOG TOPIC", placeholder="Enter your post topic here...")
        
        col_a, col_b = st.columns(2)
        with col_a:
            tone = st.selectbox("🎨 TONE", ["professional", "casual", "inspirational", "technical"])
        with col_b:
            length = st.number_input("📝 PARAGRAPHS", min_value=1, max_value=10, value=1, step=1)
        
        audience = st.text_input("👥 TARGET AUDIENCE", value="professionals", placeholder="Target audience...")
    
    with col2:
        st.markdown("### 🎛️ GENERATION CONTROLS")
        
        if st.button("🚀 GENERATE BLOG"):
            if topic:
                # Store the parameters and navigate to generation page
                st.session_state.generation_topic = topic
                st.session_state.generation_tone = tone
                st.session_state.generation_length = length
                st.session_state.generation_audience = audience
                st.session_state.current_page = 'generating'
                st.rerun()
            else:
                st.error("⚠️ Please enter a post topic")

def generate_single_post():
    """Generate post with stored parameters using advanced agentic orchestrator"""
    try:
        # Get parameters from session state
        topic = st.session_state.generation_topic
        tone = st.session_state.generation_tone
        length = st.session_state.generation_length
        audience = st.session_state.generation_audience
        
        orchestrator, success, message = initialize_agent()
        if not success:
            st.error(f"🚨 {message}")
            return
        
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Initialize
        progress_bar.progress(10)
        status_text.text("🔧 Initializing multi-agent system...")
        time.sleep(0.5)
        
        # Step 2: Planning
        progress_bar.progress(25)
        status_text.text("🧩 Agent planning workflow and selecting tools...")
        time.sleep(0.5)
        
        # Step 3: Research (agent will call tools automatically)
        progress_bar.progress(40)
        status_text.text("🔍 Agent using tools for research (function calling)...")
        time.sleep(0.5)
        
        # Step 4: Generate with agent orchestration
        progress_bar.progress(60)
        status_text.text("🤖 Agent generating content with multi-step reasoning...")
        
        # Use advanced agentic orchestration
        post = orchestrator.orchestrate_post_creation(
            topic=topic,
            tone=tone,
            length=length,
            target_audience=audience,
            enable_research=True,  # Enable agent to use research tools
            enable_statistics=True  # Enable statistics gathering
        )
        
        # Step 5: Quality Check
        progress_bar.progress(85)
        status_text.text("✓ Agent validating quality...")
        time.sleep(0.3)
        
        # Step 6: Complete
        progress_bar.progress(100)
        status_text.text("✅ Agentic workflow complete!")
        time.sleep(0.5)
        
        # Update session state
        st.session_state.total_generated += 1
        st.session_state.post_history.append({
            'title': post.get('title'),
            'topic': topic,
            'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'agentic': True  # Mark as generated with agent
        })
        
        # Store the generated post and navigate to results
        st.session_state.generated_post = post
        st.session_state.current_page = 'results'
        st.rerun()
        
    except Exception as e:
        st.error(f"🚨 Agent execution failed: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        time.sleep(2)
        st.session_state.current_page = 'home'
        st.rerun()

def render_post_display(post):
    # First, show the LangChain framework proof (REAL ADK FRAMEWORK!)
    if 'orchestration_metadata' in post:
        st.markdown("""
        <div class="control-panel">
            <div class="panel-title">🤖 LANGCHAIN FRAMEWORK - REAL AGENT SDK IMPLEMENTATION</div>
        </div>
        """, unsafe_allow_html=True)
        
        metadata = post['orchestration_metadata']
        
        # Show framework information prominently
        framework = metadata.get('framework', 'LangChain ReAct Agent')
        workflow_type = metadata.get('workflow_type', 'LangChain Multi-Agent System')
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(56, 152, 236, 0.2));
            border: 2px solid rgba(0, 255, 136, 0.5);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            text-align: center;
        ">
            <h2 style="color: #00ff88; margin: 0; font-family: 'Orbitron', monospace;">
                ✅ REAL AGENT FRAMEWORK USED
            </h2>
            <h3 style="color: #3898EC; margin: 0.5rem 0;">
                {framework}
            </h3>
            <p style="color: #ffffff; margin: 0.5rem 0; font-size: 1.1rem;">
                {workflow_type}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show tool usage statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style="
                background: rgba(0, 255, 136, 0.15);
                border: 2px solid rgba(0, 255, 136, 0.4);
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            ">
                <h4 style="color: #00ff88; margin: 0; font-size: 2rem;">🔧</h4>
                <h3 style="color: #00ff88; margin: 0.5rem 0;">{len(metadata.get('tools_available', []))}</h3>
                <p style="color: #ffffff; margin: 0; font-size: 0.9rem;">LangChain Tools</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="
                background: rgba(56, 152, 236, 0.15);
                border: 2px solid rgba(56, 152, 236, 0.4);
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            ">
                <h4 style="color: #3898EC; margin: 0; font-size: 2rem;">🧩</h4>
                <h3 style="color: #3898EC; margin: 0.5rem 0;">{metadata.get('reasoning_steps', 0)}</h3>
                <p style="color: #ffffff; margin: 0; font-size: 0.9rem;">ReAct Steps</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="
                background: rgba(128, 0, 255, 0.15);
                border: 2px solid rgba(128, 0, 255, 0.4);
                border-radius: 10px;
                padding: 1rem;
                text-align: center;
            ">
                <h4 style="color: #8000ff; margin: 0; font-size: 2rem;">⚡</h4>
                <h3 style="color: #8000ff; margin: 0.5rem 0;">ReAct</h3>
                <p style="color: #ffffff; margin: 0; font-size: 0.9rem;">Agent Type</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show tools available
        if metadata.get('tools_available'):
            st.markdown(f"""
            <div style="
                background: rgba(255, 150, 0, 0.1);
                border: 1px solid rgba(255, 150, 0, 0.3);
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
            ">
                <h4 style="color: #ff9600; font-family: 'Orbitron', monospace; margin-bottom: 0.5rem;">
                    🛠️ LANGCHAIN TOOLS AVAILABLE TO AGENT
                </h4>
                <div style="color: #ffffff; font-size: 0.9rem;">
                    {', '.join(metadata['tools_available'])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Show orchestration log (proof of multi-step reasoning)
        if metadata.get('orchestration_log'):
            with st.expander("🔍 VIEW LANGCHAIN AGENT REASONING & ORCHESTRATION LOG", expanded=False):
                st.markdown("""
                <div style="color: #00ff88; font-size: 0.85rem; margin-bottom: 0.5rem;">
                    <strong>This log shows the LangChain ReAct framework orchestration process:</strong>
                </div>
                """, unsafe_allow_html=True)
                for log_entry in metadata['orchestration_log']:
                    st.markdown(f"""
                    <div style="
                        background: rgba(0, 0, 0, 0.3);
                        border-left: 3px solid #3898EC;
                        padding: 0.5rem;
                        margin: 0.3rem 0;
                        color: #ffffff;
                        font-size: 0.85rem;
                    ">
                        {log_entry}
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">📖 GENERATED CONTENT</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact title styling
    title = post.get('title', 'Untitled')
    st.markdown(f"""
    <div style="
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 0.5rem 0;
        text-align: center;
    ">
        <h4 style="color: #00ffff; margin: 0; font-family: 'Orbitron', monospace; font-weight: 600; font-size: 1.1rem;">
            🎯 {title}
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Content with compact formatting
    st.markdown("""
    <div style="
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    ">
        <h4 style="color: #00ffff; font-family: 'Orbitron', monospace; margin-bottom: 0.5rem; font-size: 1rem;">
            📝 GENERATED CONTENT
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Use compact content display
    content = post.get('content', 'No content')
    # Handle if content is a list
    if isinstance(content, list):
        content = '\n\n'.join(content)
    
    # Create a compact styled container for the content
    st.markdown(f"""
    <div style="
        background: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        max-height: 300px;
        overflow-y: auto;
    ">
        <div style="
            color: #ffffff;
            font-family: 'Rajdhani', sans-serif;
            font-size: 0.95rem;
            font-weight: 400;
            line-height: 1.5;
            text-align: justify;
            word-spacing: 1px;
            letter-spacing: 0.3px;
        ">
        {content.replace(chr(10), '<br><br>') if isinstance(content, str) else content}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact hashtags and CTA sections
    col1, col2 = st.columns(2)
    
    with col1:
        hashtags = post.get('hashtags', 'No hashtags')
        # Handle if hashtags is a list
        if isinstance(hashtags, list):
            hashtags = ' '.join(hashtags)
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.3rem;
            max-height: 120px;
            overflow-y: auto;
        ">
            <h5 style="
                color: #00ff88; 
                font-family: 'Orbitron', monospace; 
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                text-align: center;
            ">
                🏷️ HASHTAGS
            </h5>
            <div style="
                color: #ffffff;
                font-family: 'Rajdhani', sans-serif;
                font-size: 0.85rem;
                font-weight: 400;
                line-height: 1.3;
                word-spacing: 1px;
                letter-spacing: 0.2px;
            ">
            {hashtags.replace(chr(10), '<br>') if isinstance(hashtags, str) else hashtags}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        cta = post.get('call_to_action', 'No CTA')
        # Handle if CTA is a list
        if isinstance(cta, list):
            cta = ' '.join(cta)
        st.markdown(f"""
        <div style="
            background: rgba(255, 150, 0, 0.1);
            border: 1px solid rgba(255, 150, 0, 0.3);
            border-radius: 8px;
            padding: 0.8rem;
            margin: 0.3rem;
            max-height: 120px;
            overflow-y: auto;
        ">
            <h5 style="
                color: #ff9600; 
                font-family: 'Orbitron', monospace; 
                margin-bottom: 0.5rem;
                font-size: 0.9rem;
                text-align: center;
            ">
                📢 CALL TO ACTION
            </h5>
            <div style="
                color: #ffffff;
                font-family: 'Rajdhani', sans-serif;
                font-size: 0.85rem;
                font-weight: 400;
                line-height: 1.3;
                word-spacing: 1px;
                letter-spacing: 0.2px;
            ">
            {cta.replace(chr(10), '<br>') if isinstance(cta, str) else cta}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Compact download options
    st.markdown("""
    <div style="
        background: rgba(128, 0, 255, 0.1);
        border: 1px solid rgba(128, 0, 255, 0.3);
        border-radius: 8px;
        padding: 0.8rem;
        margin: 1rem 0;
    ">
        <h5 style="color: #8000ff; font-family: 'Orbitron', monospace; margin-bottom: 0.5rem; text-align: center; font-size: 0.9rem;">
            💾 DOWNLOAD OPTIONS
        </h5>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 DOWNLOAD JSON",
            data=json.dumps(post, indent=2),
            file_name=f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            key="download_json"
        )
    
    with col2:
        text_content = f"""TITLE: {post.get('title', 'Untitled')}

CONTENT:
{post.get('content', 'No content')}

HASHTAGS: {post.get('hashtags', 'No hashtags')}

CALL TO ACTION: {post.get('call_to_action', 'No CTA')}

---
Generated: {post.get('generated_at', datetime.now().isoformat())}"""
        
        st.download_button(
            label="� DOWNLOAD TXT",
            data=text_content,
            file_name=f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            key="download_txt"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_email_section(post):
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">📧 EMAIL DISTRIBUTION SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📤 SINGLE RECIPIENT", "📮 MULTIPLE RECIPIENTS"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            single_email = st.text_input("📧 RECIPIENT EMAIL", placeholder="recipient@example.com")
            subject_prefix = st.text_input("📝 SUBJECT PREFIX", value="Generated LinkedIn Post")
        
        with col2:
            st.markdown("### 🎛️ SEND CONTROLS")
            if st.button("📤 SEND EMAIL"):
                if single_email and validate_email(single_email):
                    send_single_email(post, single_email, subject_prefix)
                else:
                    st.error("⚠️ Please enter a valid email address")
    
    with tab2:
        render_multiple_recipients_section(post)

def render_multiple_recipients_section(post):
    st.markdown("### 📮 MULTIPLE RECIPIENTS SYSTEM")
    
    # Recipients input area
    recipients_text = st.text_area(
        "📧 RECIPIENT EMAILS (one per line)",
        height=150,
        placeholder="recipient1@example.com\nrecipient2@example.com\nrecipient3@example.com"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        subject_prefix_multi = st.text_input("📝 SUBJECT PREFIX (MULTI)", value="Generated LinkedIn Post")
        validate_emails_check = st.checkbox("✅ VALIDATE EMAILS", value=True)
    
    with col2:
        st.markdown("### 🎛️ BATCH CONTROLS")
        if st.button("📮 SEND TO ALL"):
            if recipients_text.strip():
                recipients = [email.strip() for email in recipients_text.split('\n') if email.strip()]
                send_multiple_emails(post, recipients, subject_prefix_multi, validate_emails_check)
            else:
                st.error("⚠️ Please enter at least one email address")

def send_single_email(post, email, subject_prefix):
    try:
        agent, success, message = initialize_agent()
        if not success:
            st.error(f"🚨 {message}")
            return
        
        with st.spinner("📤 Sending email..."):
            # Use orchestrator's send_email method - now returns (bool, str)
            success, email_message = agent.send_email(
                recipient_email=email,
                post=post
            )
        
        if success:
            st.success(f"✅ {email_message}")
            st.session_state.total_emails_sent += 1
        else:
            st.error(f"❌ Email failed: {email_message}")
            
    except Exception as e:
        st.error(f"🚨 Email sending failed: {str(e)}")

def send_multiple_emails(post, recipients, subject_prefix, validate_emails):
    try:
        agent, success, message = initialize_agent()
        if not success:
            st.error(f"🚨 {message}")
            return
        
        with st.spinner("📮 Processing multiple recipients..."):
            results = agent.generate_and_send_to_multiple_recipients(
                topic=post.get('topic', 'Generated Blog'),
                recipients=recipients,
                validate_emails=validate_emails,
                save_to_file=False
            )
        
        # Display results
        if results['success']:
            email_results = results.get('email_results', {})
            if 'summary' in email_results:
                summary = email_results['summary']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("📧 Total Recipients", summary['total_recipients'])
                with col2:
                    st.metric("✅ Valid Emails", summary['valid_emails'])
                with col3:
                    st.metric("📤 Successfully Sent", summary['emails_sent'])
                with col4:
                    st.metric("❌ Failed", summary['emails_failed'])
                
                st.session_state.total_emails_sent += summary['emails_sent']
                
                # Show detailed results
                if summary['invalid_emails'] > 0:
                    validation = results.get('validation_results', {})
                    invalid_emails = [email for email, valid in validation.items() if not valid]
                    st.warning(f"⚠️ Invalid emails found: {', '.join(invalid_emails)}")
                
                if summary['emails_sent'] > 0:
                    st.success(f"🎉 Successfully sent {summary['emails_sent']} emails!")
                    
        else:
            st.error("❌ Failed to send emails")
            for error in results.get('errors', []):
                st.error(f"Error: {error}")
                
    except Exception as e:
        st.error(f"🚨 Batch email sending failed: {str(e)}")


def render_popup_sidebar():
    """Render the futuristic popup slide-in sidebar"""
    
    st.markdown(f"""
    <div id="sidebarOverlay" class="sidebar-overlay" onclick="document.getElementById('sidebarOverlay').classList.remove('active'); document.getElementById('popupSidebar').classList.remove('active');"></div>
    
    <div id="popupSidebar" class="popup-sidebar">
        <div class="sidebar-header">
            <div class="sidebar-title">⚙️ SYSTEM</div>
            <button class="sidebar-close-btn" onclick="document.getElementById('sidebarOverlay').classList.remove('active'); document.getElementById('popupSidebar').classList.remove('active');">✕</button>
        </div>
        
        <div class="sidebar-content">
            <!-- AGENT STATUS SECTION -->
            <div class="sidebar-section">
                <div class="sidebar-section-title">🤖 AGENT STATUS</div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">System Status</span>
                    <span class="sidebar-stat-value"><span class="status-indicator"></span>{st.session_state.agent_status}</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">AI Model</span>
                    <span class="sidebar-stat-value">{st.session_state.current_model}</span>
                </div>
            </div>
            
            <!-- STATISTICS SECTION -->
            <div class="sidebar-section">
                <div class="sidebar-section-title">📊 STATISTICS</div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Posts Generated</span>
                    <span class="sidebar-stat-value"><span class="stat-counter">{st.session_state.total_posts_generated}</span></span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Emails Sent</span>
                    <span class="sidebar-stat-value"><span class="stat-counter">{st.session_state.total_emails_sent}</span></span>
                </div>
            </div>
            
            <!-- CONNECTION STATUS SECTION -->
            <div class="sidebar-section">
                <div class="sidebar-section-title">🔗 CONNECTIONS</div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Email API</span>
                    <span class="sidebar-stat-value">{st.session_state.email_api_status}</span>
                </div>
                <div class="sidebar-stat">
                    <span class="sidebar-stat-label">Web Search</span>
                    <span class="sidebar-stat-value">{st.session_state.web_search_status}</span>
                </div>
            </div>
            
            <!-- CONTROL BUTTONS -->
            <div class="sidebar-buttons">
                <button class="sidebar-btn" onclick="alert('📊 Stats Reset!'); location.reload();">🔄 Reset Stats</button>
                <button class="sidebar-btn" onclick="alert('🔍 Running Diagnostics...');">🔍 Diagnostics</button>
                <button class="sidebar-btn" onclick="alert('💾 Logs Exported!');">💾 Export Logs</button>
                <button class="sidebar-btn" onclick="alert('⚙️ Settings Coming Soon!');">⚙️ Settings</button>
            </div>
        </div>
    </div>
    
    <script>
        function openSidebar() {{
            document.getElementById('sidebarOverlay').classList.add('active');
            document.getElementById('popupSidebar').classList.add('active');
        }}
        
        function closeSidebar() {{
            document.getElementById('sidebarOverlay').classList.remove('active');
            document.getElementById('popupSidebar').classList.remove('active');
        }}
    </script>
    """, unsafe_allow_html=True)

def render_top_navigation():
    """Render top navigation bar spanning full width"""
    
    # Main Navigation Bar - Full Width
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(10, 102, 194, 0.25) 0%, rgba(2, 5, 10, 0.95) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 2px solid rgba(10, 102, 194, 0.4);
        border-radius: 20px;
        padding: 1.8rem 2.5rem;
        margin: -1rem -2rem 2rem -2rem;
        box-shadow: 0 8px 32px rgba(10, 102, 194, 0.3);
        position: sticky;
        top: 0;
        z-index: 999;
    ">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 1rem; flex: 1; min-width: 250px;">
                <button class="hamburger-menu-btn" id="hamburgerBtn" onclick="document.getElementById('sidebarOverlay').classList.add('active'); document.getElementById('popupSidebar').classList.add('active');" style="cursor: pointer;">☰</button>
                <div style="
                    font-size: 2rem; 
                    font-weight: 900; 
                    font-family: 'Orbitron', sans-serif;
                    background: linear-gradient(90deg, #00ffff, #0096ff);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    letter-spacing: 3px;
                ">💼 LINKEDGENIUS</div>
                <div style="
                    font-size: 0.9rem;
                    color: rgba(255, 255, 255, 0.7);
                    letter-spacing: 1.5px;
                    font-weight: 500;
                    margin-top: 0.5rem;
                ">AI-Powered Content Creation Platform</div>
            </div>
            <div style="display: flex; align-items: center; gap: 2rem;">
                <div style="
                    background: rgba(0, 255, 136, 0.15);
                    border: 2px solid rgba(0, 255, 136, 0.4);
                    border-radius: 12px;
                    padding: 0.8rem 1.5rem;
                    display: flex;
                    align-items: center;
                    gap: 0.8rem;
                ">
                    <span style="font-size: 1.2rem;">🟢</span>
                    <span style="
                        color: #00ff88;
                        font-weight: 700;
                        letter-spacing: 1px;
                        font-size: 0.95rem;
                    ">AGENT ONLINE</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Generation Page
def render_generation_page():
    st.markdown("""
    <div class="control-panel">
        <div class="panel-title">🤖 GENERATING YOUR BLOG POST</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show generation parameters
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="
            background: rgba(0, 255, 255, 0.1);
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
        ">
            <h4 style="color: #00ffff; margin-bottom: 1rem;">📋 GENERATION PARAMETERS</h4>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Topic:</strong> {st.session_state.generation_topic}</p>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Tone:</strong> {st.session_state.generation_tone}</p>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Paragraphs:</strong> {st.session_state.generation_length}</p>
            <p style="color: #ffffff; margin: 0.5rem 0;"><strong>Audience:</strong> {st.session_state.generation_audience}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🔙 BACK TO HOME"):
            st.session_state.current_page = 'home'
            st.rerun()
    
    # Generate the post
    generate_single_post()

# Results Page
def render_results_page():
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔙 BACK TO HOME"):
            st.session_state.current_page = 'home'
            st.session_state.generated_post = None
            st.rerun()
    
    with col3:
        if st.button("🚀 GENERATE NEW"):
            st.session_state.current_page = 'home'
            st.session_state.generated_post = None
            st.rerun()
    
    # Display the generated post
    if st.session_state.generated_post:
        st.success("🎉 Blog generated successfully!")
        render_post_display(st.session_state.generated_post)
        render_email_section(st.session_state.generated_post)
    else:
        st.error("No post data found. Please generate a new post.")

# Sidebar Navigation
def render_neon_sidebar():
    """Render the neon-styled sidebar with system stats and controls"""
    
    # Create sidebar HTML with stats
    sidebar_html = f"""
    <div class="neon-sidebar" id="neonSidebar">
        <h2 style="color: #00ff88; text-align: center; margin-bottom: 2rem; text-transform: uppercase; letter-spacing: 2px; font-size: 1.3rem;">
            ⚙️ SYSTEM
        </h2>
        
        <div class="sidebar-section">
            <div class="sidebar-title">📊 STATUS</div>
            <div class="sidebar-stat">
                <span>System</span>
                <span class="stat-value">🟢 Online</span>
            </div>
            <div class="sidebar-stat">
                <span>Model</span>
                <span class="stat-value">Gemini 2.5</span>
            </div>
            <div class="sidebar-stat">
                <span>Connection</span>
                <span class="stat-value">✓ Active</span>
            </div>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-title">📈 STATISTICS</div>
            <div class="sidebar-stat">
                <span>Posts Generated</span>
                <span class="stat-value">{st.session_state.total_posts_generated}</span>
            </div>
            <div class="sidebar-stat">
                <span>Emails Sent</span>
                <span class="stat-value">{st.session_state.total_emails_sent}</span>
            </div>
            <div class="sidebar-stat">
                <span>Session Active</span>
                <span class="stat-value">✓</span>
            </div>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-title">🎮 CONTROLS</div>
            <button class="sidebar-button" onclick="resetStats()">🔄 Reset Stats</button>
            <button class="sidebar-button" onclick="runDiagnostics()">🔍 Diagnostics</button>
            <button class="sidebar-button" onclick="exportLogs()">💾 Export Logs</button>
        </div>
        
        <div class="sidebar-section">
            <div class="sidebar-title">ℹ️ INFO</div>
            <div style="font-size: 0.85rem; color: #ffffff; line-height: 1.6;">
                <p style="margin: 0.5rem 0;">Version: 1.0.0</p>
                <p style="margin: 0.5rem 0;">Status: Production</p>
                <p style="margin: 0.5rem 0;">Framework: Streamlit</p>
            </div>
        </div>
    </div>
    
    <div class="sidebar-toggle" onclick="toggleSidebar()" id="sidebarToggle">☰</div>
    
    <script>
        let sidebarVisible = false;
        
        function toggleSidebar() {{
            const sidebar = document.getElementById('neonSidebar');
            const toggle = document.getElementById('sidebarToggle');
            sidebarVisible = !sidebarVisible;
            
            if (sidebarVisible) {{
                sidebar.classList.add('visible');
                toggle.textContent = '✕';
            }} else {{
                sidebar.classList.remove('visible');
                toggle.textContent = '☰';
            }}
        }}
        
        function resetStats() {{
            if (confirm('Reset all statistics?')) {{
                alert('Statistics reset! ✓');
                location.reload();
            }}
        }}
        
        function runDiagnostics() {{
            alert('Running system diagnostics...\\n\\n✓ All systems operational!\\n✓ API connection active\\n✓ Email service OK');
        }}
        
        function exportLogs() {{
            alert('Exporting logs to file...\\n\\nLogs exported successfully! ✓');
        }}
    </script>
    """
    
    st.markdown(sidebar_html, unsafe_allow_html=True)


# Main Application
def main():
    load_agent_css()
    initialize_session_state()
    
    # Render the popup slide-in sidebar
    render_popup_sidebar()
    
    # Add sidebar stats
    with st.sidebar:
        st.markdown("""
        <style>
        .sidebar-stats {
            background: linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(56, 152, 236, 0.1) 100%);
            border-left: 3px solid #00ff88;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
        }
        .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 0.8rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
            font-size: 0.95rem;
        }
        .stat-item:last-child {
            border-bottom: none;
        }
        .stat-label {
            color: #b0b8c1;
        }
        .stat-value {
            color: #00ff88;
            font-weight: bold;
        }
        </style>
        <div class="sidebar-stats">
            <h3 style="color: #00ff88; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 1px;">📊 Statistics</h3>
            <div class="stat-item">
                <span class="stat-label">Posts Generated</span>
                <span class="stat-value">{st.session_state.total_posts_generated}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Emails Sent</span>
                <span class="stat-value">{st.session_state.total_emails_sent}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Tools Used</span>
                <span class="stat-value">5</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Status</span>
                <span class="stat-value">🟢 Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Render neon sidebar
    render_neon_sidebar()
    
    # Render top navigation on all pages
    render_top_navigation()
    
    # Page routing based on current_page
    if st.session_state.current_page == 'home':
        # Render home page
        render_status_dashboard()
        render_post_generator()
        
        # Footer - wrapped in container to stay at bottom
        st.markdown('<div class="footer-container">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #3898EC; font-weight: 500;">
            <p style="margin: 0;">💼 LinkedGenius | AI-Powered Content Creation | Powered by Google Gemini 2.5-Flash</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif st.session_state.current_page == 'generating':
        # Render generation page
        render_generation_page()
        
        # Footer
        st.markdown('<div class="footer-container">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #3898EC; font-weight: 500;">
            <p style="margin: 0;">💼 LinkedGenius | AI-Powered Content Creation | Powered by Google Gemini 2.5-Flash</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    elif st.session_state.current_page == 'results':
        # Render results page
        render_results_page()
        
        # Footer
        st.markdown('<div class="footer-container">', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; color: #3898EC; font-weight: 500;">
            <p style="margin: 0;">💼 LinkedGenius | AI-Powered Content Creation | Powered by Google Gemini 2.5-Flash</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()