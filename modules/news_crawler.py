
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from langdetect import detect


def crawl_goal(url="https://www.goal.com/en/news/manchester-united/1", limit=20):
    print("📰 Mulai crawling Goal.com...")

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"⚠️ Gagal akses {url}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("a", class_="type-article", limit=limit)

    news_data = []
    for art in articles:
        text = art.get_text(strip=True)
        if not text:
            continue

        try:
            lang = detect(text)
        except:
            lang = "unknown"

        news_data.append({
            "text": text,
            "lang": lang,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Goal.com"
        })

    print(f"✅ Jumlah berita terkumpul dari Goal.com: {len(news_data)}")
    return news_data
