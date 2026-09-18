import dash
from dash import html, dcc, callback, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ── Load data ──
df = pd.read_csv("portfolio_prices.csv", parse_dates=["Date"])
tickers = [c for c in df.columns if c != "Date"]

# ── Calculate returns ──
returns = df.set_index("Date")[tickers].pct_change().dropna()
cum_returns = (1 + returns).cumprod() - 1

# ── Dash app ──
app = dash.Dash(__name__, title="Portfolio Risk Dashboard")

app.layout = html.Div(style={"fontFamily": "Inter, sans-serif", "padding": "24px",
                             "maxWidth": "1200px", "margin": "0 auto", "backgroundColor": "#f8fafc"}, children=[

    html.H1("Portfolio Risk Dashboard",
            style={"fontSize": "24px", "fontWeight": "800", "marginBottom": "4px"}),
    html.P(f"Interactive risk analytics for a {len(tickers)}-stock portfolio",
           style={"color": "#64748b", "marginBottom": "24px"}),

    #ticket selector
    html.Label("Select tickers:", style={"fontWeight": "600", "marginBottom": "8px"}),
    dcc.Dropdown(id="ticker-dropdown", options=[{"label": t, "value": t} for t in tickers],
                 value=tickers, multi=True,
                 style={"marginBottom": "24px", "width": "100%"}),

    #charts grid
    html.Div(style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(400px, 1fr))",
                    "gap": "24px"}, children=[

        #cumulative retunrs
        html.Div([
            html.H3("Cumulative Returns", style={"fontSize": "18px", "fontWeight": "600", "marginBottom": "8px"}),
            dcc.Graph(id="cumulative-returns-chart")
        ], style={"background": "#fff", "padding": "20px", "borderRadius": "12px",
                   "border": "1px solid #e2e8f0", "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)"}),

        # correlaion heatmap
        html.Div([
            html.H3("Returns Correlation Heatmap", style={"fontSize": "18px", "fontWeight": "600", "marginBottom": "8px"}),
            dcc.Graph(id="corr-heatmap")
        ], style={"background": "#fff", "padding": "20px", "borderRadius": "12px",
                   "border": "1px solid #e2e8f0", "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)"}),

        #Risk Metrics Table
        html.Div([
            html.H3("Risk Metrics", style={"fontSize": "18px", "fontWeight": "600", "marginBottom": "8px"}),
            html.Div(id="risk-table")
        ], style={"background": "#fff", "padding": "20px", "borderRadius": "12px",
                   "border": "1px solid #e2e8f0", "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)"}),

        #VaR Distribution
        html.Div([
            html.H3("Portfolio Return Distribution & VaR", style={"fontSize": "18px", "fontWeight": "600", "marginBottom": "8px"}),
            dcc.Graph(id="var-distribution")
        ], style={"background": "#fff", "padding": "20px", "borderRadius": "12px",
                   "border": "1px solid #e2e8f0", "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)"}),
    ])

])

@callback(
    Output("cumulative-returns-chart", "figure"),
    Output("corr-heatmap", "figure"),
    Output("risk-table", "children"),
    Output("var-distribution", "figure"),
    Input("ticker-dropdown", "value"))
def updated(selected):
    if not selected:
        selected = tickers

    sel_returns = returns[selected]
    sel_cum_returns = cum_returns[selected]

    #1. Cululative returns line chart
    fig1 = px.line(sel_cum_returns.reset_index(), x="Date", y=selected,
                   labels={"value": "Return", "variable": "Ticker"})
    fig1.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=300,
                       yaxis_tickformat=".0%", legend=dict(orientation="h", y=0.15))

    #2. Correlation heatmap
    corr = sel_returns.corr()
    fig2 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    fig2.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=300)

    #3. Risk metrics table
    portfolio_retunrs = sel_returns.mean(axis=1) # equal weight
    metrics =[]
    for t in selected:
        ann_vol = sel_returns[t].std() * np.sqrt(252)
        ann_ret = sel_returns[t].mean() * 252
        sharpe = ann_ret / ann_vol if ann_vol > 0 else 0
        var_95 = np.percentile(sel_returns[t], 5)
        metrics.append({"Ticker": t,
                        "Annualized Return": f"{ann_ret:.2%}",
                        "Annualized Volatility": f"{ann_vol:.2%}",
                        "Sharpe Ratio": f"{sharpe:.2f}",
                        "VaR (95%)": f"{var_95:.2%}"})
    table = dash_table.DataTable(data=metrics, columns=[{"name": k, "id": k} for k in metrics[0]],
                                 style_cell={"fontFamily": "Inter, sans-serif", "fontSize": "13px", "padding": "8px",
                                             "border": "1px solid #e2e8f0", "textAlign": "left"},
                                 style_header={"backgroundColor": "#f8fafc", "fontWeight": "600"})

    #4. VaR histogram
    fig4 = go.Figure()
    fig4.add_trace(go.Histogram(x=portfolio_retunrs, nbinsx=50, name="Portfolio Returns", marker_color="#636efa"))
    var_95_portfolio = np.percentile(portfolio_retunrs, 5)
    fig4.add_vline(x=var_95_portfolio, line_dash="dash", line_color="red", annotation_text=f"VaR 95%: {var_95_portfolio:.2%}")
    fig4.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=300,
                       xaxis_tickformat=".1%", showlegend=False)
    return fig1, fig2, table, fig4

if __name__ == "__main__":
    app.run(debug=True, port=8050)
    
                   