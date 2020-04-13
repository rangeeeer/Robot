import ta
def emacros(df):
    if df.shape[0]>1:
        sign='nan'
        e9=list(ta.trend.ema_indicator(df['close'],9,fillna=True))
        e3=list(ta.trend.ema_indicator(df['close'],3,fillna=True))
        a1=e3[-2]-e9[-2]
        a2=e3[-1]-e9[-1]
        if a1>=0>=a2:
            sign= "sell"
        if a1<=0<=a2:
            sign= "buy"
        return sign