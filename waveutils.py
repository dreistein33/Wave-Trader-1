import dotenv
import json
import os
import requests
import time

from binance import Client

from mathutils import convert_percent_to_mul

# So I'm thinking about separating the tasks in three classes.
# First one stores the user data
# Second one manipulates the data
# Third one observes the market.
# I need to make those classes
# And make them exchange information.


# Actually gonna create separate class to store all the data from configuration
# because it seemed to me like too much is going on in one class.
class SettingsReader:

    def __init__(self, conf_path=f'{os.getcwd()}/settings.json'):

        with open(conf_path, 'r') as f:
            self.content = json.load(f)
        self.symbol = self.content['symbol']
        self.sell_ptg = self.content['sell_percentage']
        self.stop_loss = self.content['stop_loss']
        self.sell_multiplier = convert_percent_to_mul(self.sell_ptg, loss=False)
        self.loss_multiplier = convert_percent_to_mul(self.stop_loss)
        self.buy_on_avg = self.content['buy_on_average']


class WaveEngine:

    def __init__(self, envpath=f'{os.getcwd()}/.env'):
        self.reader = SettingsReader()
        self.PUBKEY = dotenv.dotenv_values(envpath)['PUBLICKEY']
        self.PRIVKEY = dotenv.dotenv_values(envpath)['PRIVKEY']
        self.client = Client(self.PUBKEY, self.PRIVKEY)

    def get_prices(self):
        ticker_data = self.client.get_ticker(symbol=self.reader.symbol)
        if self.reader.buy_on_avg:
            buy_price = ticker_data['weightedAvgPrice']
            sell_profit = buy_price * self.reader.sell_multiplier
            sell_loss = buy_price * self.reader.loss_multiplier
        else:
            buy_price = float(input("ENTER PRICE >> "))  # Couldn't come up with better solution, gonna change it later.
            sell_profit = buy_price * self.reader.sell_multiplier
            sell_loss = buy_price * self.reader.loss_multiplier
        return buy_price, sell_profit, sell_loss

    def get_klines(self):
        klines = self.client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
        days = [time.ctime(x[0]/1000) for x in klines]
        volumes = [x[5] for x in klines]

        return days, volumes

    def compare_prices(self):
        current_price = self.client.get_symbol_ticker(self.reader.symbol)
        buy_price, *_ = self.get_prices()
        if current_price > buy_price:
            assume_buy = False
        else:
            assume_buy = True
        return assume_buy, buy_price

    def display_if_buy(self):
        assume_buy = self.compare_prices()
        if assume_buy:
            print('The transaction is going to be realised.')
        else:
            print('The transaction is going to be aborted.')

    def place_order_limit_buy(self, qty=1):
        """This is just a demo to show how would placing order work"""
        assume_buy, buy_price = self.compare_prices()
        if assume_buy:
            self.client.order_limit_buy(
                symbol=self.reader.symbol,
                quantity=qty,
                price=buy_price
            )
        else:
            self.wait_for_better_price()
            self.client.order_limit_buy(
                symbol=self.reader.symbol,
                quantity=qty,
                price=buy_price
            )

    def wait_for_better_price(self, assume_buy=False):
        while not assume_buy:
            assume_buy, _ = self.compare_prices()  # Gotta refactor to get rid of using redundant variables.
            time.sleep(5)

# TODO
# make another file and create bunch of listeners to use here

