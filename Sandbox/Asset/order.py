import datetime as dt
import pandas as pd


class Order:
    LONG = 1
    NONE = 0
    SHORT = -1

    def __init__(
        self,
        date: dt.date = dt.datetime.now().date(),
        ticker: str = "",
        size: float = 0.0,
        price: float = 0.0,
        position: int = 0,
    ):
        self._date = date
        self._ticker = ticker
        self._size = size
        self._price = price
        self._position = position

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, new_date):
        if type(new_date) == dt.date:
            self._date = new_date
        else:
            raise TypeError("Order date needs to be dt.date")

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, new_ticker):
        try:
            self._ticker = str(new_ticker)
        except:
            raise TypeError("Order ticker needs to be str")

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, new_size):
        try:
            self._size = float(new_size)
        except:
            raise TypeError("Order size needs to be float")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        try:
            self._price = float(new_price)
        except:
            raise TypeError("Order price needs to be float")

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        if new_position in [self.LONG, self.NONE, self.SHORT]:
            self._position = new_position
        else:
            raise TypeError("Order price needs to be enum LONG, SHORT, or NONE")

    def get_amount(self):
        return self.size * self.price

    def clear(self):
        self._size = 0.0
        self._price = 0.0
        self._position = self.NONE


class OrderBook:
    def __init__(self, order_list: list = []):
        def _convert_order_list(order_list):
            _new_transaction = {}

            try:
                for order in order_list:
                    _new_transaction[order.ticker] = order

            except:
                raise Exception(
                    "The order_list argument should be a list of Class Order"
                )

            return _new_transaction

        self._transaction = _convert_order_list(order_list)

    @property
    def transaction(self):
        return self._transaction

    @transaction.setter
    def transaction(self, new_transaction):
        if type(new_transaction) == list:

            def _convert_order_list(order_list):
                _new_transaction = {}

                try:
                    for order in order_list:
                        _new_transaction[order.ticker] = order

                except:
                    raise Exception(
                        "The order_list argument should be a list of Class Order"
                    )

                return _new_transaction

            self._transaction = _convert_order_list(new_transaction)

        else:
            raise TypeError("The order_list argument should be a list of Class Order")


class Holding(OrderBook):
    def __init__(self, order_list: list, universe: pd.DataFrame, date: dt.date):
        def fill_void():
            for ticker in universe["ticker"]:
                if ticker not in self.transaction:
                    self.transaction[ticker] = Order(ticker=ticker, date=date)

        super().__init__(order_list)
        fill_void()

    def calculate_asset(self, current_data) -> tuple:
        long_asset, short_asset = 0.0, 0.0

        for ticker in self.transaction:
            if self.transaction[ticker].position == Order.LONG:
                long_asset += (
                    current_data[current_data["identifier"] == ticker][
                        "adj_close_"
                    ].values[0]
                    * self.transaction[ticker].size
                )

            elif self.transaction[ticker].position == Order.SHORT:
                short_asset += (
                    self.transaction[ticker].price
                    - current_data[current_data["identifier"] == ticker][
                        "adj_close_"
                    ].values[0]
                ) * self.transaction[ticker].size

        return long_asset, short_asset
