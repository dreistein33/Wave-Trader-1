from ast import Break
import os
from time import sleep, time
import requests
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from colorama import Fore, Back, Style
from apscheduler.schedulers.blocking import BlockingScheduler
import json

path = str(os.path.abspath(__file__)).replace("main.py","") #Save the path where this code is running for later usage
f = open(f'{path}\settings.json') #Read the file settings file
settings = json.load(f)
symbol = settings['symbol']
client = Client(settings['public_api'], settings['private_api'], {"verify": True, "timeout": 100}) #Request from Binance informations about your account

tickers = client.get_ticker(symbol=symbol) #Returns the 24 hours metrics
avg =  client.get_avg_price(symbol=symbol) #Returns a 5 minutes avg price

def filter_parameters():
    f = open(f'{path}\settings.json')  #Read the file settings file
    data = json.load(f)
    sell_percentage = data['sell_percentage'] 
    stop_loss = data['stop_loss']
    #The reason why this code repeats here and the file is read again, is to let the user change tha parameters while the software is running
    f.close()

    #The code bellow is basically a system to turn the sell percentage into multipliers, so
    #if the settings request a 3% loss to trigger the stop loss, it's basically transforming
    #3% into 0.97x
    if sell_percentage  < 9.99: 
        sell_percentage_f = float(f"1.0{str(sell_percentage/2).replace('.','')}")
        buy_price_f = abs((sell_percentage/2)/100 - 1.0) 
        stop_loss_price_f = abs((stop_loss)/100 - 1.0) 
    else: 
        sell_percentage_f = float(f"1.{str(sell_percentage/2).replace('.','')}")
        buy_price_f = abs((sell_percentage/2)/100 - 1.0)
    return sell_percentage_f, buy_price_f, stop_loss_price_f

def generate_new_average(): #A function that returns the informations about the coin selected, everytime it's called, it gets the new metrics and calculates the avg prices
    global ticker_avg, sell_price, buy_price, stop_loss_price
    sell_percentage_f, buy_price_f, stop_loss_price_f = filter_parameters()
    tickers = client.get_ticker(symbol=symbol)
    ticker_avg = tickers['weightedAvgPrice']
    sell_price = float(ticker_avg)* sell_percentage_f
    buy_price = float(ticker_avg)* buy_price_f
    stop_loss_price =  buy_price * stop_loss_price_f

def print_data():
    os.system('cls')
    
    data = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")  
    data = data.json()
    actual_price = data['price']
    print(Fore.WHITE + '\n==================  ' + Fore.CYAN + 'Ticker AVG Price [24H]' + Fore.WHITE + '  ==================')
    print(Fore.WHITE + 'Average Price:          ' + Fore.CYAN + f'{round(float(ticker_avg), 4)}')
    print(Fore.WHITE + 'Teorical Sell Price:    ' + Fore.CYAN + f'{round(sell_price, 4)}')
    print(Fore.WHITE + 'Teorical Buy Price:     ' + Fore.CYAN + f'{round(buy_price, 4)}')
    print(Fore.WHITE + 'Stop Loss Price:        ' + Fore.CYAN + f'{round(stop_loss_price, 4)}')
    print(Fore.WHITE + 'Actual Price:           ' + Fore.CYAN + f'{round(float(actual_price), 4)}')

def price():
    data = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")    #Returns the real time price of a coin
    data = data.json()
    actual_price = data['price']
    sell_price_f = sell_price * 1.05
    if float(actual_price) < buy_price: 
        print('The market price is lower than the buy price, generating a new average...')
        sleep(15)
        generate_new_average()
    elif sell_price_f < float(actual_price):
        print('The Price market is now 5% higher than the maximum average price, generating a new average... ')
        sleep(15)
        generate_new_average()
    elif stop_loss_price > float(actual_price):
        print('Triggering the stop loss... ')
        sleep(15)
    else:
        print('Looking for the best market window to buy!')
    
generate_new_average()
price()

#scheduler is a cool way to run fuctions in x time, here it's used to update the avg prices in x time, so the bot keeps working
#with recent metrics, it's probably generating new averages every 6 hours
scheduler = BlockingScheduler() 
scheduler.add_job(print_data, 'interval', seconds = 2) #Just to see what's happening
scheduler.add_job(generate_new_average, 'interval', seconds = 30)
scheduler.start()