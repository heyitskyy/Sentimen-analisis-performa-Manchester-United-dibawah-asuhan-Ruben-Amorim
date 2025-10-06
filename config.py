# --- Query / target ---
QUERY = "Manchester United Ruben Amorim since:2024-11-11"
TARGET_TWEETS = 10        # target total tweet utama (tidak termasuk replies)
REPLIES_PER_TWEET = 1     # replies per tweet to fetch (0 = disable)
ALLOWED_LANGS = ["en", "id"]

# --- Selenium / driver (hanya untuk Twitter) ---
CHROMEDRIVER_PATH = "drivers/chromedriver-win64/chromedriver.exe"
HEADLESS = False           # True = headless (lebih terdeteksi). Debug pakai False.

# --- Scraping limits & safety ---
MAX_SCROLLS = 5            # maximum number of "page END" scrolls (safety)
BATCH_SAVE_EVERY = 50      # save partial CSV setiap N data
SCROLL_PAUSE = 1           # jeda antar scroll (detik)

# --- Output files ---
RESULTS_FILE = "data/results.csv"
KEYWORDS_FILE = "data/keywords.csv"

# --- YouTube API ---
# Wajib isi dengan API key dari Google Cloud Console
YOUTUBE_API_KEY = "ada de"

YT_MAX_VIDEOS = 20          # jumlah video maksimum untuk dicari berdasarkan QUERY
YT_MAX_COMMENTS_API = 2000 # batas komentar per video via API
