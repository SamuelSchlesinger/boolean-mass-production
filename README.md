# Exponential-Range Mass Production of Boolean Functions

This repository contains the manuscript *Exponential-Range Mass Production of
Boolean Functions: Local recovery and optimal quantum state preparation*
by Samuel Schlesinger.

[Read the current manuscript](main.pdf).

The paper proves that, for every fixed `0 <= gamma < 1`, every Boolean
function on `n` bits can be evaluated on as many as `2^(gamma n)` independent
inputs by a circuit of size `O_gamma(2^n / n)`.

The asymptotic coefficient is at most
`1 / (1 - gamma) + o_gamma(1)`. A deterministic nonuniform scheduler uses
`~O_ell(t q)` gates to select globally disjoint recovery sets, so the direct
proof evaluates each resource once. High-rate lifted codes and packing into
several smaller codes give a resource count of `(1 + o(1)) 2^p`.
The scheduler's small fixed menus are proved to exist for every input batch.
Efficient deterministic construction of those menus remains open here.
Both Boolean size-only upper-bound variants are formally proved in the
pinned Lean companion. The depth, randomized-construction, quantum,
local-encoding, and lower-bound results below are written proofs outside
that companion.

The simultaneous bound attains `O_gamma(2^n/n)` gates and `O_gamma(n)` depth
throughout the same range. It uses the geometric slack to leave
an exponentially small fraction of requests unfinished per phase, giving a
constant number of phases. Holmgren and Rothblum's low-depth sorting theorem
implements each phase in linear depth. This refinement does not preserve the
sharp leading coefficient.

Given the full truth table, the proof yields a randomized algorithm to
construct circuits with these size and depth bounds in time polynomial in `2^n`.
With probability at least `1 - 2^(-n)` over construction, its output circuit
is exact on every input batch. The randomness selects fixed scheduling
menus; the algorithm does not certify their correctness.

The quantum application determines the optimal worst-case total gate count
for preparing `t` copies of a specified `n`-qubit pure state:
`Theta_gamma((2^n/n) log2(t+1))`, uniformly for `1 <= t <= 2^(gamma n)`.
It uses the fixed finite Clifford+T gate set, arbitrary connectivity, and
scratch qubits returned exactly to zero. Trace-distance error is at most
`1/10` for the entire batch. The upper bound uses coherent Boolean mass
production; a packing and circuit-counting argument proves the matching
lower bound.

The coherent Boolean evaluation lemma also gives exact batch oracles with
`O_gamma(2^n/n)` gates, `O_gamma(n^2)` depth, and clean scratch space.
This depth bound applies to Boolean evaluation; no corresponding depth
bound is asserted for the full state-preparation construction.

The local hardness amplification section combines Hirahara's amplifier with
our synthesis theorem.
For any fixed `0 <= tau < 1` and `eta > 0`, the resulting encoding of an `n`-bit
function supports `2^(tau*n)` exact evaluations at total size at most
`(1/(1-tau) + eta) 2^n/n`. For some constant `alpha > 0`, approximating the
encoding with advantage `2^(-floor(alpha*n))` preserves the source's
Kolmogorov complexity up to `o(2^n)`. A random source therefore yields
approximate circuit complexity at least `(1-o(1)) 2^n/n`.
Thus functions that are expensive even to predict can support an exponential
batch at the same size order. A short comparison identifies the improved
query range in Hirahara's partial-MCSP reduction; its final approximation
exponent is unchanged by this substitution alone. Broader comparisons and
open directions are kept in the separate
[hardness magnification research note](notes/hardness-magnification.md).

Appendix D proves the restricted lower bound
`(1-gamma) S + gamma W >= (1-o(1)) 2^n/n` for circuits covering all
functions at `t = floor(2^(gamma*n))`, fixed `0 < gamma < 1`, with total
size `S = O(2^n/n)`. They may use at most `2^(mu*n)` modules, fixed
`0 < mu < 1`, with polynomial interfaces and `W` exterior gates.
A negligible exterior forces the coefficient `1/(1-gamma)` within this
architecture. The unrestricted coefficient gap remains open.

For a first reading, the introduction states the Boolean and quantum
results, previews the encoding application, and explains the sharing obstacle.
Section 2 gives the full prior-work
comparison, including recent quantum work, before the constructions.
Section 4 works through two independent Boolean requests; Sections 5-9 give
the code, scheduler, composition, and coefficient arguments. Section 10 gives
the simultaneous size and depth bound and its randomized construction.
Section 11 proves the quantum tradeoff. Section 12 proves the local hardness
amplification application and briefly relates it to Hirahara's reduction.
Section 13 records a short secure-evaluation consequence and discusses the
leading coefficient and open problems. Appendix A develops greedy scheduling
and the explicit recursive alternative. Appendices B-D give gate-level details,
exact finite accounting used in Lean, and the restricted module lower bound.

