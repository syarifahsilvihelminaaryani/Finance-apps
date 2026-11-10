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

st.title("📊 Budget vs Actuals & AI Variance Analysis")

# ==========================================
# 2. LOAD GEMINI API KEY
# ==========================================
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    if "GEMINI_API_KEY" in st.secrets:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

# ==========================================
# 3. MEMBACA FILE EXCEL
# ==========================================
excel_file = "File BUDGET VS ACTUAL.xlsx"

try:
    df = pd.read_excel(excel_file)
    st.success(f"Berhasil memuat data dari {excel_file}!")
    
    st.subheader("Preview Data Keuangan:")
    st.dataframe(df)
    
except Exception as e:
    st.error(f"Gagal memuat file Excel. Pastikan nama file di GitHub sama persis. Error: {e}")
