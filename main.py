import requests
import json
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

API_URL = "https://www.nbastore.eu/api/search"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nbastore.eu/",
    "Origin": "https://www.nbastore.eu"
}

params = {
    "query": "Mitchell and Ness jersey"
}

def send_message(msg):

    response = requests.post(
        WEBHOOK,
        json={"content": msg}
    )

    print("Discord:", response.status_code)

print("Testing NBA API...")

try:

    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    print("STATUS:", response.status_code)

    if response.status_code != 200:

        send_message(
            f"❌ NBA API STATUS: {response.status_code}"
        )

    else:

        text = response.text[:1500]

        send_message(
            f"✅ API WORKS\n\n{text}"
        )

except Exception as e:

    send_message(
        f"❌ ERROR:\n{str(e)}"
    )