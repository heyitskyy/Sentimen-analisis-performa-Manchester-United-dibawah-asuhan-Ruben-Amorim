# Sentimen analisis mengenai Performa Manchester United dibawah asuhan Ruben Amorim
<img width="2056" height="1388" alt="image" src="https://github.com/user-attachments/assets/e5e7026f-e052-49f5-9d9c-3cb36d9a6be4" />

# 📊 Dashboard Analisis Sentimen — Manchester United x Ruben Amorim

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)]()

**Zaky Ahmad** — *Kecerdasan Web dan Big Data*

---

## 📖 Tentang Proyek
Proyek ini menganalisis **sentimen publik** terhadap performa dan isu kepelatihan **Manchester United** di bawah **Ruben Amorim**, dengan menggabungkan data dari **Twitter (X)** dan **YouTube**.  
Analisis dilakukan secara otomatis melalui crawling data dan pemrosesan teks menggunakan model NLP berbasis **Transformer (IndoBERT / BERT multilingual)**.

---

## 🎯 Tujuan
- ✅ Memahami opini publik secara objektif dan terukur  
- ✅ Mengidentifikasi tren sentimen dari berbagai platform media  
- ✅ Memberikan insight bagi analis, akademisi, dan stakeholder  
- ✅ Membandingkan sentimen antara Twitter dan YouTube  

---

## 🧰 Tools

| Kategori | Teknologi |
|-----------|------------|
| **Deep Learning** | PyTorch, Transformers, IndoBERT |
| **Web Scraping** | Twitter Scraper, YouTube Data API |
| **NLP** | Sastrawi, NLTK |
| **Data Science** | Pandas, NumPy, Scikit-learn |
| **Visualization** | Streamlit, Plotly, Matplotlib, WordCloud |
| **Database** | CSV |

---

## 🧩 Deskripsi Proyek
Aplikasi ini merupakan **Dashboard Analisis Sentimen berbasis Streamlit** yang dirancang untuk memantau dan menganalisis opini publik mengenai topik tertentu (misalnya klub sepak bola, tokoh publik, atau isu sosial).  
Sistem akan **mengambil data secara otomatis** dari dua platform utama — **Twitter (X)** dan **YouTube** — lalu menggabungkannya ke dalam satu tampilan interaktif untuk **analisis tren sentimen**.

Dashboard ini membantu pengguna, peneliti, maupun dosen untuk memahami bagaimana opini masyarakat berkembang di berbagai platform media sosial.

---

## ⚙️ Fitur Utama

### ✅ 1. Scraping Data Otomatis
- Mengambil tweet dan komentar YouTube berdasarkan kata kunci tertentu  
- Bisa mengatur jumlah maksimum tweet atau komentar per video  
- Mendukung bahasa **Indonesia (id)** dan **Inggris (en)**  

### ✅ 2. Analisis Sentimen Otomatis
- Menggunakan model NLP untuk menentukan apakah teks bersentimen **positif**, **netral**, atau **negatif**  
- Setiap data dilengkapi dengan **confidence score**  

### ✅ 3. Integrasi Multi-Platform
- Menggabungkan hasil analisis dari **Twitter** dan **YouTube** ke dalam satu dataset  
- Menampilkan hasil secara terpisah untuk tiap sumber  

### ✅ 4. Dashboard Interaktif
- Dibangun dengan **Streamlit** dan **Plotly**  
- Menampilkan grafik distribusi sentimen, timeline, dan tabel data mentah  
- Dilengkapi fitur **WordCloud** (opsional)  
- Auto-refresh untuk memantau data terbaru secara real-time  

---

## 🚀 Cara Menjalankan Proyek

### 1️⃣ Clone Repository:
```bash
git clone [URL_REPOSITORY_ANDA]
cd [NAMA_FOLDER_PROYEK]
2️⃣ Setup Lingkungan:
🧩 Buat dan aktifkan virtual environment:
bash
Copy code
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
💾 Install semua dependensi:
bash
Copy code
pip install -r requirements.txt
3️⃣ Konfigurasi Kredensial:
🔑 Buat file bernama .env di folder utama.
Isi file tersebut dengan API Key YouTube Anda:

bash
Copy code
YT_API_KEY="AIzaSyXXXXXXXXXXXXXXXXXXXX"
4️⃣ Jalankan Pipeline (Bertahap):
🟥 (Wajib) Kumpulkan data YouTube:
bash
Copy code
python crawl_youtube.py
🟨 (Opsional) Tambah data berita:
bash
Copy code
python src/main.py
🟩 Proses semua data yang terkumpul:
bash
Copy code
python run_preprocessing.py
🟦 Jalankan dashboard Streamlit:
bash
Copy code
streamlit run dashboard.py

---

## 📊 Output Dashboard

Dashboard menampilkan beberapa visualisasi utama:

- Pie chart distribusi sentimen
- Bar chart per sumber data
- Timeline tren harian
- WordCloud kata dominan
- Tabel data mentah (dengan opsi download CSV)

