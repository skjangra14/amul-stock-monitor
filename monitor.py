import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCTS = {
    "Plain Lassi":
    "https://shop.amul.com/en/product/amul-high-protein-plain-lassi-200-ml-or-pack-of-30",

    "Rose Lassi":
    "https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30"
}


def send_telegram(message):

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


def check_stock(page, url):

    page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    content = page.content().lower()

    if "sold out" in content:
        return False

    if "notify me" in content:
        return False

    return True


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    for name, url in PRODUCTS.items():

        available = check_stock(
            page,
            url
        )

        print(name, available)

        if available:

            send_telegram(
                f"🚨 AMUL STOCK ALERT 🚨\n\n"
                f"{name} is available!\n\n"
                f"{url}"
            )

    browser.close()
