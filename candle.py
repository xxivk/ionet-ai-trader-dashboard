import os
import sys
import ccxt
import pandas as pd
from ta.volume import VolumeWeightedAveragePrice

# one binance client, rate-limited
ccxt_client = ccxt.binance({'enableRateLimit': True})

def _to_ccxt_symbol(sym: str) -> str:
    # "BTCUSDT" -> "BTC/USDT"
    return sym if "/" in sym else sym.replace("USDT", "/USDT")

def get_klines(pair: str, query: int = 1000, vwap_window: int =100,interval: str = "15m", compact: bool = False, tail_rows: int = 5) -> pd.DataFrame:
    try:
        symbol = _to_ccxt_symbol(pair)
        ohlcv = ccxt_client.fetch_ohlcv(symbol, timeframe=interval, limit=query)
        df = pd.DataFrame(ohlcv, columns=['timestamp','open','high','low','close','volume'])
        df = df.apply(pd.to_numeric)

        df['vwap'] = VolumeWeightedAveragePrice(
            high=df["high"], low=df['low'], close=df["close"], volume=df['volume'], window=vwap_window
        ).volume_weighted_average_price()

        for col in ['high','low','vwap']:
            df[f'{col}_s1'] = df[col].shift(1)
            df[f'{col}_s2'] = df[col].shift(2)
            df[f'{col}_s3'] = df[col].shift(3)

        df['color'] = df.apply(candle_color, axis=1)
        df['upper_wick'] = df.apply(upper_wick, axis=1)
        df['lower_wick'] = df.apply(lower_wick, axis=1)
        df['body'] = (df['open'] - df['close']).abs()
        df['strong'] = df.apply(strong_candle, axis=1)
        df['vwap_close_pct'] = (df['close'] - df['vwap']) / df['vwap'] * 100

        df['GO_LONG'] = df.apply(BUY_SIGNAL_CONDITION, axis=1)

        df['time'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)

        # full DF for the trading logic
        if not compact:
            return df

        # a small display view (safe for printing/logging)
        view_cols = ["time","close","vwap","vwap_close_pct","color","strong","GO_LONG"]
        view = df[view_cols].tail(tail_rows).copy()
        return view

    except Exception as e:
        print(f"Error fetching klines for {pair}: {e}")
        return pd.DataFrame()

# --- helpers unchanged ---
def candle_color(candle: pd.Series) -> str:
    if candle['close'] > candle['open']:
        return "GREEN"
    elif candle['close'] < candle['open']:
        return "RED"
    return "INDECISIVE"

def upper_wick(candle: pd.Series) -> float:
    return candle['high'] - max(candle['open'], candle['close'])

def lower_wick(candle: pd.Series) -> float:
    return min(candle['open'], candle['close']) - candle['low']

def strong_candle(candle: pd.Series) -> bool:
    if candle['color'] == "GREEN":
        return candle['close'] > candle['high_s1'] and candle['close'] > candle['high_s2']
    if candle['color'] == "RED":
        return candle['close'] < candle['low_s1'] and candle['close'] < candle['low_s2']
    return False

def BUY_SIGNAL_CONDITION(candle: pd.Series) -> bool:
    return (
        candle['vwap'] > 0 and
        candle['close'] > candle['vwap'] and
        0.25 <= candle['vwap_close_pct'] <= 1.50 and
        candle['color'] == "GREEN" and
        candle['strong']
    )

