import csv
import re
from collections import Counter
from datetime import datetime
import os

from config import (
    QUERY, TARGET_TWEETS, REPLIES_PER_TWEET, ALLOWED_LANGS,
    RESULTS_FILE, KEYWORDS_FILE, CHROMEDRIVER_PATH, HEADLESS,
    YT_MAX_VIDEOS, YT_MAX_COMMENTS_API,
    YOUTUBE_API_KEY
)

from modules.twitter_login import twitter_login
from modules.twitter_scraper import scrape_twitter_search, scrape_replies_for_tweet
from sentiment import analyze_sentiment
from modules.yt_api import search_videos, get_youtube_comments

# selenium imports
import undetected_chromedriver as uc


def save_results(data, filename, append=False):
    # Gunakan .empty untuk mengecek apakah DataFrame kosong
    if data.empty: # <--- SOLUSI
        print("⚠️ Data kosong, tidak ada yang disimpan.")
        return
    # ... kode penyimpanan lainnya

    keys = list(data[0].keys())

    # Jika file belum ada, tulis header
    write_header = not os.path.exists(filename) or not append

    mode = "a" if append and os.path.exists(filename) else "w"
    with open(filename, mode, newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        if write_header:
            writer.writeheader()
        writer.writerows(data)

    print(f"✅ Hasil {'ditambahkan' if append else 'disimpan'} ke {filename}")


def extract_keywords(data, filename, top_n=30):
    """Ekstrak keyword dari kolom text."""
    all_words = []
    for d in data:
        text = d.get("text", "").lower()
        words = re.findall(r'\w+', text)
        all_words.extend(words)

    freq = Counter(all_words).most_common(top_n)
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "frequency"])
        writer.writerows(freq)
    print(f"✅ Keyword frequency disimpan ke {filename}")


def create_driver():
    """Buat Chrome driver undetected."""
    options = uc.ChromeOptions()
    if HEADLESS:
        options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = uc.Chrome(options=options)
    except Exception:
        driver = uc.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    driver.set_window_size(1200, 900)
    return driver


def add_metadata(item, source):
    """Tambahkan metadata timestamp & source ke setiap item."""
    item["timestamp"] = datetime.utcnow().isoformat()
    item["source"] = source
    return item


def main():
    print("🚀 Mulai crawling (Twitter + YouTube API)...")
    all_data = []

    # === Twitter ===
    driver = None
    twitter_data = []
    try:
        driver = create_driver()
        print("🔹 Login Twitter...")
        ok = twitter_login(driver, "USERNAME", "PASSWORD", recovery_info=None)
        if ok:
            print("🔹 Crawling Twitter search...")
            tweets = scrape_twitter_search(
                driver,
                QUERY,
                max_tweets=TARGET_TWEETS,
                allowed_langs=ALLOWED_LANGS
            )
            for t in tweets:
                twitter_data.append(add_metadata(t, "twitter"))

                url = t.get("url", "")
                if url:
                    replies = scrape_replies_for_tweet(
                        driver,
                        url,
                        max_replies=REPLIES_PER_TWEET,
                        allowed_langs=ALLOWED_LANGS
                    )
                    for r in replies:
                        twitter_data.append(add_metadata(r, "twitter"))

            print(f"✅ Twitter sukses: {len(twitter_data)} item")
        else:
            print("⚠️ Login Twitter gagal — lanjut ke YouTube API.")
    except Exception as e:
        print(f"⚠️ Crawling Twitter error: {e} — lanjut ke YouTube API.")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass

    # === YouTube (API only) ===
    youtube_data = []
    try:
        if YOUTUBE_API_KEY and len(YOUTUBE_API_KEY) > 10:
            print("🔹 Crawling YouTube via API...")
            video_ids = search_videos(YOUTUBE_API_KEY, QUERY, max_results=YT_MAX_VIDEOS)
            for vid in video_ids:
                print(f"  ▶️ Ambil komentar dari video: {vid}")
                comments = get_youtube_comments(
                    YOUTUBE_API_KEY,
                    vid,
                    max_comments=YT_MAX_COMMENTS_API,
                    allowed_langs=ALLOWED_LANGS
                )
                for c in comments:
                    youtube_data.append(add_metadata(c, "youtube"))

            print(f"✅ YouTube API sukses: {len(youtube_data)} komentar")
        else:
            print("⚠️ Tidak ada API Key YouTube, skip YouTube crawling.")
    except Exception as e:
        print(f"⚠️ Gagal crawl YouTube API: {e}")

    # Gabungkan data
    all_data.extend(twitter_data)
    all_data.extend(youtube_data)

    print(f"✅ Total items collected (Twitter+YouTube): {len(all_data)}")
    if not all_data:
        print("⚠️ Tidak ada data untuk dianalisis.")
        return

    # === Sentiment Analysis ===
    analyzed = analyze_sentiment(all_data)

    # === Save & Keywords ===
    save_results(analyzed, RESULTS_FILE, append=True)  # ⬅️ append biar data fresh terus
    extract_keywords(analyzed, KEYWORDS_FILE)

    print("🎉 Selesai — Jalankan dashboard dengan:")
    print("👉  streamlit run dashboard.py")


if __name__ == "__main__":
    main()
