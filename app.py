import streamlit as st
import pandas as pd
import plotly.express as px
import os

from google import genai
from dotenv import load_dotenv

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Budget vs Actuals AI",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. LOAD GEMINI API KEY
# ==========================================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Prioritaskan Streamlit Secrets jika tersedia
try:
    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass
