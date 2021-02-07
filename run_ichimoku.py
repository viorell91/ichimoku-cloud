from ichimoku import *
from utils import *
import yfinance as yf
import pandas as pd

ibm = yf.Ticker('IBM')
period_with_displacement = get_period_with_displacement('6mo')
df = ibm.history(period=period_with_displacement)

df.drop(['Dividends','Stock Splits'], inplace=True, axis=1)
df.reset_index(inplace=True)
df.set_index('Date', inplace=True)
df['Date'] = df.index

# Load Sample Data into a dataframe
#df_old = pd.read_csv('./sample-data/ohcl_sample.csv',index_col=0)
#df_tsla = pd.read_csv('./sample-data/tsla.csv',index_col=0)
# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()
ichimoku_df.to_csv('ibm_df_default.csv', index = False) 
# Plot ichimoku
i.plot()
