from playwright.sync_api import sync_playwright
import requests
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

TEST_PRODUCT = "https://www.nbastore.eu/en/atlanta-hawks/atlanta-hawks-mitchell-and-ness-swingman-jersey-dikembe-mutombo-1996-97/t-36474995+p-67892188162142+z-9-3254539624"

def send_message(msg):

    requests.post(
        WEBHOOK,
        json={"content": msg}
    )

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()

    print("Opening product...")

    page.goto(TEST_PRODUCT, timeout=60000)

    page.wait_for_timeout(10000)

    body_text = page.locator("body").inner_text()

    print(body_text)

    # Discord ma limit długości wiadomości
    chunk = body_text[:1800]

    send_message(
        f"DEBUG PRODUCT PAGE:\n\n{chunk}"
    )

    browser.close()