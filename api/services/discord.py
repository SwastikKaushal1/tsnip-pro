import requests
import os

def send_discord_webhook(payload):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url or webhook_url == "your_discord_webhook_url_here":
        print("Error: Discord Webhook URL is missing or invalid.")
        return False
        
    response = requests.post(webhook_url, json=payload)
    return response.status_code == 204