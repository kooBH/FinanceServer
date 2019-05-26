import pandas as pd
import datetime as dt
import fix_yahoo_finance as yf
import os.path
import sys

sys.path.append('data/')

def init_symbol_DF() :
    initial_time = dt.datetime(2010,2, 1).strftime("%Y-%m-%d")

    df = pd.DataFrame

    csv_name = 'data/symbol_list.csv'

    if(os.path.isfile(csv_name)):
        df = pd.read_csv(csv_name,index_col='Name')
    else :
        df = pd.DataFrame(columns=['Name','Symbol','From','To'])
        df.set_index('Name',inplace=True)
        df.to_csv(csv_name)
    df.head()
    return df

def add_symbol(df, name='Apple' ,symbol='AAPL', init=False):
    csv_name = 'data/symbol_list.csv'
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
            'Apple':'AAPL' ,
            'Microsoft':'MSFT',
            'IBM':'IBM',
            'Oracle':'ORCL',
            'Amazon':'AMZN',
            'Tesla':'TSLA',
            'Alphabet':'GOOG',
            'Facebook':'FB',
            'Cisco':'CSCO',
            '타이완 반도체':'TSM',
            'Intel':'INTC',
            '오라클':'ORCL',
            'SAP':'SAP',
            # 한국 IT 기업
            'Samsung_Electronics':'005930.KS',
            'SK_hynix':'000660.KS',
            'LG_Electronics':'066570.KS',
            '삼성SDI':'006400.KS',
            '엔씨소프트':'036570.KS',
            '삼성SDS':'018260.KS',
            '카카오':'035720.KS',
            '삼성전기':'009150.KS',
            'LG디스플레이':'034220.KS',
            '네이버':'035420.KS',
            # 한국 지표
            
            # 비교군
            'XLK':'XLK',
            'BitCoin':'BTC-USD',
            'MSCI':'EEM',
            'ten_Year_Treasury':'IEF',
            'VIX':'^VIX'
            
        }
        for k in symbol_list:
            add_symbol(df,k,symbol_list[k]) 
            
    df.to_csv(csv_name)
    
def download():
    df = pd.read_csv('data/symbol_list.csv',index_col='Name')
    list_df = [None] * len(df.index)
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    for idx in range(0,len(df.index)):
        list_df[idx] = df.index[idx]
        print('Note::Processing  ' + list_df[idx])        
        # 이미 최신 데이터
        if(df.iloc[idx][2] == today):
            print('  Pass::Alread up-to-date.')
            continue
        try:
            #print(df.iloc[idx][1] + " ~ " + today)
            temp_df = yf.download(df.iloc[idx][0], start = df.iloc[idx][1], end =  today)
            df.iloc[idx][2] = today
            temp_df.to_csv('data/'+list_df[idx] + '.csv')
        except ValueError:
            print('Value Error')
        
    # 심볼리스트 갱신
    df.to_csv('data/symbol_list.csv')
    print('Note::data/symbol_list.csv is updated.')
   