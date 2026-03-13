import pandas as pd, numpy as np, matplotlib.pyplot as plt

def load_data(path):
    df = pd.read_csv(path)
    if 'timestamp' in df.columns: df['timestamp']=pd.to_datetime(df['timestamp'])
    else: df.index=pd.to_datetime(df.index)
    if 'timestamp' in df.columns: df=df.set_index('timestamp')
    cols={'open':'open','high':'high','low':'low','close':'close','volume':'volume'}
    df=df.rename(columns={k:v for k,v in cols.items() if k in df.columns})
    return df[['open','high','low','close']].sort_index()

def backtest_orb(df, tz='America/Chicago', session_open='08:30', session_close='15:15',
                 orb_minutes=30, entry_deadline='13:30', buffer_bps=0, R=1.0,
                 slippage_bps=0, fee_bps=0):
    df=df.tz_localize(None).tz_localize('UTC').tz_convert(tz)
    df['date']=df.index.date
    out=[]
    for d,day in df.groupby('date'):
        o=pd.Timestamp(str(d)+' '+session_open,tz=tz)
        c=pd.Timestamp(str(d)+' '+session_close,tz=tz)
        if o not in day.index: continue
        day=day.loc[(day.index>=o)&(day.index<=c)]
        if len(day)<orb_minutes+5: continue
        orb_end=o+pd.Timedelta(minutes=orb_minutes)
        deadline=pd.Timestamp(str(d)+' '+entry_deadline,tz=tz)
        orbh=day.loc[o:orb_end]['high'].max()
        orbl=day.loc[o:orb_end]['low'].min()
        up=orbh*(1+buffer_bps/1e4)
        dn=orbl*(1-buffer_bps/1e4)
        entered=False
        for t,row in day.loc[orb_end:deadline].iterrows():
            px=row['close']
            if not entered and px>up:
                side=1; entry=px*(1+slippage_bps/1e4); risk=entry-orbl; tgt=entry+R*risk; stp=entry-risk
                trail=day.loc[t:c]
                exit_time=None; exit_px=None
                for tt,rr in trail.iterrows():
                    lo,hi=rr['low'],rr['high']
                    if lo<=stp: exit_time=tt; exit_px=stp*(1-slippage_bps/1e4); break
                    if hi>=tgt: exit_time=tt; exit_px=tgt*(1-slippage_bps/1e4); break
                if exit_time is None:
                    exit_time=c; exit_px=trail.iloc[-1]['close']*(1-slippage_bps/1e4)
                fees=entry*fee_bps/1e4+exit_px*fee_bps/1e4
                ret=(exit_px-entry)/entry
                out.append({'date':d,'entry_time':t,'exit_time':exit_time,'side':'long','entry':entry,'exit':exit_px,'ret':ret-fees/entry})
                entered=True
                break
            if not entered and px<dn:
                side=-1; entry=px*(1-slippage_bps/1e4); risk=orbh-entry; tgt=entry-R*risk; stp=entry+risk
                trail=day.loc[t:c]
                exit_time=None; exit_px=None
                for tt,rr in trail.iterrows():
                    lo,hi=rr['low'],rr['high']
                    if hi>=stp: exit_time=tt; exit_px=stp*(1+slippage_bps/1e4); break
                    if lo<=tgt: exit_time=tt; exit_px=tgt*(1+slippage_bps/1e4); break
                if exit_time is None:
                    exit_time=c; exit_px=trail.iloc[-1]['close']*(1+slippage_bps/1e4)
                fees=entry*fee_bps/1e4+exit_px*fee_bps/1e4
                ret=(entry-exit_px)/entry
                out.append({'date':d,'entry_time':t,'exit_time':exit_time,'side':'short','entry':entry,'exit':exit_px,'ret':ret-fees/entry})
                entered=True
                break
    trades=pd.DataFrame(out)
    if trades.empty:
        print('No trades. Adjust params.'); return trades, None
    trades['equity']=(1+trades['ret']).cumprod()
    dd=trades['equity']/trades['equity'].cummax()-1
    sharpe=np.sqrt(252)*trades['ret'].mean()/trades['ret'].std(ddof=0) if trades['ret'].std(ddof=0)>0 else np.nan
    fig,ax=plt.subplots(figsize=(9,4))
    ax.plot(trades['entry_time'].values, trades['equity'].values)
    ax.set_title(f'ORB Equity Curve | Trades: {len(trades)} | Sharpe≈{sharpe:.2f} | MaxDD≈{dd.min():.2%}')
    ax.set_ylabel('Equity (gross multiple)'); ax.set_xlabel('Time')
    plt.tight_layout()
    return trades, fig

# Example:
# df = load_data('your_1m_candles.csv')  # expects columns: timestamp, open, high, low, close
# trades, fig = backtest_orb(df,
#     tz='America/Chicago',
#     session_open='08:30', session_close='15:15',
#     orb_minutes=30, entry_deadline='13:30',
#     buffer_bps=2, R=1.0, slippage_bps=1, fee_bps=0.5)
# trades.tail()
