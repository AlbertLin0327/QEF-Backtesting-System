### Import necessary library ###
import pandas as pd
import datetime as dt
import numpy as np

### Import necessary object ###
from Sandbox import Order, OrderBook

### Constant ###
from Sandbox import TC_RATE


### Mean Reversal Strategy
class Strategy:

    # Parameters setting
    def __init__(self):
        self.ticker_window = {}
        self.period = 5

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

        # Record cumulative return
        cumulative_return = []

        for ticker in self.ticker_window.keys():

            # If not able to calculate the return
            if len(self.ticker_window[ticker]) < self.period:
                continue

            else:
                cumulative = 0

                # Calculate the relative return
                for i in range(1, self.period):
                    cumulative += (
                        self.ticker_window[ticker][i]
                        / self.ticker_window[ticker][i - 1]
                    )

                cumulative_return.append([cumulative, ticker])

        # Sort from lower return to higher return
        cumulative_return = sorted(cumulative_return, key=lambda cr: cr[0])

        return cumulative_return

    # Main trading function
    def trade(self, data, holding, fiat):

        # The size of each betting
        betting = fiat / 10

        # Fill the window
        self.window(data)

        # count the cumulative return and sort it
        cumulative_return = self.count_cumulative_return()

        # Decide the action of every stock
        dicision = {}

        # Which stock is to long or short
        short_list = {}
        long_list = {}

        # The total weight of long short position
        short_position, long_position = 0, 0

        # The porportion to execute long and short
        porportion = len(cumulative_return) // 2

        # Calculate the weight of each betting
        if porportion > 0:
            for i in range(porportion):
                short_list[cumulative_return[-(i + 1)][1]] = porportion - i
                long_list[cumulative_return[i][1]] = porportion - i

        # Iterate through all stock
        for _, row in data.iterrows():
            ticker = row["identifier"]

            # Get rid of invalid data
            if ticker not in self.ticker_window.keys() or porportion == 0:
                continue

            # Short sell
            if ticker in short_list:
                dicision[ticker] = -1
                short_position += short_list[ticker]

            # Long buy
            elif ticker in long_list:
                dicision[ticker] = 1
                long_position += long_list[ticker]

            else:
                dicision[ticker] = 0

        # Record new orders
        new_orders = []

        if dicision != {} and not (short_position == 0 and long_position == 0):

            # Iterate all dicision
            for ticker in dicision:
                price = data.loc[data["identifier"] == ticker]["adj_close_"].values[0]

                # Short sell and make the amout negative
                if dicision[ticker] == -1:

                    new_orders.append(
                        Order(
                            ticker=ticker,
                            size=(
                                (betting / price)
                                * (short_list[ticker] / short_position)
                            ),
                            price=price,
                            position=Order.SHORT,
                        )
                    )

                # Long an stock
                elif dicision[ticker] == 1:

                    new_orders.append(
                        Order(
                            ticker=ticker,
                            size=(
                                (betting / price) * (long_list[ticker] / long_position)
                            ),
                            price=price,
                            position=Order.LONG,
                        )
                    )

            new_orders = OrderBook(new_orders)

        # If no order, then skip
        else:
            new_orders = OrderBook()

        return new_orders
