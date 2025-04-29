# notebooks/auto_label_zero.py

import os
import json
from preprocess import preprocess_10k

if __name__ == "__main__":
    filepaths = [
        ("../data/apple_10k.html", "../data/apple_labels.json"),
        ("../data/microsoft_10k.html", "../data/microsoft_labels.json"),
        ("../data/alphabet_10k.html", "../data/alphabet_labels.json"),
        ("../data/nvidia_10k.html", "../data/nvidia_labels.json"),
        ("../data/tesla_10k.html", "../data/tesla_labels.json"),
        ("../data/coinbase_10k.html", "../data/coinbase_labels.json"),
        ("../data/netflix_10k.html", "../data/netflix_labels.json"),
        ("../data/datadog_10k.html", "../data/datadog_labels.json"),
        ("../data/salesforce_10k.html", "../data/salesforce_labels.json"),
        ("../data/palantir_10k.html", "../data/palantir_labels.json"),
        ("../data/spotify_10k.html", "../data/spotify_labels.json"),
    ]

    for filepath, savepath in filepaths:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}. Please run download_10k.py first to get the 10-K.")
            continue

        paragraphs = preprocess_10k(filepath)
        labeled_data = []

        for para in paragraphs:
            labeled_data.append({
                "paragraph": para,
                "label": 0  # Automatically label every paragraph as 0
            })

        os.makedirs(os.path.dirname(savepath), exist_ok=True)
        with open(savepath, "w", encoding="utf-8") as f:
            json.dump(labeled_data, f, indent=2)

        print(f"\n✅ All paragraphs labeled 0 and saved to {savepath}!")