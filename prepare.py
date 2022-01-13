import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


from datetime import timedelta, datetime

import warnings
warnings.filterwarnings('ignore')

from acquire import super_store_frame, get_power


def prep_tssf():
    
    #get super df
    sf = super_store_frame()
    
    #convert sale date to datetime
    sf.sale_date = pd.to_datetime(sf.sale_date)
    
    #set index to datetime array; make sure it is sorted
    sf = sf.set_index('sale_date').sort_index()
    
    #assign month column to the respective datetime index month
    sf['month'] = sf.index.month
    
    #assign day of week column to datetime index weekday
    sf['day_of_week'] = sf.index.weekday
    
    #assign new weekday column but with strings that add clarity
    sf['stringday'] = sf.day_of_week.map({0: 'Monday',
                                          1: 'Tuesday',
                                          2: 'Wednesday',
                                          3: 'Thursday',
                                          4: 'Friday',
                                          5: 'Saturday',
                                          6: 'Sunday'
                                         })
    
    #assign sales total column to product of total items and item price
    sf['sales_total'] = sf.sale_amount * sf.item_price
    
    #make a list of redundant columns
    redundant = ['item', 'store']

    #drop the redundants
    sf = sf.drop(columns = redundant)
    
    #return prepped frame
    return sf


def prep_power():
    
    #get power
    power = acquire.get_power()
    
    #convert date column to datetime array
    power.Date = pd.to_datetime(power.Date)
    
    #set the index to the datetime array, then sort the index
    power = power.set_index('Date').sort_index()
    
    #add month and year columns
    power['month'] = power.index.month
    power['year'] = power.index.year
    
    #fill missing values with 0
    power = power.fillna(0)
    
    #fix columns to match personal preference
    power.columns = power.columns.str.lower().str.replace('+', '_')
    
    return power