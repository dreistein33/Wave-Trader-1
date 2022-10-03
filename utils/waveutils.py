import dotenv
import json
import os
import requests
import time
import threading

from apscheduler.schedulers.blocking import BlockingScheduler
from binance import Client

from mathutils import convert_percent_to_mul, calculate_quantity

# So I'm thinking about separating the tasks in three classes.
# First one stores the user data
# Second one manipulates the data
# Third one observes the market.
# I need to make those classes
# And make them exchange information.


# Actually gonna create separate class to store all the data from configuration
# because it seemed to me like too much is going on in one class.
class SettingsReader:

    def __init__(self):
        self.conf_path = f'{os.path.dirname(os.getcwd())}/settings.json'

        with open(self.conf_path, 'r') as f:
            self.content = json.load(f)
        self.symbol = self.content['symbol']
        self.sell_ptg = self.content['sell_percentage']
        self.stop_loss = self.content['stop_loss']
        self.sell_multiplier = convert_percent_to_mul(self.sell_ptg, loss=False)
        self.loss_multiplier = convert_percent_to_mul(self.stop_loss)
        self.buy_on_avg = self.content['buy_on_average']
        self.dca_interval = self.content['dca_interval'].lower()


class WaveEngine:

    def __init__(self, envpath=f'{os.path.dirname(os.getcwd())}/.env'):
        self.reader = SettingsReader()
        self.PUBKEY = dotenv.dotenv_values(envpath)['PUBLICKEY']
        self.PRIVKEY = dotenv.dotenv_values(envpath)['PRIVKEY']
        self.client = Client(self.PUBKEY, self.PRIVKEY)

    def update_setting(self):
        self.reader = SettingsReader()
        assert self.reader

    def check_for_change_in_config(self):
        with open(self.reader.conf_path) as f:
            content = json.load(f)
        if content != self.reader.content:
            self.update_setting()

    def get_current_price(self):
        return self.client.get_symbol_ticker(self.reader.symbol)

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
        klines = self.client.get_historical_klines(self.reader.symbol, Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")
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

    def dca_strategy(self, balance):
        sched = BlockingScheduler()
        price = self.get_current_price()
        quantity = calculate_quantity(price, balance)
        if self.reader.dca_interval == 'monthly':
            sched.add_job(self.client.order_limit_buy, args=[self.reader.symbol, quantity, price], trigger='cron',
                          day='1st fri')
        elif self.reader.dca_interval == 'daily':
            sched.add_job(self.client.order_limit_buy, args=[self.reader.symbol, quantity, price], trigger='cron',
                          hour='12')
        elif self.reader.dca_interval == 'weekly':
            sched.add_job(self.client.order_limit_buy, args=[self.reader.symbol, quantity, price], trigger='cron',
                          day_of_week='fri', hour='12')
        else:
            raise Exception("Invalid configuration in settings.json, options: daily, weekly, monthly")
        sched.start()


if __name__ == "__main__":
    # I was checking if making changes in settings during the script's work would work.
    # EDIT: IT worked.
    eng = WaveEngine()
    while True:
        x = eng.get_klines()
        thread_s = threading.Thread(target=eng.check_for_change_in_config)
        thread_s.start()
        print(x)
        time.sleep(10)

