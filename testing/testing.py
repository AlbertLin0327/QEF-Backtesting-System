#import necessary libraries
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def fetch(file_path): 
    # Read the file and transform to pandas.data_form
    data = pq.read_table(source=file_path).to_pandas()
    return data

def search(price_vol, year, month, day): 
    # return the price information for the given date
    try:
        return price_vol[f"{year}-{month:02}-{day:02}"]
    except:
        print("invalid date")
        return None

def search_interval(price_vol, start, end):
    # return all the information from start_date to end_date
    data = []
    for year in range(start[0], end[0] + 1):
        for month in range(1, 13):
            for day in range(1, 32):
                if f'{start[0]}-{start[1]:02}-{start[2]:02}' <= f'{year}-{month:02}-{day:02}' <= f'{end[0]}-{end[1]:02}-{end[2]:02}':
                    try:
                        data.append(price_vol[f"{year}-{month:02}-{day:02}"])
                    except:
                        continue
    return data

def main():
    print('transforming parquet to data array.')
    mapping = []
    for i in range(4):
        mapping.append(fetch(f"../Dataset/mapping/part.{i}.parquet"))
    price_vol = {}
    for year in range(1981, 2021):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    price_vol[f"{year}-{month:02}-{day:02}"] = fetch(f"../Dataset/Price-Volume/{year}/{month:02}/{day:02}")
                except:
                    continue

if __name__ == "__main__":
    main()