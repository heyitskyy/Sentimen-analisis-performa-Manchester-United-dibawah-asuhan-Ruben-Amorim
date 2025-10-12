# Sentimen analisis mengenai Performa Manchester United dibawah asuhan Ruben Amorim
<img width="2056" height="1388" alt="image" src="https://github.com/user-attachments/assets/e5e7026f-e052-49f5-9d9c-3cb36d9a6be4" />

Deskripsi Proyek

Proyek ini merupakan aplikasi Dashboard Analisis Sentimen berbasis Streamlit yang dirancang untuk memantau dan menganalisis opini publik mengenai topik tertentu (contohnya: klub sepak bola, tokoh publik, atau isu sosial). Sistem ini secara otomatis mengambil data dari dua platform utama — Twitter (X) dan YouTube — lalu menggabungkannya ke dalam satu tampilan interaktif untuk analisis tren sentimen.

Dashboard ini dapat membantu pengguna, peneliti, atau dosen dalam memahami bagaimana opini masyarakat berkembang di dua platform media sosial yang berbeda.

⚙️ Fitur Utama

✅ Scraping Data Otomatis

Mengambil tweet dan komentar YouTube berdasarkan kata kunci tertentu.

Bisa diatur jumlah maksimum tweet dan komentar per video.

Mendukung bahasa Indonesia (id) dan Inggris (en).

✅ Analisis Sentimen Otomatis

Menggunakan model NLP untuk menentukan apakah teks bersentimen positif, negatif, atau netral.

Setiap data dilengkapi dengan nilai skor kepercayaan (confidence score).

✅ Integrasi Multi-Platform

Menggabungkan hasil analisis dari Twitter dan YouTube ke dalam satu dataset.

Menampilkan sumber data secara terpisah untuk analisis per platform.

✅ Dashboard Interaktif

Dibangun menggunakan Streamlit dan Plotly.

Tersedia grafik distribusi sentimen, tabel data mentah, serta WordCloud (opsional).

Auto-refresh untuk memantau data terbaru secara real-time.

🧩 Struktur Proyek
📦 sentiment-dashboard
├── app.py                     # File utama Streamlit
├── dashboard.py               # Dashboard visualisasi utama
├── sentiment.py               # Modul analisis sentimen
├── config.py                  # Konfigurasi umum proyek
├── modules/
│   ├── twitter_scraper.py     # Modul scraping data Twitter
│   ├── yt_api.py              # Modul pengambilan komentar YouTube
│   └── utils.py               # Fungsi pendukung
├── data/
│   ├── results.csv            # Hasil gabungan analisis (Twitter + YouTube)
│   └── keywords.csv           # Kata kunci pencarian
└── requirements.txt           # Daftar dependensi Python

🧠 Teknologi yang Digunakan
Kategori	Teknologi
Bahasa Pemrograman	Python 3.10+
Framework Dashboard	Streamlit
Visualisasi	Plotly, Matplotlib, WordCloud
NLP & Sentimen	TextBlob / Transformers
Scraping	Selenium (Twitter), Google API Client (YouTube)
Data Management	Pandas, CSV
API	YouTube Data API v3
⚙️ Konfigurasi dan Instalasi
1. Clone Repository
git clone https://github.com/username/sentiment-dashboard.git
cd sentiment-dashboard

2. Buat Virtual Environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

3. Install Dependensi
pip install -r requirements.txt

4. Konfigurasi API Key

Buka file config.py dan masukkan API key YouTube kamu:

YOUTUBE_API_KEY = "ISI_API_KEY_KAMU_DI_SINI"

🚀 Menjalankan Aplikasi
streamlit run dashboard.py


Akses di browser:
👉 http://localhost:8501/

📊 Output Dashboard

Dashboard menampilkan:

Distribusi sentimen (Pie Chart & Bar Chart)

Perbandingan antar platform (Twitter vs YouTube)

WordCloud kata yang paling sering muncul

Data mentah hasil scraping (tabel interaktif)

Contoh hasil visualisasi:

+-------------------+
|   Sentiment Pie   |
|   Sentiment Bar   |
|   WordCloud       |
|   Data Table      |
+-------------------+

📈 Contoh Dataset (results.csv)
text	lang	timestamp	sentiment	score	source
"Ruben Amorim is a great coach!"	en	2025-10-11	positive	0.92	twitter
"MU should keep him longer."	en	2025-10-11	positive	0.81	youtube_api
"Bad decision by the club..."	en	2025-10-11	negative	0.76	twitter
🔍 Penjelasan Analisis Sentimen

Setiap teks dianalisis menggunakan pendekatan lexicon-based atau model machine learning (tergantung konfigurasi). Nilai score menunjukkan tingkat kepastian analisis:

> 0.6 → Positive

< 0.4 → Negative

0.4 - 0.6 → Neutral

🧩 WordCloud (Opsional)

Untuk menampilkan WordCloud, tambahkan potongan kode berikut ke dalam dashboard.py:

from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.subheader("WordCloud dari Seluruh Teks")

text_data = " ".join(df["text"].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)

fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

🧪 Contoh Penggunaan
# Ubah kata kunci di config.py
QUERY = "Manchester United Ruben Amorim since:2024-11-11"

# Jalankan scraping & dashboard
python modules/twitter_scraper.py
python modules/yt_api.py
streamlit run dashboard.py

📘 Kontributor

Zaky Ahmad — Pengembang utama dan penulis laporan proyek

Dosen Pembimbing: [Nama Dosen Kamu]

Program Studi: [Nama Prodi, Universitas Kamu]
Visualisasi menunjukkan mayoritas komentar YouTube bernada positif, sementara Twitter lebih seimbang antara positif dan negatif.
