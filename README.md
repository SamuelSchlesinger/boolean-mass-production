# Exponential-Range Mass Production of Boolean Functions

This repository contains the manuscript *Exponential-Range Mass Production of
Boolean Functions: Local recovery, disjoint scheduling, and bounded
congestion* by Samuel Schlesinger.

[Read the current manuscript](main.pdf).

The paper proves that, for every fixed `0 <= gamma < 1`, every Boolean
function on `n` bits can be evaluated on as many as `2^(gamma n)` independent
inputs by a circuit of size `O_gamma(2^n / n)`. It also records the leading
coefficient delivered by the construction and an extension to approximation.
The manuscript includes a disclosure of the AI-assisted research process.

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
