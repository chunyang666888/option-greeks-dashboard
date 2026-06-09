import numpy as np
from greeks import core as G


def test_put_call_parity():
    S, K, T, r, sigma = 100.0, 105.0, 0.5, 0.03, 0.2
    c = G.bs_price(S, K, T, r, sigma, "call")
    p = G.bs_price(S, K, T, r, sigma, "put")
    # C - P = S*e^{-qT} - K*e^{-rT}  (q=0 here)
    assert abs((c - p) - (S - K * np.exp(-r * T))) < 1e-6


def test_call_price_positive_increasing_with_spot():
    K, T, r, sigma = 100.0, 0.5, 0.03, 0.2
    prices = [G.bs_price(s, K, T, r, sigma, "call") for s in (90, 100, 110)]
    assert prices[0] < prices[1] < prices[2]


def test_call_delta_in_zero_one():
    g = G.bs_greeks(100, 100, 0.5, 0.03, 0.2, "call")
    assert 0 < g["delta"] < 1
    assert g["gamma"] > 0
    assert g["vega"] > 0


def test_put_delta_negative():
    g = G.bs_greeks(100, 100, 0.5, 0.03, 0.2, "put")
    assert -1 < g["delta"] < 0


def test_iv_recovers_sigma():
    S, K, T, r, sigma = 100.0, 100.0, 0.5, 0.03, 0.35
    price = G.bs_price(S, K, T, r, sigma, "call")
    iv = G.implied_vol(price, S, K, T, r, "call")
    assert abs(iv - sigma) < 1e-6


def test_iv_put_symmetric():
    S, K, T, r, sigma = 100.0, 100.0, 0.5, 0.03, 0.30
    price = G.bs_price(S, K, T, r, sigma, "put")
    iv = G.implied_vol(price, S, K, T, r, "put")
    assert abs(iv - sigma) < 1e-6


def test_vectorised_bs_price():
    S = np.array([90.0, 100.0, 110.0])
    out = G.bs_price(S, 100.0, 0.5, 0.03, 0.2, "call")
    assert out.shape == (3,)
    assert np.all(out > 0)
