import pandas as pd
import requests

DEEPSEEK_API_KEY = "your_api_key_here"
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

df = pd.read_csv('btc_data.csv')

# Test 5 different time windows
for i in [30, 60, 90, 120, 150]:
    window = df.iloc[i-24:i]
    
    current_price = float(window.iloc[0]['close'])
    price_24h_ago = float(window.iloc[-1]['close'])
    price_change = ((current_price - price_24h_ago) / price_24h_ago) * 100
    
    prompt = f"""You are a momentum trader. BTC price changed {price_change:.2f}% in 24h.

RULES:
- If price UP > +1.5%: Reply BUY
- If price DOWN < -1.5%: Reply SELL  
- Otherwise: Reply HOLD

Current change: {price_change:.2f}%

Your decision (one word):"""

    response = requests.post(
        DEEPSEEK_URL,
        headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )
    
    if response.status_code == 200:
        signal = response.json()['choices'][0]['message']['content'].strip()
        print(f"Hour {i}: Price Change: {price_change:+.2f}% → Signal: {signal}")
    else:
        print(f"Hour {i}: API Error")