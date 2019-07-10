import pandas as pd
import numpy as np
import os
from bars import TIB,VIB,DIB
from tqdm import tqdm
import multiprocessing as mp

def some():
    path = 'MiniKospi/'
    list_file = os.listdir(path)
    list_file.sort()
    data = pd.DataFrame(columns=['close','volume']) 
    data.index.names = ['timestamp']
    cnt=0
    for file in tqdm(list_file) :
        tmp = pd.read_csv(path+file,index_col=0)
        tmp = tmp.drop(columns=['date','time','sell','buy'])
        tmp.index = pd.to_datetime(tmp.index)
        tmp.index.names = ['timestamp']
        data = data.append(tmp)
        cnt+=1
        if cnt > 3: break;
    weekly = [g for n, g in data.groupby(pd.Grouper(level='timestamp', freq='W'))]
    
    output_tick = mp.Queue()
    output_volume = mp.Queue()
    output_dollar = mp.Queue()

    procs = []
    print('**** 1 *****')
    procs.append(mp.Process(target=TIB, args=(weekly,output_tick)) ) 
    procs.append(mp.Process(target=VIB, args=(weekly,output_volume)) )
    procs.append(mp.Process(target=DIB, args=(weekly,output_dollar)) )  
    print('**** 2 *****')
    for proc in procs:
        proc.start()
    display(procs)
    for proc in procs:
        proc.join()
    print('**** 3 *****')
    tick = output_tick.get()
    volume = output_volume.get()
    dollar = output_dollar.get()
    print('**** 4 *****')
    output_tick.close()
    output_volume.close()
    output_dollar.close()
    print('**** 5 *****')
    
    
    return tick,volume,dollar