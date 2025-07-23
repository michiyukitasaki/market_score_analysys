#!/usr/bin/env python
import yfinance as yf, pandas as pd, numpy as np
import datetime as dt

def market_score(date_str, symbol="1306.T"):
    close = yf.download(
        symbol, end=date_str, period="120d",
        progress=False, auto_adjust=True
    )["Close"].squeeze()

    ret5  = close.pct_change(5).iloc[-1]
    ma25  = close.rolling(25).mean().iloc[-1]
    dev25 = (close.iloc[-1] - ma25) / ma25

    delta = close.diff()
    up =  delta.clip(lower=0).rolling(14).mean()
    dn = (-delta.clip(upper=0)).rolling(14).mean()
    rsi14 = (100 - 100 / (1 + up / dn)).iloc[-1]

    return np.sign([ret5, dev25, rsi14 - 50]).sum()

# ------------ main ------------ #
target_day   = dt.date.today().strftime("%Y-%m-%d")
score_today  = market_score(target_day)

verdict = (
    "❗悪い地合い（逆張り向き）" if score_today <= -1 else
    "✅良い地合い（順張り向き）" if score_today >=  1 else
    "🤔中立"
)

print(
    f"{target_day} の market_score は {score_today}\n"
    f"判定 : {verdict}\n\n"
    "（−3 ↔ +3 の 7 段階 ／ ret5・25日乖離・RSI14 の符号合計）"
)
