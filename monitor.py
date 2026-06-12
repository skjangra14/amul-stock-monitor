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

    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    text = r.text.lower()

    for word in [
        "notify me",
        "add to cart",
        "buy now",
        "sold out",
        "out of stock"
    ]:
        print(word, "=>", word in text)

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
