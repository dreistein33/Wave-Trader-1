import dotenv
import json
import os
import requests
import time

from binance import Client

from mathutils import convert_percent_to_mul


class WaveEngine:

    def __init__(self, path='settings.json', envpath='.env'):
        self.path = path
        self.PUBKEY = dotenv.dotenv_values(envpath)['PUBLICKEY']
        self.PRIVKEY = dotenv.dotenv_values(envpath)['PRIVKEY']
        self.client = Client(self.PUBKEY, self.PRIVKEY)

        with open(path, 'r') as f:
            self.content = json.load(f)

        self.symbol = self.content['symbol']
        self.sell_ptg = self.content['sell_percentage']
        self.stop_loss = self.content['stop_loss']
        self.sell_multiplier = convert_percent_to_mul(self.sell_ptg, loss=False)
        self.loss_multiplier = convert_percent_to_mul(self.stop_loss)









