"""option-greeks-dashboard — Black-Scholes pricing, Greeks & implied volatility.

Pure-numpy core (``core``). The ``dashboard`` module renders a self-contained
interactive Plotly HTML (plotly is an *optional* dependency — install it only
if you want the visualisation). Everything else works with numpy alone.
"""

from . import core, dashboard

__all__ = ["core", "dashboard"]
