import requests
from fake_useragent import UserAgent
from telegram import Bot
import time
from config import TELEGRAM_TOKEN, CHAT_ID

url = "https://clob.polymarket.com/last-trade-price?token_id=74180574891940211586540652408963663559079632808239698566399710384857667960547"


PRICE_THRESHOLD_PERCENTAGE = 5

previous_price = None

def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

def check_price(seconds):
    global previous_price
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        current_price = float(json_data.get("price", 0))

        if previous_price is not None:
            price_difference = current_price - previous_price
            percentage_change = (price_difference / previous_price) * 100
            if (seconds - 30) % 3600 == 0:
                message = f"Current Price: {current_price}\nPercentage Change: {percentage_change}"
                send_telegram_message(message)


            if percentage_change >= PRICE_THRESHOLD_PERCENTAGE:
                message = f"Price increased by {percentage_change:.2f}% in the last hour. Current price: {current_price}"
                k = 0
                while k <= 10:
                    send_telegram_message(message)

        if seconds % 3600 == 0:
          previous_price = current_price
          print(previous_price)

    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    print("Start script")
    i = 0
    while True:
        check_price(i)
        time.sleep(30)
        i +=30
        
