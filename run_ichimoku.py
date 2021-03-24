from ichimoku import *
from utils import *
import yfinance as yf
import pandas as pd

ticker = yf.Ticker('PFE')
period_with_displacement = get_period_with_displacement('9mo')
df = ticker.history(period=period_with_displacement)

df.drop(['Dividends','Stock Splits'], inplace=True, axis=1)
df.reset_index(inplace=True)
df.set_index('Date', inplace=True)
df['Date'] = df.index
# store ticker's long name to be used in the plot title
df['Company Name'] = ticker.info['longName']

# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()
# Plot ichimoku
i.plot()
