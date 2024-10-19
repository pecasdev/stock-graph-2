import yfinance as yf
from datetime import datetime as dt


class StockApi:
    def __init__(self, history_start_date: dt, history_end_date: dt):
        self.clearCache()
        self.history_start_date = history_start_date
        self.history_end_date = history_end_date

    def getClosePriceOnDate(self, symbol, date):
        if symbol not in self.cache:
            data = yf.Ticker(symbol).history(
                period="1d", start=self.history_start_date, end=self.history_end_date
            )
            self.cache[symbol] = data["Close"]

        return self.cache[symbol].get(date.strftime("%Y-%m-%d"), None)

    def clearCache(self):
        self.cache = {}
