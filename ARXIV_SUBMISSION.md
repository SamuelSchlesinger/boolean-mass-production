# arXiv submission sheet

Use the source archive at
`output/exponential-range-mass-production-arxiv.tar.gz`. It contains only the
single required source file, `main.tex`.

## Metadata

Title:

```text
Exponential-Range Mass Production of Boolean Functions: Local recovery, disjoint scheduling, and bounded congestion
```

Authors:

```text
Samuel Schlesinger
```

Primary category:

```text
cs.CC - Computational Complexity
```

Cross-list: none recommended. The main result is a Boolean circuit-complexity
theorem; the coding ingredients do not make `cs.IT` the primary subject.

Abstract:

```text
We study the cost of evaluating one Boolean function on many independent inputs. For $f:\{0,1\}^n\to\{0,1\}$, let $f^{\times t}$ evaluate $f$ on $t$ such inputs. Uhlig showed that $t=2^{o(n/\log n)}$ copies preserve the sharp one-copy asymptotic. We retain the optimal order of growth throughout every fixed exponential range below the $2^n$-copy scale: for every fixed $0\le\gamma<1$, $C(f^{\times t})=O_\gamma(2^n/n)$ for all $t\le 2^{\gamma n}$. The bound is uniform in $f$ and $t$, but does not preserve Uhlig's sharp one-copy leading constant. The proof uses local coded recovery instead of scanning the whole truth table. An evaluation code gives each requested symbol many affine-line recovery sets. A deterministic scheduler chooses disjoint lines within request groups, so each shorter resource function is queried at most once per group; induction handles the demand across groups. With $k+1$ equal input blocks this gives the copy exponents $1/2,2/3,3/4,\ldots$, which approach one. Unlike a purely combinatorial batch-code guarantee, the schedule is computed from the input addresses and its Boolean gates are included in the circuit bound.
```

Comments:

```text
20 pages, no figures. Accompanying Lean 4 formalization at https://github.com/SamuelSchlesinger/algebraic-circuits/tree/b94cbedb988f5b4aa72be15de80879333c5e4725
```

Journal reference: leave blank.

Report number: leave blank.

DOI: leave blank.

## Processing choices

- Processor: `pdflatex`.
- TeX Live: 2025 is appropriate. The source includes arXiv's documented
  `cleveref` aliases for theorem-like environments.
- Upload the source archive, not `main.pdf`. arXiv will compile the source.
- The source is intentionally identified and names Samuel Schlesinger.

## Author decision still required

Choose the arXiv distribution license in the submission interface. This choice
is intentionally not preselected here: arXiv treats it as irrevocable, and the
repository currently does not declare an open-content license. Do not select a
Creative Commons option unless that is the intended grant.

## Final submission checklist

- Confirm the title, author spelling, and abstract in the metadata preview.
- Confirm `cs.CC` as the primary category and omit a cross-list unless there is
  a specific audience reason to add one.
- Select the intended license.
- Compile with `pdflatex` under TeX Live 2025.
- Open arXiv's generated PDF and verify that it has 20 pages, identifies
  Samuel Schlesinger, and labels theorem, lemma, proposition, and section
  cross-references correctly.
- Check that the bibliography includes Holmgren--Rothblum, Hiltgen--Paterson,
  and Polyanskii--Vorobyev.
- Submit only after the arXiv preview matches the locally reviewed manuscript.
