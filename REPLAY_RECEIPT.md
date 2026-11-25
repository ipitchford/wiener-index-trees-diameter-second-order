# Replay receipt (0.1.0-candidate, 25 November 2026)

**Environment.** macOS arm64. Commands as in the publish brief, from a fresh copy of the approved candidate, cwd = package
root, flags `-I -B -O`, `PYTHONDONTWRITEBYTECODE=1`; standard output went to a separate directory, never over the shipped
results. Interpreters were printed inside the run: `uv run --no-project --python 3.12 python3` resolved through a
`python3` shim to CPython 3.14.7 (standard-library scripts); `uv run --no-project --python 3.12 --with ...` built an
ephemeral environment on CPython 3.12.11 with numpy 2.3.5, sympy 1.14.0 and mpmath 1.3.0 (scripts with pinned packages).
The rigidity scan ran under the host's shared research runner (one core, 1 GB).

| Command (all under `python3 -I -B -O`) | Interpreter | Exit | Time | Result |
|---|---|---|---|---|
| `code/coefficients.py 8` | 3.14.7 | 0 | <1 s | Table 2 constants, h ≤ 8 |
| `code/diameter5.py 54` | 3.14.7 | 0 | <1 s | `(5530, [(24, 3, 28, 4)])` |
| `code/diameter5.py --check` | 3.14.7 | 0 | 1 s | exhaustive n = 6..19 and centre scans: Passed |
| `code/graph_check.py --depth 6 --max-order 15 --order-dp 249` | 3.14.7 | 0 | 1 s | All small-tree checks passed; M_8(249) = 215016 |
| `code/continuum_check.py` | 3.14.7 | 0 | <1 s | constructions to h = 10^18 |
| `code/calibration_replay.py` | 3.14.7 | 0 | <1 s | split excess on 66,049 pairs |
| `code/forest_replay.py` | 3.12.11 + numpy | 0 | 1 s | exact maxima d = 4..9 |
| `code/calibration_certificate.py` | 3.12.11 + sympy, mpmath | 0 | 1 s | ALL CHECKS PASSED (also writes the JSON) |
| `code/claims_check.py` | 3.12.11 + numpy, mpmath | 0 | <1 s | ALL CHECKS PASSED (also writes the JSON) |
| `code/rigidity_onset.py --nmax-small 3000 --nmax-large 3000` | 3.12.11 + numpy | 0 | 2024 s | ALL CHECKS PASSED (also writes the JSON) |

Every output, the three JSON files included, was byte-identical to the shipped file in `results/`; every standard-error
stream was empty.

**Negative control (under -O).** In a second fresh copy the expected value in `code/graph_check.py` was changed from 5530
to 5531 (`require(value == 5531)`); the script stopped with "CHECK FAILED", exit 1.

**After the replay** only the title-page DOI line of `manuscript.tex`, the rebuilt PDF (three pdflatex passes, 14 pages; a
word-level text comparison with the approved PDF shows only the DOI line) and the release records changed; the scripts,
recorded results and `requirements.txt` are byte-identical to the replayed candidate.

**Cross-platform policy** (declared before tagging; see ENVIRONMENT.txt and `ci/compare_outputs.py`): fresh outputs must
match line by line with every word, integer, fraction and fixed-precision symbolic value equal exactly; printed
double-precision decimals may differ by at most relative or absolute 1e-12. No output contains an interpreter or platform
version. The GitHub Actions workflow `.github/workflows/replay.yml` checks the manifest, reruns the nine fast scripts under
`python -O` on Linux, compares under this policy and runs the negative control (one blocking job, under a minute of
computation). The rigidity scan runs only on manual request, compares its two outputs exactly and does not block.

**Scope.** The scripts check the finite claims: the constants, the diameter-five formula on small orders, the order-249
example, the constructions, the Section 5 constants and the exact maxima up to 3000 vertices. The proofs carry the general
theorems.
