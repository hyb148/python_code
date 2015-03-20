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
#bars = Quandl.get("GOOG/NYSE_SPY", collapse="daily")
#mydata = Quandl.get("WIKI/AAPL", authtoken=auth_tok)
                    
data = Quandl.get("WIKI/KO", authtoken=auth_tok, trim_start='2000-12-12', trim_end='2014-12-30')

print(data)