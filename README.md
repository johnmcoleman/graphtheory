# Energy Trading Bot

Quantitative backtesting platform for energy commodity strategies, built with Python and Streamlit.

## Strategies

| Strategy | Description |
|---|---|
| **Mean Reversion (OU Process)** | Ornstein-Uhlenbeck z-score mean reversion — staple of energy desks |
| **Dual Momentum** | Absolute + relative momentum with ADX trend filter — used by CTAs |
| **Kalman Filter Trend** | Adaptive trend estimation via Kalman filtering — RenTech-style |
| **Volatility Squeeze Breakout** | Bollinger/Keltner squeeze detection — vol-regime strategy |
| **Pairs Trading (Spread)** | Cointegration-based spread trading — energy relative value |

## Supported Commodities

Crude Oil (WTI), Natural Gas, Brent Crude, Heating Oil, RBOB Gasoline

## Quickstart

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features

- Interactive candlestick charts with buy/sell signal overlays
- Equity curve vs buy-and-hold benchmark
- Drawdown analysis and monthly returns heatmap
- Configurable transaction costs (commission + slippage in bps)
- Round-trip trade log with per-trade P&L
- Head-to-head strategy comparison across all five strategies
