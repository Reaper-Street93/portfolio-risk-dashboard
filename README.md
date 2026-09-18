# Portfolio Risk Dashboard

A small web dashboard I built to get hands-on with portfolio risk analysis in Python. You pick some stocks from a dropdown and it shows how they've performed, how they move together, and how risky they are, all updating live as you change the selection.

## What it shows

- **Cumulative returns:** how much each stock would have grown (or shrunk) since the start of the period.
- **Correlation heatmap:** which stocks tend to move together. Red means they move in the same direction, blue means opposite.
- **Risk metrics table:** for each stock, the annualized return, annualized volatility, Sharpe ratio (return per unit of risk) and 95% Value at Risk.
- **Return distribution & VaR:** a histogram of daily returns for an equal-weighted portfolio of whatever you've selected, with a line marking the 95% VaR. That's roughly "on a bad day (worst 5%), you'd lose at least this much."

## The stocks

AAPL, MSFT, GOOGL, JPM, GS, NVDA, AMZN, BLK, META and TSLA.

**Heads up: the prices are made up.** `generate_data.py` simulates two years of daily prices (2024–2025) using a random walk, so the numbers look realistic but aren't real market data. The point was to build the analysis, not to make investment calls. Swapping in real prices would just mean replacing `portfolio_prices.csv` with a file in the same format.

## Built with

- **Python**
- **Dash**: the web framework that turns Python into an interactive page
- **Plotly**: the charts
- **pandas**: loading the data and calculating returns
- **NumPy**: the math (volatility, percentiles)

## Running it

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python generate_data.py   # creates portfolio_prices.csv (already included, so optional)
python app.py
```

Then open http://127.0.0.1:8050 in your browser.

## How the code is laid out

- `generate_data.py` creates the fake price data and saves it to `portfolio_prices.csv`.
- `app.py` is the dashboard. It loads the prices, works out daily and cumulative returns, lays out the page, and has one callback that redraws all four panels whenever you change the ticker selection.
