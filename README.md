# Sentimen analisis mengenai Performa Manchester United dibawah asuhan Ruben Amorim
<img width="2056" height="1388" alt="image" src="https://github.com/user-attachments/assets/e5e7026f-e052-49f5-9d9c-3cb36d9a6be4" />

## 📜 Ringkasan Proyek

Proyek ini bertujuan untuk menganalisis persepsi publik terhadap topik “Manchester United — Ruben Amorim” berdasarkan komentar di Twitter dan YouTube.
Sistem melakukan scraping data otomatis, kemudian melakukan analisis sentimen (positif, netral, negatif), dan akhirnya menampilkan hasil dalam bentuk dashboard interaktif berbasis Streamlit.
Dengan pendekatan ini, pengguna dapat memantau opini publik secara real-time dan mendapatkan wawasan mengenai arah sentimen terhadap topik tertentu.

## 🚀 Teknologi yang Digunakan

Proyek ini dibangun menggunakan serangkaian teknologi dan library Python yang modern untuk menangani setiap tahapan pipeline data.

- **Bahasa Pemrograman:** Python 3.11+
- **Manajemen Lingkungan:** `venv`
- **Pengumpulan Data (Crawling):**
    - **twitter:** `selenium` untuk crawling twitter, `selemnium stealth` agar tidak terdetect oleh anti-bot twitter.
    - **YouTube:** `google-api-python-client` untuk berinteraksi dengan YouTube Data API v3 secara stabil dan resmi.
- **Preprocessing & Pembersihan Data:** `pandas` untuk manipulasi data, `Sastrawi` untuk _stopword removal_ Bahasa Indonesia.
- **Analisis Sentimen:** `transformers` dari Hugging Face untuk menjalankan model Machine Learning canggih.
    - **Model:** `w11wo/indonesian-roberta-base-sentiment-classifier`, sebuah model RoBERTa yang di-_fine-tune_ untuk analisis sentimen Bahasa Indonesia dengan output rating bintang (1-5 stars).
- **Visualisasi & Dashboard:** `Streamlit` sebagai framework aplikasi web, `Plotly` untuk membuat grafik interaktif (hover, zoom, filter), dan `Matplotlib` + `wordcloud` untuk generasi Word Cloud.
- **Manajemen Kredensial:** `python-dotenv` untuk mengelola API Key secara aman.

## ⚙️ Arsitektur & Alur Kerja Pipeline

**1. Stasiun Pengumpulan Data (Crawling)**
   - **`src/main.py` (untuk Berita):** Menjalankan crawler `youtube_scraper.py` dan `twitter_scraper.py` secara paralel untuk mengumpulkan artikel berita.
   - **Output:** File-file `.csv` mentah di folder `data/raw/`. Proses ini bersifat inkremental (menambahkan data baru tanpa menghapus yang lama).

**2. Stasiun Pembersihan (Preprocessing)**
   - **`preprocessing.py`:** Script ini membaca *semua* file CSV dari `data`, menggabungkannya, menghapus duplikat, membersihkan teks (menghapus URL, mention, tanda baca), dan menstandarisasi format tanggal.

**3. Stasiun Analisis (Machine Learning)**
   - **`sentiment.py`:** Membaca data bersih dari stasiun sebelumnya. Script ini "pintar": ia hanya akan menganalisis baris data yang belum memiliki label sentimen.
   - **Proses:** Teks bersih dikirim ke model IndoBERT (`w11wo/indonesian-roberta-base-sentiment-classifier`) untuk mendapatkan rating sentimen (1-5 stars).
   - **Output:** File final `data/results.csv` yang diperkaya dengan data sentimen dan siap untuk divisualisasikan.

**4. Stasiun Visualisasi (Dashboard)**
   - **`dashboard.py`:** Aplikasi Streamlit yang membaca file `results.csv`.
   - **Proses:** Mengubah rating bintang menjadi label (Positif, Netral, Negatif), kemudian membuat semua visualisasi secara dinamis dan interaktif menggunakan Plotly.
   - **Output:** Sebuah dashboard web interaktif yang dapat diakses melalui browser.

## 📊 Cara Menjalankan Proyek

1.  **Clone Repository:**
    ```bash
    git clone [URL_REPOSITORY_ANDA]
    cd [NAMA_FOLDER_PROYEK]
    ```

2.  **Setup Lingkungan:**
    - Buat dan aktifkan virtual environment:
      ```bash
      python -m venv venv
      # Windows
      venv\Scripts\activate
      # macOS/Linux
      source venv/bin/activate
      ```
    - Install semua dependensi:
      ```bash
      pip install -r requirements.txt
      ```

3.  **Konfigurasi Kredensial:**
    - Edit file bernama `config.py` di folder utama.
    - Isi file tersebut dengan API Key YouTube Anda:
      ```
      YT_API_KEY="AIzaSyXXXXXXXXXXXXXXXX"
      ```

4.  **Jalankan Pipeline (Bertahap):**
    - **(Wajib) Kumpulkan data:**
      ```bash
      python main.py
      ```

5.  **Tampilkan Dashboard:**
    ```bash
    streamlit run dashboard/app.py
    ```
    Buka URL yang ditampilkan di terminal pada browser Anda.

## 💡 Hasil & Kesimpulan Awal

Berdasarkan analisis data yang telah terkumpul, beberapa temuan awal yang menarik adalah:
- **Kinerja Manchester United di bawah Ruben Amorim** menunjukkan peningkatan dalam beberapa aspek, namun masih memicu reaksi beragam dari publik.
- **Media olahraga global** cenderung menulis dengan nada netral dan analitis, berfokus pada taktik, rotasi pemain, serta hasil pertandingan.
- **Opini publik di YouTube** jauh lebih emosional — kombinasi antara dukungan antusias terhadap perubahan gaya bermain dan kritik terhadap inkonsistensi hasil.
- **WordCloud** memperlihatkan kata dominan seperti “style”, “progress”, “pressing”, “structure”, serta “frustrating” yang mencerminkan narasi umum seputar performa tim.
- **Grafik tren sentimen** memperlihatkan peningkatan sentimen positif pasca kemenangan besar, serta lonjakan negatif setelah kekalahan penting.

## Kesimpulan
Proyek ini berhasil menunjukkan bagaimana analisis sentimen berbasis NLP dan scraping multi-platform dapat memberikan pemahaman lebih dalam terhadap dampak kepemimpinan Ruben Amorim di Manchester United — baik dari sudut pandang media profesional maupun reaksi emosional fans.

