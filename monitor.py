import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCTS = {
    "Plain Lassi": "https://shop.amul.com/en/product/amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    "Rose Lassi": "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
}

def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": message}
    )

import json

def check_stock(url):

    api_url = (
        "https://shop.amul.com/api/1/entity/ms.products"
        '?q={"alias":"amul-high-protein-rose-lassi-200-ml-or-pack-of-30"}&limit=1'
    )

    response = requests.get(api_url, timeout=30)

    print("Status:", response.status_code)

    data = response.json()

    print(json.dumps(data, indent=2)[:5000])

    return False
    
for name, url in PRODUCTS.items():

    print(f"Checking {name}")
    print(url)

    result = check_stock(url)

    print(f"Available = {result}")

    if result:
        send_telegram(
            f"🚨 STOCK AVAILABLE 🚨\n\n{name}\n\n{url}"
        )
