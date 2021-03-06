# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt 
from statsmodels.formula.api import ols 
import seaborn as sns;  sns.set()
import matplotlib.pyplot as plt
import itertools as it

# https://seaborn.pydata.org/generated/seaborn.jointplot.html
def joint(target_1,target_2,col='Close',dur=240,eng='c'):
    ols_df1 = pd.read_csv('data/'+target_1 + '.csv',index_col='Date',engine = eng)
    ols_df1 = ols_df1[[col]]
    ols_df1.columns = [target_1]
    ols_df2 = pd.read_csv('data/'+target_2 + '.csv',index_col='Date',engine = eng)
    ols_df2 = ols_df2[[col]]
    ols_df2.columns = [target_2]
    new_df = pd.concat([ols_df1, ols_df2], axis=1, sort=False)
    new_df = new_df.dropna()
    new_df = new_df[-dur:]
    ret_index = new_df.pct_change()
    ret_index = ret_index.dropna()
    sns.jointplot(target_1, target_2, data = ret_index, kind='reg')

    
def isValid(target,start='2016-01-04',end='2018-12-28',eng='c'):
    #fig, ax  = plt.subplots(len(target), figsize=(100,20))
    for i in range(len(target)):
        print('plotting : ' + target[i])
        val_df = pd.read_csv('data/'+target[i]+ '.csv',index_col='Date',engine = eng)
        val_df = val_df[['Close']]
        val_df = val_df.loc[start:end]
        val_df.columns = [target[i]]
        #plt.set_title(target[i])
        val_df.plot(figsize=(40,4))
        #val_df.plot()        
        #title = target[i]
        #ax[i%4,(int)(i/4)].plot(val_df, color='red')
        #ax[i].plot(val_df, color='red')
        #ax[i%4,(int)(i/4)].set_title(title)
        #ax[i,j].set_xticklabels([tyme.strftime("%Y-%m") for tyme in df.index[-60:]])
        #ax[i%4,(int)(i/4)].set_xticklabels([tyme.strftime("%m-%d") for tyme in df.index[-60:]], rotation=45)
        #ax[i,j].plot(data.iloc[-60:]['DJIA']).plot(ax= ax[j,i])                            
       # plt.show()

# + Weekly Monthly
#
# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DatetimeIndex.html
#
# https://stackoverflow.com/questions/20584627/how-do-you-pull-weekly-historical-data-from-yahoo-finance
#
# ```python
# df.resample('W', how='mean')
# ``` 
# index 를 DataTimeIndex로 변환하면 resampling을 할 수 있다.
# 
# https://stackoverflow.com/questions/34597926/converting-daily-stock-data-to-weekly-based-via-pandas-in-python 
#

