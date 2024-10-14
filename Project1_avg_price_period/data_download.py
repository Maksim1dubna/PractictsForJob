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
    average_of_list = sum(price['Close'].values) / len(price['Close'].values)
    return average_of_list
