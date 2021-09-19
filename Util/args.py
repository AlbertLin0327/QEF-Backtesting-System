### Import necessary library ###
import argparse
import datetime as dt


def get_args() -> argparse.Namespace:
    """
    Get arguments from command line and 35arguments can be specified.
        1. start-date: The starting of backtesting interval
        2. end-date: The ending of backtesting interval
        3. strategy_file: The filename (without .py) of strategy being tested
        4. universe_file: The universe filename.
        5. save_file: The specified path to save the result

    Parameters
    ----------
    None

    Returns
    -------
    argparse.Namespace
        a list of (argument: value) pair
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start-date",
        required=True,
        help="Backtesting Strating Time, fromat: YYYY-mm-dd",
    )
    parser.add_argument(
        "--end-date", required=True, help="Backtesting Ending Time, fromat: YYYY-mm-dd"
    )
    parser.add_argument(
        "--strategy_file",
        required=True,
        help="Backtesting Strategy File Name (Without .py)",
    )
    parser.add_argument(
        "--universe_file", required=True, help="Backtesting Universe Path Name"
    )
    parser.add_argument(
        "--save_file",
        default=dt.datetime.now().strftime("%m-%d-%Y,%H:%M:%S"),
        help="Historical Strategy",
    )

    args = parser.parse_args()

    return args
