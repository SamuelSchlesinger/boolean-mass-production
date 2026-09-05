# Exponential-Range Mass Production of Boolean Functions

This repository contains the manuscript *Exponential-Range Mass Production of
Boolean Functions: Local recovery, disjoint scheduling, and bounded
congestion* by Samuel Schlesinger.

[Read the current manuscript](main.pdf).

The paper proves that, for every fixed `0 <= gamma < 1`, every Boolean
function on `n` bits can be evaluated on as many as `2^(gamma n)` independent
inputs by a circuit of size `O_gamma(2^n / n)`.

The asymptotic coefficient is at most
`1 / (1 - gamma) + o_gamma(1)`. A deterministic nonuniform scheduler uses
`~O_ell(t q)` gates to select globally disjoint recovery sets, so the direct
proof evaluates each resource once. High-rate lifted codes and packing into
several smaller codes give a resource count of `(1 + o(1)) 2^p`.
Appendix C explains the exact accounting used in the formalization:
request identity, inactive slots, resource-bank padding, whole field blocks
at every input length, and the final real-rate quantifiers.

The scheduler's small fixed menus are proved to exist for every input batch.
An efficient uniform algorithm to construct those general menus remains open
here. Both upper-bound variants are formally proved in the pinned Lean
companion.

For a first reading, the introduction explains the sharing obstacle and the
coefficient calculation, and Section 3 works through two independent requests.
The notation and codeword/resource tables support the direct proof in
Sections 4-8. Sections 9-10 compare earlier work and discuss open problems.
Appendix A gives the explicit recursive construction, Appendix B supplies
gate-level implementation details, and Appendix C connects the argument
with the Lean formalization.

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
- `scripts/linear_scheduler.py` implements fixed-menu evaluation with record
  sorting networks and a small exact high-rate code.
- `scripts/check_improvements.py` checks the combinatorial and implementation
  invariants, including exhaustive small cases and end-to-end recovery.
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

Run the dependency-free exact checks with:

```sh
python3 scripts/check_improvements.py
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
