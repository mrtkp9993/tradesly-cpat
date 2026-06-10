import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import pandas_ta as ta
from candlestick_pat_names import replace_pattern_name

st.set_page_config(page_title="tradesly: Candlestick Pattern Backtesting", page_icon=":chart_with_upwards_trend:", layout="wide")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.header("tradesly: Candlestick Pattern Backtesting")

st.sidebar.divider()

# Get stock code
stock_code = st.sidebar.text_input("Enter stock code", value="AAPL")

# Get Period
period = st.sidebar.selectbox("Period", ["Daily", "Intra-day"], index=0)

# Stop loss percentage
stoploss = st.sidebar.slider("Stop Loss", min_value=0.0, max_value=1.0, value=0.05)

# Take profit percentage
takeprofit = st.sidebar.slider("Take Profit", min_value=0.0, max_value=1.0, value=0.1)

# Analyze button
analyze_button = st.sidebar.button("Analyze")

st.sidebar.divider()
st.sidebar.link_button("Website", "https://muratkoptur.com")

def backtest(signal, direction, opens, highs, lows):
    hold = False
    trade_count = win = loss = 0
    pct_returns = []
    entry = tp_price = sl_price = 0.0
    for i in range(len(signal) - 1):
        if not hold and signal[i]:
            entry = opens[i + 1]
            hold = True
            if direction == "long":
                tp_price = entry * (1 + takeprofit)
                sl_price = entry * (1 - stoploss)
            else:
                tp_price = entry * (1 - takeprofit)
                sl_price = entry * (1 + stoploss)
        elif hold:
            if direction == "long":
                hit_tp = highs[i + 1] >= tp_price
                hit_sl = lows[i + 1] <= sl_price
            else:
                hit_tp = lows[i + 1] <= tp_price
                hit_sl = highs[i + 1] >= sl_price
            if hit_tp:
                trade_count += 1
                win += 1
                hold = False
                pct_returns.append(takeprofit)
            elif hit_sl:
                trade_count += 1
                loss += 1
                hold = False
                pct_returns.append(-stoploss)

    if trade_count == 0:
        return None
    gross_win = win * takeprofit
    gross_loss = loss * stoploss
    total_return = float(np.prod([1 + r for r in pct_returns]) - 1)
    return {
        'Trade Count': trade_count,
        'Win': win,
        'Loss': loss,
        'Win Rate %': win / trade_count * 100,
        'Avg Return %': float(np.mean(pct_returns)) * 100,
        'Total Return %': total_return * 100,
        'Profit Factor': gross_win / gross_loss if gross_loss > 0 else np.inf,
    }


if analyze_button:
    with st.spinner("Get data..."):
        df = yf.download(stock_code, period="max" if period == 'Daily' else '2y',
                         interval="1d" if period == "Daily" else "1h",
                         auto_adjust=True, multi_level_index=False, progress=False)

    if df is None or df.empty:
        st.error(f"No data found for {stock_code}.")
        st.stop()

    with st.spinner("Calculating patterns..."):
        df.ta.cdl_pattern(name="all", append=True)

    pattern_cols = [c for c in df.columns if c.startswith("CDL")]
    opens = df['Open'].to_numpy()
    highs = df['High'].to_numpy()
    lows = df['Low'].to_numpy()

    results = []
    with st.spinner("Backtesting..."):
        for pattern in pattern_cols:
            values = df[pattern].to_numpy()
            bullish = backtest(values > 0, "long", opens, highs, lows)
            if bullish is not None:
                results.append({'Pattern': f"{pattern} (Bullish)", **bullish})
            bearish = backtest(values < 0, "short", opens, highs, lows)
            if bearish is not None:
                results.append({'Pattern': f"{pattern} (Bearish)", **bearish})

    results = pd.DataFrame(results)

    if results.empty:
        st.warning(f"No patterns produced any trades for {stock_code} with the chosen settings.")
        st.stop()

    with st.spinner("Cleaning results..."):
        results = results[results['Trade Count'] > 1]
        results = results[(results['Win Rate %'] > 0) & (results['Win Rate %'] < 100)]
        results['Pattern'] = results['Pattern'].apply(replace_pattern_name)
        results = results.sort_values(by=['Avg Return %'], ascending=False)
        results = results.reset_index(drop=True)
        results = results.round(3)
        results = results[['Pattern', 'Trade Count', 'Win', 'Loss', 'Win Rate %',
                           'Avg Return %', 'Total Return %', 'Profit Factor']]

    st.dataframe(results, width="stretch", hide_index=True)
