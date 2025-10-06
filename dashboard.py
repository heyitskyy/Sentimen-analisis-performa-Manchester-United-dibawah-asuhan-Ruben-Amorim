import streamlit as st
import pandas as pd
import plotly.express as px

from config import RESULTS_FILE, KEYWORDS_FILE

# ====== FIX AUTO REFRESH ======
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Twitter + YouTube Sentiment Dashboard", layout="wide")

st.title("Sentimen Performa Manchester United dibawah asuhan Ruben Amorim")

# --- Auto Refresh setiap 60 detik ---
st_autorefresh(interval=60 * 1000, key="refresh")

# --- Load Data ---
@st.cache_data(ttl=60)  # cache hanya berlaku 60 detik
def load_data():
    try:
        df = pd.read_csv(RESULTS_FILE)
    except Exception as e:
        st.error(f"Gagal load data hasil crawling: {e}")
        return pd.DataFrame()
    return df

# Tombol manual refresh
if st.button("🔄 Refresh Data Sekarang"):
    st.cache_data.clear()

df = load_data()

if df.empty:
    st.warning("⚠️ Belum ada data. Jalankan `python main.py` dulu untuk crawling.")
    st.stop()

# --- Statistik ---
st.subheader("📈 Statistik Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Data", len(df))

if "source" in df.columns:
    # --- PENTING: Perbaikan Error AttributeError ---
    # Konversi kolom 'source' ke string untuk menghindari AttributeError
    df["source"] = df["source"].astype(str)
    
    # Hitung sumber Twitter. Gunakan .str.lower() untuk memastikan pencarian seragam.
    twitter_count = (df["source"].str.lower() == "twitter").sum()
    
    # Hitung sumber YouTube. Gunakan .str.contains() dan case=False.
#     youtube_count = (df["source"].str.contains("youtube", case=False)).sum()
    
#     col2.metric("Sumber Twitter", twitter_count)
#     col3.metric("Sumber YouTube", youtube_count)
# else:
#     col2.metric("Sumber Twitter", 0)
#     col3.metric("Sumber YouTube", 0)
#     st.warning("⚠️ Kolom 'source' tidak ditemukan. Pastikan crawler menambahkan kolom ini.")

# --- Distribusi Sentiment ---
if "sentiment" in df.columns:
    st.subheader("😊 Distribusi Sentiment")
    sent_counts = df["sentiment"].value_counts().reset_index()
    sent_counts.columns = ["Sentiment", "Jumlah"]

    fig_sent = px.pie(
        sent_counts,
        values="Jumlah",
        names="Sentiment",
        color="Sentiment",
        color_discrete_map={"positive": "green", "neutral": "gray", "negative": "red"},
        title="Sentiment Analysis"
    )
    st.plotly_chart(fig_sent, use_container_width=True)
else:
    st.warning("⚠️ Kolom 'sentiment' tidak ditemukan. Analisis sentiment belum tersedia.")

# --- Timeline ---
if "timestamp" in df.columns:
    st.subheader("⏱️ Timeline Sentiment")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    timeline = df.groupby([df["timestamp"].dt.date, "sentiment"]).size().reset_index(name="count")
    fig_time = px.line(
        timeline,
        x="timestamp",
        y="count",
        color="sentiment" if "sentiment" in df.columns else None,
        title="Perubahan Sentiment dari Waktu ke Waktu"
    )
    st.plotly_chart(fig_time, use_container_width=True)
else:
    st.info("⏱️ Tidak ada kolom 'timestamp'. Timeline tidak bisa ditampilkan.")

# --- Keyword Frequency ---
st.subheader("🔑 Keyword Frequency")
try:
    kw_df = pd.read_csv(KEYWORDS_FILE)
    if not kw_df.empty and "keyword" in kw_df.columns and "frequency" in kw_df.columns:
        fig_kw = px.bar(
            kw_df.head(20),
            x="keyword",
            y="frequency",
            title="Top Keywords",
            text="frequency"
        )
        fig_kw.update_traces(textposition="outside")
        st.plotly_chart(fig_kw, use_container_width=True)
    else:
        st.warning("⚠️ File keyword kosong atau kolom tidak lengkap.")
except Exception as e:
    st.warning(f"Keyword file belum ada: {e}")

# --- Data Table ---
st.subheader("📜 Data Mentah")
cols_show = [c for c in ["source", "text", "sentiment", "timestamp"] if c in df.columns]
if cols_show:
    st.dataframe(df[cols_show].head(15000))
else:
    st.dataframe(df.head(50))