## Machine-checked companion

An accompanying [Lean 4 formalization at revision `8dd82c9`](https://github.com/SamuelSchlesinger/algebraic-circuits/tree/8dd82c96f44dbeeaca31f4cc96c687c6d87d1489)
machine-checks both the explicit recursive construction and the complete
nonuniform construction with its improved leading coefficient.
With Lean 4.33.1 and mathlib 4.33.1, the umbrella module
`Algebraic.MassProduction` exposes two corresponding endpoints:

- `BlockInduction.exponentialMassProduction` proves the explicit alternative
  in its rational, discrete-exponent formulation.
- `Nonuniform.realSharpMassProduction` proves the coefficient theorem for
  every real `0 <= gamma < 1` and every `epsilon > 0`, uniformly over all
  functions and positive integer `t <= 2^(gamma*n)` at sufficiently large
  input lengths. The full scheduler, code and packing, raw-input composition,
  parameter estimates, rational approximation, and rounding are included.

Both endpoints use only the standard axioms `propext`, `Classical.choice`,
and `Quot.sound`, with no proof placeholders. The cost charges NOT, AND, and
OR; constant sources and structural wiring are free. The pinned revision was
checked with:

```sh
lake build Algebraic AlgebraicTests --wfail
lake test
lake lint
git diff --check
```

## AI-assisted development and provenance

The project began in an interactive conversation on ChatGPT.com, exported to
the author's computer as a LaTeX document. Later work used Claude Fable 5 and
5.1 through Claude Code and ChatGPT 5.6 Sol through Codex in a series of
interactive sessions. These systems assisted with mathematical experiments,
broad literature searches, and parts of the proof strategy and its internal
constructions; their role went beyond prose editing. The author chose which
directions to pursue, checked and revised the arguments and literature claims,
and takes responsibility for the paper.

## Repository contents

- `main.tex` is the canonical source and defaults to the identified public and
  arXiv version; use `\anonymoustrue` only for a separate double-blind copy.
- `main.pdf` is the checked-in, reproducibly generated identified manuscript.
- `build.sh` builds the PDF and rejects LaTeX warnings.
- `ARXIV_SUBMISSION.md` contains paste-ready metadata and the final submission
  checklist.
- `REVIEW.md` records the improvements, proof boundaries, and validation.
- `notes/hardness-magnification.md` preserves the broader literature comparisons,
  parameter calculations, conditional inverse-bit bound, and research directions
  outside the manuscript.
- `scripts/linear_scheduler.py` implements fixed-menu evaluation with record
  sorting networks and a small exact high-rate code.
- `scripts/check_improvements.py` checks the combinatorial and implementation
  invariants, including exhaustive small cases and end-to-end recovery.
- `scripts/check_quantum.py` checks finite identities used in the quantum proof,
  including scratch-space cleanup on entangled inputs, rotation decomposition,
  error allocation, and tensor-power separation. It is not a formal proof or
  a quantum circuit synthesizer.
- `scripts/package_arxiv.py` recreates the verified source-only submission
  archive and checks arXiv's abstract format and length requirements.
- `.githooks/pre-commit` checks that a staged PDF matches the staged source.

The bibliography is contained in `main.tex`; there is no separate BibTeX
database. Historical exploratory drafts are intentionally omitted from the
publication tree so that this repository has one canonical manuscript.

## Building

The build requires `latexmk`, pdfLaTeX, and the standard LaTeX packages named
in the preamble of `main.tex`.

```sh
./build.sh
```

Run the dependency-free checks with:

```sh
python3 scripts/check_improvements.py
python3 scripts/check_quantum.py
```

The checks include a certified universal two-request menu and fixed sampled
menus in the theorem's slack regime. The sampled menus are tested on specified
batches, not certified universal. Comparator counts concern record networks;
they are not measurements of individual Boolean gates or Python runtime.

The build runs in a temporary directory and replaces `main.pdf` only after a
warning-free compilation. To verify that the checked-in PDF is current without
modifying it, run:

```sh
./build.sh --check
```

To prepare the arXiv upload after these checks, run
`python3 scripts/package_arxiv.py` and follow [the submission guide](ARXIV_SUBMISSION.md).

To enable the optional repository hook:

```sh
git config core.hooksPath .githooks
```

## Status and licensing

This is a research manuscript, not a peer-reviewed publication. No reuse
license has yet been selected; add explicit licenses for the paper and the
build scripts before treating the repository as an openly licensed release.
