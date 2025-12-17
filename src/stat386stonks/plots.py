import pandas as pd
import matplotlib.pyplot as plt

def plot_closing_prices(df: pd.DataFrame):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    for sym in df["Symbol"].unique():
        sub = df[df["Symbol"] == sym].sort_values("Date")
        plt.figure(figsize=(10, 4))
        plt.plot(sub["Date"], sub["adjusted close"])
        plt.title(f"Adjusted Close Over Time: {sym}")
        plt.ylabel("Adjusted Close")
        plt.tight_layout()
        plt.show()

def plot_all_pct_change(df: pd.DataFrame, symbols=None):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    if symbols is None:
        symbols = df["Symbol"].unique()

    plt.figure(figsize=(12, 6))
    for sym in symbols:
        sub = df[df["Symbol"] == sym].sort_values("Date")
        plt.plot(sub["Date"], sub["Pct_Change"], label=sym)

    plt.title("Percent Change (from first date)")
    plt.ylabel("Pct Change")
    plt.legend()
    plt.tight_layout()
    plt.show()

def compare_two(symbol1: str, symbol2: str, df: pd.DataFrame):
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    s1 = df[df["Symbol"] == symbol1].sort_values("Date")
    s2 = df[df["Symbol"] == symbol2].sort_values("Date")

    plt.figure(figsize=(12, 5))
    plt.plot(s1["Date"], s1["adjusted close"], label=symbol1)
    plt.plot(s2["Date"], s2["adjusted close"], label=symbol2)
    plt.title(f"{symbol1} vs {symbol2} — Adjusted Close")
    plt.xlabel("Date")
    plt.ylabel("Adjusted Close")
    plt.legend()
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 5))
    plt.plot(s1["Date"], s1["Pct_Change"], label=symbol1)
    plt.plot(s2["Date"], s2["Pct_Change"], label=symbol2)
    plt.title(f"{symbol1} vs {symbol2} — Percent Change")
    plt.xlabel("Date")
    plt.ylabel("Pct Change")
    plt.legend()
    plt.tight_layout()
    plt.show()