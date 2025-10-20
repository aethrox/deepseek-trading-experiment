import pandas as pd
import requests

# DeepSeek API Configuration
DEEPSEEK_API_KEY = "your_api_key_here"  # API key'ini buraya yapıştır
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    deltas = [prices[i] - prices[i+1] for i in range(len(prices)-1)]
    
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    if avg_loss == 0:
        return 50
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_hybrid_signal(window_data):
    """Get trading signal using technical indicators + DeepSeek confirmation"""
    
    # Convert to float
    closes = [float(x) for x in window_data['close'].tolist()]
    volumes = [float(x) for x in window_data['volume'].tolist()]
    
    current_price = closes[0]
    
    # 1. RSI Calculation (14 period)
    if len(closes) >= 14:
        rsi = calculate_rsi(closes[:14])
    else:
        rsi = 50  # Neutral
    
    # 2. Trend Analysis (SMA)
    sma_short = sum(closes[:6]) / 6   # 6-hour average
    sma_long = sum(closes[:24]) / 24  # 24-hour average
    trend = "BULLISH" if sma_short > sma_long else "BEARISH"
    
    # 3. Price momentum
    change_6h = ((current_price - closes[6]) / closes[6]) * 100
    change_24h = ((current_price - closes[-1]) / closes[-1]) * 100
    
    # 4. Volume trend
    vol_recent = sum(volumes[:6]) / 6
    vol_older = sum(volumes[6:12]) / 6
    vol_trend = "INCREASING" if vol_recent > vol_older else "DECREASING"
    
    # Create prompt for DeepSeek (confirmation only)
    prompt = f"""You are a trading signal validator. Review these technical indicators and confirm the trading decision.

TECHNICAL INDICATORS:
- RSI (14): {rsi:.1f} (Oversold<30, Neutral=30-70, Overbought>70)
- Trend: {trend} (6h SMA vs 24h SMA)
- 6h momentum: {change_6h:+.2f}%
- 24h momentum: {change_24h:+.2f}%
- Volume: {vol_trend}

TRADING RULES:
1. BUY if: RSI < 40 AND trend turning bullish AND volume increasing
2. SELL if: RSI > 60 AND trend turning bearish AND momentum negative
3. HOLD if: Mixed signals or unclear pattern

Based on these indicators, reply with ONE word only: BUY, SELL, or HOLD

Your decision:"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0
    }
    
    try:
        response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            signal_text = result['choices'][0]['message']['content'].strip().upper()
            
            if "BUY" in signal_text:
                return 1, rsi, trend
            elif "SELL" in signal_text:
                return -1, rsi, trend
            else:
                return 0, rsi, trend
        else:
            return 0, rsi, trend
    except:
        return 0, rsi, trend

def run_backtest():
    # Load data
    df = pd.read_csv('btc_data.csv')
    df = df.sort_values('date').reset_index(drop=True)  # Oldest first
    
    # Backtest settings
    initial_capital = 1000
    capital = initial_capital
    position = 0
    entry_price = 0
    trades = []
    
    print("🔄 Starting HYBRID backtest...")
    print(f"💰 Initial Capital: ${initial_capital}")
    print(f"📊 Testing on {len(df)} hours of data")
    print("-" * 60)
    
    # Start from hour 24
    for i in range(24, len(df)):
        window = df.iloc[i-24:i]
        current_price = float(df.iloc[i]['close'])
        current_date = df.iloc[i]['date']
        
        # Get hybrid signal
        signal, rsi, trend = get_hybrid_signal(window)
        
        # Execute trades
        if signal == 1 and position == 0:
            position = 1
            entry_price = current_price
            print(f"🟢 BUY  @ ${current_price:,.2f} | {current_date} | RSI:{rsi:.0f} {trend}")
            
        elif signal == -1 and position == 1:
            exit_price = current_price
            profit = ((exit_price - entry_price) / entry_price) * capital
            capital += profit
            
            trades.append({
                'entry': entry_price,
                'exit': exit_price,
                'profit': profit,
                'return_%': ((exit_price - entry_price) / entry_price) * 100
            })
            
            print(f"🔴 SELL @ ${exit_price:,.2f} | {current_date} | RSI:{rsi:.0f} | P&L: ${profit:,.2f}")
            position = 0
    
    # Close position if open
    if position == 1:
        exit_price = float(df.iloc[-1]['close'])
        profit = ((exit_price - entry_price) / entry_price) * capital
        capital += profit
        trades.append({
            'entry': entry_price,
            'exit': exit_price,
            'profit': profit,
            'return_%': ((exit_price - entry_price) / entry_price) * 100
        })
        print(f"🔴 SELL @ ${exit_price:,.2f} (Close at end) | P&L: ${profit:,.2f}")
    
    # Results
    print("\n" + "=" * 60)
    print("📈 HYBRID BACKTEST RESULTS")
    print("=" * 60)
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Capital: ${capital:,.2f}")
    print(f"Total Return: ${capital - initial_capital:,.2f} ({((capital/initial_capital - 1) * 100):.2f}%)")
    print(f"Number of Trades: {len(trades)}")
    
    if trades:
        trades_df = pd.DataFrame(trades)
        print(f"\nWinning Trades: {len(trades_df[trades_df['profit'] > 0])}")
        print(f"Losing Trades: {len(trades_df[trades_df['profit'] < 0])}")
        print(f"Win Rate: {(len(trades_df[trades_df['profit'] > 0]) / len(trades_df) * 100):.1f}%")
        print(f"Average Profit per Trade: ${trades_df['profit'].mean():,.2f}")
        print(f"Best Trade: ${trades_df['profit'].max():,.2f}")
        print(f"Worst Trade: ${trades_df['profit'].min():,.2f}")
    
    print("=" * 60)

if __name__ == "__main__":
    run_backtest()