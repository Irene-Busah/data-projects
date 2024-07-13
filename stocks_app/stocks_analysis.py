# Import packages
import pandas as pd
import streamlit as st
import yfinance as yf  # type: ignore
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import requests

st.write(
    """
    # Enhanced Stock Price App

    Shown are the stock **closing price**, **volume**, **technical indicators**, **news sentiment**, 
    **portfolio tracker**, and **price prediction**!
    """
)

# Sidebar for user input
st.sidebar.header("User Input")
tickerSymbol = st.sidebar.text_input("Enter Stock Ticker", "AAPL")

# Fetch data from Yahoo Finance
tickerData = yf.Ticker(tickerSymbol)
historical_data = tickerData.history(period="1d", start="2010-5-31", end="2024-5-31")

# Display Closing Price and Volume
st.write(f"## {tickerSymbol} Closing Price (in dollars)")
st.line_chart(historical_data.Close)

st.write(f"## {tickerSymbol} Volume")
st.line_chart(historical_data.Volume)

# Technical Indicators: SMA, EMA, RSI
historical_data["SMA50"] = historical_data["Close"].rolling(window=50).mean()
historical_data["SMA200"] = historical_data["Close"].rolling(window=200).mean()


def compute_rsi(data, window):
    diff = data.diff(1).dropna()
    gain = diff.where(diff > 0, 0)
    loss = -diff.where(diff < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


historical_data["RSI"] = compute_rsi(historical_data["Close"], 14)

st.write(f"## {tickerSymbol} Technical Indicators")
st.write("### Simple Moving Average (SMA)")
st.write(
    "SMA50 and SMA200 are the average of the closing prices over the last 50 and 200 days, respectively. They help in identifying the trend direction."
)
st.line_chart(historical_data[["Close", "SMA50", "SMA200"]])

st.write("### Relative Strength Index (RSI)")
st.write(
    "RSI measures the speed and change of price movements on a scale of 0 to 100. Values above 70 indicate overbought conditions, while values below 30 indicate oversold conditions."
)
st.line_chart(historical_data["RSI"])

# Stock Performance Comparison
st.sidebar.header("Stock Comparison")
stock_symbols = st.sidebar.text_input(
    "Enter stock symbols separated by commas", "AAPL, MSFT, GOOGL"
)
stock_list = [s.strip() for s in stock_symbols.split(",")]

st.write("## Stock Comparison")
for symbol in stock_list:
    data = yf.Ticker(symbol).history(period="1d", start="2010-5-31", end="2024-5-31")
    st.write(f"### {symbol} Closing Price (in dollars)")
    st.line_chart(data["Close"])

# News Sentiment Analysis
news_api_key = "b47bc228f4b94f4ea2e1a10be2ba0e0c"
news_api_url = (
    f"https://newsapi.org/v2/everything?q={tickerSymbol}&apiKey={news_api_key}"
)
news_data = requests.get(news_api_url).json()

# Display news sentiment
st.write("## News Sentiment")
if news_data["status"] == "ok":
    for article in news_data["articles"][:5]:
        st.markdown(f"### **{article['title']}**")
        st.markdown(f"{article['description']}")
        st.markdown(f"[Read more]({article['url']})")
        st.markdown("---")

# Portfolio Tracker
st.sidebar.header("Portfolio Tracker")
portfolio = st.sidebar.text_input(
    "Enter your portfolio (symbol:amount)",
    "AAPL:10, MSFT:5, GOOGL:2, AMZN:3, TSLA:4, NFLX:5, NVDA:7, JPM:9, WMT:11",
)
portfolio_list = [item.split(":") for item in portfolio.split(",")]

portfolio_df = pd.DataFrame(columns=["Symbol", "Amount"])

for item in portfolio_list:
    new_row = pd.DataFrame(
        {"Symbol": [item[0].strip()], "Amount": [int(item[1].strip())]}
    )
    portfolio_df = pd.concat([portfolio_df, new_row], ignore_index=True)

portfolio_df["Current Price"] = portfolio_df["Symbol"].apply(
    lambda x: yf.Ticker(x).history(period="1d").Close.iloc[-1]
)
portfolio_df["Total Value (in dollars)"] = (
    portfolio_df["Current Price"] * portfolio_df["Amount"]
)

st.write("## Portfolio Tracker")
st.write(portfolio_df)
st.bar_chart(portfolio_df.set_index("Symbol")["Total Value (in dollars)"])

# Prediction Models
data = historical_data[["Close"]].copy()
data["Prediction"] = data["Close"].shift(-30)

X = data.drop(["Prediction"], axis=1)[:-30]
y = data["Prediction"][:-30]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression().fit(X_train, y_train)
predictions = model.predict(data.drop(["Prediction"], axis=1)[-30:])

st.write("## Price Prediction")
st.write(
    "This chart shows the actual closing prices and the predicted closing prices for the next 30 days."
)
st.line_chart(data["Close"])
st.line_chart(predictions)

# Footer in Sidebar


st.sidebar.markdown(
    "<hr style='margin-top: 10px; margin-bottom: 10px;'>"
    "<div style='text-align: center; position: fixed; bottom: 0;'>"
    "<p>Stock Analysis App | July 2024 | Irene Busah</p>"
    "</div>",
    unsafe_allow_html=True,
)
