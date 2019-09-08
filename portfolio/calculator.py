from loguru import logger
from zope.interface.verify import verifyObject
from portfolio.data.interface import IDataStock, IDataForex
from csv import reader as CSVReader
from datetime import datetime


# disable logging in modules
logger.disable("portfolio.calculator")


class Calculator:
    def __init__(self, stock_data_src, forex_data_src, csv_filepath, to_currency):
        verifyObject(IDataStock, stock_data_src)
        verifyObject(IDataForex, forex_data_src)
        self._stock_data_src = stock_data_src
        self._forex_data_src = forex_data_src
        self._csv_filepath = csv_filepath
        self._to_currency = to_currency
        # read portfolio to get symbols, currencies, and weights
        self._read_portfolio()


    def get_portfolio_price(self, start_day='', num_days=100):
        if start_day:
            date_format = '%Y-%m-%d'
            start_date = datetime.strptime(start_day, date_format)
            num_days = (datetime.today() - start_date).days + 1
            if num_days < 1:
                raise Exception("start_day {} is invalid".format(start_day))
        if num_days < 1:
            raise Exception("num_days {} is invalid".format(num_days))
        # get daily price data
        price_data_list = self._get_price_data(2 * num_days)
        # get currency exchange data
        cc_data_dict = self._get_currency_exchange_data(2 * num_days)
        # compute portfolio price with currency impact
        portfolio_price = self._compute_portfolio_price_with_cc_impact(
            price_data_list,
            cc_data_dict,
        )
        # return required data rows
        if start_day:
            ret = portfolio_price.loc[start_day:]
        else:
            ret = portfolio_price[-num_days:]
        # at least return one row
        if len(ret.index) == 0:
            ret = portfolio_price[-1:]
        return ret


    def _read_portfolio(self):
        self._symbols = []
        self._currencies = []
        self._weights = []
        with open(self._csv_filepath, 'r') as csvfile:
            reader = CSVReader(csvfile, delimiter=',')
            is_header = True
            for row in reader:
                if len(row) != 3:
                    continue
                if is_header:
                    is_header = False
                    continue
                # symbol,currency,weight
                logger.debug("Portofolio item: {}", row)
                self._symbols.append(row[0])
                self._currencies.append(row[1])
                self._weights.append(float(row[2]))


    def _get_price_data(self, num_days):
        price_data_list = []
        for symbol in self._symbols:
            logger.debug("Getting price data for {}", symbol)
            price_data = self._stock_data_src.get_price_daily(symbol, num_days)
            price_data_list.append(price_data)
            logger.debug("Price data for {} is gotten", symbol)
        return price_data_list


    def _get_currency_exchange_data(self, num_days):
        cc_data_dict = {}
        for from_currency in self._currencies:
            if from_currency in cc_data_dict or from_currency == self._to_currency:
                continue
            logger.debug("Getting currency exchange data for {} -> {}", 
                            from_currency, self._to_currency)
            cc_data = self._forex_data_src.get_forex_daily(
                from_currency,
                self._to_currency,
                num_days,
            )
            cc_data_dict[from_currency] = cc_data
            logger.debug("Currency exchange data for {} -> {} is gotten", 
                            from_currency, self._to_currency)
        return cc_data_dict


    def _compute_portfolio_price_with_cc_impact(self, price_data_list, cc_data_dict):
        portfolio_price = 0
        for i in range(len(self._weights)):
            # last column of price_data is "volume", which cc_data does not have
            price_data = price_data_list[i].iloc[:, 0:-1]
            if self._currencies[i] == self._to_currency:
                # need to copy data
                price_with_cc_impact = price_data.copy()
            else:
                cc_data = cc_data_dict[self._currencies[i]]
                # use dropna() to remove NaN rows
                price_with_cc_impact = (price_data * cc_data).dropna()
            weighted_price_with_cc_impact = price_with_cc_impact * self._weights[i]
            portfolio_price = (portfolio_price + weighted_price_with_cc_impact).dropna()
        return portfolio_price
