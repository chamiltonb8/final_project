import re
import pandas as pd

def _strip_leading_numbers(col: str) -> str:
    return re.sub(r"^\d+\.\s*", "", col)

def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names, types, sort order, and create engineered features.
    Adds:
      - Close_diff: per-symbol diff of close
      - Pct_Change: per-symbol % change from first adjusted close
    """
    df = df.copy()

    # normalize columns
    df.columns = [_strip_leading_numbers(c) for c in df.columns]

    # date + sort
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Symbol", "Date"]).reset_index(drop=True)

    # numeric conversions (keep only what you need)
    numeric_cols = ["open", "high", "low", "close", "adjusted close", "volume", "dividend amount"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # features
    df["Close_diff"] = df.groupby("Symbol")["close"].diff()
    df["Pct_Change"] = df.groupby("Symbol")["adjusted close"].transform(
        lambda x: (x / x.iloc[0] - 1) * 100
    )

    # reorder (if cols exist)
    front = [c for c in ["Symbol", "Date"] if c in df.columns]
    rest = [c for c in df.columns if c not in front]
    return df[front + rest]