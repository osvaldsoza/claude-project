import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from fetcher import load_data, TICKERS

st.set_page_config(page_title="Ações 2025", page_icon="📈", layout="wide")

st.title("📈 Performance de Ações Brasileiras — 2025")
st.caption("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3) · Dados: Yahoo Finance")

# Sidebar
with st.sidebar:
    st.header("Filtros")
    selected = st.multiselect(
        "Ações",
        options=list(TICKERS.keys()),
        default=list(TICKERS.keys()),
    )
    chart_type = st.radio(
        "Tipo de gráfico",
        ["Cotação absoluta (R$)", "Retorno acumulado (%)"],
    )

if not selected:
    st.warning("Selecione ao menos uma ação na barra lateral.")
    st.stop()

with st.spinner("Carregando dados..."):
    data = load_data()

COLORS = {"PETR4": "#009c3b", "ITUB4": "#002776", "VALE3": "#FEDF00"}

# --- Gráfico principal ---
st.subheader("Cotação / Retorno acumulado")
fig = go.Figure()

for name in selected:
    if name not in data:
        st.warning(f"Sem dados para {name}.")
        continue
    close = data[name]["Close"].squeeze()
    if chart_type.startswith("Retorno"):
        first = close.iloc[0]
        y = ((close / first) - 1) * 100
        ylabel = "Retorno acumulado (%)"
        hover = "%{y:.2f}%"
    else:
        y = close
        ylabel = "Preço de fechamento (R$)"
        hover = "R$ %{y:.2f}"

    fig.add_trace(
        go.Scatter(
            x=close.index,
            y=y,
            name=name,
            line=dict(color=COLORS[name], width=2),
            hovertemplate=f"<b>{name}</b><br>%{{x|%d/%m/%Y}}<br>{hover}<extra></extra>",
        )
    )

fig.update_layout(
    xaxis_title="Data",
    yaxis_title=ylabel,
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=420,
    margin=dict(t=20, b=0),
)
if chart_type.startswith("Retorno"):
    fig.add_hline(y=0, line_dash="dot", line_color="gray", line_width=1)

st.plotly_chart(fig, use_container_width=True)

# --- Volume ---
st.subheader("Volume diário")
fig_vol = go.Figure()
for name in selected:
    if name not in data:
        continue
    vol = data[name]["Volume"].squeeze()
    fig_vol.add_trace(
        go.Bar(
            x=vol.index,
            y=vol,
            name=name,
            marker_color=COLORS[name],
            opacity=0.75,
            hovertemplate=f"<b>{name}</b><br>%{{x|%d/%m/%Y}}<br>Vol: %{{y:,.0f}}<extra></extra>",
        )
    )
fig_vol.update_layout(
    barmode="group",
    xaxis_title="Data",
    yaxis_title="Volume (ações)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=300,
    margin=dict(t=20, b=0),
)
st.plotly_chart(fig_vol, use_container_width=True)

# --- Tabela de métricas ---
st.subheader("Métricas — 2025")

rows = []
for name in selected:
    if name not in data:
        continue
    close = data[name]["Close"].squeeze()
    daily_ret = close.pct_change().dropna()
    total_ret = (close.iloc[-1] / close.iloc[0] - 1) * 100
    vol_ann = daily_ret.std() * (252 ** 0.5) * 100
    best_idx = daily_ret.idxmax()
    worst_idx = daily_ret.idxmin()
    rows.append(
        {
            "Ação": name,
            "Retorno total (%)": f"{total_ret:+.2f}%",
            "Mínimo (R$)": f"R$ {close.min():.2f}",
            "Máximo (R$)": f"R$ {close.max():.2f}",
            "Volatilidade anualizada (%)": f"{vol_ann:.2f}%",
            "Melhor dia": f"{best_idx.strftime('%d/%m/%Y')} ({daily_ret[best_idx]*100:+.2f}%)",
            "Pior dia": f"{worst_idx.strftime('%d/%m/%Y')} ({daily_ret[worst_idx]*100:+.2f}%)",
        }
    )

if rows:
    st.dataframe(pd.DataFrame(rows).set_index("Ação"), use_container_width=True)
