from langdetect import detect
from textblob import TextBlob

# Dummy IndoBERT → disini seharusnya model asli IndoBERT
def predict_sentiment_indo(text: str):
    if "bagus" in text.lower():
        return "Positive", 0.9
    elif "jelek" in text.lower():
        return "Negative", -0.9
    return "Neutral", 0.0


def analyze_sentiment(tweets):
    analyzed = []
    for t in tweets:
        text = t["text"]
        lang = t["lang"]

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

        analyzed.append({
            "text": text,
            "lang": lang,
            "sentiment": label,
            "score": score
        })
    return analyzed
