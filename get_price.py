import os
from abc import ABC, abstractmethod
from binance import Client as BinanceClient, exceptions as binance_exceptions
from dotenv import load_dotenv
import pandas as pd
import time
import datetime
import requests

# Load .env API keys
load_dotenv()

DATA_DIR = "price_data"  # Folder to store data


class ExchangeClient(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_price_data(self):
        """Get current price and symbol from exchange"""
        pass
    
    @abstractmethod
    def get_exchange_name(self):
        """Return exchange name for file naming"""
        pass


class BinanceExchangeClient(ExchangeClient):
    def __init__(self):
        super().__init__()
    
    def get_price_data(self):
        try:
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()
            return {
                "price": float(data["price"]),
                "symbol": data["symbol"]
            }
        except Exception as e:
            print(f"Binance error occurred: {e}")
            return None
            
    def get_exchange_name(self):
        return "binance"


class OSLExchangeClient(ExchangeClient):
    def __init__(self):
        super().__init__()

    def get_price_data(self):
        try:
            url = "https://trade-hk.oslsandbox.com/api/v4/instrument?symbol=BTCUSD"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()

            for item in data:
                if item["symbol"] == "BTCUSD":
                    return {
                        "price": float(item["bidPrice"]),
                        "symbol": item["symbol"]
                    }
            return None
        except Exception as e:
            print(f"OSL error occurred: {e}")
            return None
            
    def get_exchange_name(self):
        return "osl"


class HashKeyExchangeClient(ExchangeClient):
    def __init__(self):
        super().__init__()
    
    def get_price_data(self):
        try:
            url = "https://api-pro.sim.hashkeydev.com/quote/v1/ticker/price?symbol=BTCUSD"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            data = response.json()
            for item in data:
                if item["s"] == "BTCUSD":
                    return {
                        "price": float(item["p"]),
                        "symbol": item["s"]
                    }
            return None
        except Exception as e:
            print(f"HashKey error occurred: {e}")
            return None

    def get_exchange_name(self):
        return "hashkey"


def main():
    # Initialize exchange clients
    exchanges = [
        BinanceExchangeClient(),
        OSLExchangeClient(),
        HashKeyExchangeClient()
    ]
    
    while True:
        for exchange in exchanges:
            price_data = exchange.get_price_data()
            if price_data:
                store_price_data(
                    exchange_name=exchange.get_exchange_name(),
                    price=price_data["price"],
                    symbol=price_data["symbol"]
                )
            else:
                print(f"Failed to retrieve price from {exchange.get_exchange_name()}, retrying next time")
        
        time.sleep(0.5)
        

def store_price_data(exchange_name, price, symbol):
    timestamp = datetime.datetime.now()
    
    try:
        # Ensure data directory exists
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR, exist_ok=True)
            print(f"Created directory: {DATA_DIR}")
            
        csv_file = os.path.join(DATA_DIR, f"{symbol}_{exchange_name}.csv")
        
        new_data = pd.DataFrame([{
            "Timestamp": timestamp,
            "Symbol": symbol,
            "Price": price,
        }])

        if os.path.isfile(csv_file):
            df = pd.read_csv(csv_file)
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_csv(csv_file, index=False)
    except Exception as e:
        print(f"Error storing price data: {e}")
        # Create alternative file path in current directory if data dir fails
        csv_file = f"{symbol}_{exchange_name}.csv"
        new_data.to_csv(csv_file, index=False)


if __name__ == "__main__":
    main()