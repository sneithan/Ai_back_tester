import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Offline AI Trading Bot (Backtest Mode)")

symbols = os.listdir("data")
symbol = st.sidebar.selectbox("Select Symbol", [s.replace(".csv", "") for s in symbols])
df = pd.read_csv(f"data/{symbol}.csv")
df["time"] = pd.to_datetime(df["time"])

st.line_chart(df.set_index("time")["close"])

# Mock predictions
df["signal"] = np.random.choice(["BUY", "SELL", "HOLD"], size=len(df))
df["entry_price"] = df["close"].where(df["signal"] != "HOLD")
df["pnl"] = (df["close"].diff().fillna(0) * np.where(df["signal"] == "BUY", 1, -1)).fillna(0)

equity = 10000 + df["pnl"].cumsum()
st.subheader("Equity Curve")
st.line_chart(equity)

st.subheader("Trade Log")
st.dataframe(df[["time", "signal", "close", "pnl"]].head(100))

csv = df.to_csv(index=False)
st.download_button("Download Trade Data", csv, "trades.csv", "text/csv")