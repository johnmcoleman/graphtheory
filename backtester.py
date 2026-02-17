"""
Backtesting engine with transaction costs, slippage, and performance analytics.

Uses a standard returns-based approach:
    strategy_return[t] = position[t-1] * asset_return[t] - costs[t]

This avoids lookahead bias (position is lagged one bar) and cleanly
accounts for transaction costs on every position change.
"""

import pandas as pd
import numpy as np


class BacktestEngine:
    def __init__(
        self,
        initial_capital: float = 100_000,
        commission_bps: float = 10,
        slippage_bps: float = 5,
    ):
        self.initial_capital = initial_capital
        self.commission = commission_bps / 10_000
        self.slippage = slippage_bps / 10_000
        self.trades_df: pd.DataFrame = pd.DataFrame()

    def run(self, data: pd.DataFrame) -> pd.DataFrame:
        """Run backtest. *data* must contain 'Close' and 'signal' columns."""
        df = data.copy()
        close = df["Close"]
        signal = df["signal"]

        asset_ret = close.pct_change().fillna(0)

        # Position held during bar t is the signal from bar t-1
        position = signal.shift(1).fillna(0)

        # Transaction cost every time position changes
        turnover = position.diff().fillna(0).abs()
        cost = turnover * (self.commission + self.slippage)

        strat_ret = position * asset_ret - cost

        df["position"] = position
        df["returns"] = strat_ret
        df["portfolio_value"] = self.initial_capital * (1 + strat_ret).cumprod()

        # Buy-and-hold benchmark
        df["bh_value"] = self.initial_capital * (1 + asset_ret).cumprod()

        # Drawdown
        peak = df["portfolio_value"].cummax()
        df["drawdown"] = (df["portfolio_value"] - peak) / peak

        # Extract individual round-trip trades
        self.trades_df = self._extract_trades(df)

        return df

    # ------------------------------------------------------------------
    # Trade extraction
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_trades(df: pd.DataFrame) -> pd.DataFrame:
        close = df["Close"]
        signal = df["signal"]
        changes = signal.diff().fillna(signal)
        events = changes[changes != 0]

        trades: list[dict] = []
        entry: dict | None = None

        for idx, _ in events.items():
            new_sig = signal.loc[idx]
            if entry is not None:
                ep = close.loc[entry["date"]]
                xp = close.loc[idx]
                d = entry["dir"]
                ret = d * (xp / ep - 1)
                trades.append(
                    {
                        "Entry Date": entry["date"],
                        "Exit Date": idx,
                        "Direction": "LONG" if d == 1 else "SHORT",
                        "Entry Price": round(ep, 4),
                        "Exit Price": round(xp, 4),
                        "Return %": round(ret * 100, 2),
                    }
                )
                entry = None
            if new_sig != 0:
                entry = {"date": idx, "dir": new_sig}

        return pd.DataFrame(trades)

    # ------------------------------------------------------------------
    # Performance metrics
    # ------------------------------------------------------------------
    def metrics(self, df: pd.DataFrame) -> dict:
        ret = df["returns"].dropna()
        pv = df["portfolio_value"]

        total_ret = pv.iloc[-1] / self.initial_capital - 1
        n_days = len(ret)
        ann = 252 / max(n_days, 1)
        ann_ret = (1 + total_ret) ** ann - 1
        ann_vol = ret.std() * np.sqrt(252)

        sharpe = ann_ret / ann_vol if ann_vol > 0 else 0.0

        down = ret[ret < 0]
        down_vol = down.std() * np.sqrt(252) if len(down) > 0 else 0.0
        sortino = ann_ret / down_vol if down_vol > 0 else 0.0

        max_dd = df["drawdown"].min()
        calmar = ann_ret / abs(max_dd) if max_dd != 0 else 0.0

        win = (ret > 0).sum()
        lose = (ret < 0).sum()
        win_rate = win / (win + lose) if (win + lose) > 0 else 0.0

        gross_p = ret[ret > 0].sum()
        gross_l = abs(ret[ret < 0].sum())
        pf = gross_p / gross_l if gross_l > 0 else float("inf")

        bh_ret = df["bh_value"].iloc[-1] / self.initial_capital - 1

        return {
            "Total Return": f"{total_ret:.2%}",
            "Annualized Return": f"{ann_ret:.2%}",
            "Annualized Volatility": f"{ann_vol:.2%}",
            "Sharpe Ratio": f"{sharpe:.2f}",
            "Sortino Ratio": f"{sortino:.2f}",
            "Max Drawdown": f"{max_dd:.2%}",
            "Calmar Ratio": f"{calmar:.2f}",
            "Win Rate (daily)": f"{win_rate:.2%}",
            "Profit Factor": f"{pf:.2f}",
            "Total Trades": len(self.trades_df),
            "Buy & Hold Return": f"{bh_ret:.2%}",
            "Final Portfolio": f"${pv.iloc[-1]:,.2f}",
        }

    # ------------------------------------------------------------------
    # Monthly returns (for heatmap)
    # ------------------------------------------------------------------
    @staticmethod
    def monthly_returns(df: pd.DataFrame) -> pd.DataFrame:
        monthly = df["returns"].resample("ME").apply(lambda x: (1 + x).prod() - 1)
        tbl = pd.DataFrame(
            {"Year": monthly.index.year, "Month": monthly.index.month, "Return": monthly.values}
        )
        pivot = tbl.pivot_table(values="Return", index="Year", columns="Month", aggfunc="first")
        pivot.columns = [
            "Jan", "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
        ]
        return pivot
