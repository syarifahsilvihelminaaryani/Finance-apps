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
    
    # ==========================================
    # 4. FITUR AI GEMINI (VARIANCE COMMENTARY)
    # ==========================================
    st.divider()
    st.subheader("🤖 Analisis Komentar AI (Gemini)")
    
    if not GEMINI_API_KEY:
        st.warning("⚠️ GEMINI_API_KEY belum diatur! Masukkan API key di menu Secrets Streamlit.")
    else:
        if st.button("🚀 Jalankan Analisis AI"):
            with st.spinner("Sedang Menganalisis Data Keuangan..."):
                try:
                    # Inisialisasi client Google GenAI
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    # Mengubah data tabel ke string agar bisa dibaca AI
                    data_summary = df.to_string()
                    
                    prompt = f"Bertindaklah sebagai Senior Financial Auditor. Analisis data Budget vs Actual berikut dan berikan komentar serta rekomendasi perbaikan secara profesional dalam Bahasa Indonesia:\n\n{data_summary}"
                    
                    # Memanggil model Gemini AI
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=prompt,
                    )
                    
                    st.markdown("### Hasil Analisis AI:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghubungi Gemini AI: {e}")

except Exception as e:
    st.error(f"Gagal memuat file Excel. Pastikan nama file di GitHub sama persis. Error: {e}")
