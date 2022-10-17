import pandas as pd


def supertrend(high:pd.Series,low:pd.Series,close:pd.Series, length:int, multiplier:int):

    tr1 = pd.Series(high - low)
    tr2 = pd.Series(abs(high - close.shift(1)))
    tr3 = pd.Series(abs(low - close.shift(1)))
    frames = [tr1, tr2, tr3]
    tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
    atr = tr.ewm(length).mean()
    
    # H/L AVG AND BASIC UPPER &amp; LOWER BAND
    hl_avg = (high + low) / 2
    upper_band = (hl_avg + multiplier * atr).dropna()
    lower_band = (hl_avg - multiplier * atr).dropna()

    # FINAL UPPER BAND
    final_bands_upper = [x for x in upper_band - upper_band]
    final_bands_lower = final_bands_upper.copy()
    for i in range(len(final_bands_upper)):
        if i == 0:
            final_bands_upper[i] = 0
        else:
            if (upper_band[i] < final_bands_upper[i-1]) | (close[i-1] >
            final_bands_upper[i-1]):
                final_bands_upper[i] = upper_band[i]
            else:
                final_bands_upper[i] = final_bands_upper[i-1]
    
    # FINAL LOWER BAND
    for i in range(len(final_bands_lower)):
        if i == 0:
            final_bands_lower[i]= 0
        else:
            if (lower_band[i] > final_bands_lower[i-1]) | (close[i-1] <
            final_bands_lower[i-1]):
                final_bands_lower[i] = lower_band[i]
            else:
                final_bands_lower[i] = final_bands_lower[i-1]
    
    final_bands_upper=pd.Series(final_bands_upper)
    final_bands_lower=pd.Series(final_bands_lower)

    # SUPERTREND
    supertrend = [x for x in final_bands_upper - final_bands_upper]
    for i in range(len(supertrend)):
        if i == 0:
            supertrend[i] = 0
        elif (supertrend[i-1] == final_bands_upper[i-1] and
        close[i] < final_bands_upper[i]):
            supertrend[i] = final_bands_upper[i]
        elif (supertrend[i-1] == final_bands_upper[i-1] and
        close[i] > final_bands_upper[i]):
            supertrend[i] = final_bands_lower[i]
        elif (supertrend[i-1] == final_bands_lower[i-1] and
        close[i] > final_bands_lower[i]):
            supertrend[i] = final_bands_lower[i]
        elif (supertrend[i-1] == final_bands_lower[i-1] and
        close[i] < final_bands_lower[i]):
            supertrend[i] = final_bands_upper[i]

         
    supertrend=pd.Series(supertrend)
    supertrend.index=high.index
    supertrend = supertrend.dropna()
    
    # ST UPTREND/DOWNTREND
    upt = []
    dt = []
    close = close.iloc[len(close) - len(supertrend):]
    for i in range(len(supertrend)):
        if close[i] > supertrend[i]:
            upt.append(supertrend[i])
            dt.append(0)
        elif close[i] < supertrend[i]:
            upt.append(0)
            dt.append(supertrend[i])
        else:
            upt.append(0)
            dt.append(0)
            
    UpT,DT = pd.Series(upt),pd.Series(dt)
    UpT.index=supertrend.index
    DT.index=supertrend.index

    return  supertrend, UpT, DT


def Tenkan_Sen(high:pd.Series,low:pd.Series,cl_period = 9 )-> pd.Series:

    High=high.rolling(cl_period).max()
    Low=low.rolling(cl_period).min()

    return  (High+Low)/2
    
    
def Kijun_Sen(high:pd.Series,low:pd.Series,cl_period = 26 )-> pd.Series:

    High=high.rolling(cl_period).max()
    Low=low.rolling(cl_period).min()

    return  (High+Low)/2

def Senkou_SpanA(high:pd.Series,low:pd.Series,lag_spanA_period=30)-> pd.Series:

    return  ((Tenkan_Sen(high,low)+Kijun_Sen(high,low))/2).shift(lag_spanA_period)


def Senkou_SpanB(high:pd.Series,low:pd.Series,lag_spanB_period=120)-> pd.Series:

    High=high.rolling(lag_spanB_period).max()
    Low=low.rolling(lag_spanB_period).min()

    return  ((High+Low)/2).shift(lag_spanB_period)

def Chikou_Span(close:pd.Series,lag_span_period=30)-> pd.Series:

    return  close.shift(-lag_span_period)


