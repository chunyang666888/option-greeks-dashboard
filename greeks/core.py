"""Black-Scholes pricing, Greeks, and implied-volatility calibration (numpy only).

Notation
--------
S : spot price
K : strike price
T : time to expiry (years)
r : risk-free rate (annual, continuous)
sigma : volatility (annual)
q : continuous dividend yield (default 0)
"""

from math import erf, sqrt, log, exp
import numpy as np


def _norm_cdf(x):
    x = np.asarray(x, dtype=float)
    # numpy core has no scalar erf; vectorized math.erf keeps it numpy-only.
    return 0.5 * (1.0 + np.vectorize(erf)(x / sqrt(2.0)))


def _norm_pdf(x):
    x = np.asarray(x, dtype=float)
    return np.exp(-0.5 * x * x) / sqrt(2.0 * np.pi)


def bs_price(S, K, T, r, sigma, option_type="call", q=0.0):
    """Black-Scholes price for a European option.

    Vectorised over any numpy-array argument (broadcasting applies).
    """
    S = np.asarray(S, dtype=float)
    K = np.asarray(K, dtype=float)
    T = np.asarray(T, dtype=float)
    r = np.asarray(r, dtype=float)
    sigma = np.asarray(sigma, dtype=float)
    q = np.asarray(q, dtype=float)
    if np.any(sigma <= 0) or np.any(T <= 0):
        raise ValueError("sigma and T must be positive")
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    disc = np.exp(-r * T)
    div_disc = np.exp(-q * T)
    if option_type == "call":
        return div_disc * S * _norm_cdf(d1) - disc * K * _norm_cdf(d2)
    elif option_type == "put":
        return disc * K * _norm_cdf(-d2) - div_disc * S * _norm_cdf(-d1)
    raise ValueError("option_type must be 'call' or 'put'")


def bs_greeks(S, K, T, r, sigma, option_type="call", q=0.0):
    """Return dict of all first-order Greeks (delta, gamma, vega, theta, rho).

    Vega / rho are per 1.00 (100%) vol / rate move; divide by 100 for per-1% moves.
    """
    S = float(S); K = float(K); T = float(T); r = float(r)
    sigma = float(sigma); q = float(q)
    if sigma <= 0 or T <= 0:
        raise ValueError("sigma and T must be positive")
    d1 = (log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    disc = exp(-r * T)
    div_disc = exp(-q * T)
    pdf = _norm_pdf(d1)
    gamma = div_disc * pdf / (S * sigma * sqrt(T))
    vega = S * div_disc * pdf * sqrt(T)  # per 1.00 vol
    if option_type == "call":
        delta = div_disc * _norm_cdf(d1)
        theta = (-S * div_disc * pdf * sigma / (2 * sqrt(T))
                 - r * K * disc * _norm_cdf(d2)
                 + q * S * div_disc * _norm_cdf(d1))
        rho = K * T * disc * _norm_cdf(d2)  # per 1.00 rate
    else:
        delta = -div_disc * _norm_cdf(-d1)
        theta = (-S * div_disc * pdf * sigma / (2 * sqrt(T))
                 + r * K * disc * _norm_cdf(-d2)
                 - q * S * div_disc * _norm_cdf(-d1))
        rho = -K * T * disc * _norm_cdf(-d2)
    return {"delta": delta, "gamma": gamma, "vega": vega,
            "theta": theta, "rho": rho}


def implied_vol(price, S, K, T, r, option_type="call", q=0.0, tol=1e-8, max_iter=100):
    """Implied volatility via bisection on sigma in [1e-4, 5]."""
    lo, hi = 1e-4, 5.0
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        diff = bs_price(S, K, T, r, mid, option_type, q) - price
        if abs(diff) < tol:
            return mid
        if diff > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)
