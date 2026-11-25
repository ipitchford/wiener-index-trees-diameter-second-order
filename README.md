# The maximum Wiener index of trees with prescribed diameter: the sharp second-order constant

Version 0.1.0-candidate. DOI [10.5281/zenodo.24520149](https://doi.org/10.5281/zenodo.24520149) (all versions:
[10.5281/zenodo.24520148](https://doi.org/10.5281/zenodo.24520148)). Release page:
https://evidencepress.org/releases/wiener-index-trees-diameter-second-order/

**Status: unrefereed research candidate.** The proofs have had internal AI-assisted review only (see
[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)); this is not peer review, independent reproduction or formal verification.

## What this is about

Take a network shaped like a tree (no loops) with n points and add up the distances between every pair of points.
Divided by the number of pairs, this total is the average distance. It is called the **Wiener index**: the chemist
Harry Wiener introduced it in 1947 to predict the boiling points of paraffins, and it is now a standard measure of how
spread out a network is.

Suppose you are told the **diameter** d, the longest distance in the tree. How spread out can the tree be? No distance
can exceed d, so the average is below d. The question is how far below it must fall. Plesník, who settled the
*smallest* total for given n and d, remarked that upper bounds seem much more difficult; the maximum has since been
called Plesník's problem.

For trees the answer starts with a simple term, (d/2 - ε/4)n², where ε is 0 or 1 by the parity of d. The interesting
part is the **shortfall** below it. In 2020 Stijn Cambie showed that the shortfall grows like (dn)^(3/2) and pinned its
coefficient between about 0.4714 and 0.4833, a gap of about 2.5 percent, taking limits in a fixed order.

## What is new

1. **The exact coefficient.** Whenever d grows but stays small compared with n, with no order of limits imposed, the
   shortfall is (κ + o(1))(dn)^(3/2) with κ = sqrt((175 - sqrt 7)/756) ≈ 0.47747 (Theorem 1.1).
2. **Fixed diameter.** For every fixed d ≥ 4 the next two terms, with rational constants computed from the electrical
   resistance of small rooted trees (Theorem 1.2, Table 2). For example M_8(n) = 4n² - sqrt(70) n^(3/2) - n + O(sqrt n).
3. **Rigidity.** For large n every best tree is built from a finite catalogue of branch shapes (Theorem 4.1), so for
   each fixed d an exact algorithm running in time polynomial in log n exists (Corollary 4.2; proved, not implemented).
4. **Diameter five.** An explicit formula for the maximum and every maximiser, for every n ≥ 6 (Theorem 8.1).
5. **Where rigidity begins.** Exact maxima for diameters 6 to 11 up to 3000 vertices show where the predicted catalogue
   actually takes over in that range (Section 4).

The best trees split each branch in half, again and again, and each new split comes when only a quarter as much height remains as at the split before.

## Idea of the proof

An exact distance identity writes the shortfall as a sum, over branches, of a depth cost and the squares of subtree
sizes. Treat the leaves as an electric current flowing out from the centre: the squared sizes are then the energy of
that current. For large diameter the problem becomes continuous (mass flowing down, splitting for free) and is solved
by one polynomial, V = τ²/2 + τx² - x⁴/7, whose splitting excess is a sum of two squares. Equality holds only for equal
halves at the right height, and that forces the factor 1/4.

## Credit

Cambie (2020) found the (dn)^(3/2) scale and the bracket [sqrt 2/3, 29/60], built lower constructions from branches
that fork in two at geometrically spaced heights (ratio about 0.38), and proved that every leaf of a maximiser lies at
full depth; that lemma is used here. Earlier exact results are due to Wang and Guo, Wagner, and Mukwembi and Vetrík.

## Limits

- Trees only. For graphs of odd diameter the answer differs at the first term; for even diameter it agrees only if a
  question of Cambie (are the graph maximisers trees for large n?) has a positive answer.
- "Exact" refers to the leading coefficient; lower-order terms in the joint regime are open, as is the regime where d
  is a fixed fraction of n.
- The thresholds in the fixed-diameter and rigidity theorems are effective but not computed, and the fast algorithm is
  not implemented.
- Unrefereed candidate. The scripts check identities, constants and finite cases; the proofs carry the general claims.

## Contents

| Path | What it is |
|---|---|
| `manuscript.pdf`, `manuscript.tex` | The paper (14 pages; self-contained LaTeX source, no external figures) |
| `code/coefficients.py` | c_h and β_h for h ≤ 8 (Table 2) |
| `code/graph_check.py` | Independent recursion for h ≤ 6; M_d(249) for d = 4..9 by a full-tree DP with reconstructed distances (M_8(249) = 215016); diameter five on all trees up to 15 vertices |
| `code/diameter5.py` | Theorem 8.1 at a given n, and `--check` against exhaustive enumeration up to 19 vertices |
| `code/continuum_check.py` | The constructions of Theorem 5.1 up to h = 10^18 |
| `code/calibration_replay.py` | Floating-point replay of the calibration and the split excess on a grid |
| `code/forest_replay.py` | Exact maxima for d = 4..9 by a forest recursion (numpy) |
| `code/calibration_certificate.py` | Exact symbolic certificate of every Section 5 constant and inequality (sympy) |
| `code/claims_check.py` | Every other number quoted in the text |
| `code/rigidity_onset.py` | Exact maxima and catalogue flags for d = 6..11, n ≤ 3000 (slow, about 35 minutes) |
| `results/` | Recorded outputs of every script |
| `ci/compare_outputs.py`, `.github/workflows/replay.yml` | Cross-platform comparison and CI |
| `refs.bib`, `AI_INDEX.md`, `RESEARCH_GATES.json`, `REVIEW_SUMMARY.md`, `REPLAY_RECEIPT.md`, `ENVIRONMENT.txt` | Records |

## Replay

From the package root, with Python 3.12 or later and the pins in `requirements.txt` (numpy 2.3.5, sympy 1.14.0,
mpmath 1.3.0). Every check raises explicitly and also fails under `python -O`.

```sh
python3 -I -B -O code/coefficients.py 8                > results/coefficients.txt
python3 -I -B -O code/diameter5.py 54                  > results/diameter-five-54.txt
python3 -I -B -O code/diameter5.py --check             > results/diameter-five-check.txt
python3 -I -B -O code/graph_check.py --depth 6 --max-order 15 --order-dp 249 > results/graph-check.txt
python3 -I -B -O code/continuum_check.py               > results/mesh-check.txt
python3 -I -B -O code/calibration_replay.py            > results/calibration-replay.txt
python3 -I -B -O code/forest_replay.py                 > results/forest-replay.txt
python3 -I -B -O code/calibration_certificate.py       > results/calibration-certificate.txt
python3 -I -B -O code/claims_check.py                  > results/claims-check.txt
python3 -I -B -O code/rigidity_onset.py --nmax-small 3000 --nmax-large 3000 > results/rigidity-onset.txt
```

The last three also write `results/*.json`. Run them in a copy if you want to compare with the recorded files using
`python3 -I ci/compare_outputs.py results <copy>/results`.

**Comparison policy** (declared before tagging; the same in CI, ENVIRONMENT.txt and REPLAY_RECEIPT.md): every word,
integer, fraction and fixed-precision symbolic value must match exactly; printed double-precision decimals must agree
within relative or absolute 1e-12. On the release platform every output was byte-identical to the recorded file. CI on
Linux runs the nine fast scripts, the comparison and a negative control on every push; the slow rigidity scan runs only
on manual request and does not block.

## Licence and citation

Text, manuscript, recorded outputs and records: CC0-1.0. Code: MIT. See [LICENSE.md](LICENSE.md) and
[CITATION.cff](CITATION.cff). Creator: Anonymous.
