# -*- coding: utf-8 -*-

from typing import Tuple
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import decimal
import mplfinance as mpf
import time


class Ichimoku():
    INTERVAL_LENGTH_THRESHOLD = 25
    """
    @param: ohcl_df <DataFrame> 

    Required columns of ohcl_df are: 
        Date<Float>,Open<Float>,High<Float>,Close<Float>,Low<Float>
    """
    def __init__(self, ohcl_df):
        self.ohcl_df = ohcl_df

    def run(self):
        tenkan_window = 9
        kijun_window = 26
        senkou_span_b_window = 52
        cloud_displacement = 26
        chikou_shift = -26
        ohcl_df = self.ohcl_df

        last_date = datetime.timestamp(ohcl_df["Date"].iloc[-1])
        forelast_date = datetime.timestamp(ohcl_df["Date"].iloc[-2])
        period = last_date - forelast_date

        ext_beginning = decimal.Decimal(last_date+period)
        ext_end = decimal.Decimal(last_date + ((period*cloud_displacement)+period))
        dates_ext = list(self.drange(ext_beginning, ext_end, str(period)))
        dates_ext = [datetime.fromtimestamp(x) for x in dates_ext]
        dates_ext_df = pd.DataFrame({"Date": dates_ext})
        dates_ext_df.index = dates_ext # also update the df index
        ohcl_df = ohcl_df.append(dates_ext_df)

        # Tenkan 
        tenkan_sen_high = ohcl_df['High'].rolling( window=tenkan_window ).max()
        tenkan_sen_low = ohcl_df['Low'].rolling( window=tenkan_window ).min()
        ohcl_df['tenkan_sen'] = (tenkan_sen_high + tenkan_sen_low) /2
        # Kijun 
        kijun_sen_high = ohcl_df['High'].rolling( window=kijun_window ).max()
        kijun_sen_low = ohcl_df['Low'].rolling( window=kijun_window ).min()
        ohcl_df['kijun_sen'] = (kijun_sen_high + kijun_sen_low) / 2
        # Senkou Span A 
        ohcl_df['senkou_span_a'] = ((ohcl_df['tenkan_sen'] + ohcl_df['kijun_sen']) / 2).shift(cloud_displacement)
        # Senkou Span B 
        senkou_span_b_high = ohcl_df['High'].rolling( window=senkou_span_b_window ).max()
        senkou_span_b_low = ohcl_df['Low'].rolling( window=senkou_span_b_window ).min()
        ohcl_df['senkou_span_b'] = ((senkou_span_b_high + senkou_span_b_low) / 2).shift(cloud_displacement)
        # Chikou
        ohcl_df['chikou_span'] = ohcl_df['Close'].shift(chikou_shift)

        self.ohcl_df = ohcl_df
        return ohcl_df

    def plot(self):

        # consider the cloud displacement of 26 days and senkou_span_b displacement (52 days)
        df = self.ohcl_df.iloc[80:,:]

        fig, axlist = mpf.plot(df,type='candle',style='yahoo',figratio=(18,8),show_nontrading=True,returnfig=True)
        ax = axlist[0]

        lines = self.plot_ichimoku_lines(df, ax)
        self.plot_ichimoku_cloud(df,ax)
        
        mpf.plot(df,type='candle',style='yahoo',ax=ax,addplot=lines,show_nontrading=True)
        self.pretty_plot(fig, ax)

        red_cloud_intervals = self.get_pre_relevant_cloud_intervals_by_type(df,'red')
        green_cloud_intervals = self.get_pre_relevant_cloud_intervals_by_type(df,'green')
        fig.savefig('alltimeplot.png')
        self.save_relevant_cloud_figures(df, fig, ax, red_cloud_intervals, 'red')
        self.save_relevant_cloud_figures(df, fig, ax, green_cloud_intervals, 'green')

    def save_relevant_cloud_figures(self, df, fig, ax, relevant_cloud_intervals, cloud_type):
        for interval in relevant_cloud_intervals:
            interval_date_start = interval[0].date()
            interval_date_stop = interval[1].date()
            price = df[pd.Timestamp(interval_date_start):pd.Timestamp(interval_date_stop)][['Open', 'Close']]
            max_price = price.max().max()
            min_price = price.min().min()
            max_price_norm = max_price + (max_price*10/100)
            min_price_norm = min_price - (min_price*10/100)
            ax.set_ylim([min_price_norm, max_price_norm])
            ax.set_xlim([interval_date_start, interval_date_stop])
            fig.savefig('pre-'+cloud_type+'-plot'+str(interval_date_start)+'.png')


    def pretty_plot(self, fig, ax):
        ax.legend()
        fig.autofmt_xdate()
        ax.xaxis_date()

        ax.grid(linestyle='-', linewidth='0.5')
        ax.yaxis.tick_right()
        ax.tick_params(axis='x', size=14)
        ax.tick_params(axis='y', size=14)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
       # fig.tight_layout()
        ax.autoscale_view()

    def plot_ichimoku_cloud(self, df, ax):
        date_axis = df.index

        green_cloud_values = df['senkou_span_a'] > df['senkou_span_b']  
        red_cloud_values = df['senkou_span_b'] > df['senkou_span_a']

        # green cloud
        ax.fill_between(date_axis,df['senkou_span_a'], df['senkou_span_b'], where=green_cloud_values, facecolor='#008000', alpha=0.25)
        # red cloud
        ax.fill_between(date_axis,df['senkou_span_a'], df['senkou_span_b'], where=red_cloud_values, facecolor='#ff0000', alpha=0.25)
        return ax

    def plot_ichimoku_lines(self, df, ax):
        ap = [mpf.make_addplot(df[['senkou_span_a','senkou_span_b']],ax=ax, width=.7), 
        mpf.make_addplot(df['tenkan_sen'],ax=ax, width=.7),
        mpf.make_addplot(df['kijun_sen'],ax=ax, width=.7),
        mpf.make_addplot(df['chikou_span'],ax=ax, width=.7)]
        
        return ap

    def get_pre_relevant_cloud_intervals_by_type(self, df, cloud_type):

        red_cloud_values = df['senkou_span_b'] > df['senkou_span_a']

        red_df = pd.DataFrame({'Date':red_cloud_values.index, 'isRed':red_cloud_values})
        red_df = red_df.reset_index(drop=True)

        ranges = self.get_sorted_relevant_cloud_interval_indexes(red_df, cloud_type)

        filtered_indexes = list(filter(lambda x: len(x) > self.INTERVAL_LENGTH_THRESHOLD, ranges))

        if cloud_type == 'red':
            intervals = [(df['Date'].iloc[r.start-40], df['Date'].iloc[r.start-10]) 
                for r in filtered_indexes 
                if r.start>=40 and not red_df['isRed'].iloc[r.start-40]]
        else: 
            intervals = [(df['Date'].iloc[r.start-40], df['Date'].iloc[r.start-10]) 
                for r in filtered_indexes 
                if r.start>=40 and red_df['isRed'].iloc[r.start-40]]

        return intervals

    def get_sorted_relevant_cloud_interval_indexes(self, red_df, cloud_type):
        red_cloud_start_index = ""
        red_cloud_end_index = ""
        ranges = []

        red_cloud = True if cloud_type == 'red' else False

        for index, row in red_df.iterrows():
            if row['isRed'] is red_cloud and not red_cloud_start_index:
                red_cloud_start_index = index
            if row['isRed'] is not red_cloud and red_cloud_start_index and not red_cloud_end_index:
                red_cloud_end_index = index
                ranges.append(range(red_cloud_start_index,red_cloud_end_index)) 
                red_cloud_start_index = ""
                red_cloud_end_index = ""
       
        ranges.sort(key=len, reverse=True)

        return ranges

    # Range generator for decimals
    def drange(self, x, y, jump): 
        while x < y:
            yield float(x)
            x += decimal.Decimal(jump)