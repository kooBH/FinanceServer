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

def ols_comb(             
           dep,inds,
           comb_num=1,
           show_summary = False,
           do_shift = True,
           show_plot = True,  
           show_line = False,  
           start='2016-01-04',
           end='2018-12-28'
            ):
    ols_ind=[]
    for i in inds:
        tmp = pd.read_csv('data/'+i+'.csv',index_col='Date',engine='c')
        tmp = tmp[['Close']]
        tmp = tmp.loc[start:end]
        tmp.columns = [i]
        ols_ind.append(tmp)

    ols_dep1 = pd.read_csv('data/'+dep+'.csv',index_col='Date',engine='c')
    ols_dep1 = ols_dep1[['Close']]
    ols_dep1 = ols_dep1.loc[start:end]
    ols_dep1.columns = [dep]    
    
    ret_df = pd.DataFrame(columns=['rsqaured',*inds])
    com = it.combinations(range(len(inds)), comb_num)
    if(comb_num==1):
         for idx in com:
                ols_df = pd.concat([ols_dep1, ols_ind[idx[0]]], axis=1, sort=False)
                ols_df = ols_df.pct_change()
                ols_df = ols_df.dropna()
                model_fit = ols(dep+'~1+'+inds[idx[0]],data=ols_df).fit()
                if(show_line):
                    print('%.5f'%(model_fit.rsquared), end='')
                    print(dep + ' ~ '+ inds[idx[0]])
                if(show_summary):
                    print(model_fit.summary())  
                temp_df = pd.DataFrame( {'rsqaured':model_fit.rsquared,inds[idx[0]]:[model_fit.params.values[1]]})
                ret_df = ret_df.append(temp_df, sort=True)    
                
    elif(comb_num==2):
        for idx in com:
            ols_df = pd.concat([ols_dep1, ols_ind[idx[0]],ols_ind[idx[1]]], axis=1, sort=False)
            ols_df = ols_df.pct_change()
            ols_df = ols_df.dropna()
            model_fit = ols(dep+'~1+'+inds[idx[0]]+'+'+inds[idx[1]],data=ols_df).fit()
            if(show_line):
                print('%.5f'%(model_fit.rsquared), end='')
                print(dep + ' ~ '+ inds[idx[0]] +' + '+inds[idx[1]])
            if(show_summary):
                print(model_fit.summary())  
            temp_df = pd.DataFrame( {'rsqaured':model_fit.rsquared,inds[idx[0]]:[model_fit.params.values[1]], inds[idx[1]]:[model_fit.params.values[2]]})
            ret_df = ret_df.append(temp_df, sort=True)    
    elif(comb_num==3):
        for idx in com:
            ols_df = pd.concat([ols_dep1, ols_ind[idx[0]],ols_ind[idx[1]],ols_ind[idx[2]]], axis=1, sort=False)
            ols_df = ols_df.pct_change()
            ols_df = ols_df.dropna()
            model_fit = ols(dep+'~1+'+inds[idx[0]]+'+'+inds[idx[1]]+'+'+inds[idx[2]],data=ols_df).fit()
            if(show_line):
                print('%.5f'%(model_fit.rsquared), end='')
                print(dep + ' ~ '+ inds[idx[0]] +' + '+inds[idx[1]]+' + '+inds[idx[2]])
            if(show_summary):
                print(model_fit.summary())
            temp_df = pd.DataFrame( {'rsqaured':model_fit.rsquared,inds[idx[0]]:[model_fit.params.values[1]], inds[idx[1]]:[model_fit.params.values[2]],inds[idx[2]]:[model_fit.params.values[3]]})
            ret_df = ret_df.append(temp_df, sort=True)        
    elif(comb_num==4):
        for idx in com:
            ols_df = pd.concat([ols_dep1, ols_ind[idx[0]],ols_ind[idx[1]],ols_ind[idx[2]],ols_ind[idx[3]]], axis=1, sort=False)
            ols_df = ols_df.pct_change()
            ols_df = ols_df.dropna()
            model_fit = ols(dep+'~1+'+inds[idx[0]]+'+'+inds[idx[1]]+'+'+inds[idx[2]]+'+'+inds[idx[3]],data=ols_df).fit()
            if(show_line):
                print('%.5f'%(model_fit.rsquared), end='')        
                print(dep + ' ~ '+ inds[idx[0]] +' + '+inds[idx[1]]+' + '+inds[idx[1]]+' + '+inds[idx[2]]+' + '+inds[idx[3]])
            if(show_summary):
                print(model_fit.summary())
            temp_df = pd.DataFrame( {'rsqaured':model_fit.rsquared,inds[idx[0]]:[model_fit.params.values[1]], inds[idx[1]]:[model_fit.params.values[2]],inds[idx[2]]:[model_fit.params.values[3]],inds[idx[3]]:[model_fit.params.values[4]]})
            ret_df = ret_df.append(temp_df, sort=True)        
    if(show_plot):        
        ret_df['rsqaured'] = ret_df['rsqaured'].round(4)    
        ret_df = ret_df.set_index('rsqaured')
        ret_df.sort_index(inplace=True)
        ax = ret_df.plot(kind='bar', stacked=True, rot=45);
        ax.set_ylabel("coef")
        


        
    
    