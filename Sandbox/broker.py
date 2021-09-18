from Sandbox import Holding, Order, OrderBook


class Broker:
    def calculate_turnover(self, total_assets: float, executions: OrderBook):

        turnover_amount = 0.0

        for ticker in executions.transaction:
            if executions.transaction[ticker].position != Order.NONE:
                turnover_amount += executions.transaction[ticker].get_amount()

        return turnover_amount / total_assets

    def execute(self, holdings: Holding, executions: OrderBook):

        long_pnl, short_pnl, fiat_pnl = 0.0, 0.0, 0.0

        for ticker in executions.transaction:

            if (
                holdings.transaction[ticker].position == Order.LONG
                and executions.transaction[ticker].position == Order.SHORT
            ):

                if (
                    executions.transaction[ticker].size
                    <= holdings.transaction[ticker].size
                ):
                    pnl = (
                        executions.transaction[ticker].price
                        - holdings.transaction[ticker].price
                    ) * executions.transaction[ticker].size

                    fiat_pnl += (
                        executions.transaction[ticker].price
                        * executions.transaction[ticker].size
                    )

                    holdings.transaction[ticker].price = (
                        holdings.transaction[ticker].get_amount()
                        - executions.transaction[ticker].price
                        * executions.transaction[ticker].size
                    ) / (
                        holdings.transaction[ticker].size
                        - executions.transaction[ticker].size
                    )
                    holdings.transaction[ticker].size -= executions.transaction[
                        ticker
                    ].size

                else:
                    pnl = (
                        executions.transaction[ticker].price
                        - holdings.transaction[ticker].price
                    ) * holdings.transaction[ticker].size

                    fiat_pnl += (
                        executions.transaction[ticker].price
                        * holdings.transaction[ticker].size
                    )

                    holdings.transaction[ticker].price = executions.transaction[
                        ticker
                    ].price
                    holdings.transaction[ticker].size = (
                        executions.transaction[ticker].size
                        - holdings.transaction[ticker].size
                    )
                    holdings.transaction[ticker].position = Order.SHORT

                long_pnl += pnl

            elif (
                holdings.transaction[ticker].position == Order.SHORT
                and executions.transaction[ticker].position == Order.LONG
            ):

                if (
                    executions.transaction[ticker].size
                    <= holdings.transaction[ticker].size
                ):
                    pnl = (
                        holdings.transaction[ticker].price
                        - executions.transaction[ticker].price
                    ) * executions.transaction[ticker].size

                    fiat_pnl += pnl

                    holdings.transaction[ticker].price = (
                        holdings.transaction[ticker].get_amount()
                        - executions.transaction[ticker].price
                        * executions.transaction[ticker].size
                    ) / (
                        holdings.transaction[ticker].size
                        - executions.transaction[ticker].size
                    )
                    holdings.transaction[ticker].size -= executions.transaction[
                        ticker
                    ].size

                else:
                    pnl = (
                        holdings.transaction[ticker].price
                        - executions.transaction[ticker].price
                    ) * holdings.transaction[ticker].size

                    fiat_pnl += (
                        holdings.transaction[ticker].price
                        * holdings.transaction[ticker].size
                        - executions.transaction[ticker].price
                        * executions.transaction[ticker].size
                    )

                    holdings.transaction[ticker].price = executions.transaction[
                        ticker
                    ].price
                    holdings.transaction[ticker].size = (
                        executions.transaction[ticker].size
                        - holdings.transaction[ticker].size
                    )
                    holdings.transaction[ticker].position = Order.LONG

                short_pnl += pnl

            elif (
                holdings.transaction[ticker].position == Order.LONG
                and executions.transaction[ticker].position == Order.LONG
            ):

                holdings.transaction[ticker].price = (
                    holdings.transaction[ticker].get_amount()
                    + executions.transaction[ticker].price
                    * executions.transaction[ticker].size
                ) / (
                    holdings.transaction[ticker].size
                    + executions.transaction[ticker].size
                )
                holdings.transaction[ticker].size += executions.transaction[ticker].size

                fiat_pnl += executions.transaction[ticker].get_amount() * (-1)

            elif (
                holdings.transaction[ticker].position == Order.SHORT
                and executions.transaction[ticker].position == Order.SHORT
            ):

                holdings.transaction[ticker].price = (
                    holdings.transaction[ticker].get_amount()
                    + executions.transaction[ticker].price
                    * executions.transaction[ticker].size
                ) / (
                    holdings.transaction[ticker].size
                    + executions.transaction[ticker].size
                )
                holdings.transaction[ticker].size += executions.transaction[ticker].size

            elif holdings.transaction[ticker].position == Order.NONE:

                holdings.transaction[ticker].price = executions.transaction[
                    ticker
                ].price
                holdings.transaction[ticker].size += executions.transaction[ticker].size
                holdings.transaction[ticker].position = executions.transaction[
                    ticker
                ].position

                if executions.transaction[ticker].position == Order.LONG:
                    fiat_pnl += executions.transaction[ticker].get_amount() * (-1)

            if holdings.transaction[ticker].size == 0.0:
                holdings.transaction[ticker].clear()

        return long_pnl, short_pnl, fiat_pnl
