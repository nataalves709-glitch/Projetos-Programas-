import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# =======================
# Leitura do dataset
# =======================
CSV_PATH = "ecommerce_estatistica.csv"
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"Arquivo '{CSV_PATH}' não encontrado. Coloque o CSV na mesma pasta do app."
    )

# tenta UTF-8; se falhar, usa latin-1
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(CSV_PATH, encoding="latin-1")

# tentativa leve de coerção numérica (sem quebrar campos de texto)
for col in df.columns:
    if df[col].dtype == "object":
        try:
            df[col] = pd.to_numeric(df[col].str.replace(",", "."), errors="ignore")
        except Exception:
            pass

numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

# Correlação só com numericas
corr = df[numeric_cols].corr(numeric_only=True) if len(numeric_cols) > 1 else pd.DataFrame()

# =======================
# App Dash
# =======================
app = Dash(__name__)
server = app.server  # útil para deploy (Render/Heroku)
app.title = "Dashboard E-commerce"

controls = html.Div(
    [
        html.H3("Controles"),
        html.Label("Categoria (Barras/Pizza)"),
        dcc.Dropdown(
            id="bcat",
            options=[{"label": c, "value": c} for c in categorical_cols],
            placeholder="Selecione a coluna categórica",
        ),
        html.Label("Valor (Barras/Pizza)"),
        dcc.Dropdown(
            id="bval",
            options=[{"label": c, "value": c} for c in numeric_cols],
            placeholder="Selecione a coluna numérica",
        ),
        html.Label("Agregação (Barras)"),
        dcc.Dropdown(
            id="bagg",
            options=[
                {"label": "Soma", "value": "sum"},
                {"label": "Média", "value": "mean"},
                {"label": "Mediana", "value": "median"},
                {"label": "Contagem", "value": "count"},
            ],
            value="sum",
            clearable=False,
        ),
        html.Hr(),
        html.Label("X (Dispersão/Densidade/Regressão)"),
        dcc.Dropdown(
            id="dx",
            options=[{"label": c, "value": c} for c in numeric_cols],
            placeholder="Selecione X",
        ),
        html.Label("Y (Dispersão/Regressão; opcional na Densidade)"),
        dcc.Dropdown(
            id="dy",
            options=[{"label": c, "value": c} for c in numeric_cols],
            placeholder="Selecione Y",
        ),
        html.Label("Cor (opcional)"),
        dcc.Dropdown(
            id="rcolor",
            options=[{"label": c, "value": c} for c in (categorical_cols + numeric_cols)],
            placeholder="Coluna para colorir pontos (opcional)",
        ),
        html.Hr(),
        html.Label("Categoria (Pizza)"),
        dcc.Dropdown(
            id="pcat",
            options=[{"label": c, "value": c} for c in categorical_cols],
            placeholder="Selecione categoria para Pizza",
        ),
        html.Label("Valor (Pizza)"),
        dcc.Dropdown(
            id="pval",
            options=[{"label": c, "value": c} for c in numeric_cols],
            placeholder="Selecione valor para Pizza",
        ),
    ],
    style={"width": "320px", "padding": "16px", "borderRight": "1px solid #eee"},
)

app.layout = html.Div(
    [
        html.H1("Análise de E-commerce"),
        html.Div(
            [
                controls,
                html.Div(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="bar",
                            children=[
                                dcc.Tab(label="Barras", value="bar"),
                                dcc.Tab(label="Pizza", value="pie"),
                                dcc.Tab(label="Densidade", value="density"),
                                dcc.Tab(label="Regressão", value="reg"),
                                dcc.Tab(label="Mapa de Calor (Correlação)", value="heat"),
                                dcc.Tab(label="Tabela (prévia)", value="table"),
                            ],
                        ),
                        dcc.Graph(id="main-graph", style={"height": "70vh"}),
                        dcc.Graph(id="table-preview", style={"height": "45vh"}),
                    ],
                    style={"flex": 1, "padding": "16px"},
                ),
            ],
            style={"display": "flex"},
        ),
    ],
    style={"fontFamily": "system-ui, -apple-system, Segoe UI, Roboto"},
)

