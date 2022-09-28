import dotenv
import json
import os
import requests
import time

from binance import Client


class WaveEngine:

    def __init__(self):
        self.PUBKEY = dotenv.dotenv_values('.env')['PUBLICKEY']
        self.PRIVKEY = dotenv.dotenv_values('.env')['PRIVKEY']

    def get_settings(self, path='settings.json'):
        with open(path, 'r') as f:
            content = json.load(f)
        symbol = content['symbol']
        sell_ptg = content['sell_percentage']
        stop_loss = content['stop_loss']
        return symbol, sell_ptg, stop_loss


