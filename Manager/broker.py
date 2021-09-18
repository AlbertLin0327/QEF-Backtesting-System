import matplotlib
import sys

from Lib import mean, square_deviation, stddev
from Sandbox import Order, OrderBook, Holding

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Broker:

    # Parameters setting
    def __init__(self):
        self.years = []
        self.assets = []
        self.long_asset = []
        self.short_asset = []
        self.long_pnl = []
        self.short_pnl = []
        self.daily_return = []

    # Appending valid trading date
    def setYear(self, date):
        self.years.append(date)

    def run(self, long_asset, short_asset, total_fiat, long_pnl, short_pnl):
        # print(long_asset + short_asset + total_fiat)
        self.assets.append(total_fiat + long_asset + short_asset)
        self.long_pnl.append(long_pnl)
        self.short_pnl.append(short_pnl)
        self.long_asset.append(long_asset)
        self.short_asset.append(short_asset)
        self.cal_daily_return()

    def cal_sharpe_ratio(self):

        # Return the Sharpe ration
        r_p = mean(self.daily_return)
        theta_p = stddev(self.daily_return)

        # Sharpe ration = (expected porfolio return - risk free rate) / porfolio standard deviation
        sharpe_ratio = r_p / theta_p

        # Since it is daily value, annualize it by multiply by the square of trading days
        return (len(self.years) ** 0.5) * sharpe_ratio

    def cal_daily_return(self):
        if len(self.assets) > 2:
            daily_return = self.assets[-1] / self.assets[-2] - 1
            self.daily_return.append(daily_return)

    def plot(self, data, path, title, ylabel):

        fig = plt.figure(figsize=(10, 10))

        # plot the assets curve
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel(ylabel)
        years = self.years[-len(data):]
        # draw the fitting curve
        plt.plot(years, data)

        # plt.show()
        fig.savefig(path + "/" + title.replace(" ", "_"))
    
    def plot_all(self, path):
        self.plot(self.long_pnl, path, "Long PnL", "PnL")
        self.plot(self.short_pnl, path, "Short PnL", "PnL")
        self.plot(self.assets,path, "Total Assets", "Assets")
        self.plot(
            (self.long_asset + np.cumsum(self.long_pnl)),
            path,
            "Long Assets",
            "Assets",
        )
        self.plot(
            (self.short_asset + np.cumsum(self.short_pnl)),
            path,
            "Short Assets",
            "Assets",
        )
        self.plot(
            self.daily_return,
            path,
            "Daily Return",
            "Return",
        )
