from playwright.sync_api import sync_playwright
import requests
import os
import json
import re
import time

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

URL = "https://www.nbastore.eu/en/men-jerseys-sale-items"

DB_FILE = "sent_products.json"

TARGET_SIZE = "S"
MIN_DISCOUNT = 30

def send_message(msg):

    response = requests.post(
        WEBHOOK,
        json={"content": msg}
    )

    print("Discord status:", response.status_code)

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

    print("Collecting products...")

    links = page.locator("a").evaluate_all(
        """elements => elements.map(el => ({
            text: el.innerText,
            href: el.href
        }))"""
    )

    found_any = False

    checked_links = []

    for item in links:

        try:

            text = item["text"]
            link = item["href"]

            if not text:
                continue

            if not link:
                continue

            if "Mitchell & Ness" not in text:
                continue

            if "Jersey" not in text:
                continue

            if not link.startswith("http"):
                continue

            if link in checked_links:
                continue

            checked_links.append(link)

            print(f"Checking: {link}")

            prices = re.findall(r'\d+[.,]?\d*', text)

            prices = [
                float(p.replace(",", "."))
                for p in prices
            ]

            if len(prices) < 2:
                continue

            current_price = min(prices)
            old_price = max(prices)

            discount = round(
                100 - ((current_price / old_price) * 100),
                2
            )

            print(
                f"Price: {current_price} / {old_price} | Discount: {discount}%"
            )

            if discount < MIN_DISCOUNT:
                continue

            product_page = browser.new_page()

            product_page.goto(link, timeout=60000)

            product_page.wait_for_timeout(5000)

            product_text = product_page.locator("body").inner_text()

            product_page.close()

            if (
                f"Size:{TARGET_SIZE}" not in product_text
                and f"\n{TARGET_SIZE}\n" not in product_text
            ):

                print(f"Size {TARGET_SIZE} not available")
                continue

            if "Out of Stock" in product_text:

                print("Product out of stock")
                continue

            if link in sent_products:

                print("Already sent")
                continue

            message = f"""
🔥 NBA DEAL ALERT

🏀 {text[:200]}

📏 Size {TARGET_SIZE} Available

💸 {current_price}€
📉 -{discount}%

🔗 {link}
"""

            send_message(message)

            print("Deal sent to Discord")

            sent_products.append(link)

            found_any = True

            time.sleep(2)

        except Exception as e:

            print("ERROR:", e)

    save_sent(sent_products)

    if not found_any:

        send_message(
            f"ℹ️ Bot działa poprawnie, ale nie znaleziono nowych promocji Mitchell & Ness w rozmiarze {TARGET_SIZE} (-30% lub więcej)."
        )

    browser.close()

    print("BOT FINISHED")