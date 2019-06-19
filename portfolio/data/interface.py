from zope.interface import Interface
from pandas import DataFrame


class IData(Interface):
    def get_price_daily(symbol: str, num_days: int) -> DataFrame:
        '''Get daily stock price (timestamp, open, high, low, close, volume)'''


    def get_forex_daily(from_currency: str, to_currency: str, 
                        num_days: int) -> DataFrame:
        '''Get daily currency exchange rate (timestamp, open, high, low, close)'''


    def get_close_price(price: DataFrame) -> DataFrame:
        '''Extract close price from input'''
