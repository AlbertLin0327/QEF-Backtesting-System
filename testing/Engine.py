### import necessary libraries
import datetime
import pandas as pd

class Engine:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.cur_p = 0 
        self.data = pd.DataFrame()
        self.valid_date = []

    def fectcher(self):
        print("--- Start Engine ---")
        print("--- " + self.start_date.strftime("%Y/%m/%d") + " ---")
        delta = datetime.timedelta(days=1)
        tmp = self.start_date
        while tmp <= self.end_date:
            file_path = f"../Dataset/Price-Volume/" + tmp.strftime("%Y/%m/%d")
            try:
                df = pd.read_parquet(file_path)
                pd.concat(self.data, df)
                self.valid_date.append(tmp.strftime("%Y%m%d"))
            except:
                pass
            finally:
                tmp += delta
        print("--- " + self.end_date.strftime("%Y/%m/%d") + " ---")

    def feeder(self, *args):
        # interval_length = arg[0], stock_name = arg[1], stock_number = arg[2]
        # left = max(0, self.cur_p - arg[0])

        return self.data, self.valid_date

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

if __name__ == "__main__":
    