import os
import pandas as pd
import streamlit as st
from groq import Groq

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Tech Audit - Budget vs Actuals & AI Analysis",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Budget vs Actuals & AI Variance Analysis")

# ==========================================
# 2. MEMUAT GROQ API KEY
# ==========================================
try:
  if "GROQ_API_KEY" in st.secrets:
    groq_api_key = st.secrets["GROQ_API_KEY"]
  else:
    groq_api_key = os.getenv("GROQ_API_KEY")
except Exception:
  groq_api_key = os.getenv("GROQ_API_KEY")

# Inisialisasi client Groq
client = Groq(api_key=groq_api_key)


# ==========================================
# 3. FUNGSI ANALISIS AI KONSISTEN
# ==========================================
def run_ai_analysis(prompt_text):
  try:
    if not groq_api_key:
      return (
          "Kesalahan: GROQ_API_KEY belum dikonfigurasi di Streamlit Secrets."
      )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Anda adalah seorang auditor keuangan publik profesional dan"
                    " senior. Tugas Anda adalah menganalisis varians anggaran"
                    " (Budget vs Actual) secara objektif, konsisten, dan"
                    " terstruktur. Selalu gunakan format laporan audit formal"
                    " dalam Bahasa Indonesia yang baku dan profesional."
                ),
            },
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.1,
    )
    return completion.choices[0].message.content
  except Exception as e:
    return f"Terjadi kesalahan saat menghubungkan ke Groq AI: {str(e)}"


# ==========================================
# 4. MEMUAT DATASET EXCEL
# ==========================================
file_path = "BUDGET VS ACTUAL.xlsx"

st.subheader("📁 Data Keuangan (Budget vs Actual)")

try:
  if os.path.exists(file_path):
    df = pd.read_excel(file_path)
    st.dataframe(df, use_container_width=True)
  else:
    st.warning(
        f"File {file_path} tidak ditemukan di direktori repositori. Silakan"
        " unggah file Excel tersebut ke GitHub."
    )
    df = None
except Exception as e:
  st.error(f"Gagal memuat file Excel: {str(e)}")
  df = None

# ==========================================
# 5. BAGIAN INTERAKSI ANALISIS AI
# ==========================================
st.markdown("---")
st.subheader("🤖 Analisis Komentar AI (Groq)")

if df is not None:
  if st.button("🚀 Jalankan Analisis AI"):
    with st.spinner(
        "Sedang memproses analisis varians keuangan yang konsisten..."
    ):
      data_summary = df.to_string(index=False)
      prompt = (
          "Berikut adalah data laporan keuangan Budget vs Actual:\n\n"
          f"{data_summary}\n\n"
          "Berikan analisis audit keuangan yang mendalam dengan mengikuti"
          " format terstruktur persis seperti berikut:\n"
          "1. **Ringkasan Eksekutif Kinerja Keuangan**: (Evaluasi umum"
          " pencapaian anggaran secara keseluruhan)\n"
          "2. **Analisis Varians Signifikan**: (Identifikasi pos-pos anggaran"
          " yang mengalami selisih terbesar atau paling mencolok baik"
          " menguntungkan maupun merugikan)\n"
          "3. **Evaluasi Risiko & Akar Masalah**: (Analisis kemungkinan"
          " penyebab terjadinya selisih tersebut dari sudut pandang akuntansi"
          " publik)\n"
          "4. **Rekomendasi Profesional**: (Langkah tindak lanjut konkret bagi"
          " manajemen untuk penganggaran berikutnya)\n\n"
          "Jawablah SELURUHNYA menggunakan Bahasa Indonesia formal, objektif,"
          " dan konsisten sesuai format di atas."
      )

      ai_response = run_ai_analysis(prompt)

      st.markdown("### Hasil Analisis Auditor AI:")
      st.write(ai_response)
else:
  st.info(
      "Silakan pastikan file dataset tersedia agar tombol analisis dapat"
      " digunakan."
  )
