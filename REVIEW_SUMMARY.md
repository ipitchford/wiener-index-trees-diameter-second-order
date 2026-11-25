# Review summary (public, 0.1.0-candidate)

This records the internal review of the candidate: who looked, what they raised, and what was done. It is
AI-assisted internal review, not peer review or independent reproduction.

## What ran

1. **Panel (round 1).** Five Claude reviewer roles (editor, methodology, domain, perspective and devil's advocate) in
   one combined review pass. The methodology role checked the proofs of Sections 2-4, 7 and 8; the domain role
   checked the literature, attribution and novelty against the sources. No critical issue and no proof error was found.
2. **Independent proof audit of Sections 5 and 6** (the calibration lemma, the large-height constant and the joint
   limit), by a separate reviewer. It found no error and listed presentation and rigour items (table below).
3. **Lead checks.** A clean replay of every script, brute-force checks of the rigidity computation over all
   non-isomorphic trees for n = 10..18 and d = 6..9, and a negative control.
4. **Revision round.** One round addressed every item and added two extensions: an exact symbolic certificate of every
   Section 5 constant and inequality (`code/calibration_certificate.py`), and exact computations of where the branch
   catalogue of Theorem 4.1 takes over for diameters 6 to 11 up to 3000 vertices (`code/rigidity_onset.py`).
5. **Verification.** A re-review checked every first-round item against the revised text, and a second proof audit
   checked every rewritten proof; it also checked `rigidity_onset.py` against an independent brute force (n ≤ 20) and
   an independent re-implementation (n ≤ 1000), with no mismatch. All rewritten proofs were found correct; the minor
   wording, notation and docstring items were applied.

No second-model (Astra/Codex) adversarial review took place for this release.

## Sources

Every cited work was obtained and read where the paper relies on it, including Cambie (2020; Theorem 4.8, Lemma 4.1 and
the proof of Theorem 3.4), Cambie's thesis, Plesník (1984; Theorems 2-3 and the opening of Section 3), the survey of
Knor, Škrekovski and Tepeh (Problem 28 and Question 35), Mukwembi and Vetrík, Wang and Guo, Wagner, Stevanović,
Milosavljević and Vukičević (Section 5), Borovićanin et al., Pandey and Ravi, Doyle and Snell, Lenstra and Wiener.
Plesník is credited exactly as the paper words it: he found the minimum and remarked that upper bounds are harder; the
name "Plesník's problem" comes from Cambie and the survey.

## Main objections and dispositions

| Objection | Disposition |
|---|---|
| Correctness | No error was found in round 1, in either proof audit or in the re-review. |
| No plain introduction or roadmap; heavy notation with clashes | Section 1 rewritten context first (problem, what was known with Cambie's Theorem 4.8 displayed, results, idea of proof, roadmap); every section opens with its purpose; a notation table; overloaded symbols renamed. |
| "Matches" overstated in the abstract | Now "matches, to leading order"; subtitle "the sharp second-order constant". |
| Limits too brief | New Section 9: graphs (odd d differs at first order; even d conditional on Cambie's question), the linear regime, lower-order terms, stability of the dyadic shape, thresholds. |
| The exact algorithm read as if implemented | Corollary 4.2 is stated as an existence result and Section 9 says it is not implemented. |
| Rigidity had no demonstrated range, and the order-249 example is not rigid | Extension: exact computations for d = 6..11 and n ≤ 3000 locate where the catalogue takes over in that range (Section 4, "Where rigidity begins"); validated by brute force. |
| Sections 5-6 checked only by model reviewers | Extension: an exact sympy certificate of every Section 5 constant and inequality; the verification status is stated in Section 9. |
| Rigour gaps in Lemma 5.2 and Theorem 5.1 (integration across pieces, rounding of split levels, terminal-load bound) and a terse Lemma 6.1 | Each step written out (absolute continuity, irrationality of the split levels and gaps of at least three, an explicit comparison inequality, the debits of Lemma 6.1). |
| Attribution: Stevanović et al. mis-described; survey missing; Plesník's role | Fixed-radius paragraph rewritten from their Section 5; the survey added; Plesník cited directly from his paper. |
| How close the lower constant is attained; slow convergence | A sentence after Theorem 5.1 (h = 1) and Remark 6.3 with numbers for d = 18 and for d = 9, n = 3000. |
| Check scripts used bare `assert` | Every check raises explicitly and fails under `python -O`; a changed expected value (5530 to 5531) makes `graph_check.py` exit 1. |

## Limits that remain

Trees only; the joint-regime constant is the leading coefficient, with smaller terms and the linear regime open; the
thresholds of Theorems 1.2 and 4.1 are not computed and the algorithm is not implemented. The asymptotic proofs have
been checked by AI-assisted reading only; they have no proof-assistant certificate and have not been refereed.
