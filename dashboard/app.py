import dash
from dash import dcc, html
import requests
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
server = app.server

API_URL = "http://server:5000/data"

def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", unit="s")
        return df
    except Exception as e:
        print(f"Erro ao buscar dados: {e}")
        return pd.DataFrame()

def calculate_thresholds(values):
    lower = np.percentile(values, 5)
    upper = np.percentile(values, 95)
    return lower, upper

app.layout = html.Div([
    html.H1("Dashboard IoT", style={"textAlign": "center", "marginBottom": "20px"}),
    dcc.Interval(id="update-interval", interval=5000, n_intervals=0),
    dcc.Graph(id="sensor-data", style={"marginBottom": "40px"}),
    dcc.Graph(id="correlation-graph", style={"marginBottom": "40px"}),
    html.Div(id="summary-stats", style={"padding": "10px"})
])

@app.callback(
    dash.dependencies.Output("sensor-data", "figure"),
    [dash.dependencies.Input("update-interval", "n_intervals")]
)
def update_sensor_graph(n_intervals):
    data = fetch_data()
    if data.empty or data["timestamp"].isnull().all():
        return {"data": [], "layout": {"title": "Sem dados disponíveis"}}
    
    data = data.dropna(subset=["timestamp"])
    temperatura = data[data["sensor"] == "temperatura"]
    humidade = data[data["sensor"] == "humidade"]
    
    temp_min, temp_max = calculate_thresholds(temperatura["value"])
    hum_min, hum_max = calculate_thresholds(humidade["value"])
    
    fig = {
        "data": [
            {"x": temperatura["timestamp"], "y": temperatura["value"], "type": "line", "name": "Temperatura"},
            {"x": temperatura["timestamp"], "y": [temp_min] * len(temperatura), "type": "line", "name": "Limite Inferior (Temperatura)", "line": {"dash": "dash", "color": "red"}},
            {"x": temperatura["timestamp"], "y": [temp_max] * len(temperatura), "type": "line", "name": "Limite Superior (Temperatura)", "line": {"dash": "dash", "color": "red"}},
            {"x": humidade["timestamp"], "y": humidade["value"], "type": "line", "name": "Humidade"},
            {"x": humidade["timestamp"], "y": [hum_min] * len(humidade), "type": "line", "name": "Limite Inferior (Humidade)", "line": {"dash": "dash", "color": "blue"}},
            {"x": humidade["timestamp"], "y": [hum_max] * len(humidade), "type": "line", "name": "Limite Superior (Humidade)", "line": {"dash": "dash", "color": "blue"}},
        ],
        "layout": {"title": "Leituras dos Sensores", "xaxis": {"title": "Tempo"}, "yaxis": {"title": "Valores"}}
    }
    return fig

@app.callback(
    dash.dependencies.Output("correlation-graph", "figure"),
    [dash.dependencies.Input("update-interval", "n_intervals")]
)
def update_correlation_graph(n_intervals):
    data = fetch_data()
    if data.empty or data["timestamp"].isnull().all():
        return {"data": [], "layout": {"title": "Sem dados disponíveis", "xaxis": {"title": "Temperatura"}, "yaxis": {"title": "Humidade"}}}
    
    temperatura = data[data["sensor"] == "temperatura"]
    humidade = data[data["sensor"] == "humidade"]
    merged = pd.merge(temperatura, humidade, on="timestamp", suffixes=("_temp", "_hum"))
    
    if merged.empty or len(merged) < 2:
        return {"data": [], "layout": {"title": "Sem dados suficientes para calcular a correlação", "xaxis": {"title": "Temperatura"}, "yaxis": {"title": "Humidade"}}}
    
    temp_values = merged["value_temp"]
    hum_values = merged["value_hum"]
    correlation = np.corrcoef(temp_values, hum_values)[0, 1]
    correlation_threshold = 0.8
    correlation_status = "OK" if correlation >= correlation_threshold else "ALERTA"
    
    fig = {
        "data": [{"x": temp_values, "y": hum_values, "mode": "markers", "name": "Correlação"}],
        "layout": {"title": f"Correlação: {correlation:.2f} ({correlation_status})", "xaxis": {"title": "Temperatura"}, "yaxis": {"title": "Humidade"}}
    }
    return fig

@app.callback(
    dash.dependencies.Output("summary-stats", "children"),
    [dash.dependencies.Input("update-interval", "n_intervals")]
)
def update_summary_stats(n_intervals):
    data = fetch_data()
    if data.empty:
        return html.Div("Sem dados disponíveis.")
    
    temperatura = data[data["sensor"] == "temperatura"]["value"]
    humidade = data[data["sensor"] == "humidade"]["value"]
    
    summary = html.Div([
        html.H3("Estatísticas Resumidas"),
        html.P(f"Temperatura: Média = {temperatura.mean():.2f}, Máx = {temperatura.max():.2f}, Mín = {temperatura.min():.2f}"),
        html.P(f"Humidade: Média = {humidade.mean():.2f}, Máx = {humidade.max():.2f}, Mín = {humidade.min():.2f}")
    ])
    return summary

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
