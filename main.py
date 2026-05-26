import requests
import json
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

API_URL = "https://www.nbastore.eu/api/search"

DB_FILE = "sent_products.json"

TARGET_SIZES = ["S", "M"]

MIN_DISCOUNT = 30

def send_message(msg):

    response = requests.post(
        WEBHOOK,
        json={"content": msg}
    )

    print("Discord:", response.status_code)

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

headers = {
    "User-Agent":
    "Mozilla/5.0"
}

params = {
    "query": "Mitchell and Ness jersey"
}

print("Fetching products...")

response = requests.get(
    API_URL,
    headers=headers,
    params=params,
    timeout=30
)

print("Status:", response.status_code)

if response.status_code != 200:

    send_message(
        f"❌ NBA Store API Error: {response.status_code}"
    )

    exit()

try:

    data = response.json()

except Exception as e:

    send_message(
        f"❌ JSON ERROR: {e}"
    )

    exit()

found_any = False

products = data.get("products", [])

print("Products found:", len(products))

for product in products:

    try:

        name = product.get("name", "")

        if "Mitchell" not in name:
            continue

        if "Jersey" not in name:
            continue

        current_price = float(
            product.get("salePrice", 0)
        )

        old_price = float(
            product.get("price", 0)
        )

        if old_price <= 0:
            continue

        discount = round(
            100 - ((current_price / old_price) * 100),
            2
        )

        if discount < MIN_DISCOUNT:
            continue

        available_sizes = product.get(
            "availableSizes",
            []
        )

        size_match = any(
            size in TARGET_SIZES
            for size in available_sizes
        )

        if not size_match:
            continue

        link = (
            "https://www.nbastore.eu" +
            product.get("url", "")
        )

        if link in sent_products:
            continue

        message = f"""
🔥 NBA DEAL ALERT

🏀 {name}

📏 Sizes: {", ".join(available_sizes)}

💸 {current_price}€
📉 -{discount}%

🔗 {link}
"""

        send_message(message)

        sent_products.append(link)

        found_any = True

    except Exception as e:

        print("ERROR:", e)

save_sent(sent_products)

if not found_any:

    send_message(
        "ℹ️ Bot działa poprawnie, ale nie znaleziono nowych promocji Mitchell & Ness."
    )

print("BOT FINISHED")