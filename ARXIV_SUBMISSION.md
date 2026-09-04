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
We study the cost of evaluating one Boolean function on many independent inputs. For $f:\{0,1\}^n\to\{0,1\}$, let $f^{\times t}$ evaluate $f$ on $t$ such inputs. Uhlig showed that $t=2^{o(n/\log n)}$ copies preserve the sharp one-copy asymptotic. We retain the optimal order of growth throughout every fixed exponential range below the $2^n$-copy scale: for every fixed $0\le\gamma<1$, $C(f^{\times t})=O_\gamma(2^n/n)$ for all $t\le 2^{\gamma n}$. The bound is uniform in $f$ and $t$. Using high-rate lifted evaluation codes, we sharpen it to $(1/(1-\gamma)+o_\gamma(1))2^n/n$. The proof uses local coded recovery instead of scanning the whole truth table. An evaluation code gives each requested symbol many affine-line recovery sets. A nonuniform deterministic scheduler selects disjoint recovery sets with $\widetilde O_\ell(tq)$ gates, where $q$ is the field size and $\ell$ is the fixed geometric dimension. Its fixed menus of candidate directions work for every input batch; a forest bound proves their existence, and sorting circuits check all candidates while storing the occupied points only once. Each phase serves half the remaining requests, removing the need for recursive resource evaluation. All gates for schedule selection and routing are counted. The menu construction is existential, not an efficient uniform algorithm. We also retain an explicit greedy scheduler and its recursive proof of the order-of-growth bound, which is the route covered by the Lean companion.
```

Comments:

```text
24 pages, no figures. Lean 4 formalization of the explicit recursive alternative (not the new nonuniform scheduler or leading-coefficient refinement): https://github.com/SamuelSchlesinger/algebraic-circuits/tree/b94cbedb988f5b4aa72be15de80879333c5e4725
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
- Open arXiv's generated PDF and verify that it has 24 pages, identifies
  Samuel Schlesinger, and labels theorem, lemma, proposition, and section
  cross-references correctly.
- Check that the bibliography includes Guo--Kopparty--Sudan,
  Holmgren--Rothblum, Hiltgen--Paterson, and Polyanskii--Vorobyev.
- Confirm that the nonuniform scheduler and leading-coefficient theorem are
  described as written proofs outside the pinned Lean companion's scope.
- Submit only after the arXiv preview matches the locally reviewed manuscript.
