import pandas as pd
import numpy as np

def dollar_Bar(data,threshold,index='timestamp',col_price='close',col_volume='volume'):
    # imtermediate variables
    cur_p = data.iloc[0,0]
    
    # volume
    cur_v = 0
    cnt_v=0
    tick = pd.DataFrame(columns=[col_price]) 
    tick.index.names = [index]

    for i in range(len(data.index)):
        cur_v=data.iloc[i,1]
        cur_p = data.iloc[i,0]
        cnt_v +=cur_v*cur_p
        if(cnt_v >= threshold):
            cnt_v=0      
            tmp = data.iloc[i]                           
            tick.loc[data.index[i]] = [tmp[0]] 
    return tick    

def ewma_weight(window):
    return 2/(window+1)

def tick_init(data,threshold,column='close'):
    # target variables
    pr = 0; e_0 =0
    # imtermediate variables
    theta = []
    cur_tick = 0
    # price
    prev_p =0;d_p =0; cur_p = data.iloc[0][1]
    # b_t
    prev_b =0; cur_b =0; cum_b=0
    # p[b_t = 1]
    num_tick=0; num_p_1 =0 
    for i in data.iterrows():
        # tick
        cur_tick += 1
        if(cur_tick >= threshold):
            cur_tick = 0    
            # step 1
            prev_p = cur_p
            cur_p = i[1]['close']
            d_p = cur_p - prev_p
            if d_p != 0:
                cur_b = abs(d_p)/d_p                
            else :
                if prev_b == 0 : # 예외처리
                    cur_b = 1
                else :
                    cur_b = prev_b          
            # step 2        
            cum_b += cur_b
            theta.append(cum_b )
            num_tick+=1
            if(cur_b==1):
                num_p_1 +=1
    pr = num_p_1/num_tick

    e_0 = (np.mean(np.abs(theta))) + np.std(theta)
    return e_0,pr

def tick_procedure(data,e_0,pr,threshold=500,index='timestamp',column='close'):
    theta = 0
    cur_tick = 0
    # price
    prev_p =0;    d_p =0
    cur_p = data.iloc[0,0]
    # b_t
    prev_b =0;    cur_b =0
    # p[b_t = 1]
    num_tick=0 ;    num_p_1 =0 
    
    tick = pd.DataFrame(columns=[column]) 
    tick.index.names = [index]
    num_tick = 0
   
    for i in range(len(data.index)):
        # tick
        cur_tick += 1
        if(cur_tick >= threshold):
            cur_tick = 0
            # step 1
            prev_p = cur_p
            cur_p = data.iloc[i,0]
            d_p = cur_p - prev_p
            
            prev_b = cur_b
            if d_p != 0:
                cur_b = abs(d_p)/d_p                
            else :
                if prev_b == 0 : # 예외처리
                    cur_b = 1
                else :
                    cur_b = prev_b     
            # step 2
            theta += cur_b
            
            if(cur_b==1):
                num_p_1 +=1
            # step 3
            if(np.abs(theta) > e_0 * np.abs(2*pr - 1)):    
                tmp = data.iloc[i]           
                # reset 
                theta=0
                
                tick.loc[data.index[i]] = [tmp[0]] 
            num_tick+=1
        
    # update        
    weight = ewma_weight(num_tick)
    pr = (num_p_1/num_tick)*weight + pr*(1-weight)    
    e_0 = tick.size*weight + e_0*(1-weight)       

    return e_0,pr,tick

def volume_init(data,threshold,col_price,col_volume):
    # target variables
    pr = 0
    e_0 =0
    # imtermediate variables
    theta = []
    cur_tick = 0
    prev_p =0;    d_p =0;    cur_p = data.iloc[0][1]
    
    cur_v = 0;    cnt_v=0;    cum_v =0;    pos_v=0
    num_pos=0
    
    prev_b =0;    cur_b =0;    cum_b=0
    
    # p[b_t = 1]
    num_tick=0 ;    num_p_1 =0 
    
    v_plus=0
    e_v=0
    
    for i in data.iterrows():
        # volume 
        
        cur_v=i[1][col_volume]
       
        cnt_v +=cur_v
        if(cnt_v >= threshold):
            cnt_v = 0    
            cum_v += cur_v
            # step 1
            prev_p = cur_p
            cur_p = i[1][col_price]
            d_p = cur_p - prev_p
            
            # b_t                      
            if d_p != 0:
                cur_b = abs(d_p)/d_p                
            else :
                if prev_b == 0 : # 예외처리
                    cur_b = 1
                else :
                    cur_b = prev_b     
            # v_t       
            if cur_b ==1:
                pos_v +=cur_v
                num_pos+=1
            
            # step 2        
            cum_b += cur_b * cur_v
            theta.append(cum_b )
            num_tick+=1
            if(cur_b==1):
                num_p_1 +=1
                
    pr = num_p_1/num_tick
    e_0 = (np.mean(np.abs(theta))) + np.std(theta)
    v_plus = pr*(pos_v/num_pos)
    e_v = cum_v/num_tick

    return e_0,v_plus,e_v

