import os
from abc import ABC, abstractmethod
from binance import Client as BinanceClient, exceptions as binance_exceptions
from dotenv import load_dotenv
import pandas as pd
import time
import datetime

# Load .env API keys
load_dotenv()

DATA_DIR = "price_data"  # Folder to store data
BTC_SYMBOL = "BTCUSDT"  # Trading pair for Binance (will be mapped for other exchanges)

class ExchangeClient(ABC):
    def __init__(self, symbol):
        self.symbol = symbol
        
    @abstractmethod
    def get_price(self):
        """Get current price from exchange"""
        pass
    
    @abstractmethod
    def get_exchange_name(self):
        """Return exchange name for file naming"""
        pass

class BinanceExchangeClient(ExchangeClient):
    def __init__(self, symbol):
        super().__init__(symbol)
        self.client = BinanceClient(
            os.getenv("BINANCE_API_KEY"),
            os.getenv("BINANCE_API_SECRET")
        )
    
    def get_price(self):
        try:
            ticker = self.client.get_symbol_ticker(symbol=self.symbol)
            return float(ticker["price"])
        except (binance_exceptions.BinanceAPIException, Exception) as e:
            print(f"Binance error occurred: {e}")
            return None
            
    def get_exchange_name(self):
        return "binance"

class OSLExchangeClient(ExchangeClient):
    def __init__(self, symbol):
        super().__init__(symbol)
        # Initialize OSL client here
        # self.client = OSLClient(...)
    
    def get_price(self):
        try:
            # Implement OSL price fetching logic
            # return float(price)
            pass
        except Exception as e:
            print(f"OSL error occurred: {e}")
            return None
            
    def get_exchange_name(self):
        return "osl"

class HashKeyExchangeClient(ExchangeClient):
    def __init__(self, symbol):
        super().__init__(symbol)
        # Initialize HashKey client here
        # self.client = HashKeyClient(...)
    
    def get_price(self):
        try:
            # Implement HashKey price fetching logic
            # return float(price)
            pass
        except Exception as e:
            print(f"HashKey error occurred: {e}")
            return None
            
    def get_exchange_name(self):
        return "hashkey"


def main():
    # Initialize exchange clients
    exchanges = [
        BinanceExchangeClient(BTC_SYMBOL),
        OSLExchangeClient(BTC_SYMBOL),  # You'll need to adjust the symbol format for each exchange
        HashKeyExchangeClient(BTC_SYMBOL)
    ]
    
    while True:
        for exchange in exchanges:
            price = exchange.get_price()
            if price:
                store_price_data(
                    exchange_name=exchange.get_exchange_name(),
                    price=price,
                    symbol=exchange.symbol
                )
            else:
                print(f"Failed to retrieve price from {exchange.get_exchange_name()}, retrying next time")
        
        time.sleep(5)
        

def store_price_data(exchange_name, price, symbol):
    timestamp = datetime.datetime.now()
    csv_file = os.path.join(DATA_DIR, f"{symbol}_{exchange_name}.csv")
    
    os.makedirs(DATA_DIR, exist_ok=True)

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


if __name__ == "__main__":
    main()