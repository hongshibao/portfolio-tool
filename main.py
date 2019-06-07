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
            # symbol,weight
            print(row)
            portfolio.append((row[0], float(row[1])))
    return portfolio


def get_price_data(api_key, disable_api_rate_limit, portfolio):
    ts = TimeSeries(key=api_key, output_format='pandas')
    data = []
    meta_data = []
    symbols = [item[0] for item in portfolio]
    i = 0
    for symbol in symbols:
        print(symbol)
        tmp_data, tmp_meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
        data.append(tmp_data)
        meta_data.append(tmp_meta_data)
        # API rate limit
        if not disable_api_rate_limit and i % 5 == 4:
            time.sleep(60)
        i = i + 1
    return data, meta_data


def compute_portfolio_price(price_data, portfolio):
    weights = [item[1] for item in portfolio]
    portfolio_price = price_data[0] * weights[0]
    for i in range(1, len(price_data)):
        portfolio_price = portfolio_price + price_data[i] * weights[i]
    return portfolio_price


def get_currency_exchange_data(api_key, from_currency, to_currency):
    cc = ForeignExchange(key=api_key, output_format='pandas')
    cc_data, _ = cc.get_currency_exchange_daily(from_symbol=from_currency,
                                                to_symbol=to_currency,
                                                outputsize='compact')
    return cc_data


def compute_price_with_currency_impact(price_data, cc_data):
    # Last column of price_data is volume, which cc_data does not have
    return (price_data.iloc[:, 0:-1] * cc_data).dropna()


def compute_portfolio_price_with_currency_impact(api_key,
                                                 disable_api_rate_limit,
                                                 csv_filepath,
                                                 from_currency,
                                                 to_currency):
    portfolio = read_portfolio(csv_filepath)
    price_data, _ = get_price_data(api_key, disable_api_rate_limit, portfolio)
    portfolio_price = compute_portfolio_price(price_data, portfolio)
    cc_data = get_currency_exchange_data(api_key, from_currency, to_currency)
    final_price = compute_price_with_currency_impact(portfolio_price, cc_data)
    return final_price


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
    parser.add_argument("--api-key", type=str, default="")
    parser.add_argument("--csv-filepath", type=str, default="")
    parser.add_argument("--from-currency", type=str, default="USD")
    parser.add_argument("--to-currency", type=str, default="SGD")
    parser.add_argument("--fig-filepath", type=str, default="fig.png")
    parser.add_argument("--price-scaling", default=False, action='store_true')
    parser.add_argument("--disable-api-rate-limit", default=False, action='store_true')
    args = parser.parse_args()

    final_price = compute_portfolio_price_with_currency_impact(
        args.api_key.strip(),
        args.disable_api_rate_limit,
        args.csv_filepath.strip(),
        args.from_currency.strip(),
        args.to_currency.strip(),
    )
    final_close_price = get_close_price(final_price)
    plot_data(final_close_price, args.price_scaling, args.fig_filepath.strip())


if __name__ == "__main__":
    exit(main())
