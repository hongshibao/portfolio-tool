from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import zope.interface
import data.interface
import time

@zope.interface.implementer(data.interface.IData)
class AlphaVantageData:
    def __init__(self, api_key, enable_api_rate_control):
        self._api_key = api_key
        self._enable_api_rate_control = enable_api_rate_control
        self._api_call_count = 0
        self._api_rate_control_limit = 5
        self._api_rate_control_time = 60 # in seconds


    def check_api_rate_limit(self):
        if self._enable_api_rate_control:
            self._api_call_count = self._api_call_count + 1
            if self._api_call_count > 1 and \
                    self._api_call_count % self._api_rate_control_limit == 1:
                time.sleep(self._api_rate_control_time)


    def get_price_daily(self, symbol):
        self.check_api_rate_limit()
        ts = TimeSeries(key=self._api_key, output_format='pandas')
        data, _ = ts.get_daily(symbol=symbol, outputsize='compact')
        return data


    def get_forex_daily(self, from_currency, to_currency):
        self.check_api_rate_limit()
        cc = ForeignExchange(key=self._api_key, output_format='pandas')
        cc_data, _ = cc.get_currency_exchange_daily(
            from_symbol=from_currency,
            to_symbol=to_currency,
            outputsize='compact',
        )
        return cc_data


    def get_close_price(self, price):
        return price['4. close']
