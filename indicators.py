import dotenv
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


# The way of using this class is simple
# Create instance of an object class
# The object is bound to one market pair e.g. BTC/USDT
# Happily read the indicators!
# Big win =]
class Indicator:
    def __init__(self, market):
        self.market = market
        self.headers = {
            'X-RapidAPI-Key': dotenv.dotenv_values('.env')['RAPIDAPI'],
            'X-RapidAPI-Host': 'crypto-indicators-rest.p.rapidapi.com'
        }
        # This api seems to work well.
        # There are plenty of indicators,
        # Which may be helpful to users.
        # Limit - 2000 requests per month for free.
        # I will add all available indicators ASAP.
        self.url = 'https://crypto-indicators-rest.p.rapidapi.com/'

    def rsi(self, timeframe='1d', period=14):
        url = self.url + 'rsi'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def stochastic_rsi(self,
                       timeframe='1d',
                       rsiperiod=14,
                       stochasticperiod=14,
                       kperiod=3,
                       dperiod=3):
        url = self.url + 'stochasticrsi'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'rsiPeriod': rsiperiod,
            'stochasticPeriod': stochasticperiod,
            'kPeriod': kperiod,
            'dPeriod': dperiod
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def macd(self,
             timeframe='1d',
             fastperiod=12,
             slowperiod=26,
             signalperiod=9,
             simplemaoscillator=False,
             simplemasignal=False):
        url = self.url + 'macd'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'fastPeriod': fastperiod,
            'slowPeriod': slowperiod,
            'signalPeriod': signalperiod,
            'SimpleMAOscillator': simplemaoscillator,
            'SimpleMASignal': simplemasignal
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def adx(self, timeframe='1d', period=14):
        url = self.url + 'adx'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def atr(self, timeframe='1d', period=14):
        url = self.url + 'atr'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def awesome_oscillator(self, timeframe='1d', fastperiod=5, slowperiod=34):
        url = self.url + 'awesomeOscillator'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'fastPeriod': fastperiod,
            'slowPeriod': slowperiod
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def bollinger_bands(self, timeframe='1d', period=14):
        url = self.url + 'bollingerBands'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def cci(self, timeframe='1d', period=20):
        url = self.url + 'cci'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def force_index(self, timeframe='1d', period=1):
        url = self.url + 'forceIndex'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def kst(self,
            timeframe='1d',
            rocper1=10,
            rocper2=15,
            rocper3=20,
            rocper4=30,
            smarocper1=10,
            smarocper2=10,
            smarocper3=10,
            smarocper4=15,
            signalperiod=9):
        url = self.url + 'kst'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'ROCPer1': rocper1,
            'ROCPer2': rocper2,
            'ROCPer3': rocper3,
            'ROCPer4': rocper4,
            'SMAROCPer1': smarocper1,
            'SMAROCPer2': smarocper2,
            'SMAROCPer3': smarocper3,
            'SMAROCPer4': smarocper4,
            'signalPeriod': signalperiod
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def money_flow_index(self, timeframe='1d', period=14):
        url = self.url + 'moneyFlowIndex'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def on_balance_volume(self, timeframe='1d'):
        url = self.url + 'onBalanceVolume'
        data = {
            'market': self.market,
            'timeframe': timeframe
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def parabolic_stop_and_reverse(self, timeframe='1d', step=0.2, max_=0.2):
        url = self.url + 'psar'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'step': step,
            'max': max_
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def sma(self, timeframe='1d', period=9):
        url = self.url + 'sma'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def stochastic_oscillator(self, timeframe='1d', period=14, signalperiod=3):
        url = self.url + 'stochasticOscillator'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period,
            'signalPeriod': signalperiod
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def trix(self, timeframe='1d', period=18):
        url = self.url + 'trix'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def volume_profile(self, timeframe='1d', nofbars=14):
        url = self.url + 'volumeProfile'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'noOfBars': nofbars
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def ema(self, timeframe='1d', period=9):
        url = self.url + 'ema'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def wma(self, timeframe='1d', period=9):
        url = self.url + 'wma'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def wema(self, timeframe='1d', period=7):
        url = self.url + 'wema'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def williams_r(self, timeframe='1d', period=14):
        url = self.url + 'williamsR'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'period': period
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def ichimoku_cloud(self,
                       timeframe='1d',
                       conversionperiod=9,
                       baseperiod=26,
                       spanperiod=52,
                       displacement=26):
        url = self.url + 'ichimokuCloud'
        data = {
            'market': self.market,
            'timeframe': timeframe,
            'conversionPeriod': conversionperiod,
            'basePeriod': baseperiod,
            'spanPeriod': spanperiod,
            'displacement': displacement
        }
        response = requests.get(url, headers=self.headers, params=data)
        if response.status_code == 200:
            return response.json()
        else:
            return None

# if __name__ == '__main__':
#     x = get_rsi('BTCUSDT', 24, interval='15m')
#     print(x)
