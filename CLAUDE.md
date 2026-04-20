# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
/Users/osvaldsoza/Library/Python/3.9/bin/streamlit run app.py

# Stop the app
pkill -f "streamlit run app.py"
```

> `streamlit` is installed in `/Users/osvaldsoza/Library/Python/3.9/bin/` which is not on PATH — use the full path or add it to PATH.

## Architecture

Two-file app: data fetching is isolated in `fetcher.py`; all Streamlit rendering lives in `app.py`.

**`fetcher.py`** — single entry point `load_data()` decorated with `@st.cache_data(ttl=3600)`. Downloads `Close` and `Volume` columns for each ticker via `yfinance`. Returns `dict[str, pd.DataFrame]` keyed by short name (`PETR4`, `ITUB4`, `VALE3`). The `TICKERS` dict maps short names to Yahoo Finance B3 symbols (`*.SA` suffix) and is imported by `app.py` to drive the sidebar selector.

**`app.py`** — three visual sections rendered in sequence:
1. Line chart (cotação absoluta or retorno acumulado %) — toggled via sidebar radio
2. Grouped bar chart for daily volume
3. Metrics table (total return, min/max price, annualized volatility, best/worst day)

Sidebar `multiselect` drives which tickers appear in all three sections. `COLORS` dict in `app.py` assigns brand colors per ticker.

## GitHub

Repositório: https://github.com/osvaldsoza/claude-project

Sincronização automática: um hook `PostToolUse` em `.claude/settings.local.json` faz commit e push para `origin/main` após cada edição de arquivo (ferramentas `Write` e `Edit`). Mensagem de commit gerada automaticamente com timestamp.

Para desativar temporariamente, remova ou comente o bloco `hooks` em `.claude/settings.local.json`.

## Key details

- Data period is hardcoded to `2025-01-01` → `2025-12-31` in `fetcher.py` (`START`/`END`).
- Annualized volatility = `daily_returns.std() × √252 × 100`.
- Accumulated return baseline is the first trading day's close price (`close.iloc[0]`).
