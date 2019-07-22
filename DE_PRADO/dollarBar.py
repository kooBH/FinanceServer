import pandas as pd
import numpy as np
from tqdm import tqdm_notebook

from multiprocessing import Pool
#from numba import jit

#@jit(nopython=True, cache=True)

def dollarBar(
    df,
    interval='W',
    col_price='close',
    col_volume='volume',
    col_dollar='dollar',
    index_name='timestamp',
    exp_num_bar=20
    ):
    '''
    df : dataFrame with datetime index
    exp_num_bar : expected number of dollar bars in single interval
    '''
    df = df.filter([col_price,col_volume])
    df[col_dollar] = df[col_price] * df[col_volume]
    logic_rule = {
        col_dollar  : 'sum',
    }         
    df_sampled = df.resample (interval).apply(logic_rule)
    threshold = np.mean(df_sampled[col_dollar])                
    
    threshold=threshold/exp_num_bar

    cnt_t=0
    # imtermediate variables
    cur_p = 0
    # volume
    cur_v= 0
    cnt_v=0
    
    cnt_d=0
    
    dollar = pd.DataFrame(columns=[col_price]) 
    dollar.index.names = [index_name]

    for i in tqdm_notebook(range(len(df.index))):
        cur_d = (df.iloc[i])[col_dollar]
        cnt_d +=cur_d
        
        if(cnt_d >= threshold):
            cnt_d=0      
            tmp = df.iloc[i]                           
            dollar.loc[df.index[i]] = [tmp[col_price]]
    return dollar
