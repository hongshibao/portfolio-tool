# portfolio-tool
This is a simple tool to compute daily closed price with currency impact for your portfolio. The daily stock price and currency exchange rate are from [Alpha Vantage](https://www.alphavantage.co/) [API](https://www.alphavantage.co/documentation/). You can add new data sources (e.g. [IEX](https://iexcloud.io/), [Tiingo](https://www.tiingo.com/), [Yahoo! Finance](https://finance.yahoo.com/)) by implementing the data interface [IDataStock](portfolio/data/interface.py#L5) and [IDataForex](portfolio/data/interface.py#L10) in `portfolio/data/interface.py`.

## Environment Setup
1. Install python3 using `pyenv`

   1. Follow these instructions for `pyenv` [installation](https://github.com/pyenv/pyenv#installation) or use `pyenv` [automatic installer](https://github.com/pyenv/pyenv-installer).

   2. Install python 3.7.3:

          $ pyenv install 3.7.3

2. Install `pipenv`

   1. Clone this repository and go to the repository root folder:

          $ git clone git@github.com:hongshibao/portfolio-tool.git
          $ cd portfolio-tool

   2. Switch to use python 3.7.3 for this repository:

          $ pyenv local 3.7.3

   3. Make sure it will run python 3.7.3 in this repository:

          $ python --version

      It should output `Python 3.7.3`. Otherwise, please check whether `pyenv` installation is complete.

   4. Use `pip` to install `pipenv`:

          $ pip install pipenv

3. Install package dependencies using `pipenv`

        $ pipenv install

   It will also create a virtual environment dedicated to this repository.

4. Activate the dedicated virtual environment

        $ pipenv shell

5. (Optional) Install this `portfolio-tool` package locally in develop/editable mode

        $ pip install -e .

    Remove `-e` to disable develop/editable mode.

## Usage
Run --help to get usage and arguments:

    $ python -m portfolio.app --help

```
Usage: app.py [OPTIONS]

Options:
  --data-api-key TEXT        Alpha Vantage API key, which will read from env
                             var DATA_API_KEY if not specified
  --enable-api-rate-control  Enable API rate limit control
  --csv-filepath TEXT        The portfolio CSV file
  --to-currency TEXT         Destination currency for the portfolio
  --start-day TEXT           Start day (YYYY-MM-DD) in EST time zone for
                             portfolio price data, priority is higher than
                             --num-days
  --num-days INTEGER         The number of days for latest portfolio price
                             data
  --fig-filepath TEXT        The path and file name for time series figure
                             output
  --price-scaling            Do price scaling
  --help                     Show this message and exit.
```

Free Alpha Vantage API key can be claimed [here](https://www.alphavantage.co/support/#api-key). But there is API rate limit for free API keys. Argument *--enable-api-rate-control* can enable API rate control to make sure it will not reach the Alpha Vantage API rate limit.

The portfolio CSV has 3 columns: *symbol*, *currency*, and *weight*. Here is an example portfolio CSV data:
```
symbol,currency,weight
XLP,USD,0.033
XLY,USD,0.148
CWB,USD,0.148
FEZ,USD,0.031
AAXJ,USD,0.070
GLD,USD,0.104
VGIT,USD,0.141
TLT,USD,0.119
TIP,USD,0.148
TLH,USD,0.048
```
The list of available physical currency can be downloaded [here](https://www.alphavantage.co/physical_currency_list/).

Example output without price scaling:

![figure without price scaling](resources/fig.png)

Example output with price scaling:

![figure with price scaling](resources/fig-scaling.png)

## Docker
There is a docker image `thinkpoet/portfolio-tool` available to run the script using `docker run`:

       $ docker pull thinkpoet/portfolio-tool:latest
       $ docker run --rm -v ${your_local_portfolio_csv_absolute_path}:/data/input/portfolio.csv  -v ${your_local_output_folder_absolute_path}:/data/output thinkpoet/portfolio-tool:latest --data-api-key=${your_api_key} --enable-api-rate-control --csv-filepath=/data/input/portfolio.csv --fig-filepath=/data/output/figure.png
