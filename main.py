from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import os
import json

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

URL = "https://www.nbastore.eu/en/men-jerseys-sale-items"

DB_FILE = "sent_products.json"

def send_message(msg):

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )

def load_sent():

    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_sent(data):

    with open(DB_FILE, "w") as f:
        json.dump(data, f)

sent_products = load_sent()

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("Opening NBA Store...")

    page.goto(URL, timeout=60000)

    page.wait_for_timeout(10000)

    soup = BeautifulSoup(
        page.content(),
        "html.parser"
    )

    products = soup.find_all("a")

    found_any = False

    for product in products:

        text = product.get_text(" ", strip=True)

        if "Mitchell & Ness" not in text:
            continue

        if "Men" not in text and "Jersey" not in text:
            continue

        try:

            prices = []

            for word in text.split():

                cleaned = (
                    word.replace("€", "")
                    .replace(",", ".")
                )

                try:
                    prices.append(float(cleaned))
                except:
                    pass

            if len(prices) < 2:
                continue

            current_price = min(prices)
            old_price = max(prices)

            discount = round(
                100 - ((current_price / old_price) * 100),
                2
            )

            if discount < 30:
                continue

            link = product.get("href")

            if not link:
                continue

            if link.startswith("/"):
                link = "https://www.nbastore.eu" + link

            if link in sent_products:
                continue

            message = f"""
🔥 NBA DEAL ALERT

🏀 {text[:150]}

💸 {current_price}€
📉 -{discount}%

🔗 {link}
"""

            send_message(message)

            sent_products.append(link)

            found_any = True

        except Exception as e:
            print(e)

    save_sent(sent_products)

    if not found_any:

        send_message(
            "ℹ️ Bot działa poprawnie, ale nie znaleziono nowych promocji Mitchell & Ness -30%"
        )

    browser.close()