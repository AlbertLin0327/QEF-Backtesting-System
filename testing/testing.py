# import necessary libraries
import pandas as pd
import datetime
import pandas as pd
import numpy as np
import matplotlib
# import talib
import os

matplotlib.use("Agg")
import matplotlib.pyplot as plt

### Constant ###
TAIWAN_50 = [
    "0050", "1101", "1102", "1216", "1301", "1303", 
    "1326", "1402", "1590", "2002", "2207", "2227",
    "2303", "2308", "2317", "2327", "2330", "2352",
    "2357", "2379", "2382", "2395", "2408", "2409",
    "2412", "2454", "2603", "2609", "2610", "2615",
    "2801", "2880", "2881", "2882", "2884", "2885",
    "2886", "2887", "2891", "2892", "2912", "3008",
    "3034", "3045", "3711", "4904", "4938", "5871",
    "5876", "5880", "6415", "6505", "8046", "9910",
]

### Mean Reversal Strategy
class Strategy:

    #Parameters setting 
    def __init__(self):
        self.ticker_window = {}
        self.period = 21
        self.betting = 100000

    # Find the price window
    def window(self, data):

        # Go through all entry
        for _, row in data.iterrows():
            ticker = row["identifier"]

            # Add ticker to the window
            if ticker not in self.ticker_window.keys():
                self.ticker_window[ticker] = np.array([row["adj_close_"]])
            else:
                self.ticker_window[ticker] = np.append(
                    self.ticker_window[ticker], row["adj_close_"]
                )

            # Trim to an adequate size of window
            self.ticker_window[ticker] = self.ticker_window[ticker][-(self.period + 1):]

    # Calculate the cumulative return of all the stocks
    def count_cumulative_return(self):
        cum_ret = []
        p = 0
        for ticker in self.ticker_window.keys():
            if len(self.ticker_window[ticker]) < self.period:
                continue
            else:
                cum = 0
                for i in range(1, self.period):
                    cum += self.ticker_window[ticker][i - 1] / self.ticker_window[ticker][i]
                cum_ret.append([cum, ticker])
        cum_ret = sorted(cum_ret, key=lambda cr : cr[0])
        return cum_ret

    # Main trading function
    def trade_asset(self, data, holding):

        # Fill the window
        self.window(data)

        # count the cumulative return and sort it
        cum_ret = self.count_cumulative_return()
        # Decide the action of every stock
        dicision = {}
        short_position, long_position = 0, 0
        short_list = {}
        long_list = {}
        if len(cum_ret) >= 20:
            for i in range(10):
                short_list[cum_ret[-(i + 1)][1]] = -(i + 1)
                long_list[cum_ret[i][1]] = i
            # print(long_list)
            # print(short_list)
        # Iterate through all stock
        for _, row in data.iterrows():
            ticker = row["identifier"]

            # Get rid of invalid data
            if ticker not in self.ticker_window.keys() or len(cum_ret) < 20:
                continue
            
            if ticker in short_list and (ticker not in holding or holding[ticker]['position'] > 0) :
                dicision[ticker] = -1
                short_position += 1
            
            elif ticker in long_list and (ticker not in holding or holding[ticker]['position'] < 0):
                dicision[ticker] = 1
                long_position += 1
            
            else :
                dicision[ticker] = 0
        # if long_position != 0 or short_position != 0:
        #     print("LS")
        #     print(long_position, short_position)
        new_holding = {}

        if dicision != {} and not (short_position == 0 and long_position == 0):

            # Iterate all dicision
            for ticker in dicision:
                price = data.loc[data["identifier"] == ticker]["adj_close_"].values[0]

                # Keep same position if hold
                if dicision[ticker] == 0:
                    if ticker in holding:
                        new_holding[ticker] = holding[ticker]
                    else:
                        new_holding[ticker] = {
                            "price": price,
                            "amount": 0,
                            "position": 0,
                        }

                # Short sell and make the amout negative
                elif dicision[ticker] == -1:

                    new_holding[ticker] = {
                        "price": price,
                        "amount": -(self.betting / short_position) / price,
                        "position": -1,
                    }

                # Long an stock
                elif dicision[ticker] == 1:

                    new_holding[ticker] = {
                        "price": price,
                        "amount": (self.betting / long_position) / price,
                        "position": 1,
                    }
        return new_holding, dicision          



# # MA Cross Strategy
# class Strategy:

#     # Parameters setting
#     def __init__(self):
#         self.ticker_window = {}
#         self.ma_long = 20
#         self.ma_short = 5
#         self.betting = 100000

#     # Find the price window
#     def window(self, data):

#         # Go through all entry
#         for _, row in data.iterrows():
#             ticker = row["identifier"]

#             # Add ticker to the window
#             if ticker not in self.ticker_window.keys():
#                 self.ticker_window[ticker] = np.array([row["adj_close_"]])
#             else:
#                 self.ticker_window[ticker] = np.append(
#                     self.ticker_window[ticker], row["adj_close_"]
#                 )

#             # Trim to an adequate size of window
#             self.ticker_window[ticker] = self.ticker_window[ticker][
#                 -(self.ma_long + 1) :
#             ]

#     # Main trading function
#     def trade_asset(self, data, holding):

#         # Find window
#         self.window(data)

#         # Find the action of every stock
#         dicision = {}
#         short_position, long_position = 0, 0

#         # Iterate through all stock
#         for _, row in data.iterrows():
#             ticker = row["identifier"]

#             # Get rid of invalid entry
#             if (
#                 ticker not in self.ticker_window.keys()
#                 or len(self.ticker_window[ticker]) < self.ma_long
#             ):
#                 continue

#             # Find short and long MA
#             short_price = talib.SMA(self.ticker_window[ticker], self.ma_short)[-1]
#             long_price = talib.SMA(self.ticker_window[ticker], self.ma_long)[-1]

