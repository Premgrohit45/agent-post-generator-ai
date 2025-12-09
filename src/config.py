"""
Configuration helper to support both local .env and Streamlit Cloud secrets
"""
import os
from dotenv import load_dotenv


load_dotenv()

def get_secret(key: str, default=None):
    """
    Get secret from Streamlit secrets or environment variables.
    Prioritizes Streamlit secrets for cloud deployment.
    """
    
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass

    
    return os.getenv(key, default)
