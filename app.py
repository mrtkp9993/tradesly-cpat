import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import talib
import pandas_ta as ta
from lib.candlestick_pat_names import candlestickNames

st.set_page_config(page_title="tradesly: Candlestick Pattern Backtesting", page_icon=":chart_with_upwards_trend:", layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.image("assets/banner.webp", use_column_width=True)
st.header("tradesly: Candlestick Pattern Backtesting")

st.markdown("""Backtest Candlestick Patterns with simple strategy.

1. If signal, buy at open of next candle.
2. If price is above `entry * (1 + take profit)`, sell at open of next candle.
3. If price is below `entry * (1 - stop loss)`, sell at open of next candle.

            """)

st.divider()

st.sidebar.markdown("""
## Our Paid Apps
* [tradeslyFX Forex](https://play.google.com/store/apps/details?id=com.tradesly.tradeslyfx)
* [tradeslyPro Cryptocurrency](https://play.google.com/store/apps/details?id=com.tradesly.tradeslypro)
* [tradeslyNX Borsa Istanbul](https://play.google.com/store/apps/details?id=com.tradesly.tradeslynxbist)
            """)

st.sidebar.divider()

# Get stock code
stock_code = st.sidebar.text_input("Enter stock code", value="AAPL")

# Stop loss percentage
stoploss = st.sidebar.slider("Stop Loss", min_value=0.0, max_value=1.0, value=0.05)

# Take profit percentage
takeprofit = st.sidebar.slider("Take Profit", min_value=0.0, max_value=1.0, value=0.1)

# Analyze button
analyze_button = st.sidebar.button("Analyze")

if analyze_button:
    with st.spinner("Get data..."):
        df = yf.download(stock_code, period="max")

    if df.shape[0] == 0 or df.shape[1] < 6:
        st.error(f"No data found for {stock_code}.")

    with st.spinner("Calculating patterns..."):
        df.ta.cdl_pattern(name="all", append=True)

    results = pd.DataFrame(columns = ['Pattern', 'Trade Count', 'Win', 'Loss', 'Win Rate', 'Min Return %', 'Max Return %', 'Avg Return %'])
    with st.spinner("Backtesting..."):
        for pattern in df.columns[7:]:
            hold = False
            trade_count = 0
            win = 0
            loss = 0
            pct_returns = []
            for i in range(len(df.index)-1):
                try:
                    if not hold and df[pattern][i] == 100.0:
                        entry = df['Open'][i+1]
                        hold = True
                        sl_price = entry * (1 - stoploss)
                        tp_price = entry * (1 + takeprofit)
                    elif hold and df['High'][i+1] >= tp_price:
                        trade_count += 1
                        win += 1
                        hold = False
                        pct_returns.append((tp_price - entry) / entry)
                    elif hold and df['Low'][i+1] <= sl_price:
                        trade_count += 1
                        loss += 1
                        hold = False
                        pct_returns.append((sl_price - entry) / entry)
                except:
                    pass
            if trade_count > 0:
                results = results.append({'Pattern': pattern, 'Trade Count': trade_count, 'Win': win, 'Loss': loss, 'Win Rate': win/trade_count, 'Avg Return %': np.mean(pct_returns)}, ignore_index=True)
    with st.spinner("Cleaning results..."):
        results = results[results['Trade Count'] > 1]
        results['Pattern'] = results['Pattern'].apply(lambda x: candlestickNames[x])
        results = results.sort_values(by=['Avg Return %'], ascending=False)
        results = results.reset_index(drop=True)
        results = results.round(3)
        results = results[['Pattern', 'Trade Count', 'Win', 'Loss', 'Win Rate', 'Avg Return %']]

    st.dataframe(results, use_container_width=True, hide_index=True)
