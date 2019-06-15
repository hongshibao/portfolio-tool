import zope.interface.verify
import data.interface
import csv

class Calculator:
    def __init__(self, data_src, csv_filepath, to_currency):
        zope.interface.verify.verifyObject(data.interface.IData, data_src)
        self._data_src = data_src
        self._csv_filepath = csv_filepath
        self._to_currency = to_currency
        # read portfolio to get symbols, currencies, and weights
        self.read_portfolio()


    def get_portfolio_price(self, num_days):
        # get daily price data
        price_data_list = self.get_price_data(2 * num_days)
        # get currency exchange data
        cc_data_dict = self.get_currency_exchange_data(2 * num_days)
        # compute portfolio price with currency impact
        portfolio_price = self.compute_portfolio_price_with_cc_impact(
            price_data_list,
            cc_data_dict,
        )
        return portfolio_price[-num_days:]


    def read_portfolio(self):
        self._symbols = []
        self._currencies = []
        self._weights = []
        with open(self._csv_filepath, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            is_header = True
            for row in reader:
                if is_header:
                    is_header = False
                    continue
                # symbol,currency,weight
                print(row) #TODO use log
                self._symbols.append(row[0])
                self._currencies.append(row[1])
                self._weights.append(float(row[2]))


    def get_price_data(self, num_days):
        price_data_list = []
        for symbol in self._symbols:
            price_data = self._data_src.get_price_daily(symbol, num_days)
            price_data_list.append(price_data)
            print(symbol) #TODO
        return price_data_list


    def get_currency_exchange_data(self, num_days):
        cc_data_dict = {}
        for from_currency in self._currencies:
            if from_currency in cc_data_dict:
                continue
            cc_data = self._data_src.get_forex_daily(
                from_currency,
                self._to_currency,
                num_days,
            )
            cc_data_dict[from_currency] = cc_data
            print("{} -> {}".format(from_currency, self._to_currency)) #TODO
        return cc_data_dict


    def compute_portfolio_price_with_cc_impact(self, price_data_list, cc_data_dict):
        portfolio_price = 0
        for i in range(len(self._weights)):
            # last column of price_data is "volume", which cc_data does not have
            price_data = price_data_list[i].iloc[:, 0:-1]
            cc_data = cc_data_dict[self._currencies[i]]
            # use dropna() to remove NaN rows
            price_with_cc_impact = (price_data * cc_data).dropna()
            weighted_price_with_cc_impact = price_with_cc_impact * self._weights[i]
            portfolio_price = (portfolio_price + weighted_price_with_cc_impact).dropna()
        return portfolio_price
