### Import necessary library ###
import datetime as dt
import os

### Import necessary object ###
from Sandbox import Container
from Engine import Engine, Data
from Manager import PortfolioManager

### Import necessary util function ###
from Util.args import get_args
from Util.processor import save_result


def main():

    # Parse Command line Arguments
    args = get_args()

    start = dt.datetime.strptime(args.start_date, "%Y-%m-%d")
    end = dt.datetime.strptime(args.end_date, "%Y-%m-%d")

    # Fetch Data from Universe
    data = Data(start, end)
    data.fetch_all()

    # Get main Component for backtesting
    manager = PortfolioManager()
    sandbox = Container(args.strategy_file, args.universe_file)
    engine = Engine(data, start, end, sandbox, manager)

    # Start Executing backtesting
    engine.run()

    # Save result to save_path
    save_path = "./history-strategy/" + args.save_file

    save_result(manager, save_path, args)


# Execute Main function
if __name__ == "__main__":
    main()