def ols_comb(             
           dep,inds,
           comb_num=1,
           show_summary = False,
           do_shift = True,
           show_plot = True,  
           show_line = False,
           weekly=True,
           start='2016-01-04',
           end='2018-12-28',
           engine='c'
            ):
    ols_ind=[]
    ### for coverting to weekly data
    logic = {'Open'  : 'first',
    'High'  : 'max',
    'Low'   : 'min',
    'Close' : 'last',
    'Adj Close':'last',
    'Volume': 'sum'}
    offset = pd.offsets.timedelta(days=-6)
    ###
    
    ### Data Preparation ###
    for i in inds:
        tmp = pd.read_csv('data/'+i+'.csv',index_col='Date',engine=engine)
         # Need to covnert index to datetimeindex
        if(weekly):           
            tmp.index = pd.to_datetime(tmp.index)
            tmp = tmp.resample('W', loffset=offset).apply(logic)
        tmp = tmp[['Close']]
        tmp = tmp.loc[start:end]
        tmp.columns = [i]
        ols_ind.append(tmp)

    ols_dep1 = pd.read_csv('data/'+dep+'.csv',index_col='Date',engine=engine)
     # Need to covnert index to datetimeindex
    if(weekly):       
        ols_dep1.index = pd.to_datetime(ols_dep1.index)
        ols_dep1 = ols_dep1.resample('W', loffset=offset).apply(logic)
    ols_dep1 = ols_dep1[['Close']]
    ols_dep1 = ols_dep1.loc[start:end]
    ols_dep1.columns = [dep]    
    
    ret_df = pd.DataFrame(columns=['rsqaured',*inds])
    # get all posiible combinations
    com = it.combinations(range(len(inds)), comb_num)
  
    for c in com:
        ols_df = ols_dep1
        for idx in range(comb_num):
            ols_df = pd.concat([ols_df, ols_ind[c[idx]]], axis=1, sort=False)
        ols_df = ols_df.pct_change()
        ols_df = ols_df.dropna()
        # ols 명령어 생성
        ols_str = [dep,'~1']
        for idx in range(comb_num):
            ols_str.append('+')
            ols_str.append(inds[c[idx]])
        ols_str ="".join(ols_str)
        
        model_fit = ols(ols_str,data=ols_df).fit()        
        
        if(show_line):
            print('%.5f'%(model_fit.rsquared), end='')
            print(ols_str)
            
        if(show_summary):
            print(model_fit.summary()) 
            
        ols_tuple = {'rsqaured':model_fit.rsquared}
        for idx in range(comb_num):
            ols_tuple[inds[c[idx]]] = [model_fit.params.values[idx+1]]
            
        temp_df = pd.DataFrame( ols_tuple)
        ret_df = ret_df.append(temp_df, sort=True)    
        
    if(show_plot):        
        ret_df['rsqaured'] = ret_df['rsqaured'].round(4)    
        ret_df = ret_df.set_index('rsqaured')
        ret_df.sort_index(inplace=True)
        ax = ret_df.plot(kind='bar', stacked=True, rot=45,title="OLS : " + str(comb_num)+ " Vars",figsize=(20,10),fontsize=20);
        ax.set_ylabel("coef",fontsize=24)
        ax.set_xlabel("rsqaured",fontsize=24)
        ax.title.set_size(32)
        
def cokur(
    target1,
    target2,
    start='2016-01-04',
    end='2018-12-28',
    engine='c',
    value = 'Close'
    ):      
    
    df1 = pd.read_csv('data/'+target1+'.csv',index_col='Date',engine=engine)
    df2 = pd.read_csv('data/'+target2+'.csv',index_col='Date',engine=engine)

    df1 = df1.loc[start:end]
    df2 = df2.loc[start:end]

    df1 = df1[[value]]
    df2 = df2[[value]]

    df1 = df1.pct_change()
    df2 = df2.pct_change()

    nom = (((df1 - df1.mean()).pow(2)) * ((df2 - df2.mean()).pow(2))).mean()
    denom = ((df1.std().pow(2)))  *   ((df2.std().pow(2)))

    cokur = nom/denom
    return cokur

def corr(
    target1,
    targets,
    start='2016-01-04',
    end='2018-12-28',
    engine='c',
    value = 'Close',
    weekly=True
    ):   
    
    ### for coverting to weekly data
    logic = {
    'Open'  : 'first',
    'High'  : 'max',
    'Low'   : 'min',
    'Adj Close':'last',
    'Volume': 'sum',
    'Close' : 'last'    
    }
    offset = pd.offsets.timedelta(days=-6)
    ###
    
    df1 = pd.read_csv('data/'+target1+'.csv',index_col='Date',engine=engine)
    df1 = df1.loc[start:end]
        
    if(weekly):       
        df1.index = pd.to_datetime(df1.index)
        df1 = df1.resample('W', loffset=offset).apply(logic)
                
    df1 = df1[[value]]
    df1 = df1.pct_change()
    df1.dropna()        
    df1.columns = [target1]
    
    df_corr = pd.DataFrame(columns=['Samsung_Electronics'])

    for target2 in targets:
        df2 = pd.read_csv('data/'+target2+'.csv',index_col='Date',engine=engine)
        df2 = df2.loc[start:end]
        if(weekly):  
            df2.index = pd.to_datetime(df2.index)
            df2 = df2.resample('W', loffset=offset).apply(logic)
        
        df2 = df2[[value]]
        df2 = df2.pct_change()
        df2.dropna()
        df2.columns = [target2]        
        df3 = pd.concat([df1, df2],axis=1, sort=False)
        tmp = df3.corr()
        df_corr.loc[target2] = [tmp.iloc[0][1]]     
    return df_corr
