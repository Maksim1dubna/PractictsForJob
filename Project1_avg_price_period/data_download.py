import csv
import yfinance as yf
import numpy as np
def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data

def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
def calculate_and_display_average_price(data): #  Задание 1 Вывод средней цены за период
    price = data
    average_of_list = sum(price['Close'].values) / len(price['Close'].values)
    return average_of_list

def notify_if_strong_fluctuations(data, threshold): # Задание 2 Уведомление о сильных колебаниях цены акции (максимальное и минимальное значения цены закрытия)
    price = data
    max_cls = max(price['Close'].values)
    min_cls = min(price['Close'].values)
    res_prc = 100 * (max_cls - min_cls) / min_cls
    if res_prc > threshold:
        return res_prc
    else:
        return None

def export_data_to_csv(data, file_name = 'table_stocks'): # Задание 3 Экспорт данных в CSV
    data.to_csv(f'CSV_Tables/{file_name}.csv', sep='\t')
    return 0