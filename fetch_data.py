import requests
import pandas as pd
from datetime import datetime

# Bybit API endpoint (real market data, not testnet)
url = "https://api.bybit.com/v5/market/kline"

# Parameters
params = {
    "category": "linear",
    "symbol": "BTCUSDT",
    "interval": "60",
    "limit": 1000          # 200'den 1000'e çıkardık
}

# API request
response = requests.get(url, params=params)
data = response.json()

# Process data
if data['retCode'] == 0:
    candles = data['result']['list']
    
    # Create DataFrame
    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    
    # Convert timestamp to readable date
    df['date'] = pd.to_datetime(df['timestamp'].astype(int), unit='ms')
    
    # Arrange columns
    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    
    # Save to CSV
    df.to_csv('btc_data.csv', index=False)
    
    print("✅ Data fetched successfully!")
    print(f"📊 {len(df)} candles saved.")
    print(f"📅 Date range: {df['date'].min()} - {df['date'].max()}")
    print("\nFirst 5 rows:")
    print(df.head())
else:
    print("❌ Error:", data['retMsg'])