@app.callback(
    Output("main-graph", "figure"),
    [
        Input("tabs", "value"),
        Input("bcat", "value"),
        Input("bval", "value"),
        Input("bagg", "value"),
        Input("pcat", "value"),
        Input("pval", "value"),
        Input("dx", "value"),
        Input("dy", "value"),
        Input("rcolor", "value"),
    ],
)
def update_graph(tab, bcat, bval, bagg, pcat, pval, dx, dy, rcolor):
    if tab == "heat":
        if corr.empty:
            return go.Figure(layout_title_text="Não há colunas numéricas suficientes para correlação.")
        fig = px.imshow(corr, text_auto=True, title="Mapa de Calor — Correlação (numéricas)")
        fig.update_layout(xaxis_title="Colunas", yaxis_title="Colunas")
        return fig

    if tab == "bar":
        if bcat is None or bval is None:
            return go.Figure(layout_title_text="Selecione categoria e valor para o gráfico de barras.")
        d = df[[bcat, bval]].dropna()
        if d.empty:
            return go.Figure(layout_title_text="Sem dados após remoção de nulos.")
        if bagg == "sum":
            agg = d.groupby(bcat, as_index=False)[bval].sum()
        elif bagg == "mean":
            agg = d.groupby(bcat, as_index=False)[bval].mean()
        elif bagg == "median":
            agg = d.groupby(bcat, as_index=False)[bval].median()
        else:
            agg = d.groupby(bcat, as_index=False)[bval].count().rename(columns={bval: "count"})
            bval = "count"
        fig = px.bar(agg, x=bcat, y=bval, title=f"Barras — {bcat} por {bval} ({bagg})")
        fig.update_layout(xaxis_title=bcat, yaxis_title=bval)
        return fig

    if tab == "pie":
        if pcat is None or pval is None:
            return go.Figure(layout_title_text="Selecione categoria e valor para o gráfico de pizza.")
        d = df[[pcat, pval]].dropna()
        if d.empty:
            return go.Figure(layout_title_text="Sem dados após remoção de nulos.")
        agg = d.groupby(pcat, as_index=False)[pval].sum()
        fig = px.pie(agg, names=pcat, values=pval, title=f"Pizza — {pcat} por {pval} (soma)")
        return fig

    if tab == "density":
        if dx is None:
            return go.Figure(layout_title_text="Selecione ao menos a coluna X para densidade.")
        if dy:
            d = df.dropna(subset=[dx, dy])
            if d.empty:
                return go.Figure(layout_title_text="Sem dados após remoção de nulos.")
            fig = px.density_contour(
                d, x=dx, y=dy, title=f"Densidade 2D — {dx} vs {dy}", contours_coloring="fill"
            )
            fig.update_traces(contours_showlabels=True)
            fig.update_layout(xaxis_title=dx, yaxis_title=dy)
        else:
            d = df.dropna(subset=[dx])
            if d.empty:
                return go.Figure(layout_title_text="Sem dados após remoção de nulos.")
            fig = px.histogram(
                d, x=dx, histnorm="probability density", nbins=30,
                title=f"Densidade 1D — {dx}"
            )
            fig.update_layout(xaxis_title=dx, yaxis_title="Densidade")
        return fig

    if tab == "reg":
        if dx is None or dy is None:
            return go.Figure(layout_title_text="Selecione X e Y para regressão.")
        d = df.dropna(subset=[dx, dy])
        if d.empty:
            return go.Figure(layout_title_text="Sem dados após remoção de nulos.")
        try:
            fig = px.scatter(
                d, x=dx, y=dy, color=rcolor, trendline="ols",
                title=f"Regressão (OLS) — {dx} vs {dy}"
            )
        except Exception:
            fig = px.scatter(
                d, x=dx, y=dy, color=rcolor,
                title=f"Regressão — {dx} vs {dy} (instale statsmodels p/ linha)"
            )
        fig.update_layout(xaxis_title=dx, yaxis_title=dy)
        return fig

    return go.Figure()


@app.callback(
    Output("table-preview", "figure"),
    Input("tabs", "value"),
)
def update_table(_):
    if df.empty:
        return go.Figure()
    preview = df.head(12)
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(values=list(preview.columns), align="left"),
                cells=dict(values=[preview[c] for c in preview.columns], align="left"),
            )
        ]
    )
    fig.update_layout(title_text="Prévia dos dados (top 12 linhas)")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
