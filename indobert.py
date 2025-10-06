from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Ganti dengan model sentiment yang masih aktif
MODEL_NAME = "w11wo/indonesian-roberta-base-sentiment-classifier"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def predict_sentiment_indo(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred = torch.argmax(probs, dim=1).item()
    labels = ["negative", "neutral", "positive"]
    return labels[pred], float(probs[0][pred])
