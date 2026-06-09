# option-greeks-dashboard

Black-Scholes pricing, a full set of **Greeks**, and **implied-volatility**
calibration in numpy — plus an optional **interactive Plotly dashboard** that
renders the Greeks as a function of spot × volatility.

[![CI](https://github.com/chunyang666888/option-greeks-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/chunyang666888/option-greeks-dashboard/actions)

```
pip install numpy
pip install plotly        # only if you want the dashboard
pytest -q
```

## Core (numpy only)

```python
from greeks import core as G

G.bs_price(100, 105, 0.5, 0.03, 0.20, "call")      # 6.82...
G.bs_greeks(100, 100, 0.5, 0.03, 0.20, "call")      # delta/gamma/vega/theta/rho
G.implied_vol(6.82, 100, 105, 0.5, 0.03, "call")    # recovers 0.20
```

- `bs_price` is **vectorised** (broadcasts over any numpy-array argument).
- `bs_greeks` returns `delta, gamma, vega, theta, rho`.
- `implied_vol` uses bisection — robust and fast.

## Dashboard (optional, plotly)

```python
from greeks.dashboard import render_html
render_html(S0=100, K=100, T=0.5, r=0.03, sigma=0.2,
            option_type="call", outfile="greeks_dashboard.html")
```

Writes a self-contained HTML file: heatmaps of price / delta / gamma / vega /
theta / rho across a spot × implied-vol grid. Open it in any browser — no server.

## Why this repo

Options desks live and die by Greeks. This repo is a compact, tested reference
implementation: enough to reason about hedging, and a visual aid for interviews
and self-study.

## License

MIT
