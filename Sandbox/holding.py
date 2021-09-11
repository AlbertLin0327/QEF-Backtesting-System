from .order import Order, OrderBook
import pandas as pd
import datetime as dt


class Holding(OrderBook):
    def __init__(self, order_list: list, universe: pd.DataFrame, date: dt.date):
        def fill_void(self):
            for ticker in universe["ticker"]:
                if ticker not in self.transaction:
                    self.transaction[ticker] = Order(ticker=ticker, date=date)

        super().__init__(order_list)
        fill_void()

    def calculate_asset(self) -> tuple:
        long_asset, short_asset = 0.0, 0.0

        for ticker in self.transaction:
            if self.transaction[ticker].position == Order.LONG:
                long_asset += self.transaction[ticker].get_amount()

            elif self.transaction[ticker].position == Order.SHORT:
                short_asset += self.transaction[ticker].get_amount()

        return long_asset, short_asset
