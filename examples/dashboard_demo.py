"""Demo: price one option, show its Greeks, and try to render the dashboard."""

from greeks import core as G


def main():
    S, K, T, r, sigma = 100.0, 105.0, 0.5, 0.03, 0.20
    call = G.bs_price(S, K, T, r, sigma, "call")
    put = G.bs_price(S, K, T, r, sigma, "put")
    g = G.bs_greeks(S, K, T, r, sigma, "call")
    print(f"Call price : {call:.4f}")
    print(f"Put  price : {put:.4f}")
    print("Call Greeks:")
    for k, v in g.items():
        print(f"  {k:6s}: {v:.5f}")

    iv = G.implied_vol(call, S, K, T, r, "call")
    print(f"\nImplied vol recovered from call price: {iv:.4f} (truth 0.20)")

    try:
        from greeks.dashboard import render_html
        path = render_html(S, K, T, r, sigma, "call", "greeks_dashboard.html")
        print(f"\nDashboard written -> {path}")
    except ImportError:
        print("\n(plotly not installed — skip dashboard render; core works fine)")


if __name__ == "__main__":
    main()
