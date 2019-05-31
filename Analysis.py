# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt 
from statsmodels.formula.api import ols 
import seaborn as sns;  sns.set()
import matplotlib.pyplot as plt

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
"""
def ols_comb(dep,inds,only_rsquare=True,comb_num=1):
    ols_df = pd.DataFrame()
    if(comb_num==1):
        for idx in range(len(ols_ind)):
            ols_df = pd.concat([ols_dep1, ols_ind[idx]], axis=1, sort=False)
            
            model_fit = ols('Samsung_Electronics'+'~1+'+stan_US[idx],data=ols_df).fit()


            #print(model_fit.summary())

        for idx in range(len(ols_ind)):
            ols_df = pd.concat([ols_dep2, ols_ind[idx]], axis=1, sort=False)
            #ols_df = ols_df.pct_change()
            ols_df = ols_df.dropna()
            model_fit = ols('네이버'+'~1+'+stan_US[idx],data=ols_df).fit()
            print(model_fit.rsquared, end='')
            print(' : 네이버 ~ ' + stan_US[idx])
            #print(model_fit.summary())
    else if(comb_num==2):
        
    else if(comb_num==3):
        
    else if(comb_num==4):
        
    ols_df = ols_df.pct_change()
    ols_df = ols_df.dropna()
    print(model_fit.rsquared, end='')
    print(' :삼성전자 ~ '+ stan_US[idx])
        
"""

        
    
    