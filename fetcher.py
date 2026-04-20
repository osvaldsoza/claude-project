import yfinance as yf
import pandas as pd
import streamlit as st

TICKERS = {
    "PETR4": "PETR4.SA",
    "ITUB4": "ITUB4.SA",
    "VALE3": "VALE3.SA",
}

START = "2025-01-01"
END = "2025-12-31"


@st.cache_data(ttl=3600)
def load_data() -> dict[str, pd.DataFrame]:
    result = {}
    for name, ticker in TICKERS.items():
        df = yf.download(ticker, start=START, end=END, auto_adjust=True, progress=False)
        if not df.empty:
            df.index = pd.to_datetime(df.index)
            result[name] = df[["Close", "Volume"]].copy()
    return result
