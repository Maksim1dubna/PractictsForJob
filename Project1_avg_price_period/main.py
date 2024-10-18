import data_download as dd
import data_plotting as dplt


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")
    percentage_cls = float(input("Процент сильных колебаний цены акции (Закрытия): ")) # Задание 2 Уведомление о сильных колебаниях цены акции

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

    # Задание 1 Вывод средней цены за период
    avg = dd.calculate_and_display_average_price(stock_data)
    print(f"\nСреднее закрытия за период: {avg}")

    # Задание 2 Уведомление о сильных колебаниях цены акции (максимальное и минимальное значения цены закрытия)
    p_cls = dd.notify_if_strong_fluctuations(stock_data, percentage_cls)
    if p_cls is None:
        pass
    else:
        print(f"\nВнимание! Превышение порога {percentage_cls}%")
        print(f"Разница цен за указанный период:{p_cls}%")

    # Задание 3 Экспорт данных в CSV
    dd.export_data_to_csv(stock_data, ticker) # В качестве названия пусть забирает выбранный тикер

if __name__ == "__main__":
    main()
