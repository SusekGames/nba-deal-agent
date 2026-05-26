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

    print("Opening page...")

    page.goto(URL, timeout=60000)

    page.wait_for_timeout(10000)

    print("Page loaded")

    content = page.content()

    print(content[:5000])

    soup = BeautifulSoup(content, "html.parser")

    send_message("✅ BOT IS WORKING")

    browser.close()