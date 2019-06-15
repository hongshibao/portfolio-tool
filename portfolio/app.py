import data.alpha_vantage
import calculator
import plotter
import argparse


def run():
    parser = argparse.ArgumentParser(description="Compute Portfolio Price")
    parser.add_argument("--data-api-key", type=str, default="",
                        help="Alpha Vantage API key")
    parser.add_argument("--enable-api-rate-control",
                        default=False, action='store_true',
                        help="Enable API rate limit control")
    parser.add_argument("--csv-filepath", type=str, default="",
                        help="Portfolio csv file")
    parser.add_argument("--to-currency", type=str, default="SGD",
                        help="The currency to be used in portfolio")
    parser.add_argument("--num-days", type=int, default=100,
                        help="Show the latest NUM_DAYS price data")
    parser.add_argument("--fig-filepath", type=str, default="fig.png",
                        help="The path and file name for output figure")
    parser.add_argument("--price-scaling", default=False, action='store_true',
                        help="Do price scaling")
    args = parser.parse_args()

    data_src = data.alpha_vantage.AlphaVantageData(args.data_api_key,
                                                   args.enable_api_rate_control)
    calc = calculator.Calculator(data_src, args.csv_filepath, args.to_currency)
    portfolio_price = calc.get_portfolio_price(args.num_days)
    portfolio_close_price = data_src.get_close_price(portfolio_price)
    if args.price_scaling:
        portfolio_close_price = portfolio_close_price / portfolio_close_price[0]
    # plot
    plt = plotter.Plotter()
    plt.plot_time_series_data(portfolio_close_price, args.fig_filepath)


if __name__ == '__main__':
    run()
