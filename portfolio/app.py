from loguru import logger
import click
from portfolio.data.alpha_vantage import AlphaVantageData
from portfolio.calculator import Calculator
from portfolio.plotter import Plotter


# enable logging in scripts
logger.enable("portfolio.calculator")
logger.enable("portfolio.plotter")


# @logger.catch
@click.command()
@click.option("--data-api-key", type=str, default="", 
              help="Alpha Vantage API key")
@click.option("--enable-api-rate-control", type=bool, is_flag=True, 
              help="Enable API rate limit control")
@click.option("--csv-filepath", type=str, default="resources/portfolio.csv", 
              help="The portfolio CSV file")
@click.option("--to-currency", type=str, default="SGD", 
              help="Destination currency for the portfolio")
@click.option("--start-day", type=str, default="",
              help="Start day (YYYY-MM-DD) for portfolio price data, priority is higher than --num-days")
@click.option("--num-days", type=int, default=100, 
              help="The number of days for latest portfolio price data")
@click.option("--fig-filepath", type=str, default="fig.png", 
              help="The path and file name for time series figure output")
@click.option("--price-scaling", type=bool, is_flag=True, 
              help="Do price scaling")
def run(data_api_key, enable_api_rate_control,
        csv_filepath, to_currency, start_day, num_days,
        fig_filepath, price_scaling):
    data_src = AlphaVantageData(data_api_key, enable_api_rate_control)
    calc = Calculator(data_src, csv_filepath, to_currency)
    # get portfolio price
    logger.debug("Start to compute portfolio price with currency impact")
    portfolio_price = calc.get_portfolio_price(start_day, num_days)
    portfolio_close_price = data_src.get_close_price(portfolio_price)
    if price_scaling:
        portfolio_close_price = portfolio_close_price / portfolio_close_price[0]
    logger.debug("Computing portfolio price with currency impact is done")
    # plot
    plt = Plotter()
    logger.debug("Start to plot portfolio price time series")
    plt.plot_time_series_data(portfolio_close_price, fig_filepath)
    logger.debug("Plotting portfolio price time series is done")


if __name__ == '__main__':
    run()
