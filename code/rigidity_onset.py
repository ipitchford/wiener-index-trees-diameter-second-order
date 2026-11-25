"""Exact maxima M_d(n) and the onset of the rigid branch catalogue (Theorem 4.1).

For each diameter d in {6,...,11} and each order n in a range, the script computes,
exactly and with integer arithmetic,
  * M_d(n), the maximum Wiener index of a tree of order n and diameter d;
  * the best value attainable when every branch has an optimal stem (A R = c_h);
  * the best value attainable when at least one branch has a non-optimal stem.
It reports the orders at which no maximiser is built from optimal stems only, and the
orders at which some maximiser still uses a non-optimal stem.

Method. By Cambie's peripheral-leaf lemma (JCTB 2020, Lemma 4.1) every leaf of a
maximiser lies at depth r from the nearer centre, so a maximiser consists of a centre
(even d) or a central edge (odd d) and full-height branches; every stem vertex at depth
h = r - 1 (a tip) carries at least one leaf. Identity (4) of the manuscript gives
  (r + eps/4) n^2 - W = z r n + delta^2 + sum over branches of Q_n,
  Q_n = n A + sum_{v in stem} b_v^2 + (number of outer leaves).
A rooted dynamic programme minimises Q_n over all branches of each size, while tracking
whether the stem equals one of the optimal stems. The optimal stems are hard-coded below
from src output (coefficients.py) and re-derived here: for h = 2 the root has one or two
tips; for h = 3, 4 the stem is a path that forks into two tips at its last level.

Cross-checks: the unrestricted values are compared with an independent recurrence
(forest_replay.py) at n = 100 and 250, and with the exact value at n = 249, d = 8. Exit status 1 on any failed check (no assert statements).

Usage: python rigidity_onset.py [--nmax-small 1200] [--nmax-large 700] [--output FILE]
"""

import argparse
import json
import sys

import numpy as np

INF = np.int64(4 * 10**18)


def require(condition, label=""):
    if not condition:
        raise SystemExit("CHECK FAILED " + str(label))


# allowed child counts at stem level k (1-based, k < h) for an optimal stem
def optimal_child_counts(h, k):
    if h == 2:
        return {1, 2}
    if k <= h - 2:
        return {1}
    return {2}


def knap(cat, non, tmax):
    """Unbounded knapsack over children/branches in one increasing pass.

    Returns S[(c, f)][t]: least total cost of a multiset of parts with total size t,
    c = number of parts capped at 3, f = 1 if some part is non-optimal.
    """
    anyc = np.minimum(cat, non)
    S = {(c, f): np.full(tmax + 1, INF, dtype=np.int64) for c in (1, 2, 3) for f in (0, 1)}
    for t in range(1, tmax + 1):
        S[(1, 0)][t] = cat[t]
        S[(1, 1)][t] = non[t]
        j = np.arange(1, t)
        if t < 2:
            continue
        cj, nj, aj = cat[1:t], non[1:t], anyc[1:t]
        for c, prev in ((2, (1,)), (3, (2, 3))):
            b0 = INF
            b1 = INF
            for c0 in prev:
                p0 = S[(c0, 0)][t - j]
                p1 = S[(c0, 1)][t - j]
                b0 = min(b0, (p0 + cj).min())
                b1 = min(b1, (p1 + aj).min(), (p0 + nj).min())
            S[(c, 0)][t] = min(b0, INF)
            S[(c, 1)][t] = min(b1, INF)
    for key in S:
        S[key] = np.minimum(S[key], INF)
    return S


def level_arrays(n, d):
    """Return (cat, non) branch-cost arrays indexed by branch size b (0..n)."""
    r, eps = divmod(d, 2)
    h = r - 1
    require(h in (2, 3, 4), "optimal-stem pattern hard-coded only for 6 <= d <= 11")
    size = n
    m = np.arange(size + 1, dtype=np.int64)
    # tip level h: tip + L >= 1 leaves; cost = n*(r-h) + m^2 + (m-1), m >= 2
    cat = np.where(m >= 2, n * (r - h) + m * m + (m - 1), INF)
    non = np.full(size + 1, INF, dtype=np.int64)
    for k in range(h - 1, 0, -1):
        allowed = optimal_child_counts(h, k)
        S = knap(cat, non, size - 1)
        base = n * (r - k) + m * m
        newcat = np.full(size + 1, INF, dtype=np.int64)
        newnon = np.full(size + 1, INF, dtype=np.int64)
        for c in (1, 2, 3):
            for f in (0, 1):
                arr = np.full(size + 1, INF, dtype=np.int64)
                arr[1:] = S[(c, f)][:size]
                val = np.where(arr < INF, base + arr, INF)
                if c in allowed and f == 0:
                    newcat = np.minimum(newcat, val)
                else:
                    newnon = np.minimum(newnon, val)
        cat, non = newcat, newnon
    return cat, non


