from ichimoku import *
from utils import *
import yfinance as yf
import matplotlib.pyplot as plt

def plot_ichimoku_for_ticker(ticker_symbol, period):

    ticker = yf.Ticker(ticker_symbol)

    period_with_displacement = get_period_with_displacement(period)
    df = ticker.history(period=period_with_displacement)
    if df.empty:
        return
    df.drop(['Dividends','Stock Splits'], inplace=True, axis=1)
    df.reset_index(inplace=True)
    df.set_index('Date', inplace=True)
    df['Date'] = df.index
    # store ticker's long name to be used in the plot title
    df['Company Name'] = ticker.info['longName']
    # Initialize with ohcl dataframe
    i = Ichimoku(df)
    # Generates ichimoku dataframe
    i.run()
    # Plot ichimoku
    i.plot()
    plt.close('all')

with open("resources/S&P500.txt") as fp:
    ticker_symbols = fp.read().splitlines()
    symbols_count = len(ticker_symbols)
    count=0
    for symbol in ticker_symbols:
        count += 1
        plot_ichimoku_for_ticker(symbol, '5y')
        print('Processed '+symbol+' ('+str(count)+' of '+str(symbols_count)+')')
