"""Self-contained interactive Greeks dashboard (Plotly, optional dependency).

``render()`` builds a single HTML file with a price grid: for a range of spot
prices it computes call/put price, delta, gamma, vega, theta, rho and draws
heatmaps / line charts. Plotly is imported lazily so the numpy core stays
dependency-free.
"""

import numpy as np

from .core import bs_price, bs_greeks


def _surface(S0, K, T, r, sigma, option_type, n=40):
    """Return (spots, list of (name, 2D matrix)) for the dashboard."""
    spots = np.linspace(0.6 * S0, 1.4 * S0, n)
    sigmas = np.linspace(0.05, 1.5, n)
    fields = ["price", "delta", "gamma", "vega", "theta", "rho"]
    out = []
    for f in fields:
        mat = np.zeros((n, n))
        for i, s in enumerate(sigms := sigmas):
            for j, sp in enumerate(spots):
                if f == "price":
                    mat[i, j] = bs_price(sp, K, T, r, s, option_type)
                else:
                    g = bs_greeks(sp, K, T, r, s, option_type)
                    mat[i, j] = g[f]
        out.append((f, mat))
    return spots, sigmas, out


def render_html(S0=100.0, K=100.0, T=0.5, r=0.03, sigma=0.2,
                option_type="call", outfile="greeks_dashboard.html"):
    """Write a self-contained Plotly HTML dashboard.

    Requires ``plotly`` (pip install plotly). Returns the outfile path.
    """
    try:
        import plotly.graph_objects as go
        from plotly.offline import plot
    except ImportError as e:  # pragma: no cover
        raise ImportError("dashboard.render_html needs plotly: pip install plotly") from e

    spots, sigmas, fields = _surface(S0, K, T, r, sigma, option_type)
    figs = []
    for name, mat in fields:
        fig = go.Figure(
            data=go.Heatmap(z=mat, x=spots, y=sigmas * 100,
                            colorscale="RdYlBu_r", name=name))
        fig.update_layout(title=f"{option_type} {name}  (K={K}, T={T}y, r={r})",
                          xaxis_title="Spot", yaxis_title="Implied vol %")
        figs.append(fig)
    html = plot(figs, output_type="div", include_plotlyjs="cdn", auto_open=False)
    with open(outfile, "w", encoding="utf-8") as fh:
        fh.write("<html><head><meta charset='utf-8'><title>Greeks Dashboard"
                 "</title></head><body>" + html + "</body></html>")
    return outfile
