"""Smoke test for the dashboard module — exercises _surface without plotly."""
import numpy as np
from greeks import dashboard as D


def test_surface_shapes():
    spots, sigmas, fields = D._surface(100.0, 100.0, 0.5, 0.03, 0.2, "call")
    assert len(spots) == len(sigmas) == 40
    names = {name for name, _ in fields}
    assert names == {"price", "delta", "gamma", "vega", "theta", "rho"}
    for name, mat in fields:
        assert mat.shape == (40, 40)


def test_render_html_requires_plotly(monkeypatch):
    # If plotly missing, render_html should raise a clear ImportError.
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *a, **k):
        if name.startswith("plotly"):
            raise ImportError("no plotly")
        return real_import(name, *a, **k)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    try:
        D.render_html(outfile="_t.html")
        raised = False
    except ImportError:
        raised = True
    assert raised
