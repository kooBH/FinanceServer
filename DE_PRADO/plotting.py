def plot_star(df,color,ax):
    return df.plot(
    style='*',
    color=color,
    use_index =True,
    subplots=False,
    sharex =True,
    rot =45,
    ax=ax
    )