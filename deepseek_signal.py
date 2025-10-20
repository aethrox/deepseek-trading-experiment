import requests
import pandas as pd

# DeepSeek API Configuration
DEEPSEEK_API_KEY = "your_api_key_here"  # Buraya kendi key'ini yapıştır
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

def get_trading_signal(df):
    """
    Get last 24 hours of data and ask DeepSeek for trading signal
    """
    # Get last 24 candles (24 hours)
    recent_data = df.head(24)
    
    # Prepare data summary for DeepSeek
    current_price = float(recent_data.iloc[0]['close'])
    price_24h_ago = float(recent_data.iloc[-1]['close'])
    high_24h = float(recent_data['high'].max())
    low_24h = float(recent_data['low'].min())
    avg_volume = float(recent_data['volume'].mean())
    
    price_change = ((current_price - price_24h_ago) / price_24h_ago) * 100
    
    # Create prompt for DeepSeek
    prompt = f"""You are a crypto trading analyst. Based on the following BTC/USDT data from the last 24 hours, provide a trading signal.

Data:
- Current Price: ${current_price:,.2f}
- Price 24h ago: ${price_24h_ago:,.2f}
- Price Change 24h: {price_change:.2f}%
- 24h High: ${high_24h:,.2f}
- 24h Low: ${low_24h:,.2f}
- Average Volume: {avg_volume:.2f} BTC

Analyze the price action and momentum. Respond with ONLY one word:
- BUY (if bullish/uptrend)
- SELL (if bearish/downtrend)
- HOLD (if neutral/uncertain)

Your answer (one word only):"""

    # Send request to DeepSeek
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3  # Low temperature for consistent answers
    }
    
    response = requests.post(DEEPSEEK_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        signal_text = result['choices'][0]['message']['content'].strip().upper()
        
        # Convert to numeric signal
        if "BUY" in signal_text:
            signal = 1
        elif "SELL" in signal_text:
            signal = -1
        else:
            signal = 0
            
        return signal, signal_text, price_change
    else:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        return None, None, None

# Load data
df = pd.read_csv('btc_data.csv')

# Get signal
signal, signal_text, price_change = get_trading_signal(df)

if signal is not None:
    print("="*50)
    print("📊 DEEPSEEK TRADING SIGNAL")
    print("="*50)
    print(f"Signal: {signal_text}")
    print(f"Numeric: {signal} (1=BUY, 0=HOLD, -1=SELL)")
    print(f"24h Price Change: {price_change:.2f}%")
    print("="*50)