def volume_procedure(data,e_0,v_plus,e_v,threshold=500,index='timestamp',col_price='close',col_volume='volume'):
    # imtermediate variables
    theta = 0
    cur_tick = 0
    
    #price
    prev_p =0;    d_p =0
    cur_p = data.iloc[0,0]
    prev_b =0;    cur_b =0
    
    # volume
    cur_v = 0;    cnt_v=0;    cum_v =0;    pos_v=0
    num_pos=0
    
    # p[b_t = 1]
    num_tick=0 ;    num_p_1 =0 
    
    tick = pd.DataFrame(columns=[col_price]) 
    tick.index.names = [index]
    num_tick = 0
    
    e_v=0
    v_plus=0
    
    for i in range(len(data.index)):
        # tick

        cur_v=data.iloc[i,1]
        cnt_v +=cur_v
        if(cnt_v >= threshold):
            cnt_v=0
            cum_v +=cur_v
            
            # step 1
            prev_p = cur_p
            cur_p = data.iloc[i,0]
            d_p = cur_p - prev_p
            
            prev_b = cur_b
            if d_p != 0:
                cur_b = abs(d_p)/d_p                
            else :
                if prev_b == 0 : # 예외처리
                    cur_b = 1
                else :
                    cur_b = prev_b    
                    
            # v_t       
            if cur_b ==1:
                pos_v +=cur_v
                num_pos+=1        
                    
            # step 2
            theta += cur_b*cur_v
            
            if(cur_b==1):
                num_p_1 +=1
            # step 3
            if(np.abs(theta) > e_0 * np.abs(2*v_plus - e_v)):    
                tmp = data.iloc[i]                           
                # reset 
                theta=0                
                    #print(data.index[i])
                    #print(tmp[0])
                    #print(tmp[1])
                tick.loc[data.index[i]] = [tmp[0]] 
            num_tick+=1
        
    # update        
    weight = ewma_weight(num_tick)

    # TODO pr 도 EWMA 로 ? 
    pr = num_p_1/num_tick    
    
    e_0 = tick.size*weight + e_0*(1-weight)       

    v_plus = pr*(pos_v/num_pos)*weight + v_plus*(1-weight)
    e_v = (cum_v/num_tick)*weight + e_v*(1-weight)
    return e_0,v_plus,e_v, tick

def dollar_init(data,threshold,col_price='close',col_volume='volume'):
    # target variables
    pr = 0
    e_0 =0
    # imtermediate variables
    theta = []
    cur_tick = 0
    prev_p =0
    d_p =0
    cur_p = data.iloc[0][1]
    
    cur_v = 0
    cnt_v=0
    cum_v =0
    pos_v=0
    num_pos=0
    
    prev_b =0
    cur_b =0
    cum_b=0
    
    # p[b_t = 1]
    num_tick=0 
    num_p_1 =0 
    
    v_plus=0
    e_v=0
    
    for i in data.iterrows():
        # volume 
        
        cur_v=i[1][col_volume]
        cur_p = i[1][col_price]
        cnt_v +=cur_p
        if(cnt_v >= threshold):
            cnt_v = 0
            # dollar bar
            cur_v *= cur_p
        
            cum_v += cur_v
            # step 1
            prev_p = cur_p
            d_p = cur_p - prev_p
            
            # b_t                      
            if d_p != 0:
                cur_b = abs(d_p)/d_p                
            else :
                if prev_b == 0 : # 예외처리
                    cur_b = 1
                else :
                    cur_b = prev_b     
            # v_t       
            if cur_b ==1:
                pos_v +=cur_v
                num_pos+=1
            
            # step 2        
            cum_b += cur_b * cur_v
            theta.append(cum_b )
            num_tick+=1
            if(cur_b==1):
                num_p_1 +=1
                
    pr = num_p_1/num_tick
    e_0 = (np.mean(np.abs(theta))) + np.std(theta)
    v_plus = pr*(pos_v/num_pos)
    e_v = cum_v/num_tick

    return e_0,v_plus,e_v

