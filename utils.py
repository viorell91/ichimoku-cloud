import re
import os
import csv
import pathlib
from fastbook import *

def get_period_with_displacement(period):
    displacement = 26
    period_type_part = re.search(r'\D+', period).group()
    period_number_part = int(re.search(r'\d+', period).group())
    if period_type_part == 'y':
        period_in_days= period_number_part * 365
        return str(period_in_days) +'d'
    elif period_type_part == 'mo':
        period_in_days = period_number_part * 31 + displacement
        return str(period_in_days) +'d'
    elif period_type_part == 'd' and period_number_part > 30:
        period_in_days = period_number_part + displacement
        return str(period_in_days) +'d'
    elif period_type_part == 'd' or period_type_part == 'm':
        print ("The Ichimoku Cloud can be plotted for a period >= 1 month")
        return period
    return period

def get_normalized_df_for_ticker_and_period(ticker, period):
    period_with_displacement = get_period_with_displacement(period)
    df = ticker.history(period=period_with_displacement)
    df_len_threshold = int(re.findall( '(\d+)', period_with_displacement)[0])
    if len(df) < 100:
        return
    df.drop(['Dividends','Stock Splits'], inplace=True, axis=1)
    df.reset_index(inplace=True)
    df.set_index('Date', inplace=True)
    df['Date'] = df.index
    # store ticker's long name to be used in the plot title
    add_company_name(df, ticker)
    return df

def add_company_name(df, ticker):
    try:
        df['Company Name'] = ticker.info['longName']
    except Exception:
        print("Couldn't retrieve ticker info!")
        df['Company Name'] = ticker.ticker
        pass

def create_dir_if_not_exists(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def filter_seen_tickers(input_file_path, output_file_path):
    with open("resources/S&P500.txt") as fp:
        sp_tickers = fp.read().splitlines()
    with open(input_file_path) as fp:
        test_tickers = fp.read().splitlines()
    print('S&P Tickers: '+str(len(sp_tickers)))
    print('Test Tickers: '+str(len(test_tickers)))
    cleaned_list = [ x for x in test_tickers if x not in sp_tickers ]
    print('Cleaned-Up Test Tickers: '+str(len(cleaned_list)))
    save_list_to_file(output_file_path, cleaned_list)

def save_list_to_file(output_file_path, list):
    output_file=open(output_file_path,'w')
    list=map(lambda x:x+'\n', list)
    output_file.writelines(list)
    output_file.close()

def collect_predictions_to_list(paths, learn_inf):
    predictions_list = []
    for path in paths:
        pred,pred_idx,probs = learn_inf.predict(str(path))
        prediction_dict = {}
        prediction_dict['Company'] = path.stem
        prediction_dict['Predicted Trend'] = str(pred)
        prediction_dict['Confidence'] = str(probs[pred_idx].item())
        predictions_list.append(prediction_dict)
    return predictions_list

def export_predictions_to_csv(predictions):
    try:
        with open('Predictions_vse.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, predictions[0].keys())
            writer.writeheader()
            for data in predictions:
                writer.writerow(data)
    except IOError:
        print("I/O error")

def handle_os_path_format():
    pltfm = platform.system()
    if pltfm == 'Windows': pathlib.PosixPath = pathlib.WindowsPath