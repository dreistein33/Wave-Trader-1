import argparse

import utils.waveutils as wave

"""
SCHEME OF WORK:
1) Set trading pair in presented format in setting.json -> 'BTC/USDT'
2) Set the starting price -> $20000
3) Set the balance -> $200
4) Set number of entries -> 5 entries = $200 / 5 = $40 per entry/order
5) If price drops x% -> place new buy order
6) If price pumps x% -> place new sell order equivalent to % specified in --sell-assets argument.   
"""

parser = argparse.ArgumentParser(
    description='Binance Trading Bot',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="Usage: python bot.py -sp 20000, -b 1000 -e 5"
)
parser.add_argument('-sp', '--starting-price', type=float, help='Set the starting price for the bot.')
parser.add_argument('-b', '--balance', type=float, help='Set the amount of money you want to spend on trading.')
parser.add_argument('-e', '--entries', type=int, help='Specify the amount of entries: eg. $1000 balance / 5 entries = $200 per entry.')
parser.add_argument('-pp', '--profit-percentage', type=float, help='Specify threshold to realise the profit')
parser.add_argument('-lp', '--loss-percentage', type=float, help='Specify threshold to realise next buy order when price drops.')
parser.add_argument('-sa', '--sell-assets', type=float, help='Specify how much percent of assets bought is going to be sold when hit the profit threshold,'
                                                             'eg. -sa 50 -> current profit = $250 -> sell amount of coins equivalent to $125.')


"""
PSEUDO CODE LOOP
1) Check if work has been stopped
2) If so, observe the market and analyze if we're on profit or loss
3) If not, create new market buy order
4) Wait for the price to change 
5) If price raises by set percentage, sell amount specified in settings
7) Wait for the price to go back to starting price
8) Repeat
6) If price hits lower threshold, create another market buy order
7) Wait for the price to reach demanded value
8) Sell
9) Back to point no. 7
"""
if __name__ == '__main__':
    print("THIS IS A SUBPROCESS!")