import requests
import schedule
import time
import asyncio
from telegram import Bot
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = BACKEND_URL.rstrip("/") + "/daily-tasks"


def wait_for_backend(max_attempts: int = 12, interval_seconds: int = 5) -> bool:
    """Wait for the backend to become reachable before sending the first message."""
    for _ in range(max_attempts):
        try:
            resp = requests.get(API_URL, timeout=5)
            resp.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            time.sleep(interval_seconds)
    return False

async def send_daily_plate():
    bot = Bot(token=TELEGRAM_TOKEN)
    try:
        resp = requests.get(API_URL, timeout=10)
        resp.raise_for_status()
        response = resp.json()
    except requests.exceptions.RequestException:
        await bot.send_message(chat_id=CHAT_ID, text="Backend is unavailable, please try again later.")
        return
    
    if "message" in response:
        await bot.send_message(chat_id=CHAT_ID, text=response["message"])
        return

    message = f"🍽️ **Here is your daily plate ({response['day_type']}):**\n\n"
    for task in response["tasks"]:
        message += f"[{task['category']}] - {task['description']}\n{task['url']}\n\n"
    message += "Do not think. Just execute."

    await bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

def job():
    asyncio.run(send_daily_plate())

schedule.every().day.at("08:00").do(job)

if __name__ == "__main__":
    print("Drill Sergeant Bot is running and waiting for the scheduled time...")
    # Give the API some time to start when containers boot together
    if wait_for_backend():
        job()
    else:
        print("Backend is unavailable after multiple attempts; will try again at the scheduled time.")
    
    while True:
        schedule.run_pending()
        time.sleep(60)