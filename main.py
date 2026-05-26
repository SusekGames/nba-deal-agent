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

    browser = p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )

    context = browser.new_context(
        user_agent="""
Mozilla/5.0 (Windows NT 10.0; Win64; x64)
AppleWebKit/537.36 (KHTML, like Gecko)
Chrome/124.0.0.0 Safari/537.36
"""
    )

    page = context.new_page()

    page.add_init_script("""
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
""")

    print("Opening product...")

    page.goto(TEST_PRODUCT, timeout=60000)

    page.wait_for_timeout(10000)

    body_text = page.locator("body").inner_text()

    chunk = body_text[:1500]

    print(chunk)

    send_message(
        f"DEBUG PAGE:\n\n{chunk}"
    )

    browser.close()