#             # When short MA < long MA and previous position is long ==> short sell
#             if short_price > long_price and (
#                 ticker not in holding or holding[ticker]["position"] == "SHORT"
#             ):
#                 dicision[ticker] = "LONG"
#                 long_position += 1

#             # When short MA > long MA and previous position is short ==> long buy
#             elif short_price < long_price and (
#                 ticker not in holding or holding[ticker]["position"] == "LONG"
#             ):
#                 dicision[ticker] = "SHORT"
#                 short_position += 1

#             # If not fulfuill the condition than hold
#             else:
#                 dicision[ticker] = "HOLD"

#         # Calculate new position
#         new_holding = {}

#         if dicision != {} and not (short_position == 0 and long_position == 0):

#             # Iterate all dicision
#             for ticker in dicision:
#                 price = data.loc[data["identifier"] == ticker]["adj_close_"].values[0]

#                 # Keep same position if hold
#                 if dicision[ticker] == "HOLD":
#                     if ticker in holding:
#                         new_holding[ticker] = holding[ticker]
#                     else:
#                         new_holding[ticker] = {
#                             "price": price,
#                             "amount": 0,
#                             "position": "HOLD",
#                         }

#                 # Short sell and make the amout negative
#                 elif dicision[ticker] == "SHORT":

#                     new_holding[ticker] = {
#                         "price": price,
#                         "amount": -(self.betting / short_position) / price,
#                         "position": "SHORT",
#                     }

#                 # Long an stock
#                 elif dicision[ticker] == "LONG":

#                     new_holding[ticker] = {
#                         "price": price,
#                         "amount": (self.betting / long_position) / price,
#                         "position": "LONG",
#                     }

#         return new_holding, dicision



def sandbox(strategy, data: pd.DataFrame, holding, end):

    # Get the newset holdings and dicisions
    new_holding, dicision = strategy.trade_asset(data, holding)
    # if end: 
    # if len(new_holding) != 0:
    #     print(new_holding)
        # print("Dicision")
        # print(dicision)
    short_PnL, long_PnL = 0, 0

    if holding != {}:

        # Find all tickers and Calculate PnL
        for ticker in holding:

            # Do nothing if hold
            if ticker not in dicision or dicision[ticker] == 0:
                continue

            # Calculate PnL of previous short position
            elif holding[ticker]["position"] == -1 and dicision[ticker] == 1:
                # print("Short")
                short_PnL += holding[ticker]["amount"] * (
                    new_holding[ticker]["price"] - holding[ticker]["price"]
                )

            # Calculate PnL of previous long position
            elif holding[ticker]["position"] == 1 and dicision[ticker] == -1:
                # print("Long")
                long_PnL += holding[ticker]["amount"] * (
                    new_holding[ticker]["price"] - holding[ticker]["price"]
                )

    return long_PnL, short_PnL, new_holding


def fetch(file_path):

    # Read the file and transform to pandas.data_form
    data = pd.read_parquet(file_path)
    return data


def fetcher(price_vol: dict, date: datetime):

    # return the price information for the given date
    try:
        return price_vol[date.strftime("%Y-%m-%d")]
    except:
        return None


# Plotting functions
def plot(assets, years, path, title, ylabel):

    fig = plt.figure(figsize=(10, 10))

    # plot the assets curve
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel(ylabel)

    # draw the fitting curve
    plt.plot(years, assets)

    # plt.show()
    fig.savefig(path + '/' + title.replace(" ", "_"))


def engine(price_vol: dict, start: datetime, end: datetime):

    # The main part of the engine component
    delta = datetime.timedelta(days=1)

    data, years, current_holdings = [], [], {}

    assets, long_pnl, short_pnl = [], [], []

    ma_cross = Strategy()

    path = './image/' + start.strftime("%Y-%m-%d") + '~' + end.strftime("%Y-%m-%d")
    os.mkdir(path)
    # try:
    #     os.mkdir(path)
    #     print(path + "Success")
    # except:
    #     print("error")

    while start <= end:

        # Fetch the date
        current_data = fetcher(price_vol, start)

        if current_data is not None:
            years.append(start)
            long_asset, short_asset, current_holdings = sandbox(
                ma_cross, current_data, current_holdings, start == end
            )
            # print(long_asset, short_asset)
            assets.append(long_asset + short_asset)
            long_pnl.append(long_asset)
            short_pnl.append(short_asset)

        start += delta

    # plot PnL curve
    plot(assets, years, path, "Total PnL", "PnL")
    plot(long_pnl, years, path, "Long PnL", "PnL")
    plot(short_pnl, years, path, "Short PnL", "PnL")

    # plot PnL curve
    plot(np.cumsum(assets), years, path, "Total Assets", "Assets")
    plot(np.cumsum(long_pnl), years, path, "Long Assets", "Assets")
    plot(np.cumsum(short_pnl), years, path, "Short Assets", "Assets")


def init():

    print("--- Read in data ---")

    # Store all the price volume information
    price_vol = {}

    # Looping through the date
    start_date = datetime.date(2016, 1, 1)
    end_date = datetime.date(2020, 12, 31)
    delta = datetime.timedelta(days=1)

    # Get all the price data
    while start_date <= end_date:
        try:
            price_vol[start_date.strftime("%Y-%m-%d")] = fetch(
                f"../Dataset/Universe/Taiwan_50/Price-Volume/" + start_date.strftime("%Y/%m/%d")
            )
        except:
            pass
        finally:
            start_date += delta

    print("--- Start Engine ---")

    # Start the engine
    engine(price_vol, datetime.date(2018, 1, 1), datetime.date(2020, 12, 31))


if __name__ == "__main__":
    init()
