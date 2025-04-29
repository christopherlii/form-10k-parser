from bs4 import XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

from bs4 import BeautifulSoup
import re
import os

def preprocess_10k(filepath):
    """
    Parses and splits a 10-K HTML into paragraphs.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")
    text = soup.get_text(separator="\n")

    text = re.sub(r'\xa0', ' ', text)
    text = re.sub(r'\s+\n', '\n', text)

    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 50]

    return paragraphs

if __name__ == "__main__":
    filepath = "../data/amazon_10k.html"
    if os.path.exists(filepath):
        sections = preprocess_10k(filepath)
        print(f"Found {len(sections)} paragraphs!")
        print("Example:", sections[0][:300], "...")
    else:
        print("File not found! Please download the 10-K first.")