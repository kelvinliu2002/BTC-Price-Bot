import os
import csv
from binance import Client, exceptions
from dotenv import load_dotenv
import pandas as pd
import time
import datetime


load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

BTC_SYMBOL = "BTCUSDT"
DATA_DIR = "price_data"
CSV_FILE = os.path.join(DATA_DIR, f"{BTC_SYMBOL}".csv)

client = Client(API_KEY, API_SECRET)


def main():
    while True:
        price = get_btc_price()
        if price:
            store_price_data(price)
        else:
            time.sleep(60)


def get_btc_price(symbol=BTC_SYMBOL):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])
    except exceptions.BinanceAPIException as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

def store_price_data(price, symbol=BTC_SYMBOL):
    timestamp = datetime.datetime.now()

    os.makedirs(DATA_DIR, exist_ok=True)

    try:
        with open(CSV_FILE, "x", newline="") as csvfile:
            fieldnames = ["Timestamp", "Symbol", "Price"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass

    with open(CSV_FILE, "a", newline="") as csvfile:
        fieldnames = ["Timestamp", "Symbol", "Price"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"Timestamp": timestamp, "Symbool": symbol, "Price": price})



if __name__ == "__main__":
    main()