import numpy as np
import pandas as pd
import requests
import os
import mason_functions as mf



def get_zachs_pages(payload):
    
    #get response from api (first page)
    response = requests.get(f'https://python.zgulde.net/api/v1/{payload}?page=1')

    #assign variable to json data
    data = response.json()

    #design dataframe with the json data
    df = pd.DataFrame(data['payload'][payload])
    
    #assign variable to max page number
    max_page = data['payload']['max_page']
    
    #commence loop
    for n in range(2, max_page + 1):
        response = requests.get(f'https://python.zgulde.net/api/v1/{payload}?page={n}')     # get response from nth page
        data = response.json()      # assign variable to json data
        df_0 = pd.DataFrame(data['payload'][payload])       # design dataframe from json
        df = pd.concat([df, df_0])      # concatenate dataframes
    
    #return finished frame
    return df


def get_items():
    
    #set up if-conditional to see if a .csv is available
    if os.path.isfile('zachs_items.csv'):
        
        #if there is, read the data into a dataframe
        items = pd.read_csv('zachs_items.csv', index_col = 0)

    #otherwise
    else:
        #get items
        items = get_zachs_pages('items')
        
        #write data to frame
        items = pd.DataFrame(items)
        
        #cache data in .csv
        items.to_csv('zachs_items.csv')
    
    return items


def get_stores():
    
    #set up if-conditional to see if a .csv is available
    if os.path.isfile('zachs_stores.csv'):
        
        #if there is, read the data into a dataframe
        stores = pd.read_csv('zachs_stores.csv', index_col = 0)
    
    #otherwise
    else:
        #get stores
        stores = get_zachs_pages('stores')
        
        #write data to frame
        stores = pd.DataFrame(stores)
        
        #cache data in .csv
        stores.to_csv('zachs_stores.csv')
    
    return stores


def get_sales():
    
    #set up if-conditional to see if a .csv is available
    if os.path.isfile('zachs_sales.csv'):
        
        #if there is, read the data into a dataframe
        sales = pd.read_csv('zachs_sales.csv', index_col = 0)

    #otherwise
    else:
        #get sales
        sales = get_zachs_pages('sales')
        
        #write data to frame
        sales = pd.DataFrame(sales)
        
        #cache data in .csv
        sales.to_csv('zachs_sales.csv')
    
    return sales


def super_store_frame():
    

    items = get_items()     # get items
    stores = get_stores()   # get stores
    sales = get_sales()     # get sales

    #set up if-conditional
    if os.path.isfile('super_store_frame.csv'):

        #read .csv if available
        super_frame = pd.read_csv('super_store_frame.csv', index_col = 0)

    #otherwise:
    else:
            
        #merge first two tables with an inner join based on key columns
        join = pd.merge(sales,
                        items,
                        how = 'inner',
                        left_on = 'item',
                        right_on = 'item_id'
                    )
        
        #merge the merged table and the stores table using the store number as a foreign key
        super_frame = pd.merge(join,
                            stores,
                            how = 'inner',
                            left_on = 'store',
                            right_on = 'store_id'
                            )
        
        super_frame.to_csv('super_store_frame.csv')

    return super_frame


def get_power():
    #read .csv with pandas .read_csv function
    power = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')

    #return df
    return power