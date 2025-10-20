# 🤖 DeepSeek Crypto Trading Bot

I built this trading bot to see if I could use AI (specifically DeepSeek LLM) to make trading decisions in the crypto market. Spoiler alert: it didn't work, but I learned a ton 📚

## ⚠️ Fair Warning

**Don't use this with real money** 💸❌ I tested three different strategies and they all lost money. This is a learning project, not a get-rich-quick scheme. The crypto market is way more complex than I initially thought.

## 💡 What This Project Is About

I wanted to experiment with combining AI language models and algorithmic trading. The idea was simple: fetch BTC price data from Bybit, ask DeepSeek to analyze it, and make buy/sell decisions based on its recommendations. Then backtest everything on historical data to see if it would've worked 🔍

### 📖 What I Actually Learned
- How to work with exchange APIs (Bybit in this case) 🔌
- Using LLMs for financial analysis (harder than it sounds) 🧠
- Building and running backtests 📊
- Working with financial data in Python 🐍
- Why most simple trading bots fail 💔

## 🛠️ Tech Stack

- Python 3.x 🐍
- Bybit API for market data 📈
- DeepSeek API for the AI part 🤖
- Pandas for data wrangling 🐼
- Basic HTTP requests 🌐

## 📁 Files in This Project

```
fetch_data.py          → Grabs BTC price history from Bybit 💰
deepseek_signal.py     → Asks DeepSeek for trading signals 🎯
backtest.py            → Tests the basic momentum strategy 📉
backtest_hybrid.py     → Tests technical indicators + AI combo 🔧
test_signal.py         → Quick tests to see what signals we get ⚡
btc_data.csv          → The historical data (auto-generated) 📄
```

## 🚀 How to Run This

### Install Dependencies
```bash
pip install requests pandas
```

### ⚙️ Setup

1. You don't need Bybit API keys for fetching data (public endpoint) ✅
2. Get a DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com) 🔑
3. Drop your API key into the scripts where it says:
   ```python
   DEEPSEEK_API_KEY = "your-api-key-here"
   ```

### 🏃 Running the Code

**Fetch data:**
```bash
python fetch_data.py
```

**Test if signals are working:**
```bash
python test_signal.py
```

**Run the full backtest:**
```bash
python backtest_hybrid.py
```

## 📊 The Strategies I Tried

### Round 1: Simple Momentum 🎢
**The idea:** If price goes up more than 2.5% in 24 hours, buy. If it drops more than 2.5%, sell.

**Result:** Lost 1.15% over 1000 hours 📉 Made literally 1 trade.

### Round 2: Let AI Do Everything 🤖
**The idea:** Give DeepSeek all the price data and let it figure out patterns.

**Result:** Lost 0.65% 📉 Still only 1 trade. AI was way too cautious.

### Round 3: Hybrid Approach ⚡
**The idea:** Use actual technical indicators (RSI, moving averages, volume) and have DeepSeek confirm the signals.

**Result:** Lost 3.95% 💀 Worst performance yet. 0% win rate.

## 🤔 Why Everything Failed

### The Main Issues

1. **DeepSeek was too conservative** 🛑 - It basically said "HOLD" for everything. Even when I gave it clear rules, it barely pulled the trigger.

2. **Crypto is chaotic** 🌪️ - BTC dropped 3% over the test period and the bot just couldn't adapt fast enough.

3. **My prompts weren't good enough** 📝 - Getting an LLM to consistently make good trading decisions is really hard.

4. **Not enough trades** ⏸️ - 1-2 trades over 1000 hours means the strategy is way too picky.

### 💭 What I Realized

Real trading bots that actually make money need:
- Way more sophisticated algorithms 🧮
- High-frequency trading capabilities ⚡
- Proper risk management 🛡️
- Years of development and testing ⏳
- A lot more computing power than my laptop 💻

LLMs are probably better for:
- Analyzing news sentiment 📰
- Summarizing market reports 📋
- Supporting decisions, not making them 🤝

And the biggest lesson: **always backtest before risking real money** 💯 Even then, past performance doesn't mean future success.

## 🔮 If I Were to Continue This

Some ideas I didn't try:
- **Copy trading** 👥 - Just follow people who actually know what they're doing
- **Grid bots** 🎯 - Buy low, sell high in a price range (works in sideways markets)
- **DCA bots** 💰 - Invest small amounts regularly over time
- **Sentiment analysis** 📊 - Use AI to read crypto Twitter instead of predicting prices
- **Multiple LLMs voting** 🗳️ - Get several AI opinions and average them out

## 🤝 Want to Use This?

Feel free to fork it and experiment 🍴 Just remember this didn't make money, so don't expect miracles. It's a learning project, not a money printer 🖨️❌

## 📄 License

MIT - Do whatever you want with this code ✅

## 🙏 Thanks

- Bybit for free API access 🎁
- DeepSeek for the LLM API 🤖
- Everyone who told me this wouldn't work (you were right) 😅

---

**Bottom line:** I set out to build a trading bot and ended up learning why that's really hard 🎓 The code works, the backtesting works, but the strategy doesn't. That's still valuable experience though - now I know what doesn't work and why 💡
