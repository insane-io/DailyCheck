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
API_URL = os.getenv("BACKEND_URL") + "/daily-tasks"

async def send_daily_plate():
    bot = Bot(token=TELEGRAM_TOKEN)
    response = requests.get(API_URL).json()
    
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
    # job() 
    
    while True:
        schedule.run_pending()
        time.sleep(60)