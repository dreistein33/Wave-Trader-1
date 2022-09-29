from datetime import date, datetime
import os
import requests
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler

PATHold = str(os.path.abspath(__file__)).replace("main.py", "")  # Save the PATH where this code is running for later usage
bitcoin = [1]
ethereum = [1]

def alert_bitcoin():
    bitcoin_price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")  
    bitcoin_price = bitcoin_price.json()
    actual_price = bitcoin_price['price']
    bitcoin.append(float(actual_price)) #Append the price to the list bitcoin
    jumper = range(1, 999999999999, 3) #Creates a list like : [1, 4, 7, 10, 13, 14]
    if len(bitcoin) in jumper and len(bitcoin) > 2:
        calculator = int(len(bitcoin))-4
        price_15_ago = bitcoin[calculator]
        if len(bitcoin)>3:
            if float(actual_price) < price_15_ago*0.98 : #check if the bitcoin is 2% lower than 15m ago
                return True #Is bitcoin dumping?
    if float(actual_price) < bitcoin[len(bitcoin)-2]*0.98: #check if the bitcoin is 2% lower than 5m ago
        return True #Is bitcoin dumping?


def alert_ethereum():
    ethereum_price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT")  
    ethereum_price = ethereum_price.json()
    actual_price = ethereum_price['price']
    ethereum.append(float(actual_price)) #Append the price to the list ethereum
    jumper = range(1, 999999999999, 3) #Creates a list like : [1, 4, 7, 10, 13, 14]
    if len(ethereum) in jumper and len(ethereum) > 2:
        calculator_eth = int(len(ethereum))-4
        price_15_ago = ethereum[calculator_eth]
        if len(ethereum)>3:
            if float(actual_price) < price_15_ago*0.98 : #check if the ethereum is 2% lower than 15m ago
                return True #Is ethereum dumping?
    if float(actual_price) < ethereum[len(ethereum)-2]*0.98: #check if the ethereum is 2% lower than 5m ago
        return True #Is ethereum dumping?


scheduler = BlockingScheduler()
scheduler.add_job(alert_bitcoin, 'interval', minutes = 1)
scheduler.add_job(alert_ethereum, 'interval', minutes = 1)
scheduler.start()