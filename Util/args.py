import argparse
import datetime as dt


def get_args():

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
        "--strategy_file", required=True, help="Backtesting Strategy File Name"
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
