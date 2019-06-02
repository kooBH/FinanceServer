import numpy as np
import pandas as pd
import datetime as dt 
import seaborn as sns;  sns.set()
import matplotlib.pyplot as plt
import matplotlib as mpl

def bar_2(df):
    fig = plt.figure() # Create matplotlib figure
    ax = fig.add_subplot(111) # Create matplotlib axes
    ax2 = ax.twinx() # Create another axes that shares the same x-axis as ax.
    col_0 = df[df.columns[0]]
    col_1 = df[df.columns[1]]
    ax.set_ylim([0 ,max(col_0)+np.std(col_0)  ])
    ax2.set_ylim([min(col_1) - np.std(col_1) ,max(col_1)+np.std(col_1)])
    width = 0.3
    (df[df.columns[0]]).plot(kind='bar', color='#60b6c9', ax=ax, width=width, position=1 ,bottom = 0 )
    (df[df.columns[1]]).plot(kind='bar', color='#5d8c70', ax=ax2, width=width, position=0, bottom = 0 )
    ax.set_ylabel(df.columns[0])
    ax2.set_ylabel(df.columns[1])
    plt.show()
    
