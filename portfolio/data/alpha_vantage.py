from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
from zope.interface import implementer
from time import sleep
from portfolio.data.interface import IDataStock, IDataForex


@implementer(IDataStock)
@implementer(IDataForex)
class AlphaVantageData:
    def __init__(self, api_key, enable_api_rate_control):
        self._api_key = api_key
        self._enable_api_rate_control = enable_api_rate_control
        self._api_call_count = 0
        self._api_rate_control_limit = 5
        self._api_rate_control_time = 60 # in seconds


    def _check_api_rate_limit(self):
        if self._enable_api_rate_control:
            self._api_call_count = self._api_call_count + 1
            if self._api_call_count > 1 and \
                    self._api_call_count % self._api_rate_control_limit == 1:
                sleep(self._api_rate_control_time)


    def _rename_columns(self, data):
        data.rename(inplace=True, columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume",
        })


    def get_price_daily(self, symbol, num_days):
        self._check_api_rate_limit()
        ts = TimeSeries(key=self._api_key, output_format='pandas')
        output_size = 'compact'
        if num_days > 100:
            output_size = 'full'
        data, _ = ts.get_daily(symbol=symbol, outputsize=output_size)
        self._rename_columns(data)
        return data.iloc[-num_days:]


    def get_forex_daily(self, from_currency, to_currency, num_days):
        self._check_api_rate_limit()
        cc = ForeignExchange(key=self._api_key, output_format='pandas')
        output_size = 'compact'
        if num_days > 100:
            output_size = 'full'
        cc_data, _ = cc.get_currency_exchange_daily(
            from_symbol=from_currency,
            to_symbol=to_currency,
            outputsize=output_size,
        )
        self._rename_columns(cc_data)
        return cc_data.iloc[-num_days:]
