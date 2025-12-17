import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

BASE_URL = "https://www.alphavantage.co/query"

def fetch_weekly_adjusted(
    symbols,
    api_key: str | None = None,
    start="2015-12-04",
    end="2020-12-04",
    pause_seconds=15,
    max_attempts=3,
):
    """
    Download Alpha Vantage weekly adjusted time series for multiple symbols.
    Returns a single combined DataFrame with columns including:
    Date, Symbol, open, high, low, close, adjusted close, volume, dividend amount, split coefficient (if present)
    """
    if api_key is None:
        load_dotenv()
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise ValueError("Missing ALPHAVANTAGE_API_KEY (pass api_key=... or set in .env)")

    all_frames = []
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)

    for symbol in symbols:
        params = {"function": "TIME_SERIES_WEEKLY_ADJUSTED", "symbol": symbol, "apikey": api_key}

        data = None
        for attempt in range(max_attempts):
            r = requests.get(BASE_URL, params=params, timeout=30)
            try:
                data = r.json()
                break
            except ValueError:
                time.sleep(pause_seconds)

        if not data or "Weekly Adjusted Time Series" not in data:
            # keep going, but don’t crash whole run
            continue

        df = pd.DataFrame(data["Weekly Adjusted Time Series"]).T
        df["Date"] = pd.to_datetime(df.index)
        df["Symbol"] = symbol
        df = df.sort_values("Date")
        df = df[df["Date"].between(start_ts, end_ts)]
        df.reset_index(drop=True, inplace=True)

        all_frames.append(df)
        time.sleep(pause_seconds)

    if not all_frames:
        return pd.DataFrame()

    return pd.concat(all_frames, ignore_index=True)