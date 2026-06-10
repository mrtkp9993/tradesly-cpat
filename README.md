# tradesly: Candlestick Pattern Backtesting
[Website](https://muratkoptur.com)

A Streamlit app that backtests the 60+ TA-Lib candlestick patterns with a simple take-profit / stop-loss strategy.

![Screenshot](/assets/res.png)

## Usage

### Local Python Installation

1. Install `ta-lib` with [these instructions](https://pypi.org/project/TA-Lib/)
2. ```git clone https://github.com/mrtkp9993/tradesly-cpat```
3. ```cd tradesly-cpat```
4. ```pip install -r requirements.txt```
5. ```streamlit run app.py```

### Docker

1. ```docker pull mrtkp9993/tradesly-cpat```
2. ```docker run -p 8501:8501 mrtkp9993/tradesly-cpat```

OR

1. ```git clone https://github.com/mrtkp9993/tradesly-cpat```
2. ```cd tradesly-cpat```
3. ```docker build -t tradesly-cpat .```
4. ```docker run -p 8501:8501 tradesly-cpat```
