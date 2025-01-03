import os
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
CSV_FILE = os.path.join(DATA_DIR, f"{BTC_SYMBOL}.csv")

client = Client(API_KEY, API_SECRET)


def main():
    while True:
        price = get_btc_price()
        if price:
            store_price_data(price)
            time.sleep(5)
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

    new_data = pd.DataFrame([{"Timestamp": timestamp, "Symbol": symbol, "Price": price}])

    if os.path.isfile(CSV_FILE):
        # Read existing data
        df = pd.read_csv(CSV_FILE)

        # Concatenate new data to existing
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        # If file doesn't exist, use new_data as DataFrame
        df = new_data

    # Write the DataFrame to CSV
    df.to_csv(CSV_FILE, index=False)


if __name__ == "__main__":
    main()