import pandas as pd
import yfinance as yf
import numpy as np


def fetch_stock_data(ticker, period='1mo', pick_date='', start='2024-01-01', end='2024-01-15'):
    '''Задача №5. Реализовать функционал: Улучшенное управление временными периодами'''
    if pick_date == 'да':
        data = yf.download(ticker, start=start, end=end)
        return data
    else:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    '''Задание 1 Вывод средней цены за период'''
    price = data
    average_of_list = sum(price['Close'].values) / len(price['Close'].values)
    return average_of_list


def notify_if_strong_fluctuations(data, threshold):
    '''Задание 2 Уведомление о сильных колебаниях цены акции
    (максимальное и минимальное значения цены закрытия)'''
    price = data
    max_cls = max(price['Close'].values)
    min_cls = min(price['Close'].values)
    res_prc = 100 * (max_cls - min_cls) / min_cls
    if res_prc > threshold:
        return res_prc
    else:
        return None


def export_data_to_csv(data, file_name='table_stocks'):
    '''Задание 3 Экспорт данных в CSV'''
    data.to_csv(f'CSV_Tables/{file_name}.csv', sep=',', encoding='utf-8', index=False, header=True)
    return 0


def tech_indicators(data, ndays=1, indicator='EVM'):
    '''Задание 4 Добавление дополнительных технических индикаторов'''
    if indicator == 'EVM':
        dm = ((data['High'] + data['Low']) / 2) - ((data['High'].shift(1) + data['Low'].shift(1)) / 2)
        br = (data['Volume'] / 100000000) / (data['High'] - data['Low'])
        EVM = dm / br
        EVM_MA = pd.Series(EVM.rolling(ndays).mean(), name='EVM')
        data = data.join(EVM_MA)
        return data
    elif indicator == 'FI':
        FI = pd.Series(data['Close'].diff(ndays) * data['Volume'], name='FI')
        data = data.join(FI)
        return data
    else:
        print("Такого индекса нет!")
        return 0


'''
Ease of Movement (EMV) - показывает легкость, с которой цены растут или падают с учетом объема торгов ценной бумагой. 
Например, рост цены при небольшом объеме означает, что цены росли относительно легко, 
и давление со стороны продавцов было незначительным. 
Положительные значения EVM означают, что рынок легко движется вверх, 
а отрицательные значения указывают на легкость снижения.

FI - Индекс силы учитывает направление движения цены акции, 
протяженность движения цены акции и объем. 
Используя эти три элемента, он формирует осциллятор, 
который измеряет давление покупателей и продавцов.
'''
