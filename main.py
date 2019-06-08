from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import matplotlib.pyplot as plt
import csv
import time
import argparse


def read_portfolio(csv_filepath):
    portfolio = []
    with open(csv_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        is_header = True
        for row in reader:
            if is_header:
                is_header = False
                continue
            # symbol,currency,weight
            print(row)
            portfolio.append((row[0], row[1], float(row[2])))
    return portfolio


def check_api_rate_limit(enable_api_rate_limit_control, count):
    if enable_api_rate_limit_control and count % 5 == 4:
        time.sleep(60)


def get_price_data(api_key, enable_api_rate_limit_control, symbols):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data_list = []
    meta_data_list = []
    count = 0
    for symbol in symbols:
        print(symbol)
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
        data_list.append(data)
        meta_data_list.append(meta_data)
        # API rate limit
        check_api_rate_limit(enable_api_rate_limit_control, count)
        count = count + 1
    return data_list, meta_data_list


def get_currency_exchange_data(api_key, enable_api_rate_limit_control,
                               from_currency_list, to_currency):
    cc = ForeignExchange(key=api_key, output_format='pandas')
    cc_data_dict = {}
    count = 0
    for from_currency in from_currency_list:
        if from_currency in cc_data_dict:
            continue
        print("{} -> {}".format(from_currency, to_currency))
        cc_data, _ = cc.get_currency_exchange_daily(from_symbol=from_currency,
                                                    to_symbol=to_currency,
                                                    outputsize='compact')
        cc_data_dict[from_currency] = cc_data
        check_api_rate_limit(enable_api_rate_limit_control, count)
        count = count + 1
    return cc_data_dict


def compute_price_with_cc_impact(price_data, cc_data):
    # Last column of price_data is "volume", which cc_data does not have
    return (price_data.iloc[:, 0:-1] * cc_data).dropna()


def compute_portfolio_price_with_cc_impact(price_data_list, cc_data_dict,
                                           currencies, weights):
    portfolio_price = 0
    for i in range(len(price_data_list)):
        price_with_cc_impact = compute_price_with_cc_impact(price_data_list[i],
                                                            cc_data_dict[currencies[i]])
        portfolio_price = portfolio_price + price_with_cc_impact * weights[i]
    return portfolio_price


def get_portfolio_price(api_key, enable_api_rate_limit_control,
                        csv_filepath, to_currency):
    # read portfolio
    portfolio = read_portfolio(csv_filepath)
    # get symbols, currencies, weights from portfolio
    symbols = [item[0] for item in portfolio]
    currencies = [item[1] for item in portfolio]
    weights = [item[2] for item in portfolio]
    # get daily price data
    price_data_list, _ = get_price_data(api_key, enable_api_rate_limit_control,
                                        symbols)
    # get currency exchange data
    cc_data_dict = get_currency_exchange_data(api_key, enable_api_rate_limit_control,
                                              currencies, to_currency)
    # compute portfolio price with currency impact
    portfolio_price = compute_portfolio_price_with_cc_impact(price_data_list,
                                                             cc_data_dict,
                                                             currencies,
                                                             weights)
    return portfolio_price


def get_close_price(price_data):
    return price_data['4. close']


def plot_data(data, do_data_scaling, fig_filepath):
    plt.figure(figsize=(18,6), dpi=100)
    if do_data_scaling:
        (data / data[0]).plot(marker='o')
    else:
        data.plot(marker='o')
    plt.grid()
    plt.savefig(fig_filepath, bbox_inches='tight')


def main():
    parser = argparse.ArgumentParser(description="Compute Portfolio Price")
    parser.add_argument("--api-key", type=str, default="",
                        help="Alpha Vantage API key")
    parser.add_argument("--csv-filepath", type=str, default="",
                        help="Portfolio csv file")
    parser.add_argument("--to-currency", type=str, default="SGD",
                        help="The currency to be used in portfolio")
    parser.add_argument("--fig-filepath", type=str, default="fig.png",
                        help="The path and file name for output figure")
    parser.add_argument("--price-scaling", default=False, action='store_true',
                        help="Do price scaling")
    parser.add_argument("--enable-api-rate-limit-control",
                        default=False, action='store_true',
                        help="Enable API rate limit control")
    args = parser.parse_args()

    portfolio_price = get_portfolio_price(
        args.api_key.strip(),
        args.enable_api_rate_limit_control,
        args.csv_filepath.strip(),
        args.to_currency.strip(),
    )
    portfolio_close_price = get_close_price(portfolio_price)
    plot_data(portfolio_close_price, args.price_scaling, args.fig_filepath.strip())


if __name__ == "__main__":
    exit(main())
