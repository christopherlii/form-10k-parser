import json
from sklearn.metrics import classification_report

# Load model predictions
with open("predicted_labels/qualcomm_10k_predicted_logistics.json", "r", encoding="utf-8") as f:
    predicted_data = json.load(f)

# Load ground-truth labels
with open("ai_labeled/qualcomm_labeled_ai_batch.json", "r", encoding="utf-8") as f:
    true_data = json.load(f)

# Safe matching based on paragraph content
predicted_texts = [item["paragraph"].strip() for item in predicted_data]
predicted_labels = [item["predicted_label"] for item in predicted_data]

true_texts = [item["paragraph"].strip() for item in true_data]
true_labels = [item["label"] for item in true_data]

# Align by paragraph content (paragraphs must match)
matched_preds = []
matched_truths = []

for true_para, true_label in zip(true_texts, true_labels):
    if true_para in predicted_texts:
        idx = predicted_texts.index(true_para)
        matched_preds.append(predicted_labels[idx])
        matched_truths.append(true_label)
    else:
        print(f"⚠️ Missing paragraph in predictions: {true_para[:50]}...")

# Now they are guaranteed same length
print(f"\n✅ Matched {len(matched_preds)} paragraphs for evaluation!")

# Compute report
print("\n📈 Evaluation comparing predictions vs ground truth:\n")
print(classification_report(matched_truths, matched_preds, digits=4))
