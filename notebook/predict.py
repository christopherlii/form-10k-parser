# notebooks/predict.py

import torch
import pickle
from transformers import BertTokenizer, BertForSequenceClassification

# Load the models you trained

# Logistic Regression model
with open("../models/logistic_model.pkl", "rb") as f:
    logistic_model = pickle.load(f)

with open("../models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# BERT model
bert_model = BertForSequenceClassification.from_pretrained("../models/bert_model")
tokenizer = BertTokenizer.from_pretrained("../models/bert_model")

# Put BERT in evaluation mode
bert_model.eval()

def predict_logistic(paragraph):
    """
    Predict using logistic regression model.
    """
    X = vectorizer.transform([paragraph])
    pred = logistic_model.predict(X)
    return pred[0]

def predict_bert(paragraph):
    """
    Predict using fine-tuned BERT model.
    """
    inputs = tokenizer(paragraph, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    logits = outputs.logits
    prediction = torch.argmax(logits, dim=1).item()
    return prediction

if __name__ == "__main__":
    print("\nWelcome to the Financial Highlight Classifier!\n")
    print("Type a paragraph and see if it is a Financial Highlight (1) or Not (0).\n")
    print("Type 'exit' to quit.\n")

    while True:
        paragraph = input("Enter a paragraph: ")

        if paragraph.lower() == "exit":
            break

        pred_logistic = predict_logistic(paragraph)
        pred_bert = predict_bert(paragraph)

        print("\n[Logistic Model Prediction]", "Financial Highlight ✅" if pred_logistic == 1 else "Not Highlight ❌")
        print("[BERT Model Prediction]", "Financial Highlight ✅" if pred_bert == 1 else "Not Highlight ❌")
        print("-" * 60)
