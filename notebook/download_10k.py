# notebooks/download_10k.py

import os
import requests

def download_10k(url, save_path):
    """
    Downloads a 10-K filing directly from a full SEC HTML URL.
    """
    headers = {
        "User-Agent": "NLPFinalProject/1.0 (christopherli@nyu.edu)"  # Replace with your email
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Downloaded and saved to {save_path}")
    else:
        print(f"❌ Failed to download {url}. Status code: {response.status_code}")

"""
Follow this format for the companies: 

{
    "name": "Apple",
    "url": "https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm",
    "save_path": "data/apple_10k.html"
},
"""

if __name__ == "__main__":
    companies = [
        #look at comment above
        {
            "name": "Doordash",
            "url": "https://www.sec.gov/Archives/edgar/data/1792789/000162828023005131/dash-20221231.htm",
            "save_path": "data/doordash_10k.html"
        },

        
        
    ]

    for company in companies:
        print(f"Downloading {company['name']} 10-K...")
        download_10k(company["url"], company["save_path"])
