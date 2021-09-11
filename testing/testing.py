# import necessary libraries
import pandas as pd
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib
import sys
sys.path.append('../')
from Lib.lib import mean, square_deviation, stddev

# import talib
import os

matplotlib.use("Agg")
import matplotlib.pyplot as plt

### Constant ###
TC_RATE = 0.0
TAIWAN_50 = [
    "0050",
    "1101",
    "1102",
    "1216",
    "1301",
    "1303",
    "1326",
    "1402",
    "1590",
    "2002",
    "2207",
    "2227",
    "2303",
    "2308",
    "2317",
    "2327",
    "2330",
    "2352",
    "2357",
    "2379",
    "2382",
    "2395",
    "2408",
    "2409",
    "2412",
    "2454",
    "2603",
    "2609",
    "2610",
    "2615",
    "2801",
    "2880",
    "2881",
    "2882",
    "2884",
    "2885",
    "2886",
    "2887",
    "2891",
    "2892",
    "2912",
    "3008",
    "3034",
    "3045",
    "3711",
    "4904",
    "4938",
    "5871",
    "5876",
    "5880",
    "6415",
    "6505",
    "8046",
    "9910",
]

### Mean Reversal Strategy
class Strategy:

    # Parameters setting
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
            self.ticker_window[ticker] = self.ticker_window[ticker][
                -(self.period + 1) :
            ]

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
                    cum += (
                        self.ticker_window[ticker][i - 1]
                        / self.ticker_window[ticker][i]
                    )
                cum_ret.append([cum, ticker])
        cum_ret = sorted(cum_ret, key=lambda cr: cr[0])
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

        porportion = len(cum_ret) // 5

        if porportion > 0:
            for i in range(porportion):
                short_list[cum_ret[-(i + 1)][1]] = porportion - i
                long_list[cum_ret[i][1]] = porportion - i

        # Iterate through all stock
        for _, row in data.iterrows():
            ticker = row["identifier"]

            # Get rid of invalid data
            if ticker not in self.ticker_window.keys() or porportion == 0:
                continue

            if ticker in short_list and (
                ticker not in holding or holding[ticker]["position"] > 0
            ):
                dicision[ticker] = -1
                short_position += np.exp(short_list[ticker])

            elif ticker in long_list and (
                ticker not in holding or holding[ticker]["position"] < 0
            ):
                dicision[ticker] = 1
                long_position += np.exp(long_list[ticker])

            else:
                dicision[ticker] = 0

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
                        "amount": -(self.betting / short_position * np.exp(short_list[ticker])
) / price,
                        "position": -1,
                    }

                # Long an stock
                elif dicision[ticker] == 1:

                    new_holding[ticker] = {
                        "price": price,
                        "amount": (self.betting / long_position * np.exp(long_list[ticker])
) / price,
                        "position": 1,
                    }
        else:
            new_holding = holding
        return new_holding, dicision


def sandbox(strategy, data: pd.DataFrame, holding, end):

    # Get the newset holdings and dicisions
    new_holding, dicision = strategy.trade_asset(data, holding)
    short_PnL, long_PnL, transaction_cost = 0, 0, 0
    short_asset, long_asset = 0, 0

    if holding != {}:

        transaction_cost = 0

        # Find all tickers and Calculate PnL
        for ticker in holding:

            # Do nothing if hold
            if ticker not in dicision or dicision[ticker] == 0:
                continue

            # Calculate PnL of previous short position
            elif holding[ticker]["position"] == -1 and dicision[ticker] == 1:

                short_PnL += holding[ticker]["amount"] * (
                    new_holding[ticker]["price"] - holding[ticker]["price"]
                )

                transaction_cost += abs(
                    (holding[ticker]["amount"] - new_holding[ticker]["amount"])
                    * new_holding[ticker]["price"]
                    * TC_RATE
                )

            # Calculate PnL of previous long position
            elif holding[ticker]["position"] == 1 and dicision[ticker] == -1:

                long_PnL += holding[ticker]["amount"] * (
                    new_holding[ticker]["price"] - holding[ticker]["price"]
                )

                transaction_cost += abs(
                    (holding[ticker]["amount"] - new_holding[ticker]["amount"])
                    * new_holding[ticker]["price"]
                    * TC_RATE
                )

            # Calculate Asset of previous long position
            elif holding[ticker]["position"] == -1 and dicision[ticker] == 0:
                short_asset += holding[ticker]["amount"] * holding[ticker]["price"]

            # Calculate Asset of previous long position
            elif holding[ticker]["position"] == 1 and dicision[ticker] == 0:
                long_asset += holding[ticker]["amount"] * holding[ticker]["price"]

    return (
        long_PnL - transaction_cost,
        short_PnL - transaction_cost,
        short_asset,
        long_asset,
        new_holding,
        transaction_cost,
    )


