#import necessary libraries
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def fetch(file_path): # given file path and change it to two-dimensional data
    # print(f"Reading {file_path}")
    data = pq.read_table(source=file_path).to_pandas()
    return data

def search(price_vol, year, month, day): # given year/month/day, return the price information
    return price_vol[f"{year}-{month:02}-{day:02}"]

def main():
    print('transforming parquet to data array.')
    mapping = []
    for i in range(4):
        mapping.append(fetch(f"../Dataset/mapping/part.{i}.parquet"))
    print(mapping[0])
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