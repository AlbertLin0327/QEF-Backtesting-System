### Import necessary library ###
import matplotlib
import datetime as dt

matplotlib.use("Agg")
import matplotlib.pyplot as plt

### Import necessary object ###
from Lib import mean, square_deviation, stddev
from Sandbox import Order, OrderBook, Holding


class PortfolioManager(object):
    """
    The utility of PortfolioManager:
        1. Store result of strategy
        2. Calculate return and sharpe ratio
        3. Plot the curve
    """
    # Parameters setting
    def __init__(self) -> None:
        """
        Init function

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        # Initialize valid date
        self.valid_date = []

        # Initialize total assets
        self.assets = []

        # Initialize long assets
        self.long_asset = []

        # Initialize short assets
        self.short_asset = []

        # Initialize long pnl
        self.long_pnl = []

        # Initialize short pnl
        self.short_pnl = []

        # Initialize daily return
        self.daily_return = []

        # Initialize turnover
        self.turnover = []

        # Initialize annual data
        self.annual_return = []
        self.annual_sharpe_ratio = []

    # Appending valid trading date
    def setValidDate(self, date: dt.datetime) -> None:
        """
        Tell the manager that the date pass in has trading which is a valid date

        Parameters
        ----------
        date: dt.datetime
            Pass in the valid date into the date_list

        Returns
        -------
        None
        """
        self.valid_date.append(date)

    def run(self, long_asset: float, short_asset: float, total_fiat: float, 
            long_pnl: float, short_pnl: float, turnover: float):
        """
        The main function to execute manager.
        It will save all the passed arguments and calculate daily return

        Parameters: 
        ----------
        long_asset: float
            Pass in the current holding long assets' percentage to the initial fiat
        short_asset: float
            Pass in the current holding short assets' return
        total_fiat: float
            Pass in the current fiat's percentage to the initial fiat
        long_pnl: float
            Pass in the current long pnl
        short_pnl: float
            Pass in the current short pnl
        turnover: float   
            Pass in today's turnover

        Returns
        -------
        None
        """

        # Save the arguments
        self.assets.append(total_fiat + long_asset + short_asset)
        self.long_pnl.append(long_pnl)
        self.short_pnl.append(short_pnl)
        self.long_asset.append(long_asset)
        self.short_asset.append(short_asset)
        self.turnover.append(turnover)

        # Calculate the daily return
        self.cal_daily_return()

    def cal_sharpe_ratio(self) -> float:
        """
        Calculate the total sharpe ratio of the portfolio

        Parameters: 
        ----------
        None

        Returns
        -------
        shapre ratio: float
            the calculated sharpe ratio

        """

        # Sharpe ration = (expected porfolio return - risk free rate) / porfolio standard deviation
        r_p = mean(self.daily_return)
        theta_p = stddev(self.daily_return)
        sharpe_ratio = r_p / theta_p

        # Since it is daily value, annualize it by multiply by the square of trading days
        return (len(self.valid_date) ** 0.5) * sharpe_ratio

    def cal_daily_return(self) -> None:
        """
        Calculate the daily return of the portfolio

        Parameters: 
        ----------
        None

        Returns
        -------
        None

        """

        # Avoiding index out of range
        if len(self.assets) > 2:

            # daily return = (today's total asset / yesterday's total assest) - 1
            daily_return = self.assets[-1] / self.assets[-2] - 1
            self.daily_return.append(daily_return)

    def cal_total_return(self) -> float:
        """
        Calculate the total return of the portfolio

        Parameters: 
        ----------
        None

        Returns
        -------
        total_return: float
            the calculate total_return

        """

        # Initialize the total return to be 1.0
        total_return = 1.0

        for d in self.daily_return:

            # Total return = \prod_{all the days} (daily return) - 1.0
            total_return *= d + 1

        return total_return - 1.0

    def cal_annual_return(self) -> float:
        """
        Calculate the annual return of the portfolio

        Parameters: 
        ----------
        None

        Returns
        -------
        annual return: float
            the calculated annual return
        """

        # Calculate the annual return backward from end of the backtesting duration with period of 252 days
        for i in range(len(self.valid_date) - 1, 253, -252):
            annual_return, new_list = 1.0, self.daily_return[i - 253 : i]

            # Annual return = \prod_{last 252 days} (daily return) - 1
            for j in range(252):
                annual_return *= new_list[j] + 1

            self.annual_return.append(annual_return - 1.0)

        return self.annual_return - 1.0

    def cal_annual_sharpe_ratio(self) -> float:
        """
        Calculate the annual sharpe ratio of the portfolio

        Parameters: 
        ----------
        None

        Returns
        -------
        annual shapre ratio: float
            the calculated annual sharpe ratio
        """
        # Calculate the annual sharpe ratio backward from end of the backtesting duration with period of 252 days
        for i in range(len(self.valid_date) - 1, 253, -252):
            new_list = self.daily_return[i - 253 : i]

            # Sharpe ration = (expected porfolio return - risk free rate) / porfolio standard deviation
            r_p = mean(new_list)
            theta_p = stddev(new_list)

            # Since it is daily value, annualize it by multiply by the square of 252
            self.annual_sharpe_ratio.append((252 ** 0.5) * r_p / theta_p)

        return self.annual_sharpe_ratio

    def plot(self, data: list, path: str, title: str, ylabel: str) -> None:
        """
        Plot the curve of the given data with title and ylabel
        Save the figure with the given path
        Parameters: 
        ----------
        data: list
            the data passed in to be plot 
        path: str
            the path the figure to be saved
        title: str
            the figure's title
        ylabel: str
            the figure's ylabel
        Returns
        -------
        None

        """
        
        fig = plt.figure(figsize=(10, 10))

        # plot the given data curve
        plt.title(title)
        plt.xlabel("Time")
        plt.ylabel(ylabel)
        valid_date = self.valid_date[-len(data) :]

        # draw the fitting curve
        plt.plot(valid_date, data)

        # plt.show()
        fig.savefig(path + "/" + title.replace(" ", "_"))

    def plot_all(self, path: str) -> None:
        """
        Plot all needed figure

        Parameters: 
        ----------
        path: str
            the directory that all the figure are going to be saved

        Returns
        -------
        None 

        """

        # Plot all the needed figure
        self.plot(self.long_pnl, path, "Long PnL", "PnL")
        self.plot(self.short_pnl, path, "Short PnL", "PnL")
        self.plot(self.assets, path, "Total Assets", "Assets")
        self.plot(
            (self.long_asset + np.cumsum(self.long_pnl)),
            path,
            "Long Assets",
            "Assets",
        )
        self.plot(
            (self.short_asset + np.cumsum(self.short_pnl)),
            path,
            "Short Assets",
            "Assets",
        )
        self.plot(
            self.daily_return,
            path,
            "Daily Return",
            "Return",
        )
        self.plot(self.turnover, path, "Turnover", "Turnover Rate")
