import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

def fit_next_return_models(df: pd.DataFrame, train_frac=0.8) -> pd.DataFrame:
    """
    For each symbol:
      ret = pct_change(adjusted close)
      next_ret = ret shifted -1
      vol_change = pct_change(volume)
    Fit LinearRegression: next_ret ~ ret + vol_change (time split).
    Returns per-symbol metrics + coefficients.
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    out = []

    for symbol, g in df.groupby("Symbol"):
        g = g.sort_values("Date").copy()
        g["ret"] = g["adjusted close"].pct_change()
        g["next_ret"] = g["ret"].shift(-1)
        g["vol_change"] = g["volume"].pct_change()
        g = g.dropna(subset=["ret", "next_ret", "vol_change"])
        if len(g) < 20:
            continue

        X = g[["ret", "vol_change"]]
        y = g["next_ret"]

        split = int(len(g) * train_frac)
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]

        model = LinearRegression()
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        out.append({
            "Symbol": symbol,
            "coef_ret": float(model.coef_[0]),
            "coef_vol_change": float(model.coef_[1]),
            "intercept": float(model.intercept_),
            "r2": float(r2_score(y_test, preds)),
            "mse": float(mean_squared_error(y_test, preds)),
            "n_obs": int(len(g)),
        })

    return pd.DataFrame(out).sort_values("r2", ascending=False)