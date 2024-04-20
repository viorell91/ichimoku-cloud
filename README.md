# Ichimoku Cloud 

## Description
Generic tool for plotting beautiful Ichimoku clouds in python + mplfinance. 

The Ichimoku clouds are plotted using a [standard configuration](https://www.ichimokutrader.com/elements.html) as found on https://www.ichimokutrader.com/ 

As inspiration and rough layout serves the [example of crypto-modified ichimoku clouds](https://github.com/kumotrader/ichimoku-crypto)

Sample Generated Image:

![Ichimoku Sample Code](https://github.com/viorell91/ichimoku-cloud/blob/main/sample-data/sample_pfe.png "Ichimoku Cloud Pfizer Inc. Plot")


## Telegram Group
Link: https://t.me/kumo_trading_tech_analysis
- Learn how to use Ichimoku strategies for crypto trading
- Stay updated with automated daily Kumo Reports and analysis on promising coins


## Installation
1. install pipenv to manage dependencies (https://docs.pipenv.org/)
2. Install python-tk
3. Run `pipenv` - will install all dependencies in a virtual environment


## Running in console  `pipenv run python`
```
from ichimoku import *
# Load Sample Data into a dataframe
df = pd.read_csv('./sample-data/ibm_df_sample.csv',index_col=0)
# Initialize with ohcl dataframe
i = Ichimoku(df)
# Generates ichimoku dataframe
ichimoku_df = i.run()

# Plot ichimoku
i.plot()
```



## Ichimoku Elements
| Signal                 |  Stocks(9a-5p) | Formula                                 |
|------------------------|----------------|-----------------------------------------|
| Tenkan (conversion):   |   9            | (eg. 9-period high + 9-period low)/2))  |
| Kijun (base):          |  26            | (eg. 26-period high + 26-period low)/2))|
| Senkou span A (faster):|                | (Conversion Line + Base Line)/2))       |
| Senkou span B (slower):|  52            | (eg. 52-period high + 52-period low)/2))|
| Cloud displacement:    |  26            |                                         |
| Chikou (lagging span): |  26            |                                         |
