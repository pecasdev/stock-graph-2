from datetime import datetime

import plotly.express as px
import pandas as pd


def _reshape_data(date_to_symbol_to_profit: dict[datetime, dict[str, float]]):
    data = []
    for date, symbol_to_profit in date_to_symbol_to_profit.items():
        for symbol, profit in symbol_to_profit.items():
            data.append({"date": date, "symbol": symbol, "profit": profit})

    return pd.DataFrame(data)


def plot_graph(date_to_symbol_to_profit: dict[datetime, dict[str, float]]):
    df = _reshape_data(date_to_symbol_to_profit)
    fig = px.line(
        df,
        x="date",
        y="profit",
        color="symbol",
        labels={"date": "Date", "profit": "Net Profit (CAD/USD)"},
        title="Portfolio Profit Performance",
    )
    fig.show()
