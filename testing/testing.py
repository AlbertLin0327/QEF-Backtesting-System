#import necessary libraries
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import datetime

def fetch(file_path): 
    # Read the file and transform to pandas.data_form
    data = pq.read_table(source=file_path).to_pandas()
    return data

def fetcher(price_vol: dict, date: datetime): 
    # return the price information for the given date
    try:
        return price_vol[date.strftime('%Y-%m-%d')]
    except:
        print("invalid date")
        return None

def engine(price_vol: dict, start: datetime, end: datetime, current_holding):
    cur_holding, cur_pnl = manager()
    delta = datetime.timedelta(days=1)
    while start <= end:
        data = fetcher(price_vol, start)
        if data != None:
            sendbox(data, cur_holding)
        start += delta

def init():
    print('transforming parquet to data array.')
    mapping = []
    for i in range(4):
        mapping.append(fetch(f"../Dataset/mapping/part.{i}.parquet"))
    price_vol = {}
    start_date = datetime.date(1981, 1, 5)
    end_date = datetime.date(2020, 12, 31)
    delta = datetime.timedelta(days=1)
    while start_date <= end_date:
        try:
            price_vol[start_date.strftime('%Y-%m-%d')] = fetch(f"../Dataset/Price-Volume/" + start_date.strftime('%Y/%m/%d'))
        except:
            print("No such file")
        finally:
            start_date += delta

if __name__ == "__main__":
    init()