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

    args = parser.parse_args()
    args.start_date = dt.datetime.strptime(args.start_date, "%Y-%m-%d")
    args.end_date = dt.datetime.strptime(args.end_date, "%Y-%m-%d")

    return args
