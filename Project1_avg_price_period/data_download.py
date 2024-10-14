import yfinance as yf
import numpy as np
def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
def calculate_and_display_average_price(data):
    price = data
    lst = np.array(price['Close'].values).tolist()
    average_of_list = sum(lst) / len(lst)
    return average_of_list
