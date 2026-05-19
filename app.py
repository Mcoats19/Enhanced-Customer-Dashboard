import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table

app = Dash(__name__)
server = app.server

df = pd.DataFrame([
    ["Horizon Bank", "Financial Services", 480000, "Healthy", 88, 92, "Expansion", "AI adoption workshop"],
    ["MedNova Health", "Healthcare", 1200000, "At Risk", 61, 54, "Renewal Risk", "Executive alignment call"],
    ["Titan Logistics", "Logistics", 320000, "Critical", 42, 38, "Churn Risk", "Enablement sprint"],
    ["RetailSphere", "Retail", 760000, "Healthy", 91, 87, "Expansion", "Advanced feature demo"],
    ["Apex Financial", "Financial Services", 950000, "At Risk", 68, 60, "Adoption Risk", "Success plan refresh"],
], columns=[
    "Account", "Industry", "ARR", "Health", "Adoption", "Engagement", "Risk", "Next Action"
])

portfolio_arr = df["ARR"].sum()
avg_adoption = round(df["Adoption"].mean())
at_risk_arr = df[df["Health"].isin(["At Risk", "Critical"])]["ARR"].sum()
expansion_accounts = len(df[df["Risk"] == "Expansion"])

health_fig = px.pie(
    df,
    names="Health",
    values="ARR",
    hole=0.55,
    title="ARR by Customer Health"
)

adoption_fig = px.bar(
    df,
    x="Account",
    y="Adoption",
    color="Health",
    title="Product Adoption by Account"
)

for fig in [health_fig, adoption_fig]:
    fig.update_layout(
        paper_bgcolor="#0B1020",
        plot_bgcolor="#0B1020",
        font_color="white",
        title_font_size=18,
        margin=dict(l=30, r=30, t=60, b=30)
    )

app.layout = html.Div([
    html.Div([
        html.H1("Customer Success Command Center"),
        html.P("Enterprise portfolio intelligence for customer health, adoption, renewal risk, and expansion strategy.")
    ], className="header"),

    html.Div([
        html.Div([html.P("Portfolio ARR"), html.H2(f"${portfolio_arr/1000000:.1f}M")], className="kpi-card"),
        html.Div([html.P("Avg Adoption"), html.H2(f"{avg_adoption}%")], className="kpi-card"),
        html.Div([html.P("At-Risk ARR"), html.H2(f"${at_risk_arr/1000000:.1f}M")], className="kpi-card"),
        html.Div([html.P("Expansion Accounts"), html.H2(expansion_accounts)], className="kpi-card"),
    ], className="kpi-grid"),

    html.Div([
        html.Div(dcc.Graph(figure=health_fig), className="chart-card"),
        html.Div(dcc.Graph(figure=adoption_fig), className="chart-card"),
    ], className="chart-grid"),

    html.Div([
        html.H3("AI-Powered Customer Recommendations"),
        html.P("MedNova Health shows reduced executive engagement and declining adoption ahead of renewal. Recommend executive alignment call and targeted enablement plan."),
        html.P("Titan Logistics is trending critical due to low adoption and engagement. Recommend a 30-day onboarding recovery sprint.")
    ], className="ai-card"),

    html.Div([
        html.H3("Account Risk & Next Best Actions"),
        dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            style_table={"overflowX": "auto"},
            style_cell={
                "backgroundColor": "#121A2B",
                "color": "white",
                "border": "1px solid #263247",
                "padding": "12px",
                "fontFamily": "Inter, Arial"
            },
            style_header={
                "backgroundColor": "#1E293B",
                "fontWeight": "bold"
            }
        )
    ], className="table-card")
], className="page")

if __name__ == "__main__":
    app.run(debug=True)
