# QEF-Backtesting-System

#### This is a Quantitative Evaluation Framework written in Python. Traders can gain insight into the effectiveness of an idea without risking funds in trading accounts through the QEF-Backtesting system.    
   
## Prerequisites   
1. Fork or clone the repository.   
   
2. Downloads the data provided in the QEF shared folders and rename it as "raw_data". The folder structure is provided in the following for clarification.   
```
.
|
|--- raw_data
|   |--- mapping.csv
|   |--- pricevol.csv
|
|--- Util
    |--- data-processing.py
```   
   
3. You are advised to install Python dependencies as listed. But you can also maintain dependencies on your own.   
```
pip3 install -r dependency.txt
```
or  
```
python3 -m pip install -r dependency.txt
```
   
4. Run the data-procesing.py to process the raw_data and store them into Dataset. Remeber to execute it under the folder Util.
```
cd Util
python3 data-processing.py
```   
