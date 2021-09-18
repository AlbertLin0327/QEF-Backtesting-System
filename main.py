import datetime as dt

from Sandbox import Container
from Engine import Engine, Data
from Manager import Broker

from Util.args import get_args


def main():

    # Parse Command line Arguments
    args = get_args()
    start, end = args.start_date, args.end_date

    data = Data(start, end)
    data.fetch_all()

    broker = Broker()

    sandbox = Container(args.strategy_file, args.universe_file)

    engine = Engine(data, start, end, sandbox, broker)

    engine.run()


if __name__ == "__main__":
    main()
