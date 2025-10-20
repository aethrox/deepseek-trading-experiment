import pandas as pd
import requests

# DeepSeek API Configuration
DEEPSEEK_API_KEY = "your_api_key_here"  # Aynı key'i buraya da yapıştır
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def get_signal_for_window(window_data):
    """Get advanced trading signal with pattern analysis"""
    
    # Calculate metrics
    recent = window_data.head(6)  # Last 6 hours
    older = window_data.tail(6)   # 18-24 hours ago
    
    current_price = float(recent.iloc[0]['close'])
    price_24h_ago = float(window_data.iloc[-1]['close'])
    price_6h_ago = float(recent.iloc[-1]['close'])
    
    change_24h = ((current_price - price_24h_ago) / price_24h_ago) * 100
    change_6h = ((current_price - price_6h_ago) / price_6h_ago) * 100
    
    high_24h = float(window_data['high'].max())
    low_24h = float(window_data['low'].min())
    volatility = ((high_24h - low_24h) / low_24h) * 100
    
    # Volume analysis
    recent_vol = float(recent['volume'].mean())
    older_vol = float(older['volume'].mean())
    vol_change = ((recent_vol - older_vol) / older_vol) * 100 if older_vol > 0 else 0
    
    # Advanced prompt
    prompt = f"""Analyze BTC/USDT trading data:

PRICE ACTION:
- Current: ${current_price:,.0f}
- 6h change: {change_6h:+.2f}%
- 24h change: {change_24h:+.2f}%
- 24h range: ${low_24h:,.0f} - ${high_24h:,.0f}
- Volatility: {volatility:.2f}%

VOLUME:
- Recent 6h avg: {recent_vol:.1f} BTC
- Older period avg: {older_vol:.1f} BTC
- Volume change: {vol_change:+.1f}%

ANALYSIS TASK:
Look for patterns:
- Strong momentum with volume confirmation
- Support/resistance levels being tested
- Trend reversals

Reply with ONE word only:
- BUY: Strong bullish signal (momentum + volume)
- SELL: Strong bearish signal (breakdown + volume)
- HOLD: No clear pattern or mixed signals

Your decision:"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1  # Slightly increased for pattern recognition
    }
    
    try:
        response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            signal_text = result['choices'][0]['message']['content'].strip().upper()
            
            if "BUY" in signal_text:
                return 1
            elif "SELL" in signal_text:
                return -1
            else:
                return 0
        else:
            return 0
    except:
        return 0

def run_backtest():
    # Load data
    df = pd.read_csv('btc_data.csv')
    df = df.sort_values('date').reset_index(drop=True)  # Oldest first
    
    # Backtest settings
    initial_capital = 1000  # $1000 başlangıç
    capital = initial_capital
    position = 0  # 0 = no position, 1 = long (bought)
    entry_price = 0
    trades = []
    
    print("🔄 Starting backtest...")
    print(f"💰 Initial Capital: ${initial_capital}")
    print(f"📊 Testing on {len(df)} hours of data")
    print("-" * 60)
    
    # Start from hour 24 (need 24 hours of history for signal)
    for i in range(24, len(df)):
        # Get last 24 hours of data
        window = df.iloc[i-24:i]
        current_price = float(df.iloc[i]['close'])
        current_date = df.iloc[i]['date']
        
        # Get signal
        signal = get_signal_for_window(window)
        
        # Execute trades based on signal
        if signal == 1 and position == 0:  # BUY signal and no position
            position = 1
            entry_price = current_price
            print(f"🟢 BUY  @ ${current_price:,.2f} | {current_date}")
            
        elif signal == -1 and position == 1:  # SELL signal and have position
            exit_price = current_price
            profit = ((exit_price - entry_price) / entry_price) * capital
            capital += profit
            
            trades.append({
                'entry': entry_price,
                'exit': exit_price,
                'profit': profit,
                'return_%': ((exit_price - entry_price) / entry_price) * 100
            })
            
            print(f"🔴 SELL @ ${exit_price:,.2f} | {current_date} | P&L: ${profit:,.2f}")
            position = 0
    
    # Close position if still open
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
    print("📈 BACKTEST RESULTS")
    print("=" * 60)
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Capital: ${capital:,.2f}")
    print(f"Total Return: ${capital - initial_capital:,.2f} ({((capital/initial_capital - 1) * 100):.2f}%)")
    print(f"Number of Trades: {len(trades)}")
    
    if trades:
        trades_df = pd.DataFrame(trades)
        print(f"\nWinning Trades: {len(trades_df[trades_df['profit'] > 0])}")
        print(f"Losing Trades: {len(trades_df[trades_df['profit'] < 0])}")
        print(f"Average Profit per Trade: ${trades_df['profit'].mean():,.2f}")
        print(f"Best Trade: ${trades_df['profit'].max():,.2f}")
        print(f"Worst Trade: ${trades_df['profit'].min():,.2f}")
    
    print("=" * 60)

if __name__ == "__main__":
    run_backtest()