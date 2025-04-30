# notebooks/batch_ai_label_paragraphs.py

import os
import json
import time
import openai
from preprocess import preprocess_10k
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

BATCH_SIZE = 10
OUTPUT_FOLDER = "ai_labeled"

def batch_classify_paragraphs(paragraphs):
    joined_paragraphs = "\n\n".join([
        f"Paragraph {i+1}:\n{para.strip()}" for i, para in enumerate(paragraphs)
    ])

    prompt = f"""
Classify each of the following paragraphs using these labels:

A financial highlight should be labeled 1. A financial highlight is often a statistic about how the company is doing.
Common examples are revenue, EBITDA, year over year, etc. Keep it to these types of stats that a casual investor can
view and quickly see how the company is doing. 

Risks should be labeled 2. Risks are potential dangers that will affect the company businesses. Do not label it a risk
unless it explicitly talks about a risk that will impact the company's reputation or revenue or impact.

Products should be labeled 3. Products are simply what the company has been working on in the past year. These paragraphs
should be specifically about certain products, ie. Google has youtube and Meta has instagram. do not something as product
if it is unclear. 

AI should be labeled 4. Make sure it is talking about AI, or an LLM, or something of the sort. do not just quote intelligence
and label that as AI.

Everything else should be labeled as 0, as that is not relevant to our user to read. Most paragraphs should be 0 unless they clearly fit one of the other categories.

Return your answer as a list of numbers separated by commas, in order.
Example: 0, 1, 2, 0, 3, 0

Paragraphs:
{joined_paragraphs}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        output = response["choices"][0]["message"]["content"].strip()
        labels = [int(label.strip()) for label in output.split(",") if label.strip() in {"0", "1", "2", "3", "4"}]
        return labels
    except Exception as e:
        print("Error batch classifying paragraphs:", e)
        return [-1] * len(paragraphs)


if __name__ == "__main__":
    files = [
        "data/qualcomm_10k.html",
    ]

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            continue

        paragraphs = preprocess_10k(filepath)
        labeled_data = []

        print(f"\n🚀 Batch classifying paragraphs in {filepath}...")

        for i in range(0, len(paragraphs), BATCH_SIZE):
            batch = paragraphs[i:i+BATCH_SIZE]

            # Handle empty paragraphs automatically
            if all(not para.strip() for para in batch):
                labels = [0] * len(batch)
            else:
                labels = batch_classify_paragraphs(batch)

            for para, label in zip(batch, labels):
                labeled_data.append({"paragraph": para, "label": label})

            print(f"Processed {min(i+BATCH_SIZE, len(paragraphs))}/{len(paragraphs)} paragraphs")
            time.sleep(0.5)  # Small delay to prevent hitting rate limits

        save_name = filepath.split("/")[-1].replace("_10k.html", "_labeled_ai_batch.json")
        save_path = os.path.join(OUTPUT_FOLDER, save_name)

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(labeled_data, f, indent=2)

        print(f"✅ Saved batch labeled paragraphs to {save_path}")