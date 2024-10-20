import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

ticker = "tsla"
start = datetime.now() - timedelta(days=2)
end = datetime.now()
price = yf.download(ticker, start=start, end=end, interval="1m")  # <class 'pandas.core.frame.DataFrame'>

print(price['Close'].values)
