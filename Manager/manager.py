import matplotlib
import sys
sys.path.append('../')
# from Engine.engine import Engine
from Lib.lib import mean, square_deviation, stddev
from Sandbox.order import Order, OrderBook 
from Sandbox.holding import Holding

matplotlib.use("Agg")
import matplotlib.pyplot as plt

class Manager:

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
        self.current_holdings = current_holdings
        self.current_holdings.calculate_asset()
        # self.cal_PnL(prev_holding)
        self.cal_daily_return()

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
    
    def cal_PnL(self, prev_holdings):
        
        long_PnL, short_PnL, long_asset, short_asset = 0, 0, 0, 0

        if prev_holdings != {}:

            transaction_cost = 0

            # Find all tickers and Calculate PnL
            for ticker in prev_holdings:

                # Do nothing if hold
                if ticker not in self.OrderBook or self.OrderBook[ticker] == 0:
                    continue

                # Calculate PnL of previous short position
                elif prev_holdings[ticker].position == -1 and self.OrderBook[ticker].position == 1:

                    short_PnL += prev_holdings[ticker].size * prev_holdings[ticker].position * (
                        self.current_holding[ticker].price - prev_holdings[ticker].price
                    )

                    # transaction_cost += abs(
                    #     (holding[ticker]["amount"] - new_holding[ticker]["amount"])
                    #     * new_holding[ticker]["price"]
                    #     * TC_RATE
                    # )

                # Calculate PnL of previous long position
                elif prev_holdings[ticker].position == 1 and self.OrderBook[ticker].position == -1:

                    long_PnL += prev_holdings[ticker].size * prev_holdings[ticker].position * (
                        self.current_holding[ticker].price - prev_holdings[ticker].price
                    )

                    # transaction_cost += abs(
                    #     (holding[ticker]["amount"] - new_holding[ticker]["amount"])
                    #     * new_holding[ticker]["price"]
                    #     * TC_RATE
                    # )

                # Calculate Asset of previous long position
                elif prev_holdings[ticker].position == -1 and self.OrderBook[ticker].position == 0:
                    short_asset += prev_holdings[ticker].amount

                # Calculate Asset of previous long position
                elif prev_holdings[ticker].position == 1 and self.OrderBook[ticker].position == 0:
                    long_asset += prev_holdings[ticker].amount

            self.assets.append(long_PnL + short_PnL + long_asset + short_asset)
            self.long_pnL.append(long_PnL)
            self.short_pnl.append(short_PnL)
            self.long_asset.append(long_PnL + long_asset)
            self.short_asset.append(short_PnL + short_asset)

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
