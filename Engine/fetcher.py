import pandas as pd
import datetime as dt


class Data:
    """
    The utility of Data:
        1. Collect backtesting necessary data
    """

    def __init__(self, start: dt.datetime, end: dt.datetime, price_vol: dict = {}):
        """
        Init function

        Parameters
        ----------
        start: dt.datetime
            The start of the backtesting dataset
        end: dt.datetime
            The end of the backtesting dataset
        price_vol: dict = {}
            The dictionary (ticker -> pd.Dataframe) retrieve from the backtesting dataset

        Returns
        -------
        None
        """

        # Instance Variable
        self.start_date = start
        self.end_date = end
        self.price_vol = price_vol

    def _fetch(self, file_path: str):
        """
        Fetch price volume data from specified file path

        Parameters
        ----------
        file_path: str
            The file path of the specified data

        Returns
        -------
        data: pd.DataFrame
            The retrieved data
        """

        # Read the file and transform to pandas.data_form
        data = pd.read_parquet(file_path)

        # Transform data type of numeric data
        data["open_"] = pd.to_numeric(data["open_"], downcast="float")
        data["close_"] = pd.to_numeric(data["close_"], downcast="float")
        data["high_"] = pd.to_numeric(data["high_"], downcast="float")
        data["low_"] = pd.to_numeric(data["low_"], downcast="float")
        data["adj_close_"] = pd.to_numeric(data["adj_close_"], downcast="float")

        return data

    def fetch_all(self) -> None:
        """
        Fetch all price volume in the time interval

        Parameters
        ----------
        None

        Returns
        -------
        self.price_vol: pd.DataFrame
            The retrieved data
        """

        # Looping through the date
        start_date, end_date = self.start_date, self.end_date
        delta = dt.timedelta(days=1)

        # Get all the price data
        while start_date <= end_date:

            try:
                self.price_vol[start_date.strftime("%Y-%m-%d")] = self._fetch(
                    f"Dataset/Universe/Taiwan_50/Price-Volume/"
                    + start_date.strftime("%Y/%m/%d")
                )
            except:
                pass
            finally:
                start_date += delta

    def fetch_date(self, date: dt.date):
        """
        Fetch price volume of specified date

        Parameters
        ----------
        date: dt.date

        Returns
        -------
        self.price_vol[date]: pd.DataFrame
            The retrieved data
        """

        try:
            return self.price_vol[date.strftime("%Y-%m-%d")]
        except:
            return None
