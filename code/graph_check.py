"""Independent exact checks for fixed-diameter maximum Wiener index results.

Only the Python standard library is required.
Run "python graph_check.py" for the default checks.
"""

import argparse
from collections import defaultdict, deque
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement, product


def require(condition, label=""):
    """Fail with exit status 1 (works under python -O, unlike assert)."""
    if not condition:
        raise SystemExit("CHECK FAILED " + str(label))


def diameter_five_maximum(order):
    """Enumerate all central cuts and child counts, balancing each side exactly."""
    def best_side(size):
        costs = []
        # At least one child on each side must itself have a child.
        for children in range(1, size):
            small, larger = divmod(size, children)
            sq_sum = (children - larger) * small**2 + larger * (small + 1)**2
            costs.append(((order - 1) * children + sq_sum, children))
        best = min(cost for cost, _ in costs)
        return best, [children for cost, children in costs if cost == best]

    sides = {size: best_side(size) for size in range(2, order - 3)}
    best = -1
    witnesses = []
    for left in range(2, (order - 2) // 2 + 1):
        right = order - 2 - left
        left_cost, left_choices = sides[left]
        right_cost, right_choices = sides[right]
        value = ((left + 1) * (right + 1) + (2 * order - 1) * (order - 2)
                 - left_cost - right_cost)
        equality = [(left, right, i, j) for i in left_choices for j in right_choices
                    if left != right or i <= j]
        if value > best:
            best = value
            witnesses = equality
        elif value == best:
            witnesses.extend(equality)
    return best, witnesses


def direct_tree_invariants(tree):
    """Compute all pairwise distances by breadth-first search, independent of cut sums."""
    total = 0
    diameter = 0
    for source in range(len(tree)):
        distance = {source: 0}
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for target in tree[vertex]:
                if target not in distance:
                    distance[target] = 1 + distance[vertex]
                    queue.append(target)
        total += sum(distance.values())
        diameter = max(diameter, max(distance.values()))
    require(total % 2 == 0)
    return diameter, total // 2


def tree_key(graph):
    """Canonical encoding by simultaneous peeling and sorted rooted branches."""
    degrees = list(map(len, graph))
    leaves = [i for i, degree in enumerate(degrees) if degree == 1]
    remaining = len(graph)
    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            for vertex in graph[leaf]:
                degrees[vertex] -= 1
                if degrees[vertex] == 1:
                    new_leaves.append(vertex)
        leaves = new_leaves

    def rooted(vertex, parent):
        return tuple(sorted(rooted(i, vertex) for i in graph[vertex] if i != parent))

    if len(leaves) == 1:
        return (1, rooted(leaves[0], None))
    u, v = leaves
    return (2, tuple(sorted((rooted(u, v), rooted(v, u)))))


def verify_small_trees(max_order):
    known_counts = (0, 1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159, 7741)
    level = [((1,), (0,))]
    for n in range(3, max_order + 1):
        next_level = {}
        for graph in level:
            for parent in range(n - 1):
                child = list(graph)
                child[parent] = child[parent] + (n - 1,)
                child.append((parent,))
                next_level[tree_key(child)] = tuple(child)
        level = list(next_level.values())
        if n < len(known_counts):
            require(len(level) == known_counts[n])
        if n < 6:
            continue
        maxima = defaultdict(lambda: -1)
        counts = defaultdict(int)
        for tree in level:
            diameter, wiener = direct_tree_invariants(tree)
            if wiener > maxima[diameter]:
                maxima[diameter] = wiener
                counts[diameter] = 1
            elif wiener == maxima[diameter]:
                counts[diameter] += 1
        expected, witnesses = diameter_five_maximum(n)
        require(maxima[5] == expected and counts[5] == len(witnesses))
        print(f"n={n:2d} diameter 5: W={expected}, equality shapes={counts[5]}")
    print("All small-tree checks passed.")


def min_cost(height):
    return height * (height + 1) // 2


@lru_cache(None)
def forest_conductance(height, budget, least):
    """Best parallel conductance at exact total cost subject to child-cost order."""
    if budget == 0:
        return Fraction(0)
    best = None
    for cost in range(max(least, min_cost(height)), budget + 1):
        g = branch_conductance(height, cost)
        if g is None:
            continue
        rest = forest_conductance(height, budget - cost, cost)
        if rest is not None and (best is None or rest + g > best):
            best = g + rest
    return best


@lru_cache(None)
def branch_conductance(height, budget):
    if height == 1:
        return Fraction(1) if budget == 1 else None
    forest = forest_conductance(height - 1, budget - height, min_cost(height - 1))
    if not forest:
        return None
    return forest / (1 + forest)


def best_profiles(height, budget, least):
    """Recover all unordered child-cost multisets attaining exact-budget optimum."""
    if not budget:
        yield ()
        return
    optimum = forest_conductance(height, budget, least)
    for cost in range(max(least, min_cost(height)), budget + 1):
        g = branch_conductance(height, cost)
        if g is None:
            continue
        rest = forest_conductance(height, budget - cost, cost)
        if rest is not None and g + rest == optimum:
            for tail in best_profiles(height, budget - cost, cost):
                yield (cost,) + tail


@lru_cache(None)
def best_shapes(height, budget):
    if height == 1:
        return ((),)
    shapes = set()
    for profile in best_profiles(height - 1, budget - height, min_cost(height - 1)):
        grouped = []
        for cost in sorted(set(profile)):
            options = best_shapes(height - 1, cost)
            grouped.append(combinations_with_replacement(options, profile.count(cost)))
        for choice in product(*grouped):
            shapes.add(tuple(sorted(shape for group in choice for shape in group)))
    return tuple(sorted(shapes))


def exact_statistics(shape, level):
    """Return cost, resistance, vertex count and sum_v f_v times descendant count."""
    if not shape:
        require(level == 1)
        return 1, Fraction(1), 1, Fraction(1)
    subtrees = [exact_statistics(child, level - 1) for child in shape]
    parallel = sum(1 / resistance for _, resistance, _, _ in subtrees)
    size = 1 + sum(count for _, _, count, _ in subtrees)
    moment = size + sum(moment / resistance / parallel for _, resistance, _, moment in subtrees)
    return level + sum(cost for cost, _, _, _ in subtrees), 1 + 1 / parallel, size, moment


def show_shape(shape):
    """Parentheses encode an unordered rooted tree; a dot is a leaf."""
    if not shape:
        return "."
    return "(" + ",".join(map(show_shape, shape)) + ")"


def verify_structural_constants(depth):
    results = []
    for h in range(1, depth + 1):
        # Single path gives R=h,A=h(h+1)/2. Since every R >= 1,
        # any minimiser of the product has cost no larger than h*A.
        cap = h * min_cost(h)
        options = []
        for cost in range(min_cost(h), cap + 1):
            g = branch_conductance(h, cost)
            if g:
                options.append((Fraction(cost) / g, cost))
        c = min(value for value, _ in options)
        row = []
        for value, budget in options:
            if value != c:
                continue
            for shape in best_shapes(h, budget):
                cost, resistance, size, moment = exact_statistics(shape, h)
                require(cost == budget and cost * resistance == c)
                beta = 1 + 2 * (moment - size * resistance)
                row.append((cost, resistance, size, beta, show_shape(shape)))
        row.sort()
        print(f"h={h}, c={c}, minimum beta={min(item[3] for item in row)}")
        for entry in row:
            print("  A={}, R={}, size={}, beta={}, H={}".format(*entry))
        results.append((c, row))
    require(results[0][0] == 1)
    if depth >= 2:
        require(results[1][0] == 6)
        require([(r[0], r[3]) for r in results[1][1]] == [(3, -1), (4, 0)])
    return results


def rooted_dynamic_maxima(order, max_radius):
    """Maximise the edge sum by height and total size, including all shallow leaves.

    A forest contains child branches of the centre (or one endpoint of the
    central edge). We recover one optimal forest and check its actual diameter.
    """
    cap = order - 1
    empty = -order**4
    # Height zero admits only the empty forest.
    forest = [0] + [empty] * cap
    decisions = [[0] * (cap + 1)]
    levels = [forest]
    for height in range(1, max_radius + 1):
        branch = [0] + [
            size * (order - size) + forest[size - 1] for size in range(1, cap + 1)
        ]
        forest = [0] * (cap + 1)
        last = [0] * (cap + 1)
        for total in range(1, cap + 1):
            best = -1
            for size in range(1, total + 1):
                value = branch[size] + forest[total - size]
                if value > best:
                    best, last[total] = value, size
            forest[total] = best
        decisions.append(last)
        levels.append(forest)

    def reconstruct(adjacency, root, height, total):
        while total:
            size = decisions[height][total]
            child = len(adjacency)
            adjacency[root].append(child)
            adjacency.append([root])
            reconstruct(adjacency, child, height - 1, size - 1)
            total -= size

    for radius in range(2, max_radius + 1):
        forest = levels[radius]
        for parity in (0, 1):
            if parity:
                w, mass = max((a * (order - a) + forest[a - 1] + forest[order - a - 1], a)
                              for a in range(1, order // 2 + 1))
                g = [[1], [0]]
                reconstruct(g, 0, radius, mass - 1)
                reconstruct(g, 1, radius, order - mass - 1)
            else:
                w = forest[order - 1]
                g = [[]]
                reconstruct(g, 0, radius, order - 1)
            diameter, direct = direct_tree_invariants(g)
            require((diameter, direct) == (2 * radius + parity, w))
            yield diameter, w


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-order", type=int, default=12, help="0 skips tree enumeration")
    parser.add_argument("--order-dp", type=int, default=249, help="0 skips whole-tree dynamic checks")
    parser.add_argument("--depth", type=int, default=5, help="maximum branch depth for exact search")
    args = parser.parse_args()
    require(args.depth >= 1)
    verify_structural_constants(args.depth)
    value, shapes = diameter_five_maximum(54)
    require(value == 5530)
    print(f"n=54, d=5: W={value}, (left,right,children): {shapes}")
    if args.order_dp:
        exact = dict(rooted_dynamic_maxima(args.order_dp, 4))
        require(exact[5] == diameter_five_maximum(args.order_dp)[0])
        print(f"Full-tree height DP and reconstructed distances (n={args.order_dp}): {exact}")
    if args.max_order >= 6:
        verify_small_trees(args.max_order)
