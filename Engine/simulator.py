import datetime as dt

from Manager import Broker
from Engine import Data


class Engine:

    # Parameter setting
    def __init__(
        self,
        data: Data,
        start: dt.datetime,
        end: dt.datetime,
        sandbox,
        manager: Broker,
    ):
        self.delta = dt.timedelta(days=1)
        self.data = data
        self.start_date = start
        self.end_date = end
        self.sandbox = sandbox
        self.manager = manager

    # Main component of the engine
    def run(self):

        current_date = self.start_date

        while current_date <= self.end_date:

            # Fetch the data
            current_data = self.data.fetch_date(current_date)

            if current_data is not None:
                self.manager.setYear(current_date)
                long_asset, short_asset, long_pnl, short_pnl = self.sandbox.trading(
                    current_data
                )
                self.manager.run(long_asset, short_asset, long_pnl, short_pnl)

            current_date += self.delta

        # Plot the needed curve
        # self.manager.plot("../testing", "test", "none")
