import pandas as pd
import datetime as dt
import numpy as np

from Sandbox import Order, OrderBook


class Container:
    def __init__(self, strategy_filename: str):

        # import necessary libraries
        import importlib

        # Import Strategy file
        self.strategy_path = "Stratetgy." + strategy_filename
        self.Strategy = importlib.import_module(self.strategy_path)

        # Instance Variable
        self.holdings = None

    def broker(self, executions: OrderBook):

        long_pnl, short_pnl = 0.0, 0.0

        for ticker in executions:

            if (
                self.holdings.transaction[ticker].position == Order.LONG
                and executions[ticker].position == Order.SHORT
            ):

                if executions[ticker].size <= self.holdings.transaction[ticker].size:
                    pnl = (
                        executions[ticker].price
                        - self.holdings.transaction[ticker].price
                    ) * executions[ticker].size

                    self.holdings.transaction[ticker].price = (
                        self.holdings.transaction[ticker].get_amount()
                        - executions[ticker].price * executions[ticker].size
                    ) / (
                        self.holdings.transaction[ticker].size - executions[ticker].size
                    )
                    self.holdings.transaction[ticker].size -= executions[ticker].size

                else:
                    pnl = (
                        executions[ticker].price
                        - self.holdings.transaction[ticker].price
                    ) * self.holdings.transaction[ticker].size

                    self.holdings.transaction[ticker].price = executions[ticker].price
                    self.holdings.transaction[ticker].size = (
                        executions[ticker].size - self.holdings.transaction[ticker].size
                    )
                    self.holdings.transaction[ticker].position = Order.SHORT

                long_pnl += pnl

            elif (
                self.holdings.transaction[ticker].position == Order.SHORT
                and executions[ticker].position == Order.LONG
            ):

                if executions[ticker].size <= self.holdings.transaction[ticker].size:
                    pnl = (
                        self.holdings.transaction[ticker].price
                        - executions[ticker].price
                    ) * executions[ticker].size

                    self.holdings.transaction[ticker].price = (
                        self.holdings.transaction[ticker].get_amount()
                        - executions[ticker].price * executions[ticker].size
                    ) / (
                        self.holdings.transaction[ticker].size - executions[ticker].size
                    )
                    self.holdings.transaction[ticker].size -= executions[ticker].size

                else:
                    pnl = (
                        self.holdings.transaction[ticker].price
                        - executions[ticker].price
                    ) * self.holdings.transaction[ticker].size

                    self.holdings.transaction[ticker].price = executions[ticker].price
                    self.holdings.transaction[ticker].size = (
                        executions[ticker].size - self.holdings.transaction[ticker].size
                    )
                    self.holdings.transaction[ticker].position = Order.LONG

                short_pnl += pnl

            elif (
                self.holdings.transaction[ticker].position == Order.LONG
                and executions[ticker].position == Order.LONG
            ):

                self.holdings.transaction[ticker].price = (
                    self.holdings.transaction[ticker].get_amount()
                    + executions[ticker].price * executions[ticker].size
                ) / (self.holdings.transaction[ticker].size + executions[ticker].size)
                self.holdings.transaction[ticker].size += executions[ticker].size

            elif (
                self.holdings.transaction[ticker].position == Order.SHORT
                and executions[ticker].position == Order.SHORT
            ):

                self.holdings.transaction[ticker].price = (
                    self.holdings.transaction[ticker].get_amount()
                    + executions[ticker].price * executions[ticker].size
                ) / (self.holdings.transaction[ticker].size + executions[ticker].size)
                self.holdings.transaction[ticker].size += executions[ticker].size

            if self.holdings.transaction[ticker].size == 0.0:
                self.holdings.transaction[ticker].clear()

        return long_pnl, short_pnl

    def trading(self, current_data: pd.DataFrame):
        executions = self.Strategy.trading(current_data, self.holdings)

        long_pnl, short_pnl = self.brocker(executions)

        long_asset, short_asset = self.holdings.calculate_asset()

        return long_asset, short_asset, long_pnl, short_pnl
