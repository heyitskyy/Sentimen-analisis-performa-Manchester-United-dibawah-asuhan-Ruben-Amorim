# Sentimen analisis mengenai Performa Manchester United dibawah asuhan Ruben Amorim
<img width="2056" height="1388" alt="image" src="https://github.com/user-attachments/assets/e5e7026f-e052-49f5-9d9c-3cb36d9a6be4" />

🧠 Analisis Sentimen Publik terhadap Manchester United — Ruben Amorim
Proyek Akhir Mata Kuliah Text Mining & Sentiment Analysis

Dibuat menggunakan Python, Streamlit, Twitter Scraper, dan YouTube Data API v3

📑 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis persepsi publik terhadap topik “Manchester United — Ruben Amorim” berdasarkan komentar di Twitter dan YouTube.
Sistem melakukan scraping data otomatis, kemudian melakukan analisis sentimen (positif, netral, negatif), dan akhirnya menampilkan hasil dalam bentuk dashboard interaktif berbasis Streamlit.

Dengan pendekatan ini, pengguna dapat memantau opini publik secara real-time dan mendapatkan wawasan mengenai arah sentimen terhadap topik tertentu.

🚀 Fitur Utama
🧩 1. Data Crawling Otomatis

Twitter Scraper berbasis Selenium
Mengambil tweet berdasarkan kata kunci (QUERY) dengan batas tertentu (TARGET_TWEETS).
Dapat menelusuri balasan (reply) dan menyimpan hasil dalam format .csv.

YouTube Comment Scraper via YouTube Data API v3
Mengambil komentar publik dari beberapa video hasil pencarian sesuai kata kunci.
Komentar dan balasan (reply) disimpan lengkap dengan metadata (author, date, likes, language, dll).

📊 2. Analisis Sentimen

Analisis dilakukan terhadap teks dari Twitter dan YouTube.

Setiap entri diberi label:

positive

neutral

negative

unknown (jika gagal diklasifikasi)

Hasil analisis disimpan dalam file data/results.csv.

🧠 3. Dashboard Analitik Interaktif

Dashboard dibuat menggunakan Streamlit dengan visualisasi Plotly dan WordCloud.
Fitur utama:

Distribusi Sentimen (Pie Chart)

Perbandingan Sumber (Bar Chart)

Tren Waktu (Timeline Chart)

Top Keywords dan WordCloud

Filter berdasarkan sumber, sentiment, bahasa, dan rentang waktu

Upload CSV eksternal untuk uji coba dataset lain

🧰 Struktur Proyek
📂 sentiment-dashboard/
│
├── main.py                # Entry point untuk menjalankan crawler
├── config.py              # Konfigurasi utama proyek (API keys, limit, paths)
├── modules/
│   ├── tw_scraper.py      # Modul untuk crawling tweet via Selenium
│   ├── yt_api.py          # Modul untuk crawling komentar YouTube via API
│   └── sentiment.py       # Modul analisis sentimen teks
│
├── data/
│   ├── results.csv        # Hasil akhir gabungan (Twitter + YouTube)
│   └── keywords.csv       # Daftar kata kunci pencarian
│
├── dashboard.py           # Dashboard utama berbasis Streamlit
└── README.md              # Dokumentasi proyek (file ini)

⚙️ Konfigurasi & Cara Menjalankan
1️⃣ Instalasi Dependensi
pip install -r requirements.txt


Daftar pustaka utama:

streamlit
pandas
plotly
google-api-python-client
selenium
wordcloud
matplotlib
langdetect

2️⃣ Isi Konfigurasi API & Query

Edit file config.py:

QUERY = "Manchester United Ruben Amorim since:2024-11-11"
YOUTUBE_API_KEY = "ISI_API_KEY_KAMU_DI_SINI"
RESULTS_FILE = "data/results.csv"

3️⃣ Jalankan Crawling
python main.py


Proses ini akan mengambil data dari Twitter dan YouTube sesuai QUERY dan menyimpannya ke data/results.csv.

4️⃣ Jalankan Dashboard
streamlit run dashboard.py


Dashboard interaktif akan tampil di browser pada:
👉 http://localhost:8501

📈 Visualisasi di Dashboard
Fitur	Deskripsi
🥧 Distribusi Sentimen	Pie chart jumlah sentimen positif/negatif/netral
📊 Sentimen per Sumber	Bandingkan antara Twitter, YouTube (Top), dan YouTube (Reply)
⏱ Timeline Aktivitas	Lihat tren perubahan opini publik dari waktu ke waktu
☁️ WordCloud	Kata paling sering muncul di komentar atau tweet
🧾 Data Mentah	Tabel berisi data asli hasil crawling dan klasifikasi
🧮 Contoh Hasil Analisis
Source	Text (ringkas)	Sentiment
Twitter	Ruben Amorim is improving Man United’s tactics!	positive
YouTube	This team is hopeless, same problems every year!	negative
YouTube (Reply)	Maybe he needs more time, not fair to judge yet.	neutral

Visualisasi menunjukkan mayoritas komentar YouTube bernada positif, sementara Twitter lebih seimbang antara positif dan negatif.
