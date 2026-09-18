import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.bdate_range("2024-01-02", "2025-12-31")
tickers = ["AAPL", "MSFT", "GOOGL", "JPM", "GS", "NVDA", "AMZN", "BLK", "META", "TSLA"] 
start_prices = [150, 300, 2800, 160, 350, 200, 3300, 400, 250, 700]

data ={"Date": dates}
for ticker, start in zip(tickers, start_prices):
    # Random walk with drift (realistic daily returns)
    daily_returns = np.random.normal(0.0004, 0.018, len(dates))
    prices = [start]
    for r in daily_returns[1:]:
        prices = [start]
        for r in daily_returns[1:]:
            prices.append(round(prices[-1] * (1 + r), 2))
    data[ticker] = prices[:len(dates)]

df = pd.DataFrame(data)
df.to_csv("portfolio_prices.csv", index=False)
print(f"Created portfolio_prices.csv with {len(df)} rows and {len(tickers)} tickers")
print(df.head())
