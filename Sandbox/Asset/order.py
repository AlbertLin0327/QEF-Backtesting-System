### Import necessary library ###
import datetime as dt
import pandas as pd


class Order:
    """
    The utility of Order:
        1. Record order or holding information
    """

    # Necessary enum for self.position
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

        """
        Init function

        Parameters
        ----------
        date: dt.date = dt.datetime.now().date()
            The date of the order/ position being created
        ticker: str = ""
            The identifier of the ticker
        size: float = 0.0
            The size of the order/ position
        price: float = 0.0
            The mean price of the order/ position
        position: int = 0
            The position (Long/ Short) of the order/ position

        Returns
        -------
        None
        """

        # Instance Variable
        self._date = date
        self._ticker = ticker
        self._size = size
        self._price = price
        self._position = position

    # Setter and getter method to make sure the instance variables are in correct type
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

    # Calculate current amount of the order/ position
    def get_amount(self):
        return self.size * self.price

    # Clear current order/ position state
    def clear(self):
        self._size = 0.0
        self._price = 0.0
        self._position = self.NONE


class OrderBook:
    """
    The utility of OrderBook:
        1. Record whole orderbook of current order information
    """

    def __init__(self, order_list: list = []):
        """
        Init function

        Parameters
        ----------
        order_list: list = []
            The list of order class being placed, [Order]

        Returns
        -------
        None
        """

        # Inner function to convert order list into dictionary
        def _convert_order_list(order_list: list):
            _new_equity = {}

            # Convert the table
            try:
                for order in order_list:
                    _new_equity[order.ticker] = order
            except:
                raise Exception(
                    "The order_list argument should be a list of Class Order"
                )

            return _new_equity

        # Instance Variable
        self._equity = _convert_order_list(order_list)

    @property
    def equity(self):
        return self._equity

    # Setter and getter method to make sure the instance variables are in correct type
    @equity.setter
    def equity(self, new_equity):
        if type(new_equity) == list:

            # Same as the function defined in the init function
            def _convert_order_list(order_list):
                _new_equity = {}

                try:
                    for order in order_list:
                        _new_equity[order.ticker] = order
                except:
                    raise Exception(
                        "The order_list argument should be a list of Class Order"
                    )

                return _new_equity

            self._equity = _convert_order_list(new_equity)

        else:
            raise TypeError("The order_list argument should be a list of Class Order")


class Holding(OrderBook):
    """
    Current Holding inherit from OrderBook object:
        1. Track current holding position
    """

    def __init__(self, order_list: list, universe: pd.DataFrame, date: dt.date):
        """
        Init function

        Parameters
        ----------
        order_list: list = []
            The list of order class being placed, [Order]
        universe: pd.DataFrame
            The universe where the backtesting is taking place on
        date: dt.date
            The current date of backtesting

        Returns
        -------
        None
        """

        # Inner function to fill void fields
        def fill_void():
            for ticker in universe["ticker"]:
                if ticker not in self.equity:
                    self.equity[ticker] = Order(ticker=ticker, date=date)

        # Initialized instance variable
        super().__init__(order_list)

        # Execute fill_void
        fill_void()

    def calculate_asset(self, current_data: pd.DataFrame) -> tuple:
        """
        Calculate current long and short position values

        Parameters
        ----------
        current_data: pd.DataFrame
            current price_vol data

        Returns
        -------
        long_asset:float
            Current long position value
        short_asset:float
            Current short position value
        """

        long_asset, short_asset = 0.0, 0.0

        # Iterate through all asset
        for ticker in self.equity:

            # The value of long asset is the face value times bidding size
            if self.equity[ticker].position == Order.LONG:
                long_asset += (
                    current_data[current_data["identifier"] == ticker][
                        "adj_close_"
                    ].values[0]
                    * self.equity[ticker].size
                )

            # The values of short asset is (short - current price) times bidding size
            elif self.equity[ticker].position == Order.SHORT:
                short_asset += (
                    self.equity[ticker].price
                    - current_data[current_data["identifier"] == ticker][
                        "adj_close_"
                    ].values[0]
                ) * self.equity[ticker].size

        return long_asset, short_asset
