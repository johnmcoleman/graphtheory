"""
Trading strategies used by leading quantitative firms.

Each strategy generates a signal series: +1 (long), -1 (short), 0 (flat).
Signals at time t use only data available up to time t (no lookahead bias).
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from scipy import stats


# ---------------------------------------------------------------------------
# Base
# ---------------------------------------------------------------------------

class Strategy(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame, **params) -> pd.DataFrame:
        """Return a copy of *data* with at least a 'signal' column added."""

    @staticmethod
    def get_default_params() -> dict:
        return {}


# ---------------------------------------------------------------------------
# 1. Mean Reversion (Ornstein-Uhlenbeck z-score)
# ---------------------------------------------------------------------------

class MeanReversion(Strategy):
    name = "Mean Reversion (OU Process)"
    description = (
        "Ornstein-Uhlenbeck z-score mean reversion — the bread and butter "
        "of energy trading desks at Citadel, Two Sigma, and DE Shaw. "
        "Enters when price deviates >N\u03c3 from rolling mean, exits at reversion."
    )

    @staticmethod
    def get_default_params() -> dict:
        return {"lookback": 60, "entry_z": 2.0, "exit_z": 0.5}

    def generate_signals(self, data: pd.DataFrame, **params) -> pd.DataFrame:
        lb = params.get("lookback", 60)
        entry_z = params.get("entry_z", 2.0)
        exit_z = params.get("exit_z", 0.5)

        df = data.copy()
        prices = df["Close"]
        roll_mean = prices.rolling(lb).mean()
        roll_std = prices.rolling(lb).std()
        z = (prices - roll_mean) / roll_std

        position = 0
        signals = []
        for val in z:
            if np.isnan(val):
                signals.append(0)
                continue
            if position == 0:
                if val < -entry_z:
                    position = 1
                elif val > entry_z:
                    position = -1
            elif position == 1 and val > -exit_z:
                position = 0
            elif position == -1 and val < exit_z:
                position = 0
            signals.append(position)

        df["signal"] = signals
        df["z_score"] = z
        return df


# ---------------------------------------------------------------------------
# 2. Dual Momentum (Absolute + Relative with ADX filter)
# ---------------------------------------------------------------------------

class DualMomentum(Strategy):
    name = "Dual Momentum"
    description = (
        "Absolute + relative momentum with ADX trend-strength filter — "
        "the framework behind AQR, Man AHL, and Winton. Only enters when "
        "both time-series momentum and trend conviction align."
    )

    @staticmethod
    def get_default_params() -> dict:
        return {
            "fast_period": 12,
            "slow_period": 26,
            "signal_period": 9,
            "adx_period": 14,
            "adx_threshold": 25,
        }

    def generate_signals(self, data: pd.DataFrame, **params) -> pd.DataFrame:
        fast = params.get("fast_period", 12)
        slow = params.get("slow_period", 26)
        sig_p = params.get("signal_period", 9)
        adx_p = params.get("adx_period", 14)
        adx_thresh = params.get("adx_threshold", 25)

        df = data.copy()
        close = df["Close"]
        high = df["High"]
        low = df["Low"]

        # MACD
        ema_f = close.ewm(span=fast, adjust=False).mean()
        ema_s = close.ewm(span=slow, adjust=False).mean()
        macd_hist = (ema_f - ema_s) - (ema_f - ema_s).ewm(span=sig_p, adjust=False).mean()

        # ADX
        plus_dm = high.diff().clip(lower=0)
        minus_dm = (-low.diff()).clip(lower=0)
        tr = pd.concat(
            [high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()],
            axis=1,
        ).max(axis=1)
        atr = tr.rolling(adx_p).mean()
        plus_di = 100 * plus_dm.rolling(adx_p).mean() / atr
        minus_di = 100 * minus_dm.rolling(adx_p).mean() / atr
        dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
        adx = dx.rolling(adx_p).mean()

        # Absolute momentum
        abs_mom = close.pct_change(slow)

        df["signal"] = 0
        df.loc[(macd_hist > 0) & (adx > adx_thresh) & (abs_mom > 0), "signal"] = 1
        df.loc[(macd_hist < 0) & (adx > adx_thresh) & (abs_mom < 0), "signal"] = -1

        df["macd_hist"] = macd_hist
        df["adx"] = adx
        return df


# ---------------------------------------------------------------------------
# 3. Kalman Filter Dynamic Trend
# ---------------------------------------------------------------------------

class KalmanFilterTrend(Strategy):
    name = "Kalman Filter Trend"
    description = (
        "Adaptive trend estimation via Kalman filtering — inspired by "
        "Renaissance Technologies and Bridgewater. Separates signal from "
        "noise in real time; trades when filtered trend exceeds threshold."
    )

    @staticmethod
    def get_default_params() -> dict:
        return {
            "observation_noise": 1.0,
            "process_noise": 0.01,
            "trend_threshold": 0.001,
        }

    def generate_signals(self, data: pd.DataFrame, **params) -> pd.DataFrame:
        obs_noise = params.get("observation_noise", 1.0)
        proc_noise = params.get("process_noise", 0.01)
        threshold = params.get("trend_threshold", 0.001)

        df = data.copy()
        prices = df["Close"].values
        n = len(prices)

        # State: [level, trend]
        F = np.array([[1.0, 1.0], [0.0, 1.0]])
        H = np.array([[1.0, 0.0]])
        Q = np.array([[proc_noise, 0.0], [0.0, proc_noise * 0.1]])
        R = np.array([[obs_noise]])

        state = np.array([prices[0], 0.0])
        P = np.eye(2)

        levels = np.zeros(n)
        trends = np.zeros(n)

        for i in range(n):
            # Predict
            state_pred = F @ state
            P_pred = F @ P @ F.T + Q
            # Update
            innovation = prices[i] - H @ state_pred
            S = H @ P_pred @ H.T + R
            K = P_pred @ H.T @ np.linalg.inv(S)
            state = state_pred + K.flatten() * innovation.flatten()[0]
            P = (np.eye(2) - K @ H) @ P_pred

            levels[i] = state[0]
            trends[i] = state[1]

        df["kalman_level"] = levels
        df["kalman_trend"] = trends

        max_trend = np.nanmax(np.abs(trends))
        normed = trends / max_trend if max_trend > 0 else trends

        df["signal"] = 0
        df.loc[normed > threshold, "signal"] = 1
        df.loc[normed < -threshold, "signal"] = -1

        return df


# ---------------------------------------------------------------------------
# 4. Bollinger / Keltner Volatility Squeeze Breakout
# ---------------------------------------------------------------------------

class VolatilitySqueeze(Strategy):
    name = "Volatility Squeeze Breakout"
    description = (
        "Bollinger Band squeeze + Keltner Channel breakout — used by "
        "Jump Trading and Optiver for volatility-regime detection. "
        "Energy markets exhibit strong vol clustering, making this ideal."
    )

    @staticmethod
    def get_default_params() -> dict:
        return {
            "bb_period": 20,
            "bb_std": 2.0,
            "kc_period": 20,
            "kc_mult": 1.5,
            "momentum_period": 12,
        }

    def generate_signals(self, data: pd.DataFrame, **params) -> pd.DataFrame:
        bb_p = params.get("bb_period", 20)
        bb_s = params.get("bb_std", 2.0)
        kc_p = params.get("kc_period", 20)
        kc_m = params.get("kc_mult", 1.5)
        mom_p = params.get("momentum_period", 12)

        df = data.copy()
        close = df["Close"]
        high = df["High"]
        low = df["Low"]

        # Bollinger Bands
        bb_mid = close.rolling(bb_p).mean()
        bb_std_val = close.rolling(bb_p).std()
        bb_upper = bb_mid + bb_s * bb_std_val
        bb_lower = bb_mid - bb_s * bb_std_val

        # Keltner Channels
        tr = pd.concat(
            [high - low, (high - close.shift(1)).abs(), (low - close.shift(1)).abs()],
            axis=1,
        ).max(axis=1)
        atr = tr.rolling(kc_p).mean()
        kc_mid = close.rolling(kc_p).mean()
        kc_upper = kc_mid + kc_m * atr
        kc_lower = kc_mid - kc_m * atr

        squeeze = (bb_lower > kc_lower) & (bb_upper < kc_upper)
        momentum = close - close.shift(mom_p)

        squeeze_release = squeeze.shift(1).fillna(False) & ~squeeze

        df["signal"] = 0
        df.loc[squeeze_release & (momentum > 0), "signal"] = 1
        df.loc[squeeze_release & (momentum < 0), "signal"] = -1
        # Hold until next squeeze
        df["signal"] = df["signal"].replace(0, np.nan).ffill().fillna(0).astype(int)
        df.loc[squeeze, "signal"] = 0

        df["squeeze"] = squeeze.astype(int)
        df["momentum"] = momentum
        return df


# ---------------------------------------------------------------------------
# 5. Cointegration-Based Pairs / Spread Trading
# ---------------------------------------------------------------------------

class PairsTrading(Strategy):
    name = "Pairs Trading (Spread)"
    description = (
        "Cointegration-based spread trading — the core of energy relative-value "
        "desks at Millennium, Citadel, and Point72. Trades the mean-reverting "
        "spread between two cointegrated energy commodities."
    )

    @staticmethod
    def get_default_params() -> dict:
        return {
            "lookback": 60,
            "entry_z": 2.0,
            "exit_z": 0.5,
            "hedge_ratio_window": 60,
        }

    def generate_signals(
        self, data: pd.DataFrame, data2: pd.DataFrame | None = None, **params
    ) -> pd.DataFrame:
        lb = params.get("lookback", 60)
        entry_z = params.get("entry_z", 2.0)
        exit_z = params.get("exit_z", 0.5)
        hr_win = params.get("hedge_ratio_window", 60)

        df = data.copy()

        if data2 is None:
            return MeanReversion().generate_signals(data, **params)

        p1 = df["Close"]
        p2 = data2["Close"]

        # Rolling hedge ratio via OLS
        hedge_ratios = pd.Series(np.nan, index=df.index)
        for i in range(hr_win, len(p1)):
            y = p1.iloc[i - hr_win : i].values
            x = p2.iloc[i - hr_win : i].values
            slope = stats.linregress(x, y).slope
            hedge_ratios.iloc[i] = slope

        spread = p1 - hedge_ratios * p2
        spread_mean = spread.rolling(lb).mean()
        spread_std = spread.rolling(lb).std()
        z = (spread - spread_mean) / spread_std

        position = 0
        signals = []
        for val in z:
            if np.isnan(val):
                signals.append(0)
                continue
            if position == 0:
                if val < -entry_z:
                    position = 1
                elif val > entry_z:
                    position = -1
            elif position == 1 and val > -exit_z:
                position = 0
            elif position == -1 and val < exit_z:
                position = 0
            signals.append(position)

        df["signal"] = signals
        df["spread"] = spread
        df["z_score"] = z
        df["hedge_ratio"] = hedge_ratios
        return df


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

STRATEGIES: dict[str, Strategy] = {
    s.name: s
    for s in [
        MeanReversion(),
        DualMomentum(),
        KalmanFilterTrend(),
        VolatilitySqueeze(),
        PairsTrading(),
    ]
}
