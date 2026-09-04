# Exponential-Range Mass Production of Boolean Functions

This repository contains the manuscript *Exponential-Range Mass Production of
Boolean Functions: Local recovery, disjoint scheduling, and bounded
congestion* by Samuel Schlesinger.

[Read the current manuscript](main.pdf).

The paper proves that, for every fixed `0 <= gamma < 1`, every Boolean
function on `n` bits can be evaluated on as many as `2^(gamma n)` independent
inputs by a circuit of size `O_gamma(2^n / n)`.

The revised manuscript strengthens the asymptotic coefficient to
`1 / (1 - gamma) + o_gamma(1)`. A deterministic nonuniform scheduler uses
`~O_ell(t q)` gates to select globally disjoint recovery sets, so the direct
proof needs no recursive resource evaluation. High-rate lifted codes and
packing into several smaller codes remove the previous constant rate and
field-rounding losses.

The scheduler's small fixed menus are proved to exist for every input batch.
An efficient uniform algorithm to construct those general menus remains open
here. The new proofs are written mathematical arguments, not additions to the
pinned Lean formalization.

## Machine-checked companion

An accompanying [Lean 4 formalization at revision `b94cbed`](https://github.com/SamuelSchlesinger/algebraic-circuits/tree/b94cbedb988f5b4aa72be15de80879333c5e4725)
machine-checks the circuit model and the explicit greedy construction through
the equal-block induction, retained as an alternative proof. It does not cover
the new menu scheduler or leading-coefficient theorem.
With Lean 4.33.1 and mathlib 4.33.1, the umbrella module
`Algebraic.MassProduction` exposes the endpoint theorem
`BlockInduction.exponentialMassProduction`. It proves a rational,
discrete-exponent form of the main theorem; the passage to every real
`gamma < 1` uses rational slack and absorbs finitely many initial input
lengths. The pinned revision was checked with:

```sh
lake build --wfail
lake test
lake lint
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

To enable the optional repository hook:

```sh
git config core.hooksPath .githooks
```

## Status and licensing

This is a research manuscript, not a peer-reviewed publication. No reuse
license has yet been selected; add explicit licenses for the paper and the
build scripts before treating the repository as an openly licensed release.
