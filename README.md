

```markdown
# 🤖 AI Crypto Trading Dashboard (Powered by IO.net Intelligence)

A real-time crypto market analytics dashboard that combines:
- **Live OHLCV data from Binance**
- **VWAP-based technical signal detection**
- **Multi-model LLM analysis from IO.net Intelligence**
- **Interactive trading visualization with Streamlit + Plotly**

This dashboard helps traders quickly evaluate market trends, identify potential entry signals, and receive AI-driven trade commentary in real time.

---

## 📸 Screenshots

### 🏠 Dashboard Overview
<img src="assets/dashboard.png" width="900">

### 📈 Candlestick + VWAP Buy Signal Chart
<img src="assets/chart.png" width="900">

### 🤖 AI Trading Analysis Panel
<img src="assets/analysis.png" width="900">

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 📈 Real-Time Candlestick Chart | Plotly-based market visualization |
| 🎯 VWAP Buy Signal Detection | Identifies momentum-based bullish entries |
| 🧠 Multi-Model AI Analysis | Choose from multiple IO.net-hosted LLMs |
| 🔄 Works With Any Cryptocurrency Pair | BTC, ETH, IO, BNB, and more |
| 🧩 Streamlit UI | Clean, fast and intuitive interface |
| 🔐 Local Key Security | `.env` file keeps your key private |

---

## 🧠 Supported AI Models

Supports any model available in your **IO.net Intelligence** account:

```

deepseek-ai/DeepSeek-R1-0528
meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8
Qwen/Qwen3-Next-80B-A3B-Instruct
mistralai/Mistral-Large-Instruct-2411
LLM360/K2-Think
... and more

````

Modify `models.txt` to add or remove models.

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-trading-dashboard.git
cd ai-trading-dashboard
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add your `.env` file

Create a `.env` file in the project directory:

```
IOINTELLIGENCE_API_KEY=your_io_intelligence_key_here
```

> **Do NOT expose or commit your `.env` file.**

### 4️⃣ Run the dashboard

```bash
streamlit run app.py
```

Open in your browser:

```
http://localhost:8501
```

---

## 📡 How It Works

```
Binance → OHLCV Data → VWAP + Candle Strength
                          ↓
                 AI Prompt Generator
                          ↓
           IO.net Intelligence Model
                          ↓
          AI Trading Insight & Interpretation
```

---

## 🎯 VWAP Strategy Logic

A **BUY** signal is triggered when:

* Price **closes above VWAP**
* Candle is **bullish and strong** relative to previous highs
* VWAP deviation is **between +0.25% and +1.50%**

This aims to capture **trend continuation momentum**.

---

## 🏗 Project Structure

```
├── app.py                 # Streamlit UI Dashboard
├── candle.py              # Market data + VWAP + signal logic
├── io_net_client.py       # IO Intelligence API wrapper
├── models.txt             # AI model list
├── assets/                # UI screenshots & media
├── requirements.txt
└── .env                   # Local API key (not committed)
```

---

## 🌍 Join the IO.net Community

| Platform       | Link                                                                                 |
| -------------- | ------------------------------------------------------------------------------------ |
| 💬 Discord     | [https://discord.com/invite/ionetofficial](https://discord.com/invite/ionetofficial) |
| 🐦 Twitter / X | [https://twitter.com/ionet](https://twitter.com/ionet)                               |
| 🌍 Telegram    | [http://t.me/io_net](http://t.me/io_net)                                             |

We share dashboards, experiments, GPU compute guides, and decentralized AI research.
Come build the future of open AI compute with us 🚀

---

## ⭐ Support the Project

If this project helped you:

* ⭐ Star the GitHub repository
* 🗣 Share your screenshots in the IO community
* 🔧 Contribute improvements or new strategies

---

### Built by **Saad** ❤️ for the **IO Community** 💛

```
