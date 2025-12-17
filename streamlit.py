import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from stat386stonks import clean_prices, fit_next_return_models


st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Stock Dashboard")

@st.cache_data
def load_and_clean_data():
    # Use raw input -> clean via package (best demonstration)
    df_raw = pd.read_csv("data/weekly_5yr_all_symbols.csv")
    df = clean_prices(df_raw)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_and_clean_data()

# Sidebar controls
st.sidebar.header("Controls")

tickers = st.sidebar.multiselect(
    "Select stocks",
    sorted(df["Symbol"].unique()),
    default=[sorted(df["Symbol"].unique())[0]]
)

metric = st.sidebar.radio(
    "Metric",
    ["Adjusted Close", "% Change"]
)

top_n = st.sidebar.slider("Number of Stocks to Display in Table", 1, 7, 5)

table_options = ["Performance", "Volatility", "Mean Weekly % Increase"]
selected_table = st.sidebar.selectbox("Select Table to View", table_options)

# Optional: run models on demand
if st.sidebar.button("Run Return Models"):
    with st.spinner("Fitting models..."):
        results = fit_next_return_models(df)
    st.subheader("📉 Model Results (Next-Period Return Prediction)")
    st.dataframe(results)

# Filter data for selected stocks
df_filtered = df[df["Symbol"].isin(tickers)]

# Plot line chart
fig, ax = plt.subplots(figsize=(12, 6))

if tickers:
    for symbol in df_filtered["Symbol"].unique():
        stock_data = df_filtered[df_filtered["Symbol"] == symbol]
        if metric == "Adjusted Close":
            ax.plot(stock_data["Date"], stock_data["adjusted close"], label=symbol)
            ylabel = "Adjusted Close"
        else:
            ax.plot(stock_data["Date"], stock_data["Pct_Change"], label=symbol)
            ylabel = "% Change"
    ax.legend()
else:
    ylabel = ""

ax.set_xlabel("Date")
ax.set_ylabel(ylabel)
plt.xticks(rotation=45)
st.pyplot(fig)

# Summary stats (built from engineered features created by clean_prices)
df = df.sort_values(["Symbol", "Date"])
df["Weekly_Pct_Increase"] = df.groupby("Symbol")["adjusted close"].pct_change()

performance = df.groupby("Symbol")["Pct_Change"].last().sort_values(ascending=False)
volatility = df.groupby("Symbol")["Close_diff"].std().sort_values(ascending=False)
avg_weekly_pct = df.groupby("Symbol")["Weekly_Pct_Increase"].mean().sort_values(ascending=False)

performance_top = performance.head(top_n)
volatility_top = volatility.head(top_n)
avg_weekly_pct_top = avg_weekly_pct.head(top_n)

st.header("📈 Stock Summary Table")
if selected_table == "Performance":
    st.dataframe(performance_top.rename("Most Recent % Change"))
elif selected_table == "Volatility":
    st.dataframe(volatility_top.rename("Std of Weekly Price Changes"))
else:
    st.dataframe((avg_weekly_pct_top * 100).round(2).rename("Avg Weekly % Increase"))