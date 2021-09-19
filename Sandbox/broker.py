### Import necessary object ###
from Sandbox import Holding, Order, OrderBook


class Broker:
    """
    The utility of Broker:
        1. Execute order from strategy
        2. Calculate current equity and fiat holdings
        3. Analyze turnover rate and count long short position
    """

    def calculate_turnover(self, total_assets: float, new_orders: OrderBook) -> float:
        """
        Calculate turnover rate by examining current order
        turnover = amount of change in position / total holdings

        Parameters
        ----------
        total_assets: float
            current assets including fiat, long, and short
        new_orders: OrderBook
            the orders created by the strategy
        Returns
        -------
        turnover_rate: float
            The turnover rate of current execution
        """

        # Calculate total turnover amount
        turnover_amount = 0.0

        for ticker in new_orders.equity:
            if new_orders.equity[ticker].position != Order.NONE:
                turnover_amount += new_orders.equity[ticker].get_amount()

        # Calculate turnover rate
        turnover_rate = turnover_amount / total_assets

        return turnover_rate

    def execute(self, holdings: Holding, new_orders: OrderBook) -> tuple:
        """
        Execute new orders and update current holdings

        Parameters
        ----------
        holdings: Holding
            current holdings before executing new orders
        new_orders: OrderBook
            the orders created by the strategy
        Returns
        -------
        long_pnl: float
            The PnL aquired by a long position
        short_pnl:float
            The PnL aquired by a long position
        fiat_pnl: float
            The PnL of long and short execution
        """

        # Calculate total long, short and fiat profit and loss
        long_pnl, short_pnl, fiat_pnl = 0.0, 0.0, 0.0

        for ticker in new_orders.equity:

            # possessed long position and decide to short sell
            if (
                holdings.equity[ticker].position == Order.LONG
                and new_orders.equity[ticker].position == Order.SHORT
            ):

                # There are still long position left after executing short sell
                if new_orders.equity[ticker].size <= holdings.equity[ticker].size:

                    # Calculate PnL
                    pnl = (
                        new_orders.equity[ticker].price - holdings.equity[ticker].price
                    ) * new_orders.equity[ticker].size

                    fiat_pnl += (
                        new_orders.equity[ticker].price * new_orders.equity[ticker].size
                    )

                    # Update current holdings
                    holdings.equity[ticker].price = (
                        holdings.equity[ticker].get_amount()
                        - (
                            new_orders.equity[ticker].price
                            * new_orders.equity[ticker].size
                        )
                    ) / (holdings.equity[ticker].size - new_orders.equity[ticker].size)

                    holdings.equity[ticker].size -= new_orders.equity[ticker].size

                # All previous long position are sold and new short position are placed
                else:

                    # Calculate PnL
                    pnl = (
                        new_orders.equity[ticker].price - holdings.equity[ticker].price
                    ) * holdings.equity[ticker].size

                    fiat_pnl += (
                        new_orders.equity[ticker].price * holdings.equity[ticker].size
                    )

                    # Update current holdings
                    holdings.equity[ticker].price = new_orders.equity[ticker].price

                    holdings.equity[ticker].size = (
                        new_orders.equity[ticker].size - holdings.equity[ticker].size
                    )

                    holdings.equity[ticker].position = Order.SHORT

                long_pnl += pnl

            # possessed short position and decide to long buy
            elif (
                holdings.equity[ticker].position == Order.SHORT
                and new_orders.equity[ticker].position == Order.LONG
            ):

                # There are still short position left after executing long buy
                if new_orders.equity[ticker].size <= holdings.equity[ticker].size:

                    # Calculate PnL
                    pnl = (
                        holdings.equity[ticker].price - new_orders.equity[ticker].price
                    ) * new_orders.equity[ticker].size

                    fiat_pnl += pnl

                    # Update current holdings
                    holdings.equity[ticker].price = (
                        holdings.equity[ticker].get_amount()
                        - new_orders.equity[ticker].price
                        * new_orders.equity[ticker].size
                    ) / (holdings.equity[ticker].size - new_orders.equity[ticker].size)

                    holdings.equity[ticker].size -= new_orders.equity[ticker].size

                # All previous short position are cleared and new long position are placed
                else:

                    # Calculate PnL
                    pnl = (
                        holdings.equity[ticker].price - new_orders.equity[ticker].price
                    ) * holdings.equity[ticker].size

                    fiat_pnl += (
                        holdings.equity[ticker].price * holdings.equity[ticker].size
                        - new_orders.equity[ticker].price
                        * new_orders.equity[ticker].size
                    )

                    # Update current holdings
                    holdings.equity[ticker].price = new_orders.equity[ticker].price

                    holdings.equity[ticker].size = (
                        new_orders.equity[ticker].size - holdings.equity[ticker].size
                    )

                    holdings.equity[ticker].position = Order.LONG

                short_pnl += pnl

            # possessed long position and decide to buy more
            elif (
                holdings.equity[ticker].position == Order.LONG
                and new_orders.equity[ticker].position == Order.LONG
            ):

                # Calculate PnL
                fiat_pnl += new_orders.equity[ticker].get_amount() * (-1)

                # Update current holdings
                holdings.equity[ticker].price = (
                    holdings.equity[ticker].get_amount()
                    + new_orders.equity[ticker].price * new_orders.equity[ticker].size
                ) / (holdings.equity[ticker].size + new_orders.equity[ticker].size)

                holdings.equity[ticker].size += new_orders.equity[ticker].size

            # possessed short position and decide to sell more
            elif (
                holdings.equity[ticker].position == Order.SHORT
                and new_orders.equity[ticker].position == Order.SHORT
            ):

                # Update current holdings
                holdings.equity[ticker].price = (
                    holdings.equity[ticker].get_amount()
                    + new_orders.equity[ticker].price * new_orders.equity[ticker].size
                ) / (holdings.equity[ticker].size + new_orders.equity[ticker].size)

                holdings.equity[ticker].size += new_orders.equity[ticker].size

            # Didn't possess any position and decide to place new orders
            elif holdings.equity[ticker].position == Order.NONE:

                # Update current holdings
                holdings.equity[ticker].price = new_orders.equity[ticker].price

                holdings.equity[ticker].size += new_orders.equity[ticker].size

                holdings.equity[ticker].position = new_orders.equity[ticker].position

                # Update PnL if new orders is a long position
                if new_orders.equity[ticker].position == Order.LONG:
                    fiat_pnl += new_orders.equity[ticker].get_amount() * (-1)

            # Cleasen current holdings
            if holdings.equity[ticker].size == 0.0:
                holdings.equity[ticker].clear()

        return long_pnl, short_pnl, fiat_pnl
