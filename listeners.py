import requests
import time

from utils.constants import INTERVALS


class WaveListener:

    @classmethod
    def wait_for_price(cls, target_price, symbol):
        while True:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}").json()
            current_price = response['price']
            if current_price > target_price:
                continue
            else:
                reached_target = True
                break
            time.sleep(10)
        return reached_target

    @classmethod
    def candle_listener(cls, symbol, interval, alert_at='5%'):
        data = {'symbol': symbol, 'interval': INTERVALS[interval]}
        response = requests.get('https://api.binance.com/api/v3/klines', params=data).json()
        return response
