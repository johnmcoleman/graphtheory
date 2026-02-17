"""Data loading for energy commodities via Yahoo Finance."""

import pandas as pd
import yfinance as yf

ENERGY_TICKERS = {
    "Crude Oil (WTI)": "CL=F",
    "Natural Gas": "NG=F",
    "Brent Crude": "BZ=F",
    "Heating Oil": "HO=F",
    "RBOB Gasoline": "RB=F",
}


def fetch_energy_data(
    commodity: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """Fetch historical energy commodity data from Yahoo Finance."""
    ticker = ENERGY_TICKERS.get(commodity, commodity)
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if df.empty:
        raise ValueError(f"No data returned for {commodity} ({ticker})")
    # Flatten multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index = pd.to_datetime(df.index)
    return df


def fetch_pair_data(
    commodity_1: str,
    commodity_2: str,
    start_date: str,
    end_date: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fetch data for two commodities for pairs trading."""
    df1 = fetch_energy_data(commodity_1, start_date, end_date)
    df2 = fetch_energy_data(commodity_2, start_date, end_date)
    common_idx = df1.index.intersection(df2.index)
    return df1.loc[common_idx], df2.loc[common_idx]
