### Import necessary library ###
import pandas as pd
import datetime as dt
import numpy as np

### Import necessary object ###
from Sandbox import Holding, Order, OrderBook, Broker


class Container:
    """
    The utility of Container:
        1. Run the strategy
        2. Bridge the data between strategy and the rest of the system
    """

    def __init__(self, strategy_filename: str, universe_filename: str) -> None:
        """
        Init function

        Parameters
        ----------
        strategy_filename: str
            The filename of the strategy (Without .py)
        universe_filename: str
            The name of the universe being tested

        Returns
        -------
        None
        """

        # Import Strategy file
        import importlib

        self.strategy_path = "Sandbox.Strategy." + strategy_filename

        self.Strategy = getattr(
            importlib.import_module(self.strategy_path), "Strategy"
        )()

        # Import Universe file
        self.universe_path = "Dataset/Universe/" + universe_filename + "/mapping"

        self.Universe = pd.read_parquet(self.universe_path)

        # Initialized Broker
        self.broker = Broker()

        # current equity holdings
        self.holdings = Holding([], self.Universe, dt.datetime.now().date)

        # current fiat holdings
        self.fiat = 100

    def trading(self, current_data: pd.DataFrame, date: dt.date) -> tuple:
        """
        The main function to execute strategy.
        It will call "self.Strategy.trade" to initiate strategy.

        Parameters
        ----------
        current_data: pd.DataFrame
            Pass in the data of the universe of particular date
        date: dt.date
            Current date

        Returns
        -------
        long_asset: float
            The current value of long position
        short_asset: float
            The current value of short position (initial price - current price)
        self.fiat: float
            The current amount of fiat
        long_pnl: float
            The PnL aquired by a long position
        short_pnl: float
            The PnL aquired by a short position
        turnover: float
            The turnover rate of the stock
        """

        # Initiate strategy and get the order from it
        executions = self.Strategy.trade(
            data=current_data, holding=self.holdings, fiat=self.fiat, current_date=date
        )

        # Calculate the PnL of the order
        long_pnl, short_pnl, fiat_pnl = self.broker.execute(self.holdings, executions)

        # Calculate the holding asset
        long_asset, short_asset = self.holdings.calculate_asset(current_data)

        # Calculate current asset
        self.fiat += fiat_pnl
        total_assets = self.fiat + long_asset - short_asset

        # Calculate turnover
        turnover = self.broker.calculate_turnover(total_assets, executions)

        return long_asset, short_asset, self.fiat, long_pnl, short_pnl, turnover
