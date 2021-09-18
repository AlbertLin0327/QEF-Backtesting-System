import pandas as pd
import datetime as dt


class Data:
    def __init__(self, start: dt.datetime, end: dt.datetime, price_vol: dict = {}):
        self.start_date = start
        self.end_date = end
        self.price_vol = price_vol

    def _fetch(self, file_path):

        # Read the file and transform to pandas.data_form
        data = pd.read_parquet(file_path)

        data["adj_close_"] = pd.to_numeric(data["adj_close_"], downcast="float")

        print(data)

        return data

    def fetch_all(self):
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

        return self.price_vol

    def fetch_date(self, date: dt.date):
        try:
            return self.price_vol[date.strftime("%Y-%m-%d")]
        except:
            return None