def dollar_procedure(data,e_0,v_plus,e_v,threshold,index,col_price,col_volume):
    # imtermediate variables
    theta = 0
    cur_tick = 0
    
    #price
    prev_p =0
    d_p =0
    cur_p = data.iloc[0,0]
    prev_b =0
    cur_b =0
    
    # volume
    cur_v = 0
    cnt_v=0
    cum_v =0
    pos_v=0
    num_pos=0
    
    # p[b_t = 1]
    num_tick=0 
    num_p_1 =0 
    
    tick = pd.DataFrame(columns=[col_price]) 
    tick.index.names = [index]
    num_tick = 0
    
    e_v=0
    v_plus=0
    
    for i in range(len(data.index)):
        # tick

        cur_v=data.iloc[i,1]
        cur_p = data.iloc[i,0]
        cnt_v +=cur_v*cur_p
        if(cnt_v >= threshold):
            cnt_v=0
            # dollar bar
            cur_v *= cur_p
            
            cum_v +=cur_v            
            # step 1
            prev_p = cur_p
            
            d_p = cur_p - prev_p
            
            prev_b = cur_b
            if d_p != 0:
                cur_b = abs(d_p)/d_p                
            else :
                if prev_b == 0 : # 예외처리
                    cur_b = 1
                else :
                    cur_b = prev_b    
                    
            # v_t       
            if cur_b ==1:
                pos_v +=cur_v
                num_pos+=1        
                    
            # step 2
            theta += cur_b*cur_v
            
            if(cur_b==1):
                num_p_1 +=1
            # step 3
            if(np.abs(theta) > e_0 * np.abs(2*v_plus - e_v)):    
                tmp = data.iloc[i]                           
                # reset 
                theta=0                
                    #print(data.index[i])
                    #print(tmp[0])
                    #print(tmp[1])
                tick.loc[data.index[i]] = [tmp[0]] 
            num_tick+=1
        
    # update        
    weight = ewma_weight(num_tick)

    # TODO pr 도 EWMA 로 ? 
    pr = num_p_1/num_tick    
    
    e_0 = tick.size*weight + e_0*(1-weight)       

    v_plus = pr*(pos_v/num_pos)*weight + v_plus*(1-weight)
    e_v = (cum_v/num_tick)*weight + e_v*(1-weight)
    return e_0,v_plus,e_v, tick

##########################################################################

def TIB(weekly_data,threshold=5000,index='timestamp',column='close'):
    print('TIB start')
    tick = pd.DataFrame(columns=['close']) 
    tick.index.names = ['timestamp']
    
    e_0,pr = tick_init(weekly_data[1],threshold,column)
    for tmp in weekly_data[2:]:
        e_0,pr,t_tick = tick_procedure(tmp,e_0,pr,threshold,index,column)
        tick = pd.concat([tick, t_tick])
    
    return tick
        
def VIB(weekly_data,threshold=20000,index='timestamp',col_price='close',col_volume='volume'):
    print('VIB start')
    volume = pd.DataFrame(columns=['close']) 
    volume.index.names = ['timestamp']
    
    e_0,v_plus,e_v = volume_init(weekly_data[1],threshold,col_price,col_volume)
    for tmp in weekly_data[2:]:    
        e_0,v_plus,e_v,t_volume = volume_procedure(tmp,e_0,v_plus,e_v,threshold,index,col_price,col_volume)
        volume = pd.concat([volume, t_volume])
    
    return volume
        
def DIB(weekly_data,threshold=200000,index='timestamp',col_price='close',col_volume='volume'):
    print('DIB start')
    dollar = pd.DataFrame(columns=['close']) 
    dollar.index.names = ['timestamp']
    
    e_0,v_plus,e_v = dollar_init(weekly_data[1],threshold,col_price,col_volume)
    for tmp in weekly_data[2:]:
        e_0,v_plus,e_v,t_dollar = dollar_procedure(tmp,e_0,v_plus,e_v,threshold,index,col_price,col_volume)
        dollar = pd.concat([dollar, t_dollar])
    
    return dollar