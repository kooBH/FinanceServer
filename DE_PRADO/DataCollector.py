from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os

def fromAlphaVantage(symbol,name):
    # My API Key 별도의 파일로 분리해야함. 
    f = open("ALPHA_KEY", 'r')
    key = f.readline()
    f.close()
    ts  = TimeSeries(key=key, output_format='pandas')
    tmp, meta_tmp = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')
    tmp.index = pd.to_datetime(tmp.index)
    idxs = tmp.index
    tmp.index = [[str(i) for i in idxs.strftime("%Y-%m-%d")],[ str(i) for i in idxs.strftime("%H-%M-%S")]]
    tmp.columns = ["volume", "high","open","close","low"]
    tmp.index.names = ["date", "time"]
    if not os.path.exists( name): os.makedirs(name)
    for byDay in tmp.index.levels[0] :
        if not os.path.exists(name+'/'+byDay + '.csv') : tmp.loc[byDay].to_csv(name+'/'+byDay + '.csv')
            
def 
