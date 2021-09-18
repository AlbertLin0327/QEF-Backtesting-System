import pandas as pd
import datetime as dt
import numpy as np

from Sandbox import Holding, Order, OrderBook, Broker


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

        # Broker
        self.broker = Broker()

        # Instance Variable
        self.holdings = Holding([], self.Universe, dt.datetime.now().date)

        self.fiat = 100

    def trading(self, current_data: pd.DataFrame):

        executions = self.Strategy.trade(
            data=current_data, holding=self.holdings, fiat=self.fiat
        )

        long_pnl, short_pnl, fiat_pnl = self.broker.execute(self.holdings, executions)

        self.fiat += fiat_pnl

        long_asset, short_asset = self.holdings.calculate_asset(current_data)

        total_assets = self.fiat + long_asset - short_asset

        turnover = self.broker.calculate_turnover(total_assets, executions)

        return long_asset, short_asset, self.fiat, long_pnl, short_pnl, turnover
