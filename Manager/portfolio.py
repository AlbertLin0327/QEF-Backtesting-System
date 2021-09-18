import matplotlib
import sys
import numpy as np

from Lib import mean, square_deviation, stddev
from Sandbox import Order, OrderBook, Holding

matplotlib.use("Agg")
import matplotlib.pyplot as plt


class PortfolioManager(object):

    # Parameters setting
    def __init__(self):
        self.years = []
        self.assets = []
        self.long_asset = []
        self.short_asset = []
        self.long_pnl = []
        self.short_pnl = []
        self.daily_return = []
        self.turnover = []
        self.annual_return = []
        self.annual_sharpe_ratio = []

    # Appending valid trading date
    def setYear(self, date):
        self.years.append(date)

    def run(self, long_asset, short_asset, total_fiat, long_pnl, short_pnl, turnover):
        self.assets.append(total_fiat + long_asset + short_asset)
        self.long_pnl.append(long_pnl)
        self.short_pnl.append(short_pnl)
        self.long_asset.append(long_asset)
        self.short_asset.append(short_asset)
        self.turnover.append(turnover)
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

    def cal_total_return(self):
        total_return = 1.0

        for d in self.daily_return:
            total_return *= d + 1

        return total_return - 1.0

    def cal_annual_return(self):

        for i in range(len(self.years) - 1, 253, -252):
            annual_return, new_list = 1.0, self.daily_return[i - 253 : i]

            for j in range(252):
                annual_return *= new_list[j] + 1

            self.annual_return.append(annual_return)

        return self.annual_return

    def cal_annual_sharpe_ratio(self):

        for i in range(len(self.years) - 1, 253, -252):
            new_list = self.daily_return[i - 253 : i]

            r_p = mean(new_list)
            theta_p = stddev(new_list)

            self.annual_sharpe_ratio.append((252 ** 0.5) * r_p / theta_p)

        return self.annual_sharpe_ratio

    def plot(self, data, path, title, ylabel):

        fig = plt.figure(figsize=(10, 10))

        # plot the assets curve
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel(ylabel)
        years = self.years[-len(data) :]

        # draw the fitting curve
        plt.plot(years, data)

        # plt.show()
        fig.savefig(path + "/" + title.replace(" ", "_"))

    def plot_all(self, path):
        self.plot(self.long_pnl, path, "Long PnL", "PnL")
        self.plot(self.short_pnl, path, "Short PnL", "PnL")
        self.plot(self.assets, path, "Total Assets", "Assets")
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
        self.plot(self.turnover, path, "Turnover", "Turnover Rate")
