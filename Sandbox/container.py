import pandas as pd
import datetime as dt
import numpy as np

from Sandbox import Holding, Order, OrderBook


class Container:
    def __init__(self, strategy_filename: str, universe_filename):

        # import necessary libraries
        import importlib

        # Import Strategy file
        self.strategy_path = "Sandbox.Strategy." + strategy_filename

        self.Strategy = getattr(
            importlib.import_module(self.strategy_path), "Strategy"
        )()

        # Import Universe file
        self.universe_path = "Dataset/Universe/" + universe_filename + "/mapping"

        self.Universe = pd.read_parquet(self.universe_path)

        # Instance Variable
        self.holdings = Holding([], self.Universe, dt.datetime.now().date)

    def broker(self, executions: OrderBook):

        long_pnl, short_pnl = 0.0, 0.0

        for ticker in executions.transaction:

            if (
                self.holdings.transaction[ticker].position == Order.LONG
                and executions.transaction[ticker].position == Order.SHORT
            ):

                if (
                    executions.transaction[ticker].size
                    <= self.holdings.transaction[ticker].size
                ):
                    pnl = (
                        executions.transaction[ticker].price
                        - self.holdings.transaction[ticker].price
                    ) * executions.transaction[ticker].size

                    self.holdings.transaction[ticker].price = (
                        self.holdings.transaction[ticker].get_amount()
                        - executions.transaction[ticker].price
                        * executions.transaction[ticker].size
                    ) / (
                        self.holdings.transaction[ticker].size
                        - executions.transaction[ticker].size
                    )
                    self.holdings.transaction[ticker].size -= executions.transaction[
                        ticker
                    ].size

                else:
                    pnl = (
                        executions.transaction[ticker].price
                        - self.holdings.transaction[ticker].price
                    ) * self.holdings.transaction[ticker].size

                    self.holdings.transaction[ticker].price = executions.transaction[
                        ticker
                    ].price
                    self.holdings.transaction[ticker].size = (
                        executions.transaction[ticker].size
                        - self.holdings.transaction[ticker].size
                    )
                    self.holdings.transaction[ticker].position = Order.SHORT

                print(pnl)
                long_pnl += pnl

            elif (
                self.holdings.transaction[ticker].position == Order.SHORT
                and executions.transaction[ticker].position == Order.LONG
            ):

                if (
                    executions.transaction[ticker].size
                    <= self.holdings.transaction[ticker].size
                ):
                    pnl = (
                        self.holdings.transaction[ticker].price
                        - executions.transaction[ticker].price
                    ) * executions.transaction[ticker].size

                    self.holdings.transaction[ticker].price = (
                        self.holdings.transaction[ticker].get_amount()
                        - executions.transaction[ticker].price
                        * executions.transaction[ticker].size
                    ) / (
                        self.holdings.transaction[ticker].size
                        - executions.transaction[ticker].size
                    )
                    self.holdings.transaction[ticker].size -= executions.transaction[
                        ticker
                    ].size

                else:
                    pnl = (
                        self.holdings.transaction[ticker].price
                        - executions.transaction[ticker].price
                    ) * self.holdings.transaction[ticker].size

                    self.holdings.transaction[ticker].price = executions.transaction[
                        ticker
                    ].price
                    self.holdings.transaction[ticker].size = (
                        executions.transaction[ticker].size
                        - self.holdings.transaction[ticker].size
                    )
                    self.holdings.transaction[ticker].position = Order.LONG

                short_pnl += pnl

            elif (
                self.holdings.transaction[ticker].position == Order.LONG
                and executions.transaction[ticker].position == Order.LONG
            ):

                self.holdings.transaction[ticker].price = (
                    self.holdings.transaction[ticker].get_amount()
                    + executions.transaction[ticker].price
                    * executions.transaction[ticker].size
                ) / (
                    self.holdings.transaction[ticker].size
                    + executions.transaction[ticker].size
                )
                self.holdings.transaction[ticker].size += executions.transaction[
                    ticker
                ].size

            elif (
                self.holdings.transaction[ticker].position == Order.SHORT
                and executions.transaction[ticker].position == Order.SHORT
            ):

                self.holdings.transaction[ticker].price = (
                    self.holdings.transaction[ticker].get_amount()
                    + executions.transaction[ticker].price
                    * executions.transaction[ticker].size
                ) / (
                    self.holdings.transaction[ticker].size
                    + executions.transaction[ticker].size
                )
                self.holdings.transaction[ticker].size += executions.transaction[
                    ticker
                ].size

            elif self.holdings.transaction[ticker].position == Order.NONE:

                print(type(executions.transaction[ticker].price))

                self.holdings.transaction[ticker].price = executions.transaction[
                    ticker
                ].price
                self.holdings.transaction[ticker].size += executions.transaction[
                    ticker
                ].size
                self.holdings.transaction[ticker].position = executions.transaction[
                    ticker
                ].position

            if self.holdings.transaction[ticker].size == 0.0:
                self.holdings.transaction[ticker].clear()

        return long_pnl, short_pnl

    def trading(self, current_data: pd.DataFrame):

        executions = self.Strategy.trade(data=current_data, holding=self.holdings)

        long_pnl, short_pnl = self.broker(executions)

        long_asset, short_asset = self.holdings.calculate_asset()

        return long_asset, short_asset, long_pnl, short_pnl
