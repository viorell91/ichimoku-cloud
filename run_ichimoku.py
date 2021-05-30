from ichimoku import *
from utils import *
import yfinance as yf
import matplotlib.pyplot as plt
from pathlib import Path

from fastbook import *
from fastai.vision.widgets import *
import fastai.losses
import fastai.layers

fastai.layers.BaseLoss = fastai.losses.BaseLoss
fastai.layers.CrossEntropyLossFlat = fastai.losses.CrossEntropyLossFlat

MODEL_PATH = 'C:\\Users\\viore\\python-workspace\\ichimoku-cloud\\models\\export.pkl'
# default time period length for training plots 
TRAIN_DATA_INTERVAL_LENGTH = '106d'

def plot_ichimoku_for_ticker(ticker_symbol, period, output_dir):

    ticker = yf.Ticker(ticker_symbol)

    df = get_normalized_df_for_ticker_and_period(ticker, period)
    if df is None or df.empty:
        return
    # Initialize with ohcl dataframe
    i = Ichimoku(df)
    # Generates ichimoku dataframe
    i.run()
    # Plot ichimoku
    i.plot(output_dir, is_train=True)
    plt.close('all')

def plot_present_ichimoku_for_ticker(ticker_symbol, output_dir):

    ticker = yf.Ticker(ticker_symbol)

    #consider the last 106d to match the plot time interval of training data
    period = TRAIN_DATA_INTERVAL_LENGTH

    df = get_normalized_df_for_ticker_and_period(ticker, period)
    if df is None or df.empty:
        return
    # Initialize with ohcl dataframe
    i = Ichimoku(df)
    # Generates ichimoku dataframe
    i.run()
    # Plot ichimoku
    i.plot(output_dir, is_train=False)
    plt.close('all')

def get_predictions_for_tickers(input_file, output_dir, model_file=MODEL_PATH):
    with open(input_file) as fp:
        ticker_symbols = fp.read().splitlines()
    symbols_count = len(ticker_symbols)
    count=0
    handle_os_path_format()
    for symbol in ticker_symbols:
       count += 1
       plot_present_ichimoku_for_ticker(symbol, output_dir)
       print('Processed '+symbol+' ('+str(count)+' of '+str(symbols_count)+')')
    print("Processing successfully finished. Starting prediction...")
    paths = Path(output_dir).glob('**/*.png')
    learn_inf = load_learner(model_file)
    predictions = collect_predictions_to_list(paths, learn_inf)
    print("Prediction finished.")
    export_predictions_to_csv(predictions)

def get_training_data_for_tickers(input_file, period, output_dir):
    with open(input_file) as fp:
        ticker_symbols = fp.read().splitlines()
        symbols_count = len(ticker_symbols)
        count=0
        for symbol in ticker_symbols:
            count += 1
            plot_ichimoku_for_ticker(symbol, period, output_dir)
            print('Processed '+symbol+' ('+str(count)+' of '+str(symbols_count)+')')
        print("Processing successfully finished.")

get_training_data_for_tickers('resources/unseen_test_tickers.txt', '10y', 'ichimoku_plots_train/')
get_predictions_for_tickers("resources/all_train_tickers.txt", 'ichimoku_plots_predictions/')