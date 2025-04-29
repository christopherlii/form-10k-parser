import torch
import pickle
import json
from transformers import BertTokenizer, BertForSequenceClassification
import os

with open("../models/logistic_model.pkl", "rb") as f:
    logistic_model = pickle.load(f)

with open("../models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

bert_model = BertForSequenceClassification.from_pretrained("../models/bert_model")
tokenizer = BertTokenizer.from_pretrained("../models/bert_model")
bert_model.eval()

from preprocess import preprocess_10k

if __name__ == "__main__":
    filepath = "../data/amazon_10k.html"  

    if not os.path.exists(filepath):
        print("Amazon 10-K not found. Please download it first.")
        exit(1)

    paragraphs = preprocess_10k(filepath)
    print(f"Loaded {len(paragraphs)} paragraphs to predict.")

    results = []

    for para in paragraphs:
        X = vectorizer.transform([para])
        pred_logistic = logistic_model.predict(X)[0]

        inputs = tokenizer(para, return_tensors="pt", truncation=True, padding=True, max_length=256)
        with torch.no_grad():
            outputs = bert_model(**inputs)
        logits = outputs.logits
        pred_bert = torch.argmax(logits, dim=1).item()

        results.append({
            "paragraph": para,
            "logistic_prediction": int(pred_logistic),
            "bert_prediction": int(pred_bert)
        })

    os.makedirs("../predictions", exist_ok=True)
    with open("../predictions/amazon_predictions.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Saved predictions to ../predictions/amazon_predictions.json!")