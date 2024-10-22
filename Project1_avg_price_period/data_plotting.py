import matplotlib.pyplot as plt
import pandas as pd
import data_download as dd


def create_and_save_plot(data, ticker, period, filename=None):
    '''
    Функция была отредактирована для отбражения графиков дополнительных технических индикаторов
    и добавление их в единый график
    '''
    plt.figure(figsize=(20, 12))
    indicator = 'EVM'
    data_t_i = dd.tech_indicators(data, ndays=10,
                                  indicator=indicator)  # Задание 4 Добавление дополнительных технических индикаторов
    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            plt.subplot(2, 1, 1)
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            plt.legend()
            plt.subplot(2, 1, 2)
            plt.plot(dates, data_t_i[indicator].values, label=indicator)
            plt.title(f"{indicator} технический индикатор")
            plt.legend()
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.subplot(2, 1, 1)
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.legend()
        plt.subplot(2, 1, 2)
        plt.plot(data_t_i['Date'], data_t_i[indicator], label=indicator)
        plt.legend()

    if filename is None:
        filename = f"charts/{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")
