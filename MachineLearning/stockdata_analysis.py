# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 09:00:02 2015

@author: 3820104
"""

import pandas as pd
import os
import time
from datetime import datetime

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

import re

path = "C:/Users/3820104/Downloads/intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+"/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]
    #print (stock_list)
    df = pd.DataFrame(columns=['Date',
                               'Unix',
                               'Ticker',
                               'DE Ratio',
                               'Price',
                               'stock_p_change',
                               'SP500',
                               'sp500_p_change',
                               'Difference'])
    
    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv")
    
    ticker_list = []
    
    for each_dir in stock_list[1:25]: #skip stock_list[0] - rootdir
        each_file = os.listdir(each_dir) # files in each dir
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)
        starting_stock_value = False
        starting_sp500_value = False
        
        #print(each_file)
        #ime.sleep(15)
        if len(each_file) > 0:
            for file in each_file:                
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time)
                full_file_path = each_dir+'/'+file
                source = open(full_file_path, 'r').read()
                #print(source)
                try:
                    try: 
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]) # 0.407
                    except Exception as e:
                        #print('value_1 failed',str(e),ticker,file)
                        try:
                            value = float(source.split(gather+':</td>/n<td class="yfnc_tabledata1">')[1].split('</td>')[0]) # 0.407
                        except Exception as e:
                            print('value_2 failed',str(e),ticker,file)
                        
                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except Exception as e:
                        #print('sp500_1 failed',str(e))
                        try:
                            sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df.index == sp500_date)]
                            sp500_value = float(row["Adjusted Close"])
                        except Exception as e:
                            print('sp500_2 failed',str(e))
                    
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        #<span id="yfs_l10_a">37.74</span>
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                            stock_price = float(stock_price.group(1))
                            #print(stock_price)
                        except Exception as e:
                            #print('stock_price_1 failed',str(e))
                            try:
                                stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price)
                                stock_price = float(stock_price.group(1))
                            except Exception as e:
                                print('stock_price_2 failed',str(e))
                            
                            #print('stock_price:',str(e), ticker, file)
                            #time.sleep(15)
    
                   #print("stock_price:",stock_price,"ticker:", ticker)
                    
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value
                        
                    
                    stock_p_change = ((stock_price - starting_stock_value)/starting_stock_value)*100
                    sp500_p_change = ((sp500_value - starting_sp500_value)/starting_sp500_value)*100
                    
                    
                    
                    #print(ticker+":",value)
                    df = df.append({'Date':date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change':stock_p_change,
                                    'SP500':sp500_value,
                                    'sp500_p_change':sp500_p_change,
                                    'Difference':stock_p_change-sp500_p_change}, ignore_index = True)
                except Exception as e:
                    print('unknown',str(e),file,ticker)
                    #time.sleep(1)
                    pass

    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])
            plot_df['Difference'].plot(label=each_ticker)
            plt.legend()
        except:
            pass
            
    save = gather.replace(' ', '').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)
    plt.show()
    
    
        
Key_Stats()
