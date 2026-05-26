from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

URL = "https://www.nbastore.eu/en/men-jerseys-sale-items"

def send_message(msg):

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    page.goto(URL, timeout=60000)

    page.wait_for_timeout(5000)

    soup = BeautifulSoup(page.content(), "lxml")

    products = soup.select(".product-card")

    for product in products:

        try:

            title = product.select_one(
                ".product-card-title"
            ).text.strip()

            if "Mitchell & Ness" not in title:
                continue

            current_price = float(
                product.select_one(".sales")
                .text.replace("€", "")
                .strip()
            )

            old_price = float(
                product.select_one(".was-price")
                .text.replace("€", "")
                .strip()
            )

            discount = round(
                100 - ((current_price / old_price) * 100),
                2
            )

            if discount < 30:
                continue

            link = (
                "https://www.nbastore.eu" +
                product.select_one("a")["href"]
            )

            message = f'''
🔥 NBA DEAL

{title}

💸 {current_price}€
📉 -{discount}%

🔗 {link}
'''

            send_message(message)

        except:
            continue

    browser.close()