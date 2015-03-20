# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 10:31:43 2015

@author: 3820104
"""

import pandas as pd
import os
import Quandl
import time

auth_tok = open("auth_key.txt","r").read()
                    
path = path = "C:/Users/3820104/Documents/_python_data/intraQuarter"

def Stock_Prices():
    df = pd.DataFrame()
    statspath = path+"/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]
    for each_dir in stock_list[1:]:
        try:
            ticker = each_dir.split("\\")[1]
            print(ticker)
            name = "WIKI/"+ticker.upper()
            data = Quandl.get(name,
                              authtoken=auth_tok, 
                              trim_start='2000-12-12', 
                              trim_end='2014-12-30')
            data[ticker.upper()] = data["Adj. Close"]
            df = pd.concat([df, data[ticker.upper()]], axis = 1)
        except Exception as e:
            print(str(e))
            
    df.to_csv("stock_prices.csv")
    
Stock_Prices()