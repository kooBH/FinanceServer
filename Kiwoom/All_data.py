import kiwoom
import pandas as pd
import sys,os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QAxContainer import *

app = QApplication(sys.argv)

kiwoom = kiwoom.kiwoom()
kiwoom.comm_connect()

temp_df = pd.read_csv('상장법인목록/code_KOSPI.csv')
cnt =1
for i in temp_df.index:
    print(str(temp_df.loc[i]['회사명'])+ ' 작업 중... ' + str(cnt) + '/' + str(temp_df.index.size))
    cnt+=1
    code = str(temp_df.loc[i]['종목코드'])
    if not os.path.exists(code): os.makedirs(code)
    kiwoom.req_minute_data(code)
    path = code+ "/"
    list_file = os.listdir(path)
    list_file = [elem[:-4] for elem in list_file]
    list_file=list(map(int,list_file))
    list_file.sort()
    list_file = [str(elem) + '.csv' for elem in list_file]
    data = pd.DataFrame(columns=['close','volume']) 
    data.index.names = ['date']
    for file in list_file :
    # display((path))
        tmp = pd.read_csv(path+file,index_col='date')
        #tmp = tmp.drop(columns=['close','volume','sell','buy'])
        tmp.index = pd.to_datetime(tmp.index)
        tmp.index.names = ['date']
        data = data.append(tmp)
    data = data.reindex(index=data.index[::-1])
    data = data.loc[~data.index.duplicated(keep='first')]
    data.to_csv(path + 'data.csv')


app.exec_()