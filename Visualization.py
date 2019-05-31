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
    ax.set_ylim([min(df[df.columns[0]]),max(df[df.columns[0]])])
    ax2.set_ylim([min(df[df.columns[1]]),max(df[df.columns[1]])])
    width = 0.3
    (df[df.columns[0]]).plot(kind='bar', color='#60b6c9', ax=ax, width=width, position=1 ,bottom = min(df[df.columns[0]]))
    (df[df.columns[1]]).plot(kind='bar', color='#5d8c70', ax=ax2, width=width, position=0, bottom = min(df[df.columns[1]]))
    display([min(df[df.columns[0]]),max(df[df.columns[1]])])                  
    ax.set_ylabel(df.columns[0])
    ax2.set_ylabel(df.columns[1])
    plt.show()
    
    
def stack(df):
    # Import Data
      # Prepare data
    x_var = 'rsqaure'
    groupby_var = 'class'
    df_agg = df.loc[:, [x_var, groupby_var]].groupby(groupby_var)
    vals = [df[x_var].values.tolist() for i, df in df_agg]

    # Draw
    plt.figure(figsize=(16,9), dpi= 80)
    colors = [plt.cm.Spectral(i/float(len(vals)-1)) for i in range(len(vals))]
    n, bins, patches = plt.hist(vals, 30, stacked=True, density=False, color=colors[:len(vals)])

    # Decoration
    plt.legend({group:col for group, col in zip(np.unique(df[groupby_var]).tolist(), colors[:len(vals)])})
    plt.title(f"Stacked Histogram of ${x_var}$ colored by ${groupby_var}$", fontsize=22)
    plt.xlabel(x_var)
    plt.ylabel("Frequency")
    plt.ylim(0, 25)
    plt.xticks(ticks=bins[::3], labels=[round(b,1) for b in bins[::3]])
    plt.show()