# AI index: The maximum Wiener index of trees with prescribed diameter (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is
a plain introduction with a roadmap). DOI 10.5281/zenodo.24520149 (concept 10.5281/zenodo.24520148). Status:
unrefereed candidate; internal AI-assisted review only.

## Normalisation

W(T) = sum of distances over unordered vertex pairs (Wiener index). M_d(n) = max W(T) over trees T with n vertices and
diameter d. d = 2r + ε, ε ∈ {0,1}, h = r − 1, z = 1 + ε. Deficit Δ_d(n) = (d/2 − ε/4)n² − M_d(n). Branch = a non-central
neighbour of a centre with its descendants; stem H = branch minus its vertices at depth r; tips = stem vertices at
depth h. A(H) = Σ_v (r − depth v) (depth cost); R(H) = effective resistance from the centre to the tips wired together
(entrance edge included, unit resistors); β(H) = 1 − 2D. c_h = min A·R over proper stems of height h; β_h = least β
among minimisers. K = √8 κ ≈ 1.35050; κ = √((175 − √7)/756) ≈ 0.4774744081. Θ = h + 1/2. Statement numbers follow the
manuscript. Cambie = Cambie (2020), doi:10.1016/j.jctb.2020.06.003, arXiv:1811.08334.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| 1 (main) | Absolute C_1, C_2: for h ≥ 1, n ≥ C_1 h, \|Δ_d(n) − 2√c_h n^{3/2}\| ≤ C_2 n h² and \|2√c_h − KΘ^{3/2}\| ≤ 0.49; hence Δ_d(n)/(dn)^{3/2} → κ whenever d → ∞ and d/n → 0 (joint limit, no order imposed) | Theorem 1.1; Sections 5–6 (Lemma 5.2, Theorem 5.1, Lemma 6.1) | written proof; Section 5 constants certified exactly (calibration_certificate.py); scale (dn)^{3/2} and bracket [√2/3, 29/60] due to Cambie |
| 1a | κ lies strictly inside Cambie's bracket [0.4714, 0.4833] | Section 1.3 | exact (calibration_certificate.py, claims_check.py) |
| 2 (main) | Fixed d = 2r + ε ≥ 4: M_d(n) = (r + ε/4)n² − 2√c_h n^{3/2} − (zr + β_h)n + O_d(√n), c_h and β_h rational | Theorem 1.2; Sections 2–3 (Lemmas 2.1, 3.1) | written proof; Table 2 for h ≤ 8 computed by coefficients.py and checked by an independent recursion for h ≤ 6 (graph_check.py) |
| 2a | M_6(n) = 3n² − 2√6 n^{3/2} − 2n + O(√n) (Mukwembi–Vetrík expansion); M_8(n) = 4n² − √70 n^{3/2} − n + O(√n) | Section 1.3 | from Table 2 (c_2 = 6, β_2 = −1; c_3 = 35/2, β_3 = −3) |
| 3 | Rigidity: for large n every branch of every maximiser has one of finitely many optimal stems, with size and leaf counts determined up to bounded errors | Theorem 4.1 | written proof; thresholds effective, not computed |
| 3a | For each fixed d an algorithm computes M_d(n) exactly in time polynomial in log n | Corollary 4.2 | existence proof (fixed-dimension integer programming, Lenstra); not implemented |
| 3b | Fixed radius q ≥ 2: for large n the maximisers among trees of radius q are exactly the diameter-2q maximisers | Section 4 | written proof |
| 4 | Where rigidity begins: for d = 6, 7 every maximiser uses optimal stems only for every n ≥ 10 tested; for d = 8, 9, 10, 11 the last orders with a maximiser using a non-optimal stem are 597, 1034, 288, 289, and none above them up to n = 3000; at d = 8 there are 348 orders n ≤ 596 with no all-optimal maximiser, n = 249 among them | Section 4, "Where rigidity begins" | exact computation (rigidity_onset.py); tested range only |
| 5 | M_8(249) = 215016 (witness: 3 path stems with 19 leaves each and 7 forked stems with 11 per tip) | Section 7 | exact (graph_check.py, claims_check.py, rigidity_onset.py) |
| 6 | Diameter five: explicit M_5(n) and every maximiser for every n ≥ 6; n = 54: unique maximiser, W = 5530 | Theorem 8.1; Section 8 | written proof; exhaustive check n = 6..19 and centre scans (diameter5.py) |
| 7 | Diameter four constants 3 and 11/4 | Section 8 | written proof (with Wagner) |
| 8 | Large-height constructions: 2√c_h − KΘ^{3/2} ∈ [−0.4822, −0.4221] for h = 1..8; h = 1 remainder −0.48103 | Theorem 5.1 and the sentence after it | exact (claims_check.py); constructions to h = 10^18 (continuum_check.py) |
| 9 | Remark 6.3: at d = 18, 2√c_8/18^{3/2} ≈ 0.433, about 9% below κ; at d = 9, n = 3000 the normalised deficit is 0.313 and the three-term error about 10.7√n | Remark 6.3 | exact or double-precision (claims_check.py, forest_replay.py) |
| 10 | Open: graphs (odd d differs; even d conditional on Cambie's question), linear regime d/n → ρ, third-order term, shape stability, explicit thresholds | Section 9 | open |

## Evidence

| Check | Script | Output | Scope |
|---|---|---|---|
| c_h, β_h for h ≤ 8 (Table 2) | [code/coefficients.py](code/coefficients.py) | [results/coefficients.txt](results/coefficients.txt) | exact rationals |
| Independent recursion h ≤ 6; M_d(249), d = 4..9; diameter five on all trees ≤ 15 vertices | [code/graph_check.py](code/graph_check.py) | [results/graph-check.txt](results/graph-check.txt) | exact |
| Theorem 8.1 at n = 54; exhaustive n = 6..19 and centre scans to 5000 | [code/diameter5.py](code/diameter5.py) | [results/diameter-five-54.txt](results/diameter-five-54.txt), [results/diameter-five-check.txt](results/diameter-five-check.txt) | exact |
| Rounded binary constructions of Theorem 5.1 to h = 10^18 | [code/continuum_check.py](code/continuum_check.py) | [results/mesh-check.txt](results/mesh-check.txt) | exact costs, high-precision bounds |
| Calibration and split excess on 66,049 pairs | [code/calibration_replay.py](code/calibration_replay.py) | [results/calibration-replay.txt](results/calibration-replay.txt) | double-precision sanity scan |
| Exact maxima d = 4..9 by a forest recursion | [code/forest_replay.py](code/forest_replay.py) | [results/forest-replay.txt](results/forest-replay.txt) | exact integers (numpy) |
| Every Section 5 constant and inequality (split identity, α = 1/7, f′, K, f(1) = 19/14 > K, f(√2) > K, √2 + 1/√2 > 3K/2, the cubic, the bracket) | [code/calibration_certificate.py](code/calibration_certificate.py) | [results/calibration-certificate.txt](results/calibration-certificate.txt), [.json](results/calibration-certificate.json) | exact sympy |
| Every other quoted number | [code/claims_check.py](code/claims_check.py) | [results/claims-check.txt](results/claims-check.txt), [.json](results/claims-check.json) | exact where stated |
| Rigidity onset d = 6..11, n ≤ 3000 | [code/rigidity_onset.py](code/rigidity_onset.py) | [results/rigidity-onset.txt](results/rigidity-onset.txt), [.json](results/rigidity-onset.json) | exact integer DP |
| Output comparison under the declared policy | [ci/compare_outputs.py](ci/compare_outputs.py) | CI | tokens exact; decimals within 1e−12 |

Numbers quoted on the release page and in the audio: κ ≈ 0.4775; Cambie's bracket 0.4714 and 0.4833 (gap about 2.5
percent); the ratio 1/4; the diameter-8 expansion with √70; M_8(249) = 215016; M_5(54) = 5530; exact computations to 3000
vertices for diameters 6 to 11. All are proved or in the recorded output.

## Limits

Trees only. κ is the leading coefficient in the joint regime; lower-order terms there and the regime d/n → ρ > 0 are
open. Thresholds of Theorems 1.2 and 4.1 are effective but not computed; Corollary 4.2 is not implemented. The scripts
check identities, constants and finite cases; the proofs carry the general claims. Prior-art searches were of limited
scope.

## Replay and records

Replay commands and comparison policy: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt),
[REPLAY_RECEIPT.md](REPLAY_RECEIPT.md), CI [.github/workflows/replay.yml](.github/workflows/replay.yml). Review:
[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json).
Bibliography: [refs.bib](refs.bib). Dependencies: [requirements.txt](requirements.txt). Licences:
[LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff). Hashes: [MANIFEST.sha256](MANIFEST.sha256).
