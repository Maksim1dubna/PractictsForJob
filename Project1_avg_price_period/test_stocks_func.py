# Внимательно пересмотреть https://www.youtube.com/watch?v=6tNS--WetLI и составить тесты.
import unittest

import data_download as dd
import data_plotting as dplt
import yfinance as yf
import numpy as np


class TestStocks(unittest.TestCase):
    def setUp(self, ticker='AAPL', period='1mo'):
        self.stock = yf.Ticker(ticker)
        self.data = self.stock.history(period=period)

    def test_task_avg_price_1(self, data):
        return 0


if __name__ == '__main__':
    unittest.main()
