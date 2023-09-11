import requests
import time
# import schedule
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the Telegram bot token
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")


# Binance and WazirX API endpoints
binance_api_url = 'https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT'
wazirx_api_url = 'https://api.wazirx.com/sapi/v1/ticker/24hr?symbol=dogeusdt'


# Binance and WazirX API keys
binance_api_key = 'YOUR_BINANCE_API_KEY'
wazirx_api_key = 'YOUR_WAZIRX_API_KEY'

# Set your threshold for price difference
price_difference_threshold = 0.1  # Modify as needed

# Function to fetch DogeUSDT prices from Binance and WazirX
def fetch_prices():
    try:
        binance_response = requests.get(binance_api_url)
        wazirx_response = requests.get(wazirx_api_url)

        binance_data = binance_response.json()
        wazirx_data = wazirx_response.json()

        binance_price = float(binance_data['price'])
        wazirx_price = float(wazirx_data['lastPrice'])

        return binance_price, wazirx_price
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None, None


# Function to execute a spot trade
def execute_trade(binance_price, wazirx_price):
    if binance_price is None or wazirx_price is None:
        return

    price_difference = wazirx_price - binance_price
    if price_difference >= price_difference_threshold:
        print(f"Price difference is {price_difference}, executing trade...")

        # Add your trading logic here
        # Place a spot trade on Binance or WazirX as needed

    else:
        print(f"Price difference is {price_difference}, not executing trade.")


# Function to send coin values to the Telegram bot chat
# Function to send coin values to the Telegram bot chat
def send_coin_values(bot):
    while True:
        binance_price, wazirx_price = fetch_prices()
        current_time = datetime.now().strftime('%d-%B-%y %I:%M%p')


        if binance_price is not None and wazirx_price is not None:
            price_difference = wazirx_price - binance_price
            message = f'Update on : {current_time}\nCoin :Doge - USDT \nBinance Price: {binance_price}\nWazirX Price: {wazirx_price}\nPrice Difference : {price_difference}'
        else:
            message = 'Error fetching prices.'

        bot.send_message(chat_id='-4080038826', text=message)  # Replace with your chat username
        time.sleep(1500)  # Wait for 10 seconds before sending the next update

# Initialize the Telegram bot
bot = Bot(token=telegram_bot_token)

# Start sending coin values to the bot chat
send_coin_values(bot)


# Schedule the fetch and trade job every 4 hours
# schedule.every(4).hours.do(lambda: execute_trade(*fetch_prices()))
# binance_price, wazirx_price = fetch_prices()
# execute_trade(binance_price, wazirx_price)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
