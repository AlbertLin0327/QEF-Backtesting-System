from order import Order, OrderBook
from ..Util.Universe.Taiwan_50 import TAIWAN_50

### Constant ###
TC_RATE = 0.0


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
    def trading(self, data, holding):

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
                short_list[cum_ret[-(i + 1)][1]] = -(i + 1)
                long_list[cum_ret[i][1]] = i

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
                short_position += 1

            elif ticker in long_list and (
                ticker not in holding or holding[ticker]["position"] < 0
            ):
                dicision[ticker] = 1
                long_position += 1

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
        else:
            new_holding = holding
        return new_holding, dicision
