import datetime as dt
import sys
sys.path.append('../')
from Manager.manager import Manager

class Engine:

    # Parameter setting
    def __init__(self, price_vol: dict, start: dt.datetime, end: dt.datetime, sandbox, manager: Manager):
        self.delta = dt.timedelta(days=1)
        self.price_vol = price_vol
        self.start_date = start
        self.end_date = end
        self.sandbox = sandbox
        self.manager = manager


    def fetch(self, date: dt.datetime):
        
        # return the price information for the given date
        try:
            return self.price_vol[date.strftime("%Y-%m-%d")]
        except:
            return None

    # Main component of the engine
    def run(self):
        
        current_date = self.start_date
        
        while current_date <= self.end_date:
            
            # Fetch the data
            current_data = self.fetch(current_date)

            if current_data is not None:
                self.manager.setYear(current_date)
                self.manager.run(self.sandbox.perform(current_data))
        
            current_date += self.delta
        
        # Plot the needed curve
        self.manager.plot()