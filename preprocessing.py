import re
import string
import nltk
from nltk.corpus import stopwords

# download stopwords Indo (sekali saja)
nltk.download("stopwords")
stop_words = set(stopwords.words("indonesian"))

def clean_text(text: str) -> str:
    """
    Bersihkan tweet dari url, mention, hashtag, angka, dan stopwords
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)  # hapus URL
    text = re.sub(r"@\w+", "", text)  # hapus mention
    text = re.sub(r"#\w+", "", text)  # hapus hashtag
    text = re.sub(r"\d+", "", text)  # hapus angka
    text = text.translate(str.maketrans("", "", string.punctuation))  # hapus tanda baca
    text = text.strip()

    # hapus stopwords
    tokens = [word for word in text.split() if word not in stop_words]
    return " ".join(tokens)