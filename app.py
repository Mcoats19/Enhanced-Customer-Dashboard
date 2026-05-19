import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table

app = Dash(__name__)
server = app.server

df = pd.DataFrame([
    ["Horizon Bank", "Financial Services", 480000, "Healthy", 88, 92, "Expansion", "AI adoption workshop", 45],
    ["MedNova Health", "Healthcare", 1200000, "At Risk", 61, 54, "Renewal Risk", "Executive alignment call", 30],
    ["Titan Logistics", "Logistics", 320000, "Critical", 42, 38, "Churn Risk", "Enablement sprint", 18],
    ["RetailSphere", "Retail", 760000, "Healthy", 91, 87, "Expansion", "Advanced feature demo", 120],
    ["Apex Financial", "Financial Services", 950000, "At Risk", 68, 60, "Adoption Risk", "Success plan refresh", 75],
], columns=["Account", "Industry", "ARR", "Health", "Adoption", "Engagement", "Risk", "Next Action", "Renewal Days"])

portfolio_arr = df["ARR"].sum()
avg_adoption = round(df["Adoption"].mean())
at_risk_arr = df[df["Health"].isin(["At Risk", "Critical"])]["ARR"].sum()
expansion_accounts = len(df[df["Risk"] == "Expansion"])

colors = {
    "Healthy": "#22C55E",
    "At Risk": "#F59E0B",
    "Critical": "#EF4444",
    "Expansion": "#38BDF8",
}

health_fig = px.pie(
    df,
    names="Health",
    values="ARR",
    hole=0.68,
    color="Health",
    color_discrete_map=colors,
)
health_fig.update_traces(textinfo="percent+label", pull=[0.02, 0.04, 0.06])
health_fig.update_layout(
    title="ARR by Customer Health",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E5E7EB",
    margin=dict(l=20, r=20, t=60, b=20),
    legend=dict(orientation="h", y=-0.1),
)

adoption_fig = px.bar(
    df.sort_values("Adoption"),
    x="Adoption",
    y="Account",
    orientation="h",
    color="Health",
    color_discrete_map=colors,
    text="Adoption",
)
adoption_fig.update_traces(texttemplate="%{text}%", textposition="outside")
adoption_fig.update_layout(
    title="Product Adoption by Account",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E5E7EB",
    xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,.18)", range=[0, 105]),
    yaxis=dict(showgrid=False),
    margin=dict(l=20, r=40, t=60, b=20),
)

risk_fig = go.Figure()
risk_fig.add_trace(go.Scatter(
    x=df["Engagement"],
    y=df["Adoption"],
    mode="markers+text",
    text=df["Account"],
    textposition="top center",
    marker=dict(
        size=df["ARR"] / 25000,
        color=df["Renewal Days"],
        colorscale="Turbo",
        showscale=True,
        colorbar=dict(title="Renewal Days"),
        line=dict(width=1, color="#FFFFFF")
    )
))
risk_fig.update_layout(
    title="Adoption vs. Engagement Risk Map",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#E5E7EB",
    xaxis_title="Executive Engagement",
    yaxis_title="Product Adoption",
    xaxis=dict(gridcolor="rgba(148,163,184,.18)"),
    yaxis=dict(gridcolor="rgba(148,163,184,.18)"),
    margin=dict(l=40, r=30, t=60, b=40),
)

def kpi_card(label, value, trend, status="neutral"):
    return html.Div([
        html.Div(label, className="kpi-label"),
        html.Div(value, className="kpi-value"),
        html.Div(trend, className=f"kpi-trend {status}")
    ], className="kpi-card")

app.layout = html.Div([
    html.Div(className="hero", children=[
        html.Div([
            html.Div("CUSTOMER SUCCESS INTELLIGENCE", className="eyebrow"),
            html.H1("Customer Success Command Center"),
            html.P("Executive-ready portfolio intelligence for customer health, adoption, renewal risk, and expansion strategy.")
        ]),
        html.Div(className="hero-badge", children=[
            html.Div("LIVE PORTFOLIO VIEW"),
            html.Span("AI-assisted insights")
        ])
    ]),

    html.Div(className="kpi-grid", children=[
        kpi_card("Portfolio ARR", f"${portfolio_arr/1000000:.1f}M", "+8.2% QoQ", "positive"),
        kpi_card("Avg Adoption", f"{avg_adoption}%", "+12 pts", "positive"),
        kpi_card("At-Risk ARR", f"${at_risk_arr/1000000:.1f}M", "Needs action", "warning"),
        kpi_card("Expansion Accounts", expansion_accounts, "2 active signals", "positive"),
    ]),

    html.Div(className="section-grid", children=[
        html.Div(dcc.Graph(figure=health_fig), className="glass-card"),
        html.Div(dcc.Graph(figure=adoption_fig), className="glass-card"),
    ]),

    html.Div(className="section-grid", children=[
        html.Div(dcc.Graph(figure=risk_fig), className="glass-card wide"),
        html.Div(className="ai-card", children=[
            html.Div("AI NEXT BEST ACTIONS", className="eyebrow"),
            html.H3("Recommended Plays"),
            html.Div(className="recommendation critical", children=[
                html.Strong("Titan Logistics"),
                html.P("Critical adoption and engagement decline. Launch a 30-day enablement sprint and executive recovery plan.")
            ]),
            html.Div(className="recommendation warning", children=[
                html.Strong("MedNova Health"),
                html.P("Renewal approaching with low executive engagement. Schedule leadership alignment and success plan reset.")
            ]),
            html.Div(className="recommendation positive", children=[
                html.Strong("RetailSphere"),
                html.P("Strong adoption and engagement. Recommend advanced feature demo tied to expansion opportunity.")
            ]),
        ])
    ]),

    html.Div(className="table-card", children=[
        html.Div(className="table-header", children=[
            html.H3("Account Risk & Next Best Actions"),
            html.P("Prioritized customer portfolio view for CS, Sales, and executive stakeholders.")
        ]),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={"overflowX": "auto"},
            style_cell={
                "backgroundColor": "rgba(15,23,42,.95)",
                "color": "#E5E7EB",
                "border": "1px solid rgba(148,163,184,.18)",
                "padding": "14px",
                "fontFamily": "Inter, Arial, sans-serif",
                "fontSize": "14px",
                "textAlign": "left",
            },
            style_header={
                "backgroundColor": "rgba(30,41,59,.95)",
                "fontWeight": "700",
                "color": "#FFFFFF",
            },
            style_data_conditional=[
                {"if": {"filter_query": "{Health} = Healthy", "column_id": "Health"}, "color": "#22C55E", "fontWeight": "700"},
                {"if": {"filter_query": "{Health} = At Risk", "column_id": "Health"}, "color": "#F59E0B", "fontWeight": "700"},
                {"if": {"filter_query": "{Health} = Critical", "column_id": "Health"}, "color": "#EF4444", "fontWeight": "700"},
            ],
        )
    ])
], className="page")

if __name__ == "__main__":
    app.run(debug=True)
