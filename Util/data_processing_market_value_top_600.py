### Import necessary library ###
import pandas as pd
import argparse
import dask.dataframe as da
from tqdm import tqdm

### Import universe constant ###
from parameters import MARKET_VALUE_TOP_600

### Constant Variable ###
RAW = "../raw_data"
DATASET = "../Dataset/Universe/MARKET_VALUE_TOP_600"


### Main Program ###
def get_args() -> argparse.Namespace:
    """
    Get arguments from command line and 3 arguments can be specified.
        1. input-price-volume: file path of the price and volume file for all data
        2. input-mapping: file path of the mapping of ticker to company information
        3. output: file path for the desire root of proccessed data

    Parameters
    ----------
    None

    Returns
    -------
    argparse.Namespace
        a list of (argument: value) pair
    """

    # parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-price-volume",
        default=RAW + "/pricevol.csv",
        help="Root file for proccessed data",
    )

    parser.add_argument(
        "--input-mapping",
        default=RAW + "/mapping.csv",
        help="Root file for proccessed data",
    )

    parser.add_argument(
        "--output",
        default=DATASET,
        help="Customized root file for storing proccessed data",
    )

    # add to args list
    args = parser.parse_args()
    return args


def read_csv_file(
    filename: str, drop_fields: list = [], cleanse_is_backfill: bool = True
) -> pd.DataFrame:
    """
    Read file of the specified path

    Parameters
    ----------
    filename: str
        The path of the specified filename to read
    drop_fields: list
        The fields to drop; keep all else
    cleanse_is_backfill: bool
        Whether to change t --> True

    Returns
    -------
    pd.DataFrame
        The dataframe of the raw file
    """

    # Read the file and drop unwanted fields
    df = pd.read_csv(filename, low_memory=False)
    data = df.drop(drop_fields, axis=1)

    # map is_backfill value from 't' --> True
    if cleanse_is_backfill:
        data["is_backfill"] = data["is_backfill"].map({"t": True, "f": False})

    # Return the extracted csv file
    return data


def proccessor_date_to_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize by date and store the id fields. Also, apply some type trandformation on them

    Parameters
    ----------
    df: pd.DataFrame
        The original dataframe of pricevol

    Returns
    -------
    pd.DataFrame
        The dataframe of the (date: [id]) pairs
    """

    # Change date_ and db_timestamp string to datetime format
    df["date_"] = pd.to_datetime(df["date_"], format="%Y-%m-%d")
    df["db_timestamp"] = pd.to_datetime(
        df["db_timestamp"], format="%Y-%m-%d %H:%M:%S.%f"
    )

    # Change price to float type
    df["high_"] = df["high_"].apply(float)
    df["low_"] = df["low_"].apply(float)
    df["open_"] = df["open_"].apply(float)
    df["close_"] = df["close_"].apply(float)
    df["volume_"] = df["volume_"].apply(float)
    df["adj_close_"] = df["adj_close_"].apply(float)

    # Group by date and extract thir id
    data = (
        df.groupby(pd.Grouper(key="date_", freq="1d"))["id"].apply(list).reset_index()
    )

    # Remove empty date
    data = data[data.id.str.len() != 0]

    return data


def find_valid_interval(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter dataframe and select those in 0050, also find interval where all stock exists

    Parameters
    ----------
    df: pd.DataFrame
        The original dataframe of pricevol

    Returns
    -------
    pd.DataFrame
        The filtered dataframe
    """

    df = df.loc[df["identifier"].isin(MARKET_VALUE_TOP_600)]

    return df


def save_df_as_parquet(df: pd.DataFrame, path: str, chunksize: int = 10000) -> None:
    """
    Convert dataframe to parquet file

    Parameters
    ----------
    df: pd.DataFrame
        The original dataframe to be transformed
    path: str
        The root path to store the parquet file
    chunksize: int=20000
        The size of one parquet file

    Returns
    -------
    None
    """

    # Transform dataframe to dask.dataframe and store as parquet
    ddf = da.from_pandas(df, chunksize=chunksize)
    ddf.to_parquet(path)


def save_prices_file(
    df: pd.DataFrame, table: pd.DataFrame, path: str = DATASET, chunksize: int = 5000
) -> None:
    """
    Convert price-volume dataframe to parquet file into time structure folder

    Parameters
    ----------
    df: pd.DataFrame
        The original dataframe for all price and volume data
    table: pd.DataFrame
        The dataframe to map date to id
    path: str=DATASET
        The root file to store the price volume file
    chunksize: int=10000
        The size of one parquet file

    Returns
    -------
    None
    """

    # Iterate over all time
    with tqdm(total=table.shape[0]) as pbar:
        for index, data in tqdm(table.iterrows()):

            # Filter desired data out of dataframe
            filtered_df = (
                df.loc[df["id"].isin(data["id"])].set_index("id").reset_index()
            )

            # Parse date for folder structure formatting
            date_str = data["date_"].date()
            year, month, date = (
                date_str.strftime("%Y"),
                date_str.strftime("%m"),
                date_str.strftime("%d"),
            )

            # If the full frame is valid
            if len(filtered_df) == len(MARKET_VALUE_TOP_600):

                # Save the filtered dataframe to parquet file
                save_df_as_parquet(
                    filtered_df,
                    f"{path}/Price-Volume/{year}/{month}/{date}/",
                    chunksize,
                )

            # Update tqdm
            pbar.update(1)


def main():

    # Get arguments if needed
    args = get_args()
    print(args)

    # Open mapping.csv and save as parquet file
    print("--- Start Processing mapping.csv and save as parquet ---")
    mapping = read_csv_file(args.input_mapping, ["vendor_timestamp"])

    # Filter mapping with only Taiwan 50.
    mapping = mapping.loc[
        (mapping["ticker"].isin(MARKET_VALUE_TOP_600)) & (mapping["exchange"] == "TW")
    ].reset_index()

    save_df_as_parquet(mapping, args.output + "/mapping", 15000)

    # Save mapping file
    print("--- Start Processing pricevol.csv and save as parquet ---")
    price_vol = read_csv_file(args.input_price_volume, ["vendor_timestamp"])

    # Filter stock data with only taiwan 0050
    price_vol = find_valid_interval(price_vol)

    # Turn to (date: [id]) pair dataframe
    date_id = proccessor_date_to_id(price_vol)

    # Sort pricevol according to identifier
    price_vol = price_vol.sort_values("identifier")

    # Save the processed filefile as parquet
    save_prices_file(price_vol, date_id, args.output)

    print("--- End Processing ---")


# Execute main function
if __name__ == "__main__":
    main()
