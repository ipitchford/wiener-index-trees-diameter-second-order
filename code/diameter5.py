"""Exact maximum Wiener index of trees of order n and diameter five.

Run 'python diameter5.py 54' for an example and 'python diameter5.py --check'
for exhaustive checks. No dependencies outside the standard library.
"""

import argparse
import itertools
from math import isqrt


def require(condition, label=""):
    """Fail with exit status 1 (works under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED " + str(label))


def balanced_sizes(total, count):
    """Encode a multiset of star orders as (small order, large count, count)."""
    small, large_count = divmod(total, count)
    return small, large_count, count


def branch_cost(n, total, count):
    """Return (n-1) times the number of stars plus their squared orders."""
    small, extra, _ = balanced_sizes(total, count)
    return count * (n - 1 + small * small) + extra * (2 * small + 1)


def side_optima(n, total):
    """Return the optimum side cost and all branch counts giving that cost."""
    if n < 257:
        counts = range(1, total)
    else:
        # floor K for K=(n-2)/(2 sqrt(n-1)), by integer arithmetic
        centre = isqrt((n - 2) ** 2 // (4 * (n - 1)))
        counts = range(max(1, centre - 3), min(total - 1, centre + 4) + 1)
    costs = [(branch_cost(n, total, k), k) for k in counts]
    best = min(value for value, _ in costs)
    return best, [k for value, k in costs if value == best]


def extremisers(n):
    """Return maximum and tuples (small side size, its k, large side size, its k).

    Side sizes exclude central vertices. Each side contains k stars whose orders
    differ by at most one. Output has one descriptor per unlabelled maximiser.
    """
    if n < 6:
        raise ValueError("A tree of diameter five needs at least six vertices")
    middle = (n - 2) // 2
    first = 2 if n < 257 else max(2, middle - 12)
    best = -1
    descriptors = set()
    for s in range(first, middle + 1):
        t = n - 2 - s
        left_cost, left_k = side_optima(n, s)
        right_cost, right_k = side_optima(n, t)
        w = (s + 1) * (t + 1) + (2 * n - 1) * (n - 2) - left_cost - right_cost
        if w < best:
            continue
        if w > best:
            best = w
            descriptors.clear()
        for k in left_k:
            for j in right_k:
                if s != t or k <= j:
                    descriptors.add((s, k, t, j))
    return best, sorted(descriptors)


def partitions(total, lower=1):
    """All nondecreasing positive partitions, by recursion."""
    yield (total,)
    for first in range(lower, total // 2 + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def direct_wiener(left, right):
    """Build the graph from arbitrary star orders and sum all BFS distances."""
    graph = [[1], [0]]
    def attach(parent):
        vertex = len(graph)
        graph[parent].append(vertex)
        graph.append([parent])
        return vertex
    for centre, stars in enumerate([left, right]):
        for order in stars:
            stem = attach(centre)
            for _ in range(order - 1):
                attach(stem)
    w = 0
    for source in range(len(graph)):
        depth = [-1] * len(graph)
        depth[source] = 0
        queue = [source]
        for v in queue:
            for u in graph[v]:
                if depth[u] == -1:
                    depth[u] = depth[v] + 1
                    queue.append(u)
        w += sum(depth[source+1:])
    return w


def check():
    for n in range(6, 20):
        expected = -1
        witnesses = set()
        for s in range(2, (n-2)//2+1):
            t = n-2-s
            for left, right in itertools.product(partitions(s), partitions(t)):
                if left[-1] == 1 or right[-1] == 1:
                    continue
                w = direct_wiener(left, right)
                if w < expected:
                    continue
                if w > expected:
                    expected = w
                    witnesses.clear()
                if s != t or left <= right:
                    witnesses.add((left, right))
        actual, descriptors = extremisers(n)
        def expand(s, k):
            a, rem = divmod(s, k)
            return (a,) * (k-rem) + (a+1,) * rem
        actual_witnesses = set()
        for s, k, t, j in descriptors:
            a, b = expand(s,k), expand(t,j)
            actual_witnesses.add((b,a) if s==t and b<a else (a,b))
        require(actual == expected and actual_witnesses == witnesses, n)
    # Larger independent optimiser uses the convex branch-count envelope,
    # rather than either of the two truncation windows in extremisers().
    for n in (*range(257, 401), 512, 777, 1024, 2026, 4096, 5000):
        m = n-1
        p = (isqrt(1+4*m)-1)//2
        lmin = p if p*(p+1)==m else p+1
        lmax = p+1
        cand = {}
        for s in range(2,n-3):
            lo=max(1,min(s-1,s//lmax))
            hi=max(lo,min(s-1,(s+lmin-1)//lmin))
            vals=[(branch_cost(n,s,k),k) for k in range(lo,hi+1)]
            v=min(x for x,k in vals)
            cand[s]=(v,[k for x,k in vals if x==v])
        expected=-1
        desc=set()
        for s in range(2,(n-2)//2+1):
            t=n-2-s
            x,ks=cand[s]
            y,js=cand[t]
            w=(s+1)*(t+1)+(2*n-1)*(n-2)-x-y
            if w<expected:continue
            if w>expected:
                expected=w
                desc.clear()
            desc.update((s,k,t,j) for k in ks for j in js if s!=t or k<=j)
        require((expected,sorted(desc))==extremisers(n),n)
    print("BFS + all isomorphism classes: n=6..19; independent full centre scan: n=257..400,512,777,1024,2026,4096,5000. Passed.")


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n",nargs="?",type=int,default=54)
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    if args.check:
        check()
    else:
        print(extremisers(args.n))
