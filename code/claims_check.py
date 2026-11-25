"""Recompute the individual numbers quoted in the manuscript text.

Covers: the remainders 2 sqrt(c_h) - K (h+1/2)^(3/2) for h <= 8 (Theorem 5.1 window),
the slow-convergence example of Remark 6.3, the n = 3000, d = 9 example, Cambie's bracket,
the thresholds used in the proofs of Theorem 5.1 and Lemma 6.1, and two exact maxima.
Exit status 1 on any failure. Usage: python claims_check.py [--output FILE]
"""

import argparse
import json
import os
import sys
from fractions import Fraction

from mpmath import mp, mpf, sqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rigidity_onset  # noqa: E402  (exact M_d(n) by dynamic programming)

mp.dps = 40


def require(condition, label):
    if not condition:
        raise SystemExit("CHECK FAILED: " + label)
    print("PASS", label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/claims-check.json")
    args = ap.parse_args()
    out = {}
    c = {1: Fraction(1), 2: Fraction(6), 3: Fraction(35, 2), 4: Fraction(77, 2), 5: Fraction(72),
         6: Fraction(120), 7: Fraction(186), 8: Fraction(273)}
    a = sqrt((7 - sqrt(7)) / 6)
    K = 1 / (2 * a) + a - a**3 / 7
    kappa = sqrt((175 - sqrt(7)) / 756)
    lower = sqrt((175 + sqrt(7)) / 756)
    upper = 3 / (7 * sqrt(2))
    require(abs(K / sqrt(8) - kappa) < mpf(10) ** -35, "K/sqrt8 = kappa")
    rem = {}
    for h, ch in c.items():
        theta = mpf(h) + mpf(1) / 2
        v = 2 * sqrt(mpf(ch.numerator) / ch.denominator) - K * theta ** mpf(1.5)
        rem[h] = float(v)
        require(-lower <= v <= -upper, "Theorem 5.1 window at h=%d (remainder %.5f)" % (h, v))
        require(abs(v) <= mpf("0.49"), "|remainder| <= 0.49 at h=%d" % h)
    out["remainder_2sqrtc_minus_KTheta"] = rem
    require(abs(rem[1] - (-0.48103)) < 5e-6, "h=1 remainder -0.48103")
    out["lower_constant"] = float(lower)
    out["upper_constant"] = float(upper)
    require(round(float(lower), 5) == 0.48475 and round(float(upper), 5) == 0.30305, "constants 0.48475, 0.30305")
    # Remark 6.3: slow convergence at h = 8 (d = 18)
    r18 = 2 * sqrt(273) / mpf(18) ** mpf(1.5)
    out["ratio_2sqrtc8_over_18^1.5"] = float(r18)
    out["relative_gap_to_kappa_at_d18"] = float(1 - r18 / kappa)
    out["2sqrt_c8"] = float(2 * sqrt(273))
    out["K_Theta8"] = float(K * mpf(8.5) ** mpf(1.5))
    require(round(float(r18), 3) == 0.433, "2 sqrt(c_8)/18^(3/2) = 0.433")
    # n = 3000, d = 9 example (exact maximum by dynamic programming)
    n, d = 3000, 9
    M = rigidity_onset.maxima(n, d)[0]
    require(M == 36860816, "M_9(3000) = 36860816 (also forest_replay.py)")
    deficit = Fraction(17, 4) * n * n - M
    norm = float(deficit) / (d * n) ** 1.5
    pred = float(2 * sqrt(mpf(35) / 2) * mpf(n) ** mpf(1.5)) + (2 * 4 - 3) * n
    out["d9_n3000"] = {"M": M, "deficit": float(deficit), "normalised_deficit": norm,
                       "fixed_d_prediction": pred, "residual_over_sqrt_n": (float(deficit) - pred) / n ** 0.5}
    # Cambie bracket and kappa
    out["sqrt2_over_3"] = float(sqrt(2) / 3)
    out["29_over_60"] = 29 / 60
    out["kappa"] = float(kappa)
    out["K"] = float(K)
    require(float(sqrt(2) / 3) < float(kappa) < 29 / 60, "kappa inside Cambie bracket")
    # thresholds in the proofs
    out["a2_over_2"] = float(a * a / 2)
    out["2_over_a2"] = float(2 / (a * a))
    require(float(a * a / 2) < 0.363 and 2.75 < float(2 / (a * a)) < 2.76, "a^2/2 < 0.363, 2/a^2 = 2.756")
    require(float(0.363 * 2.756 + 0.5) <= 2.756 - 1, "first split inside the branch when J >= 1")
    C0 = lower - upper
    out["C0"] = float(C0)
    require(C0 < mpf("0.19"), "C_0 < 0.19")
    # sigma_* < 3K/2 (root of f = K beyond a_+)
    mp.dps = 40
    f = lambda s: 1 / (2 * s) + s - s**3 / 7
    sigma_star = mp.findroot(lambda s: f(s) - K, 1.5)
    out["sigma_star"] = float(sigma_star)
    require(sigma_star < 3 * K / 2 and sigma_star > sqrt(2), "sqrt2 < sigma_* < 3K/2")
    # exact maxima quoted in the text
    require(rigidity_onset.maxima(249, 8)[0] == 215016, "M_8(249) = 215016")
    out["M8_249"] = 215016
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    for k, v in out.items():
        print(k, v)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
