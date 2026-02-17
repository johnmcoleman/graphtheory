"""
Energy Trading Bot — Quantitative Backtesting Platform
=======================================================
Streamlit UI for backtesting quant-grade strategies on energy commodities.

Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_loader import ENERGY_TICKERS, fetch_energy_data, fetch_pair_data
from strategies import STRATEGIES
from backtester import BacktestEngine

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Energy Trading Bot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-card h3 {
        color: #94a3b8;
        font-size: 0.85rem;
        margin-bottom: 4px;
        font-weight: 500;
    }
    .metric-card p {
        font-size: 1.6rem;
        font-weight: 700;
        margin: 0;
    }
    .positive { color: #22c55e; }
    .negative { color: #ef4444; }
    .neutral  { color: #e2e8f0; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #16213e;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0f3460;
        color: #e2e8f0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif"),
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# ── Helpers ──────────────────────────────────────────────────────────────────

def _color(val_str: str) -> str:
    """Return CSS class based on sign of a formatted percentage / number."""
    try:
        num = float(val_str.replace("%", "").replace("$", "").replace(",", ""))
        if num > 0:
            return "positive"
        elif num < 0:
            return "negative"
    except ValueError:
        pass
    return "neutral"


def metric_card(label: str, value: str) -> str:
    css = _color(value)
    return (
        f'<div class="metric-card">'
        f'<h3>{label}</h3>'
        f'<p class="{css}">{value}</p>'
        f"</div>"
    )


# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("Configuration")

strategy_name = st.sidebar.selectbox("Strategy", list(STRATEGIES.keys()))
strategy = STRATEGIES[strategy_name]
st.sidebar.caption(strategy.description)

is_pairs = strategy_name == "Pairs Trading (Spread)"

commodity = st.sidebar.selectbox("Primary Commodity", list(ENERGY_TICKERS.keys()), index=0)
if is_pairs:
    commodity2 = st.sidebar.selectbox("Second Commodity", list(ENERGY_TICKERS.keys()), index=1)

col_d1, col_d2 = st.sidebar.columns(2)
start_date = col_d1.date_input("Start", value=pd.Timestamp("2020-01-01"))
end_date = col_d2.date_input("End", value=pd.Timestamp.today())

st.sidebar.markdown("---")
st.sidebar.subheader("Strategy Parameters")
defaults = strategy.get_default_params()
params: dict = {}
for k, v in defaults.items():
    label = k.replace("_", " ").title()
    if isinstance(v, int):
        params[k] = st.sidebar.slider(label, 2, 200, v)
    elif isinstance(v, float):
        params[k] = st.sidebar.slider(label, 0.001, 10.0, v, step=0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("Backtest Settings")
capital = st.sidebar.number_input("Initial Capital ($)", value=100_000, step=10_000)
comm = st.sidebar.slider("Commission (bps)", 0, 50, 10)
slip = st.sidebar.slider("Slippage (bps)", 0, 50, 5)

run_btn = st.sidebar.button("Run Backtest", type="primary", use_container_width=True)

# ── Title ────────────────────────────────────────────────────────────────────
st.title("Energy Trading Bot")
st.caption("Quantitative backtesting platform for energy commodity strategies")

if not run_btn:
    st.info("Configure your strategy in the sidebar and click **Run Backtest** to begin.")
    st.stop()

# ── Data loading ─────────────────────────────────────────────────────────────
with st.spinner("Fetching market data ..."):
    try:
        if is_pairs:
            data, data2 = fetch_pair_data(
                commodity, commodity2, str(start_date), str(end_date)
            )
        else:
            data = fetch_energy_data(commodity, str(start_date), str(end_date))
            data2 = None
    except Exception as e:
        st.error(f"Data fetch failed: {e}")
        st.stop()

# ── Signal generation ────────────────────────────────────────────────────────
with st.spinner("Generating signals ..."):
    if is_pairs:
        signals_df = strategy.generate_signals(data, data2=data2, **params)
    else:
        signals_df = strategy.generate_signals(data, **params)

# ── Backtest ─────────────────────────────────────────────────────────────────
engine = BacktestEngine(initial_capital=capital, commission_bps=comm, slippage_bps=slip)
results = engine.run(signals_df)
perf = engine.metrics(results)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_dash, tab_analysis, tab_trades, tab_compare = st.tabs(
    ["Dashboard", "Analysis", "Trade Log", "Strategy Comparison"]
)

# ── TAB 1: Dashboard ─────────────────────────────────────────────────────────
with tab_dash:
    # Key metrics row
    cols = st.columns(6)
    highlights = [
        ("Total Return", perf["Total Return"]),
        ("Sharpe Ratio", perf["Sharpe Ratio"]),
        ("Sortino Ratio", perf["Sortino Ratio"]),
        ("Max Drawdown", perf["Max Drawdown"]),
        ("Win Rate", perf["Win Rate (daily)"]),
        ("Final Portfolio", perf["Final Portfolio"]),
    ]
    for col, (lbl, val) in zip(cols, highlights):
        col.markdown(metric_card(lbl, val), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Price + signals chart
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.6, 0.4],
        subplot_titles=[f"{commodity} — Price & Signals", "Portfolio Value"],
    )

    fig.add_trace(
        go.Candlestick(
            x=results.index,
            open=results["Open"],
            high=results["High"],
            low=results["Low"],
            close=results["Close"],
            name="Price",
            increasing_line_color="#22c55e",
            decreasing_line_color="#ef4444",
        ),
        row=1,
        col=1,
    )

    # Entry / exit markers
    buys = results[results["signal"].diff().fillna(0) > 0]
    sells = results[results["signal"].diff().fillna(0) < 0]
    fig.add_trace(
        go.Scatter(
            x=buys.index,
            y=buys["Low"] * 0.995,
            mode="markers",
            marker=dict(symbol="triangle-up", size=10, color="#22c55e"),
            name="Buy Signal",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=sells.index,
            y=sells["High"] * 1.005,
            mode="markers",
            marker=dict(symbol="triangle-down", size=10, color="#ef4444"),
            name="Sell Signal",
        ),
        row=1,
        col=1,
    )

    # Equity curve
    fig.add_trace(
        go.Scatter(
            x=results.index,
            y=results["portfolio_value"],
            name="Strategy",
            line=dict(color="#3b82f6", width=2),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=results.index,
            y=results["bh_value"],
            name="Buy & Hold",
            line=dict(color="#64748b", width=1, dash="dot"),
        ),
        row=2,
        col=1,
    )

    fig.update_layout(**PLOTLY_LAYOUT, height=700, showlegend=True)
    fig.update_xaxes(rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# ── TAB 2: Analysis ──────────────────────────────────────────────────────────
with tab_analysis:
    col_a, col_b = st.columns(2)

    # Drawdown chart
    with col_a:
        st.subheader("Drawdown")
        fig_dd = go.Figure()
        fig_dd.add_trace(
            go.Scatter(
                x=results.index,
                y=results["drawdown"] * 100,
                fill="tozeroy",
                line=dict(color="#ef4444", width=1),
                fillcolor="rgba(239,68,68,0.25)",
                name="Drawdown %",
            )
        )
        fig_dd.update_layout(**PLOTLY_LAYOUT, height=350, yaxis_title="Drawdown %")
        st.plotly_chart(fig_dd, use_container_width=True)

    # Monthly returns heatmap
    with col_b:
        st.subheader("Monthly Returns")
        monthly = engine.monthly_returns(results)
        if not monthly.empty:
            fig_hm = go.Figure(
                go.Heatmap(
                    z=monthly.values * 100,
                    x=monthly.columns.tolist(),
                    y=monthly.index.astype(str).tolist(),
                    colorscale=[
                        [0, "#ef4444"],
                        [0.5, "#1e293b"],
                        [1, "#22c55e"],
                    ],
                    zmid=0,
                    text=np.where(
                        np.isnan(monthly.values),
                        "",
                        np.char.mod("%.1f%%", monthly.values * 100),
                    ),
                    texttemplate="%{text}",
                    hovertemplate="Year %{y}, %{x}: %{z:.2f}%<extra></extra>",
                    colorbar=dict(title="%"),
                )
            )
            fig_hm.update_layout(**PLOTLY_LAYOUT, height=350)
            st.plotly_chart(fig_hm, use_container_width=True)
        else:
            st.write("Not enough data for monthly breakdown.")

    # Full performance table
    st.subheader("Performance Summary")
    perf_df = pd.DataFrame(perf.items(), columns=["Metric", "Value"])
    st.dataframe(perf_df, use_container_width=True, hide_index=True)

# ── TAB 3: Trade Log ─────────────────────────────────────────────────────────
with tab_trades:
    st.subheader("Round-Trip Trades")
    if engine.trades_df.empty:
        st.info("No round-trip trades detected. Try adjusting strategy parameters or the date range.")
    else:
        st.dataframe(engine.trades_df, use_container_width=True, hide_index=True)
        wins = (engine.trades_df["Return %"] > 0).sum()
        total = len(engine.trades_df)
        avg_win = engine.trades_df.loc[engine.trades_df["Return %"] > 0, "Return %"].mean()
        avg_loss = engine.trades_df.loc[engine.trades_df["Return %"] <= 0, "Return %"].mean()
        c1, c2, c3 = st.columns(3)
        c1.metric("Trades", total)
        c2.metric("Avg Winner", f"{avg_win:.2f}%" if not np.isnan(avg_win) else "N/A")
        c3.metric("Avg Loser", f"{avg_loss:.2f}%" if not np.isnan(avg_loss) else "N/A")

# ── TAB 4: Strategy Comparison ───────────────────────────────────────────────
with tab_compare:
    st.subheader("Head-to-Head: All Strategies")
    st.caption("Runs every strategy on the same data with the same backtest settings.")

    if st.button("Run Comparison", type="primary"):
        comp_rows: list[dict] = []
        fig_comp = go.Figure()
        colors = ["#3b82f6", "#22c55e", "#f59e0b", "#ef4444", "#a855f7"]

        for idx, (sname, strat) in enumerate(STRATEGIES.items()):
            try:
                if sname == "Pairs Trading (Spread)" and data2 is not None:
                    sdf = strat.generate_signals(data.copy(), data2=data2, **strat.get_default_params())
                else:
                    sdf = strat.generate_signals(data.copy(), **strat.get_default_params())
                eng = BacktestEngine(initial_capital=capital, commission_bps=comm, slippage_bps=slip)
                res = eng.run(sdf)
                m = eng.metrics(res)
                m["Strategy"] = sname
                comp_rows.append(m)
                fig_comp.add_trace(
                    go.Scatter(
                        x=res.index,
                        y=res["portfolio_value"],
                        name=sname,
                        line=dict(color=colors[idx % len(colors)], width=2),
                    )
                )
            except Exception as exc:
                st.warning(f"{sname}: {exc}")

        # Buy & hold reference
        fig_comp.add_trace(
            go.Scatter(
                x=results.index,
                y=results["bh_value"],
                name="Buy & Hold",
                line=dict(color="#64748b", width=1, dash="dot"),
            )
        )
        fig_comp.update_layout(**PLOTLY_LAYOUT, height=500, title="Equity Curves")
        st.plotly_chart(fig_comp, use_container_width=True)

        if comp_rows:
            comp_df = pd.DataFrame(comp_rows)
            col_order = ["Strategy"] + [c for c in comp_df.columns if c != "Strategy"]
            st.dataframe(comp_df[col_order], use_container_width=True, hide_index=True)