def side_arrays(cat, non, tmax):
    """Least total branch cost for side total t with >=1 and with >=2 branches."""
    S = knap(cat, non, tmax)
    ge1 = {f: np.minimum(np.minimum(S[(1, f)], S[(2, f)]), S[(3, f)]) for f in (0, 1)}
    ge2 = {f: np.minimum(S[(2, f)], S[(3, f)]) for f in (0, 1)}
    return ge1, ge2


def maxima(n, d):
    """Return (M, M_optimal_only, M_with_nonoptimal) as exact integers (4W for odd d)."""
    r, eps = divmod(d, 2)
    z = 1 + eps
    cat, non = level_arrays(n, d)
    if eps == 0:
        ge1, ge2 = side_arrays(cat, non, n - 1)
        Dcat, Dnon = ge2[0][n - 1], ge2[1][n - 1]
        top4 = 4 * r * n * n
        out = []
        for D in (min(Dcat, Dnon), Dcat, Dnon):
            out.append(None if D >= INF else (top4 - 4 * (z * r * n + int(D))) // 4)
        return tuple(out)
    ge1, _ = side_arrays(cat, non, n - 3)
    best = {0: None, 1: None}
    for u in range(1, n - 2):
        v = n - 2 - u
        delta4 = (2 * u + 2 - n) ** 2  # 4*delta^2
        for f in (0, 1):
            if f == 0:
                cands = [(ge1[0][u], ge1[0][v])]
            else:
                anyu = min(ge1[0][u], ge1[1][u]); anyv = min(ge1[0][v], ge1[1][v])
                cands = [(ge1[1][u], anyv), (anyu, ge1[1][v])]
            for a, b in cands:
                if a >= INF or b >= INF:
                    continue
                val = delta4 + 4 * int(a + b)
                if best[f] is None or val < best[f]:
                    best[f] = val
    top4 = (4 * r + 1) * n * n
    res = []
    for D4 in (min(x for x in best.values() if x is not None), best[0], best[1]):
        res.append(None if D4 is None else (top4 - 4 * z * r * n - D4) // 4)
        if D4 is not None:
            require((top4 - 4 * z * r * n - D4) % 4 == 0, ("integrality", n, d))
    return tuple(res)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmax-small", type=int, default=1200, help="largest n for d=6,7")
    ap.add_argument("--nmax-large", type=int, default=700, help="largest n for d=8..11")
    ap.add_argument("--output", default="results/rigidity-onset.json")
    a = ap.parse_args()

    # independent values from forest_replay.py (unrestricted recurrence), d = 6..9
    forest = {100: {6: 24953, 7: 27202, 8: 31678, 9: 33826},
              250: {6: 167720, 7: 182636, 8: 216811, 9: 231563}}
    for n, row in forest.items():
        for d, w in row.items():
            M = maxima(n, d)[0]
            require(M == w, ("forest cross-check", n, d, M, w))
    require(maxima(249, 8)[0] == 215016, "n=249, d=8")

    report = {"description": __doc__.strip().split("\n")[0], "diameters": {}}
    for d in (6, 7, 8, 9, 10, 11):
        nmax = a.nmax_small if d <= 7 else a.nmax_large
        r = d // 2
        nmin = 2 * r + 4
        no_opt_maximiser, some_nonopt_maximiser = [], []
        for n in range(nmin, nmax + 1):
            M, Mopt, Mnon = maxima(n, d)
            if Mopt is None or Mopt < M:
                no_opt_maximiser.append(n)
            if Mnon is not None and Mnon == M:
                some_nonopt_maximiser.append(n)
        entry = {
            "n_range": [nmin, nmax],
            "orders_with_no_optimal_stem_maximiser_count": len(no_opt_maximiser),
            "largest_order_with_no_optimal_stem_maximiser": max(no_opt_maximiser) if no_opt_maximiser else None,
            "largest_order_where_some_maximiser_uses_nonoptimal_stem": max(some_nonopt_maximiser) if some_nonopt_maximiser else None,
            "orders_where_some_maximiser_uses_nonoptimal_stem_tail": some_nonopt_maximiser[-15:],
        }
        report["diameters"][str(d)] = entry
        print("d=%d n in [%d,%d]: no all-optimal maximiser at %d orders (largest %s); "
              "some maximiser uses a non-optimal stem up to n=%s"
              % (d, nmin, nmax, len(no_opt_maximiser), entry["largest_order_with_no_optimal_stem_maximiser"],
                 entry["largest_order_where_some_maximiser_uses_nonoptimal_stem"]), flush=True)
    with open(a.output, "w") as fh:
        json.dump(report, fh, indent=1, sort_keys=True)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()
