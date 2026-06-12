import os
import requests
from bs4 import BeautifulSoup
import json

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



def check_stock(url):

    alias = url.split("/")[-1]

    api_url = (
        "https://shop.amul.com/api/1/entity/ms.products"
        f'?q={{"alias":"{alias}"}}&limit=1'
    )

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "frontend": "1",
        "Referer": url,
        "base_url": url
    }

    response = requests.get(
        api_url,
        headers=headers,
        timeout=30
    )

    print("Status:", response.status_code)
    print(response.text[:1000])

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
