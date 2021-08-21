# import necessary libraries
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot(assets, years):

    fig = plt.figure(figsize=(10, 10))

    # plot the assets curve
    plt.title("Assets curve")
    plt.xlabel("Time")
    plt.ylabel("Assets")

    # draw the fitting curve
    plt.plot(years, assets)

    # plt.show()
    fig.savefig("PnL.png")


def sendbox(data: pd.DataFrame, cur_holdings):

    # Random buy some stock at the opening and sell at the closing
    if cur_holdings is None:
        asset = 10000
    else:
        asset = sum(cur_holdings * data[-2]["close_"])

    current_holdings = (
        asset * np.random.dirichlet(np.ones(len(data[-1]))) / data[-1]["open_"]
    )

    newAsset = sum(current_holdings * (data[-1]["close_"]))

    return current_holdings, newAsset


def fetch(file_path):

    # Read the file and transform to pandas.data_form
    data = pq.read_table(source=file_path).to_pandas()
    return data


def fetcher(price_vol: dict, date: datetime):

    # return the price information for the given date
    try:
        return price_vol[date.strftime("%Y-%m-%d")]
    except:
        return None


def engine(price_vol: dict, start: datetime, end: datetime):

    # The main part of the engine component
    delta = datetime.timedelta(days=1)

    data, years, assets, current_holdings = [], [], [], None

    while start <= end:

        # Fetch the date
        current_data = fetcher(price_vol, start)

        if current_data is not None:
            years.append(start)
            data.append(current_data)
            current_holdings, current_asset = sendbox(data, current_holdings)
            assets.append(current_asset)

        start += delta

    # plot assets curve
    plot(assets, years)


def init():

    print("--- Read in data ---")

    # Store all the price volume information
    price_vol = {}

    # Looping through the date
    start_date = datetime.date(1981, 1, 5)
    end_date = datetime.date(2020, 12, 31)
    delta = datetime.timedelta(days=1)

    # Get all the price data
    while start_date <= end_date:
        try:
            price_vol[start_date.strftime("%Y-%m-%d")] = fetch(
                f"../Dataset/Price-Volume/" + start_date.strftime("%Y/%m/%d")
            )
        except:
            pass
        finally:
            start_date += delta

    print("--- Start Engine ---")

    # Start the engine
    engine(price_vol, datetime.date(1981, 1, 5), datetime.date(2020, 12, 31))


if __name__ == "__main__":
    init()
