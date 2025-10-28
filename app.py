import streamlit as st
import plotly.graph_objects as go
from candle import get_klines
from io_net_client import IOIntelligenceClient
import pandas as pd
import time

# ------------------------------------------------------------
# ✅ Streamlit Page Setup
# ------------------------------------------------------------
st.set_page_config(page_title="AI Trading Dashboard", layout="wide", page_icon="📈")

st.title("🤖 IO.net Intelligence AI Trading Analyst ")
st.caption("Powered by IO.net Intelligence + VWAP strategy")

# ------------------------------------------------------------
# ✅ Load AI Models (from models.txt)
# ------------------------------------------------------------
try:
    with open("models.txt", "r", encoding="utf-8") as f:
        AI_MODELS = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    st.error("❌ models.txt not found. Please add your model list file.")
    st.stop()

# ------------------------------------------------------------
# ✅ User Inputs
# ------------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    pair = st.selectbox("Select Pair", ["BTCUSDT", "ETHUSDT", "IOUSDT", "BNBUSDT"])
with col2:
    interval = st.selectbox("Select Timeframe", ["5m", "15m", "1h", "4h"])
with col3:
    model = st.selectbox("🧠 Select AI Model", AI_MODELS, index=0)

st.divider()

# ------------------------------------------------------------
# ✅ Fetch and Display Market Data
# ------------------------------------------------------------
if st.button("📊 Fetch & Analyze"):
    with st.spinner("Fetching market data..."):
        df = get_klines(pair, interval=interval, compact=False)
        time.sleep(1)

    if df.empty:
        st.error("❌ No market data fetched. Check Binance connection or API limits.")
        st.stop()

    st.success(f"✅ Loaded {len(df)} candles for {pair} ({interval})")

    # Show last 10 rows
    st.subheader("Recent Market Snapshot")
    st.dataframe(df.tail(10), use_container_width=True)

    # --------------------------------------------------------
    # 📈 Candlestick + VWAP Chart
    # --------------------------------------------------------
    st.subheader("Market Visualization")

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df["time"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name="Candles"
    ))

    fig.add_trace(go.Scatter(
        x=df["time"],
        y=df["vwap"],
        mode="lines",
        line=dict(color="orange", width=2),
        name="VWAP"
    ))

    # Optional: Mark Buy Signals
    buy_signals = df[df["GO_LONG"] == True]
    if not buy_signals.empty:
        fig.add_trace(go.Scatter(
            x=buy_signals["time"],
            y=buy_signals["close"],
            mode="markers",
            marker=dict(color="green", size=10, symbol="triangle-up"),
            name="BUY Signal"
        ))

    fig.update_layout(
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        height=600,
        margin=dict(l=20, r=20, t=30, b=30)
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------------------------------
    # 🤖 AI Analysis
    # --------------------------------------------------------
    st.subheader("AI Trading Analysis")

    context = df.tail(5).to_string(index=False)
    prompt = f"""
    You are a professional crypto trading analyst.
    Analyze the following OHLC 15m candle data for {pair}:

    {context}

    Provide a clear analysis:
    - Is there a BUY opportunity based on VWAP alignment and candle strength?
    - Mention potential risk and stop-loss levels briefly.
    """

    st.info("Asking AI for analysis...")
    try:
        client = IOIntelligenceClient()
        ai_response = client.chat(
            [{"role": "user", "content": prompt}],
            model=model,
            temperature=0.6
        )
        st.success("🧠 AI Analysis Result")
        st.write(ai_response)
    except Exception as e:
        st.error(f"AI request failed: {e}")

# ------------------------------------------------------------
# 🕒 Footer
# ------------------------------------------------------------
st.divider()
st.caption("Built with ❤️ using Streamlit, Plotly, and IO.net Intelligence API.")
