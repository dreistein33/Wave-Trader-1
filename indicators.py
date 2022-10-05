import requests
import time

from utils.constants import INTERVALS
from utils.mathutils import calculate_price_difference


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
    """This method calculates MA of n period."""
    candles = get_candle_data(symbol, interval, n)
    # Use index 4 because Binance api provides data in lists
    # And the close price is actually placed at index four.
    if len(candles) == n:
        close_prices = [float(x[4]) for x in candles]
        summed_prices = sum(close_prices)
        average = summed_prices / len(close_prices)
        return average
    else:
        return None


def get_rsi(symbol, n, interval='1d'):
    """This method calculates RSI of n period."""
    candles = get_candle_data(symbol, interval, n)
    if len(candles) == n:
        close_prices = [float(x[4]) for x in candles]
        # close_prices[i] - close_prices[i-1] - Difference between prices
        price_changes = calculate_price_difference(close_prices)
        pos_price_changes = [p for p in price_changes if p > 0]
        # print(pos_price_changes)
        neg_price_changes = [p for p in price_changes if p < 0]
        # print(neg_price_changes)
        # RS = average gain / average loss
        # Average gain = sum(pos_price_changes) / n
        # Average loss = sum(neg_price_changes) / n -> Note we use absolute numbers
        # RSI = 100 - 100 / (1 + RS)
        avg_gain = sum(pos_price_changes) / (n - 1)
        avg_loss = sum(neg_price_changes) / (n - 1)
        rs = avg_gain / avg_loss
        rsi = 100 - 100 / (1 + rs)
        return rsi
    else:
        return None


def get_ema(symbol, interval, n):
    # ema = price(today) * k + ema(yesterday) * (1 - k)
    k = 2 / (n + 1)
    pass


class Ema:
    def __init__(self, symbol, interval, n):
        self.symbol = symbol
        self.n = n
        self.k = 2 / (n + 1)
        self.prev_ema = get_moving_average(symbol, interval, n)

    def calculate_ema(self):
        response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={self.symbol}").json()
        current_price = float(response['price'])
        ema = self.k * (current_price - self.prev_ema) + self.prev_ema
        self.prev_ema = ema
        return ema


# if __name__ == '__main__':
#     x = get_rsi('BTCUSDT', 24, interval='15m')
#     print(x)

