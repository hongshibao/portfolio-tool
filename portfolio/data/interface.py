from zope.interface import Interface
from pandas import DataFrame


class IDataStock(Interface):
    def get_price_daily(symbol: str, num_days: int) -> DataFrame:
        '''Get daily stock price with columns (open, high, low, close, volume), and indexed by date'''


class IDataForex(Interface):
    def get_forex_daily(from_currency: str, to_currency: str, num_days: int) -> DataFrame:
        '''Get daily currency exchange rate with columns (open, high, low, close), and indexed by date'''
