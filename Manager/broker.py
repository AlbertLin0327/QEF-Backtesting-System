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
        self.current_holdings = []
        self.assets = []
        self.total_assets = 0
        self.long_pnl = []
        self.short_pnl = []
        self.long_asset = []
        self.short_asset = []
        self.transaction_cost = []
        self.daily_return = []
        self.tmp = []
        self.OrderBook = {}

    # Appending valid trading date
    def setYear(self, date):
        self.years.append(date)

    def run(self, long_asset, short_asset, long_pnL, short_pnl):

        # Get the return value from sandbox and maintain it
        prev_holding = self.current_holdings

        print(long_asset, short_asset, long_pnL, short_pnl)

        # self.cal_daily_return()

    def cal_sharpe_ratio(self):

        # Return the Sharpe ration
        r_p = mean(self.daily_return)
        theta_p = stddev(self.daily_return)

        # Sharpe ration = (expected porfolio return - risk free rate) / porfolio standard deviation
        sharpe_ratio = r_p / theta_p

        # Since it is daily value, annualize it by multiply by the square of trading days
        return (len(self.years) ** 0.5) * sharpe_ratio

    def annual_sharpe_ratio(self):
        r_p = mean(self.tmp)
        theta_p = stddev(self.tmp)
        return (252 ** 0.5) * r_p / theta_p

    def cal_annual_return(self):
        return sum(self.tmp)

    def cal_daily_return(self):
        if len(self.assets) > 1 and self.total_assets != 0:
            daily_return = self.assets[-1] / self.total_assets - 1
            self.daily_return.append(daily_return)
            self.tmp.append(daily_return)
        self.total_assets += self.assets[-1]

    def plot(self, path, title, ylabel):

        fig = plt.figure(figsize=(10, 10))

        # plot the assets curve
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel(ylabel)

        # draw the fitting curve
        plt.plot(self.years, self.assets)

        # plt.show()
        fig.savefig(path + "/" + title.replace(" ", "_"))
