import os
import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# 1. Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR    = os.path.join(PROJECT_ROOT, "ai_labeled")
MODEL_DIR   = os.path.join(PROJECT_ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

# 2. Load every company’s JSON
companies = [
    "airbnb", "alphabet", "apple", "coinbase", "datadog",
    "microsoft", "netflix", "nvidia", "palantir", "panw",
    "salesforce", "tesla"
]

texts, labels = [], []
for company in companies:
    path = os.path.join(DATA_DIR, f"{company}_labeled_ai_batch.json")
    if not os.path.exists(path):
        print(f"⚠️  Missing file: {path}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        batch = json.load(f)
    for item in batch:
        texts.append(item["paragraph"])
        labels.append(item["label"])

# 3. Vectorize on all data
vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1,2))
X_all = vectorizer.fit_transform(texts)

# 4. Train on 100% of your data
model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_all, labels)

# 5. Save model & vectorizer
with open(os.path.join(MODEL_DIR, "logistic_model.pkl"), "wb") as f:
    pickle.dump(model, f)
with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "wb") as f:
    pickle.dump(vectorizer, f)

print(f"✅ Trained on all {len(texts)} samples and saved artifacts to '{MODEL_DIR}'")
