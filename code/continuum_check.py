"""Exact costs of rounded binary constructions, plus high-precision bound checks."""

from decimal import Decimal, localcontext
from fractions import Fraction
from math import isqrt


def require(condition, label=""):
    """Fail with exit status 1 (works under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED " + str(label))


def trial_cost(height):
    """Return exact A, R, terminal count and stem size for the dyadic trial."""
    n = 2 * height + 1
    # tau_k = n(7-sqrt(7))/(24*4**k), irrational, so round half-integer via floor+1/2.
    numerator = 7 * n - 1 - isqrt(7 * n * n)
    denominator = 24
    levels = []
    while numerator >= denominator:
        levels.append(numerator // denominator)
        denominator *= 4
    levels.append(0)

    last = height
    edges = 1
    area, size = 0, 0
    resistance = Fraction()
    for floor_time in levels:
        require(0 <= floor_time < last)
        duration = last - floor_time
        area += edges * duration * (last + floor_time + 1) // 2
        resistance += Fraction(duration, edges)
        size += edges * duration
        last = floor_time
        if floor_time:
            edges *= 2
    return area, resistance, edges, size


def dec(rat):
    return Decimal(rat.numerator) / Decimal(rat.denominator)


def check():
    # Known exact values C_h from a separate rational forest DP.
    exact = [1, 6, Fraction(35, 2), Fraction(77, 2), 72, 120]
    with localcontext() as ctx:
        ctx.prec = 60
        one = Decimal(1)
        sqrt7 = Decimal(7).sqrt()
        norm = (50 * one / 27 - 2 * sqrt7 / 189).sqrt()
        lower_cost = (50 * one / 27 + 2 * sqrt7 / 189).sqrt() / Decimal(8).sqrt()
        upper_cost = 3 / (7 * Decimal(2).sqrt())
        print("K =", norm)
        for h in (1, 2, 3, 4, 5, 6, 17, 64, 256, 1024, 4096, 65536, 10**9, 10**18):
            A, R, tips, size = trial_cost(h)
            T = Decimal(h) + Decimal("0.5")
            scale = norm * T * T.sqrt()
            trial = 2 * dec(A * R).sqrt()
            require(trial <= scale - upper_cost)
            # The universal bound applies to the exact optimum, hence to each trial.
            require(trial >= scale - lower_cost)
            if h <= len(exact):
                optimum = 2 * dec(Fraction(exact[h - 1])).sqrt()
                require(scale - lower_cost <= optimum <= trial)
            print(f"h={h} tips={tips} size={size} trial-minus-scale={trial - scale:.9f}")


if __name__ == "__main__":
    check()
