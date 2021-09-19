# QEF-Backtesting-System

usage: main.py [-h] --start-date START_DATE --end-date END_DATE
               --strategy_file STRATEGY_FILE --universe_file UNIVERSE_FILE
               [--save_file SAVE_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --start-date START_DATE
                        Backtesting Strating Time, fromat: YYYY-mm-dd
  --end-date END_DATE   Backtesting Ending Time, fromat: YYYY-mm-dd
  --strategy_file STRATEGY_FILE
                        Backtesting Strategy File Name
  --universe_file UNIVERSE_FILE
                        Backtesting Universe Path Name
  --save_file SAVE_FILE
                        Historical Strategy

for example, you can use 
python3 main.py --start-date 2019-01-01 --end-date 2019-3-31 --strategy_file mean_reversal --universe_file Taiwan_50
to see the result of the given duration with strategy and universe.

