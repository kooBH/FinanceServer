from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os

def fromAlphaVantage(symbol,name):
    # 별도의 파일에서 API KEY를 가져옴. 
    f = open("ALPHA_KEY", 'r')
    key = f.readline()
    f.close()
    # AlphaVantage에서 데이터를 받아온다.
    ts  = TimeSeries(key=key, output_format='pandas')
    tmp, meta_tmp = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')
    tmp.index = pd.to_datetime(tmp.index)
    idxs = tmp.index
    # 일자별로 파일을 분할해서 저장한다
    tmp.index = [[str(i) for i in idxs.strftime("%Y-%m-%d")],[ str(i) for i in idxs.strftime("%H-%M-%S")]]
    # 이름 정리
    tmp.columns = ["volume", "high","open","close","low"]
    tmp.index.names = ["date", "time"]
    # 중복된 파일은 생성하지 않음.
    if not os.path.exists( name): os.makedirs(name)
    for byDay in tmp.index.levels[0] :
        if not os.path.exists(name+'/'+byDay + '.csv') : tmp.loc[byDay].to_csv(name+'/'+byDay + '.csv')
            