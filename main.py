import datetime as dt
import os

from Sandbox import Container
from Engine import Engine, Data
from Manager import PortfolioManager

from Util.args import get_args
from Util.processor import save_result


def main():

    # Parse Command line Arguments

    args = get_args()
    start, end = dt.datetime.strptime(
        args.start_date, "%Y-%m-%d"
    ), dt.datetime.strptime(args.end_date, "%Y-%m-%d")

    data = Data(start, end)
    data.fetch_all()

    manager = PortfolioManager()

    sandbox = Container(args.strategy_file, args.universe_file)

    engine = Engine(data, start, end, sandbox, manager)

    engine.run()

    save_path = "./history-strategy/" + args.save_file
    os.mkdir(save_path)

    save_result(manager, save_path, args)


if __name__ == "__main__":
    main()
