import json
import pandas as pd
import time

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


def add_order_info_to_csv(new_order):
    try:
        df = pd.read_csv(wave.ORDERS_PATH, index_col=0)
        df_dict = pd.DataFrame([new_order])
        output = pd.concat([df, df_dict], ignore_index=True)
        output.to_csv(path_or_buf=wave.ORDERS_PATH)
    # Handle the error in case the file was empty.
    except pd.errors.EmptyDataError:
        df_dict = pd.DataFrame([new_order])
        df_dict.to_csv(path_or_buf=wave.ORDERS_PATH)


def remove_order_info_from_csv(indexes: list):
    try:
        df = pd.read_csv(wave.ORDERS_PATH, index_col=0)
        output = df.drop(index=indexes)
        output.reset_index(drop=True, inplace=True)
        output.to_csv(wave.ORDERS_PATH)
    except pd.errors.EmptyDataError:
        print('Cannot manipulate content of file since the file is empty.')


def return_orders_on_profit(df, profit_mul, price):
    filtered_df = df[df['price'] * (1 + profit_mul) <= price]
    return filtered_df


def load_order_data():
    try:
        df = pd.read_csv(wave.ORDERS_PATH, index_col=0)
        return df
    except pd.errors.EmptyDataError:
        return None


def update_entries_in_config(entries):
    with open(wave.CONFIG_PATH, 'r') as f:
        content = json.load(f)
        content['entries'] = entries

    with open(wave.CONFIG_PATH, 'w') as f:
        json.dump(content, f)


def is_df_empty(df):
    return len(df.index) == 0


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
# balance_per_entry = args.balance / args.entries

if __name__ == '__main__':
    config = wave.SettingsReader()
    engine = wave.WaveEngine(config.symbol)
    balance_per_entry = config.balance / config.entries
    while True:
        # Get current price every single iteration of loop.
        current_price = engine.get_current_price()
        # [+] BUY ORDER SECTION [+]
        if len(config.buy_thresholds) > 0:
            if current_price <= config.buy_thresholds[0]:
                print(f'Buying {config.symbol} for {current_price}')
                new_order = engine.place_buy_order_with_market_price(balance_per_entry)
                time.sleep(5)
                add_order_info_to_csv(new_order)
                config.entries -= 1
                config.buy_thresholds.pop(0)
                config.update_config()

        # [-] SELL ORDER SECTION [-]
        orders = load_order_data()
        if orders is not None:
            # Check if current price is equal or greater by x% than price in order
            # Return only the orders where above condition is met
            # Then remove those orders from the original dataframe
            # And update the updated dataframe to the csv file
            orders_to_sell = return_orders_on_profit(orders, config.profit_mul, current_price)
            if not is_df_empty(orders_to_sell):
                for items in orders_to_sell['origQty']:
                    engine.place_sell_order_with_market_price(items)
                    time.sleep(5)
                    config.entries += 1
                    threshold_to_update = current_price * (1 - config.loss_mul)
                    config.buy_thresholds.append(threshold_to_update)
                    config.buy_thresholds = sorted(config.buy_thresholds, reverse=True)
                    config.update_config()
                remove_order_info_from_csv(orders_to_sell.index)

        time.sleep(10)
