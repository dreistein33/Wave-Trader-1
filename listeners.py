import requests
import time

from utils.constants import INTERVALS


# To make it a listener I will use it in while loop as separate thread.
# Wondering about async tho, might improve performance.
def reached_price(target_price, symbol):
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()
    current_price = response['price']
    if current_price > target_price:
        reached_target = False
    else:
        reached_target = True
    return reached_target


def get_candle_data(symbol, interval, limit=100, alert_at='5%'):
    data = {
            'symbol': symbol,
            'interval': INTERVALS[interval],
            'limit': limit
            }
    response = requests.get('https://api.binance.com/api/v3/klines', params=data).json()
    return response


def get_moving_average(symbol, interval, n):
    """This method calculates MA(n)"""
    candles = get_candle_data(symbol, interval, n)
    # Use index 4 because Binance api provides data in lists
    # And the close price is actually placed at index four.
    close_prices = [float(x[4]) for x in candles]
    summed_prices = sum(close_prices)
    average = summed_prices / len(close_prices)

    return average
