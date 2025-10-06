# sentimen.py
from langdetect import detect
from textblob import TextBlob
import pandas as pd

# Dummy IndoBERT → ganti dengan model IndoBERT asli jika tersedia
def predict_sentiment_indo(text: str):
    """
    Prediksi sentimen untuk teks bahasa Indonesia (dummy).
    """
    text_lower = text.lower()
    if "bagus" in text_lower:
        return "Positive", 0.9
    elif "jelek" in text_lower:
        return "Negative", -0.9
    else:
        return "Neutral", 0.0

def analyze_sentiment(tweets):
    """
    tweets: list of dict, tiap dict minimal punya 'text' dan optional 'lang' dan 'timestamp'.
    Mengembalikan DataFrame dengan kolom:
    ['text', 'lang', 'timestamp', 'sentiment', 'score']
    """
    analyzed = []
    for t in tweets:
        text = t.get("text", "")
        lang = t.get("lang")
        timestamp = t.get("timestamp")

        # Jika lang tidak tersedia, deteksi otomatis
        if not lang:
            try:
                lang = detect(text)
            except:
                lang = "id"  # default

        # Analisis sentimen
        if lang == "id":
            label, score = predict_sentiment_indo(text)
        else:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0:
                label, score = "Positive", polarity
            elif polarity < 0:
                label, score = "Negative", polarity
            else:
                label, score = "Neutral", polarity

        # Pastikan timestamp datetime
        if timestamp:
            timestamp = pd.to_datetime(timestamp, errors="coerce")
        else:
            timestamp = pd.Timestamp.now()

        # Normalisasi label agar konsisten
        label = label.capitalize()  # Positive, Neutral, Negative

        analyzed.append({
            "text": text,
            "lang": lang,
            "timestamp": timestamp,
            "sentiment": label,
            "score": score
        })

    # Kembalikan sebagai DataFrame
    df = pd.DataFrame(analyzed)
    return df

if __name__ == "__main__":
    # Contoh penggunaan
    tweets_example = [
        {"text": "Ini produk bagus sekali!", "lang": "id", "timestamp": "2025-10-06 09:00:00"},
        {"text": "I hate this!", "lang": "en", "timestamp": "2025-10-06 09:05:00"},
        {"text": "Biasa saja", "lang": "id", "timestamp": "2025-10-06 09:10:00"},
        {"text": "Je lekt sekali", "timestamp": "id"}  # tanpa lang
    ]

    df_sentiment = analyze_sentiment(tweets_example)
    print(df_sentiment)
