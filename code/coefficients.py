"""Exact fixed-diameter Wiener coefficients by conductance dynamic programming."""
import argparse
from fractions import Fraction


def coefficients(max_height):
    if max_height < 1:
        raise ValueError("height must be positive")
    budget = max_height**2 * (max_height + 1) // 2
    # At a fixed depth cost, retain the highest conductance and then the
    # highest sum of the voltage gaps from internal vertices to the tips.
    states = {1: (Fraction(1), Fraction(0))}
    for height in range(1, max_height + 1):
        c = min(cost / conductance for cost, (conductance, _) in states.items())
        winners = [(cost, 1 / conductance, 1 - 2 * gap)
                   for cost, (conductance, gap) in states.items()
                   if cost / conductance == c]
        beta = min(entry[2] for entry in winners)
        yield height, c, beta, sorted(winners)
        if height == max_height:
            return
        root_cost = height + 1
        limit = budget - root_cost
        forests = [None] * (limit + 1)
        forests[0] = (Fraction(0), Fraction(0))
        for cost, (conductance, gap) in states.items():
            for total in range(cost, limit + 1):
                previous = forests[total - cost]
                if previous is None:
                    continue
                candidate = (previous[0] + conductance,
                             previous[1] + conductance * gap)
                if forests[total] is None or candidate > forests[total]:
                    forests[total] = candidate
        states = {}
        for total, forest in enumerate(forests[1:], 1):
            if forest is not None:
                parallel, weighted_gap = forest
                states[total + root_cost] = (
                    parallel / (1 + parallel),
                    (1 + weighted_gap) / parallel
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("height", type=int, nargs="?", default=8)
    for h, c, beta, winners in coefficients(parser.parse_args().height):
        print(f"h={h}  c={c}  beta={beta}  winning (A,R,beta for best gap at A):",
              ", ".join(f"({a},{r},{b})" for a, r, b in winners))
