import os
import pandas as pd
from io_net_client import IOIntelligenceClient
from candle import get_klines

# Initialize IO Intelligence client
client = IOIntelligenceClient()

# Step 1: Fetch market data
pair = "IOUSDT"
df = get_klines(pair, interval="15m", compact=True)
if df.empty:
    print("❌ No market data fetched, check Binance API or internet.")
    exit()

print(f"📊 Latest {pair} market snapshot:")
print(df)

# Step 2: Prepare a summary for the AI
context = df.tail(5).to_string(index=False)
prompt = f"""
You are a professional crypto trading analyst.
Analyze the following  OHLC on 15m candle data for {pair}:

{context}

Explain if there is a BUY opportunity based on VWAP alignment and candle strength.
Be clear, concise, and mention risk or stop-loss if applicable.
"""

# Step 3: Ask the AI model
print("\n🤖 Asking AI for analysis...")
ai_response = client.chat(
    [{"role": "user", "content": prompt}],
    model="deepseek-ai/DeepSeek-R1-0528",
    temperature=0.6
)

# Step 4: Show the results
print("\n🧠 AI Analysis:")
print(ai_response)
