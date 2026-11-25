"""Exact symbolic checks of the constants and inequalities in Section 5 (Lemma 5.2, Theorem 5.1).

Every check is an exact sympy computation (identities by expansion, signs of
expressions in sqrt(7) and sqrt(2) decided exactly); 50-digit decimals are printed for
reference. Exit status 1 on any failure (no assert statements, so it also fails under -O).
Usage: python calibration_certificate.py [--output results/calibration-certificate.json]
"""

import argparse
import json

import sympy as sp


def require(condition, label):
    if not bool(condition):
        raise SystemExit("CHECK FAILED: " + label)
    print("PASS", label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="results/calibration-certificate.json")
    args = ap.parse_args()

    t, x, y, z, s = sp.symbols("t x y z s", positive=True)
    g = lambda tt, xx: tt**2 / 2 + tt * xx**2 - xx**4 / 7
    f = 1 / (2 * s) + s - s**3 / 7

    # (11) split identity
    lhs = g(t, y) + g(t, z) - g(t, y + z)
    rhs = sp.Rational(1, 2) * (t - 2 * y * z) ** 2 + sp.Rational(4, 7) * y * z * (y - z) ** 2
    require(sp.expand(lhs - rhs) == 0, "split identity (11)")

    # coefficient 1/7: equal split of mass x at t = x^2/2 has zero excess only for alpha = 1/7
    al = sp.symbols("alpha")
    G = lambda tt, xx: tt**2 / 2 + tt * xx**2 - al * xx**4
    exc = sp.expand(2 * G(t, x / 2) - G(t, x))
    tmin = sp.solve(sp.diff(exc, t), t)
    require(len(tmin) == 1 and sp.simplify(tmin[0] - x**2 / 2) == 0, "equal-split excess minimised at t = x^2/2")
    require(sp.solve(sp.Eq(exc.subs(t, x**2 / 2), 0), al) == [sp.Rational(1, 7)], "alpha = 1/7")

    # g(t,x) = x t^{3/2} f(x/sqrt t), so the two pieces of V agree where f = K
    require(sp.simplify(g(t, x) - x * t**sp.Rational(3, 2) * f.subs(s, x / sp.sqrt(t))) == 0,
            "g(t,x) = x t^(3/2) f(x/sqrt(t))")

    a = sp.sqrt((7 - sp.sqrt(7)) / 6)
    ap_ = sp.sqrt((7 + sp.sqrt(7)) / 6)
    fp = sp.diff(f, s)
    require(sp.simplify(fp + (6 * s**4 - 14 * s**2 + 7) / (14 * s**2)) == 0, "f'(s) = -(6s^4-14s^2+7)/(14 s^2)")
    require(sp.simplify(fp.subs(s, a)) == 0 and sp.simplify(fp.subs(s, ap_)) == 0, "f'(a) = f'(a_+) = 0")
    fpp = sp.diff(f, s, 2)
    require(sp.nsimplify(fpp.subs(s, a)).is_positive and sp.nsimplify(fpp.subs(s, ap_)).is_negative,
            "a is a local minimum and a_+ a local maximum of f")

    K = f.subs(s, a)
    Kp = f.subs(s, ap_)
    require(sp.simplify(K**2 / 8 - (175 - sp.sqrt(7)) / 756) == 0 and sp.simplify(K).is_positive,
            "K/sqrt(8) = sqrt((175 - sqrt 7)/756)")
    require(sp.simplify(Kp**2 / 8 - (175 + sp.sqrt(7)) / 756) == 0, "f(a_+)/sqrt(8) = sqrt((175 + sqrt 7)/756)")

    K2 = 8 * (175 - sp.sqrt(7)) / 756  # K^2, exact
    require(sp.simplify(f.subs(s, 1) - sp.Rational(19, 14)) == 0, "f(1) = 19/14")
    require((sp.Rational(19, 14) ** 2 - K2).is_positive, "19/14 > K")
    require(sp.simplify(f.subs(s, sp.sqrt(2)) - 27 * sp.sqrt(2) / 28) == 0, "f(sqrt 2) = 27 sqrt(2)/28")
    require((sp.Rational(27**2 * 2, 28**2) - K2).is_positive, "f(sqrt 2) > K")
    require((2 - (7 + sp.sqrt(7)) / 6).is_positive, "a_+ < sqrt 2, so the last root b of f = K exceeds sqrt 2")
    # s + 1/s >= 3K/2 for s >= b > sqrt 2: s + 1/s is increasing on [1, inf)
    require(((sp.Rational(3, 2) * sp.sqrt(2)) ** 2 - sp.Rational(9, 4) * K2).is_positive,
            "sqrt 2 + 1/sqrt 2 > 3K/2")
    # terminal bound and cubic in the upper estimate
    cub = sp.simplify((sp.Rational(1, 8) - g(sp.Rational(1, 2), y)) / y)
    require(sp.simplify(cub - (-y / 2 + y**3 / 7)) == 0, "(1/8 - g(1/2,y))/y = -y/2 + y^3/7")
    end = -3 / (7 * sp.sqrt(2))
    require(sp.simplify(cub.subs(y, 1 / sp.sqrt(2)) - end) == 0 and sp.simplify(cub.subs(y, sp.sqrt(2)) - end) == 0,
            "cubic equals -3/(7 sqrt 2) at both endpoints (convex in between)")
    # Cambie bracket
    kappa2 = (175 - sp.sqrt(7)) / 756
    require((kappa2 - sp.Rational(2, 9)).is_positive and (sp.Rational(29, 60) ** 2 - kappa2).is_positive,
            "sqrt(2)/3 < kappa < 29/60")

    b_root = sp.nsolve(f - K, s, 1.5, prec=60)
    num = {
        "a": sp.N(a, 50), "a_plus": sp.N(ap_, 50), "K": sp.N(K, 50), "sigma_star": sp.N(b_root, 50),
        "kappa": sp.N(sp.sqrt(kappa2), 50), "terminal_constant": sp.N(sp.sqrt((175 + sp.sqrt(7)) / 756), 50),
        "upper_constant": sp.N(-end, 50), "sqrt2_over_3": sp.N(sp.sqrt(2) / 3, 50), "29/60": sp.N(sp.Rational(29, 60), 50),
    }
    require(abs(f.subs(s, b_root) - K) < sp.Float("1e-45") and b_root > sp.sqrt(2), "numerical root sigma_* of f = K above sqrt 2")
    out = {k: str(v) for k, v in num.items()}
    for k, v in out.items():
        print(k, v)
    with open(args.output, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
