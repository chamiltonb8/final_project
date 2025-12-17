import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📊 Stock Dashboard")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_weekly_stock_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar controls
st.sidebar.header("Controls")

tickers = st.sidebar.multiselect(
    "Select stocks",
    sorted(df["Symbol"].unique()),
    default=[df["Symbol"].unique()[0]]
)

metric = st.sidebar.radio(
    "Metric",
    ["Adjusted Close", "% Change"]
)

# Slider for number of top stocks in tables
top_n = st.sidebar.slider("Number of Stocks to Display in Table", 1, 7, 5)

# Dropdown to select which summary table to show
table_options = ["Performance", "Volatility", "Mean Weekly Diff"]
selected_table = st.sidebar.selectbox("Select Table to View", table_options)

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
    ylabel = ""  # show empty plot

ax.set_xlabel("Date")
ax.set_ylabel(ylabel)
plt.xticks(rotation=45)
st.pyplot(fig)

# Ensure correct ordering
df = df.sort_values(["Symbol", "Date"])

# Derived weekly % increase from adjusted close
df["Weekly_Pct_Increase"] = (
    df.groupby("Symbol")["adjusted close"]
      .pct_change()
)

# Compute summary statistics
performance = df.groupby('Symbol')['Pct_Change'].last().sort_values(ascending=False)
volatility = df.groupby('Symbol')['Close_diff'].std().sort_values(ascending=False)
avg_weekly_pct = df.groupby('Symbol')['Weekly_Pct_Increase'].mean().sort_values(ascending=False)

# Apply top_n filter
performance_top = performance.head(top_n)
volatility_top = volatility.head(top_n)
avg_weekly_pct_top = avg_weekly_pct.head(top_n)

# Show selected table
st.header("📈 Stock Summary Table")
if selected_table == "Performance":
    st.dataframe(performance_top.rename("Most Recent % Change"))
elif selected_table == "Volatility":
    st.dataframe(volatility_top.rename("Std of Weekly Price Changes"))
else:
    st.dataframe((avg_weekly_pct_top * 100).round(2).rename("Avg Weekly % Increase"))
