import csv
import time
import re
from datetime import datetime
from collections import Counter

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from langdetect import detect

# ✅ tambahkan RECOVERY_INFO juga
from config import USERNAME_TWITTER, PASSWORD_TWITTER, QUERY, TARGET_TWEETS, ALLOWED_LANGS, RECOVERY_INFO  
from modules.twitter_login import twitter_login
from modules.sentiment import analyze_sentiment
from modules.visualization import visualize_results
from modules.news_crawler import crawl_goal

# === CRAWLING TWITTER ===
def crawl_tweets(driver, query, max_tweets=100):
    print("🔍 Mulai crawling Twitter...")
    search_url = f"https://twitter.com/search?q={query}&src=typed_query&f=live"
    driver.get(search_url)
    time.sleep(3)

    tweets_data = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(tweets_data) < max_tweets:
        tweets = driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')

        for t in tweets:
            text = t.text.strip()
            if text not in [d["text"] for d in tweets_data]:
                try:
                    lang = detect(text)
                except:
                    lang = "unknown"

                if lang in ALLOWED_LANGS:
                    tweets_data.append({
                        "text": text,
                        "lang": lang,
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "source": "Twitter"
                    })

        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        print(f"📊 Jumlah tweet terkumpul: {len(tweets_data)}")

    return tweets_data[:max_tweets]


# === SIMPAN CSV ===
def save_results(data, filename="data/results.csv"):
    if not data:
        print("⚠️ Tidak ada data untuk disimpan.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Hasil disimpan ke {filename}")


# === EKSTRAK KEYWORDS ===
def extract_keywords(tweets, filename="data/keywords.csv", top_n=30):
    all_words = []
    for t in tweets:
        words = re.findall(r'\w+', t["text"].lower())
        all_words.extend(words)

    freq = Counter(all_words).most_common(top_n)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "frequency"])
        writer.writerows(freq)

    print(f"✅ Keyword frequency disimpan ke {filename}")


# === MAIN ===
def main():
    print("🚀 Mulai crawling data...")

    # Setup driver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    # Login Twitter
    if not twitter_login(driver, USERNAME_TWITTER, PASSWORD_TWITTER, RECOVERY_INFO):
        driver.quit()
        return

    # Crawl dari Twitter
    tweets = crawl_tweets(driver, QUERY, TARGET_TWEETS)

    # Crawl dari Goal.com
    news = crawl_goal("https://www.goal.com/en/news/manchester-united/1", limit=20)

    driver.quit()

    # Gabungkan hasil crawling
    all_data = tweets + news
    print(f"✅ Total data terkumpul: {len(all_data)}")

    # Analisis sentimen
    analyzed = analyze_sentiment(all_data)

    # Simpan hasil ke CSV
    save_results(analyzed, "data/results.csv")

    # Visualisasi hasil
    visualize_results("data/results.csv")

    print("🎉 Selesai! Dashboard interaktif ditampilkan.")


if __name__ == "__main__":
    main()
