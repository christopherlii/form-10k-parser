# notebooks/predict_logistics.py

import os
import pickle
import json
from preprocess import preprocess_10k
from sklearn.metrics import classification_report

# 📚 1. Load model and vectorizer
with open("models/logistic_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# 📚 2. Load and preprocess new 10-K
# Change this path to whichever new 10-K you want to predict
new_10k_path = "data/qualcomm_10k.html"

paragraphs = preprocess_10k(new_10k_path)

print(f"Loaded {len(paragraphs)} paragraphs from {new_10k_path}.")

# 📚 3. Vectorize
X_new = vectorizer.transform(paragraphs)

# 📚 4. Predict
preds = model.predict(X_new)

# 📚 5. Save predictions
output_data = [{"paragraph": para, "predicted_label": int(label)} for para, label in zip(paragraphs, preds)]

save_name = os.path.basename(new_10k_path).replace(".html", "_predicted_logistics.json")
save_path = os.path.join("predicted_labels", save_name)

with open(save_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2)

print(f"✅ Saved predictions to {save_path}")

# 📚 6. (Optional) Evaluation if you have ground truth
# If you already manually labeled the new 10-K, you can evaluate automatically:

ground_truth_path = new_10k_path.replace(".html", "_labeled_ai_batch.json")

if os.path.exists(ground_truth_path):
    with open(ground_truth_path, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)
    true_labels = [item["label"] for item in ground_truth if item["label"] != -1]

    # align paragraph count
    if len(true_labels) == len(preds):
        print("\n📈 Evaluation Report (vs ground truth):")
        print(classification_report(true_labels, preds, digits=4))
    else:
        print("\n⚠️ Ground truth and prediction lengths do not match. Skipping evaluation.")
