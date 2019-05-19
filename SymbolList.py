import pandas as pd
import datetime as dt

import os.path

def init_symbol_DF() :
    initial_time = dt.datetime(2010,2, 1).strftime("%Y-%m-%d")

    df = pd.DataFrame

    csv_name = 'symbol_list.csv'

    if(os.path.isfile(csv_name)):
        df = pd.read_csv(csv_name,index_col='Name')
    else :
        df = pd.DataFrame(columns=['Name','Symbol','From','To'])
        df.set_index('Name',inplace=True)
        df.to_csv(csv_name)
    df.head()
    return df

def add_symbol(df, name='Apple Inc.' ,symbol='AAPL', init=False):
    csv_name = 'symbol_list.csv'
    if(not name in df.index):
        initial_time = dt.datetime(2010,1, 1).strftime("%Y-%m-%d")
        df.loc[name] = [symbol,initial_time,initial_time]
        print('ADD : ' + name)
    else :
        print('DUP : ' + name)
    #print(df.loc[name])
    
    if(init):
        symbol_list = {
         # 미국 IT 기업
        'Apple Inc.':'AAPL' ,
        'Microsoft Corporation':'MSFT',
        'International Business Machines Corporation':'IBM',
        'Oracle Corporation':'ORCL',
        'Amazon.com, Inc.':'AMZN',
        'Tesla, Inc.':'TSLA',
        # 한국 IT 기업
         'Samsung Electronics Co., Ltd':'005930.KS',
         'SK hynix, Inc.':'000660.KS',
        'LG Electronics Inc':'066570.KS',
        'NAVER Corporation':'035420.KS'
        }
        for k in symbol_list:
            add_symbol(df,k,symbol_list[k]) 
            
    df.to_csv(csv_name)
   