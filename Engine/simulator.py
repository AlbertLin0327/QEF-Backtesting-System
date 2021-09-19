### Import necessary library ###
import os
import numpy as np
import matplotlib
import datetime as dt

### Import necessary object ###
from Manager import PortfolioManager
from Engine import Data

### Set matplotlib ###
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class Engine:
    """
    The utility of Engine:
        1. Fetch data from Data
        2. Feed data to Sandbox
        3. Sand result to PortfolioManager
    """

    def __init__(
        self,
        data: Data,
        start: dt.datetime,
        end: dt.datetime,
        sandbox: object,
        manager: PortfolioManager,
    ):

        """
        Init function

        Parameters
        ----------
        data: Data
            The data used for backtesting
        start: dt.datetime
            The start time of the backtesting
        end: dt.datetime
            The start time of the backtesting
        sandbox: object
            The Sandbox to hold Strategy
        manager: PortfolioManager
            The Manager used calculate ratios

        Returns
        -------
        None
        """

        # Instance Variable
        self.delta = dt.timedelta(days=1)
        self.data = data
        self.start_date = start
        self.end_date = end
        self.sandbox = sandbox
        self.manager = manager

    def run(self):
        """
        Main component of Engine

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        current_date = self.start_date

        # Iterate over the time intervals
        while current_date <= self.end_date:

            # Fetch the data
            current_data = self.data.fetch_date(current_date)

            if current_data is not None:

                # Feed to Sandbox
                self.manager.setValidDate(current_date)

                (
                    long_asset,
                    short_asset,
                    total_fiat,
                    long_pnl,
                    short_pnl,
                    turnover,
                ) = self.sandbox.trading(current_data)

                # Feed to Portfolio Manager
                self.manager.run(
                    long_asset, short_asset, total_fiat, long_pnl, short_pnl, turnover
                )

            current_date += self.delta
