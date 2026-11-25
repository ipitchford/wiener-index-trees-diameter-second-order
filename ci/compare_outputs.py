# SPDX-License-Identifier: MIT
"""Compare fresh outputs of the fast scripts with the recorded files in results/.

Usage: python3 -I ci/compare_outputs.py RECORDED_DIR NEW_DIR

Declared cross-platform policy (also in README.md, ENVIRONMENT.txt and REPLAY_RECEIPT.md):
- every file must have the same number of lines, and every token that is not a decimal number with a decimal point or
  exponent (words, integers, fractions, PASS, "ALL CHECKS PASSED", fixed-precision symbolic output) must be equal exactly;
- decimal numbers (tokens with a decimal point or an exponent) are double-precision float diagnostics; they must agree
  within relative 1e-12 or absolute 1e-12 (the absolute part covers rounding-noise values such as the worst split
  excess of order 1e-15 in calibration-replay.txt);
- no output contains an interpreter or platform version, so nothing is excluded.
On the release platform every output was byte-identical to the recorded file. Exit 0 if every file agrees, 1 otherwise.
Explicit checks only (no assert), so it also works under python -O.
"""
import re
import sys
from pathlib import Path

FILES = ['coefficients.txt', 'diameter-five-54.txt', 'diameter-five-check.txt', 'graph-check.txt', 'mesh-check.txt',
         'calibration-replay.txt', 'forest-replay.txt', 'calibration-certificate.txt', 'claims-check.txt',
         'calibration-certificate.json', 'claims-check.json']
NUM = re.compile(r'^[+-]?(\d+\.\d*|\.\d+|\d+(\.\d*)?[eE][+-]?\d+)$')
REL = ABS = 1e-12


def tokens(line):
    return re.findall(r'[+-]?(?:\d+\.\d*|\.\d+)(?:[eE][+-]?\d+)?|[+-]?\d+(?:[eE][+-]?\d+)?|[^\s\d+.-]+|[+.-]', line)


def compare(old, new):
    a, b = old.splitlines(), new.splitlines()
    if len(a) != len(b):
        return f'{len(a)} recorded lines, {len(b)} new lines'
    for i, (x, y) in enumerate(zip(a, b), 1):
        tx, ty = tokens(x), tokens(y)
        if len(tx) != len(ty):
            return f'line {i}: token count differs'
        for s, t in zip(tx, ty):
            if s == t:
                continue
            if NUM.match(s) and NUM.match(t):
                u, v = float(s), float(t)
                if abs(u - v) <= max(ABS, REL * max(abs(u), abs(v))):
                    continue
            return f'line {i}: {s!r} != {t!r}'
    return None


def main():
    rec, new = Path(sys.argv[1]), Path(sys.argv[2])
    bad = 0
    for n in FILES:
        o = (rec / n).read_text()
        p = (new / n).read_text()
        err = compare(o, p)
        if err:
            bad += 1
        print(f'{n}: ' + (f'DIFFERS ({err})' if err else ('identical' if o == p else 'equal within the declared tolerance')))
    print('ALL OUTPUTS AGREE' if bad == 0 else f'{bad} OUTPUT(S) DIFFER')
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
