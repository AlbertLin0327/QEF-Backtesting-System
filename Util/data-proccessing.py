# Import necessary library
import pandas as pd
import argparse

# Get arguments from command line
def get_args() -> argparse.Namespace:
    """Get arguments from command line

    Parameters
    ----------
    None

    Returns
    -------
    argparse.Namespace
        a list of argument: value pair
    """

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="output.csv", help="Output to csv file")

    # add to args list
    args = parser.parse_args()
    return args


def main():

    # Open two files
    mapping = pd.read_csv()