def fetch(file_path):

    # Read the file and transform to pandas.data_form
    data = pd.read_parquet(file_path)
    return data


def fetcher(price_vol: dict, date: dt.datetime):

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
    fig.savefig(path + "/" + title.replace(" ", "_"))

def cal_annual_return(daily_return: list):
    annual = len(daily_return) // 252
    # print(daily_return)
    for i in range(annual + 1):
        annual_return = 0
        j = 0
        while j < 252 and i * 252 + j < len(daily_return):
            annual_return += daily_return[i * 252 + j]
            j += 1
        print(f'annual_return(year {i + 1}): {annual_return}')

def engine(price_vol: dict, start: dt.datetime, end: dt.datetime):

    # The main part of the engine component
    delta = dt.timedelta(days=1)

    data, years, current_holdings = [], [], {}

    assets, long_asset, short_asset = [], [], []
    long_pnl, short_pnl = [], []
    daily_return = []

    transaction_cost = []

    ma_cross = Strategy()

    path = "./image/" + dt.datetime.now().strftime("%m-%d-%Y_%H:%M:%S")
    os.mkdir(path)
    total = 0
    while start <= end:

        # Fetch the date
        current_data = fetcher(price_vol, start)

        if current_data is not None:
            years.append(start)
            (
                current_long_pnl,
                current_short_pnl,
                current_long_asset,
                current_short_asset,
                current_holdings,
                cost,
            ) = sandbox(ma_cross, current_data, current_holdings, start == end)

            assets.append(current_long_pnl + current_short_pnl)
            long_pnl.append(current_long_pnl)
            short_pnl.append(current_short_pnl)
            long_asset.append(current_long_asset)
            short_asset.append(current_short_asset)
            transaction_cost.append(cost)
            if len(assets) > 1 and total != 0:
                daily_return.append((assets[-1] + long_asset[-1] + short_asset[-1]) / total - 1)
            total += assets[-1] + long_asset[-1] + short_asset[-1]

        start += delta
    print(long_asset)
    print(short_asset)
    # plot PnL curve
    plot(assets, years, path, "Total PnL", "PnL")
    plot(long_pnl, years, path, "Long PnL", "PnL")
    plot(short_pnl, years, path, "Short PnL", "PnL")

    # plot Assets curve
    plot(np.cumsum(assets), years, path, "Total Assets", "Assets")
    plot(long_asset + np.cumsum(long_pnl), years, path, "Long Assets", "Assets")
    plot(short_asset + np.cumsum(short_pnl), years, path, "Short Assets", "Assets")

    plot(daily_return, years[-len(daily_return):], path, "Daily Return", "Return")
    # Transaction Cost
    plot(
        np.cumsum(transaction_cost),
        years,
        path,
        f"Accumulate Transaction Cost",
        "TC",
    )
    sharpe_ratio = mean(daily_return) / stddev(daily_return) * (len(years) ** 0.5)
    # print(f'mean: {mean(daily_return)}')
    # print(f'stddev: {stddev(daily_return)}')
    cal_annual_return(daily_return)
    print(f'total return: {sum(daily_return)}')
    print(f'Sharp ratio: {sharpe_ratio}')


def init():

    print("--- Read in data ---")

    # Store all the price volume information
    price_vol = {}

    # Looping through the date
    start_date = dt.date(2020, 1, 1)
    end_date = dt.date(2020, 12, 31)
    delta = dt.timedelta(days=1)

    # Get all the price data
    while start_date <= end_date:
        try:
            price_vol[start_date.strftime("%Y-%m-%d")] = fetch(
                f"../Dataset/Universe/Taiwan_50/Price-Volume/"
                + start_date.strftime("%Y/%m/%d")
            )
        except:
            pass
        finally:
            start_date += delta

    print("--- Start Engine ---")

    # Start the engine
    engine(price_vol, dt.date(2020, 1, 1), dt.date(2020, 12, 31))


if __name__ == "__main__":
    init()
