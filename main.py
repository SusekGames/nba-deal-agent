import requests
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

response = requests.post(
    WEBHOOK,
    json={
        "content": "🔥 TEST MESSAGE FROM NBA BOT"
    }
)

print(response.status_code)
print(response.text)