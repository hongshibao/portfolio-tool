# portfolio-tool
This is a simple tool to compute daily closed price with currency impact for your portfolio. The daily stock price and currency exchange rate are from [Alpha Vantage](https://www.alphavantage.co/) [API](https://www.alphavantage.co/documentation/).

## Usage
Follow this [tutorials](https://packaging.python.org/tutorials/installing-packages/#creating-virtual-environments) to create a python3 virtual environment. The basic usage is like so:

    $ python3 -m venv <DIR>
    $ source <DIR>/bin/activate


Install dependencies:

    $ pip install -r requirements.txt

Run --help to get usage and arguments:

    $ python portfolio/app.py --help

```
Usage: app.py [OPTIONS]

Options:
  --data-api-key TEXT        Alpha Vantage API key
  --enable-api-rate-control  Enable API rate limit control
  --csv-filepath TEXT        The portfolio CSV file
  --to-currency TEXT         Destination currency for the portfolio
  --num-days INTEGER         The number of days for latest portfolio price
                             data
  --fig-filepath TEXT        The path and file name for time series figure
                             output
  --price-scaling            Do price scaling
  --help                     Show this message and exit.
```

Free Alpha Vantage API key can be claimed [here](https://www.alphavantage.co/support/#api-key). But there is API rate limit for free API keys. Argument *--enable-api-rate-control* can enable API rate control to make sure it will not reach the Alpha Vantage API rate limit.

The portfolio CSV has 3 columns: *symbol*, *currency*, and *weight*. Check [this file](resources/portfolio.csv) for an example portfolio CSV. The list of available physical currency can be downloaded [here](https://www.alphavantage.co/physical_currency_list/).

Example output without price scaling:

![alt text](resoures/fig.png?raw=true "output figure without price scaling")

Example output with price scaling:

![alt text](resoures/fig-scaling.png?raw=true "output figure with price scaling")
