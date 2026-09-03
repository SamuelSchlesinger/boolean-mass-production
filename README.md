# Exponential-Range Mass Production of Boolean Functions

This repository contains the manuscript *Exponential-Range Mass Production of
Boolean Functions: Local recovery, disjoint scheduling, and bounded
congestion* by Samuel Schlesinger.

[Read the current manuscript](main.pdf).

The paper proves that, for every fixed `0 <= gamma < 1`, every Boolean
function on `n` bits can be evaluated on as many as `2^(gamma n)` independent
inputs by a circuit of size `O_gamma(2^n / n)`.

## Machine-checked companion

An accompanying [Lean 4 formalization](https://github.com/SamuelSchlesinger/algebraic-circuits)
machine-checks the circuit model and the constructive core through the
equal-block induction. It proves a rational, discrete-exponent form of the
main theorem; the passage to every real `gamma < 1` uses rational slack and
absorbs finitely many initial input lengths.

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

- `main.tex` is the canonical source.
- `main.pdf` is the checked-in, reproducibly generated manuscript.
- `build.sh` builds the PDF and rejects LaTeX warnings.
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
