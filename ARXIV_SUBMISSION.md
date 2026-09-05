# arXiv submission sheet

Use the source archive at
`output/exponential-range-mass-production-arxiv.tar.gz`. It contains only the
single required source file, `main.tex`.

The manuscript and both Lean upper-bound proofs are complete and locally
validated. This repository prepares an upload; it does not record an arXiv
submission or identifier. The author still completes the account, license,
preview, and final submission steps below.

## Rebuild the upload

From the repository root:

```sh
./build.sh
python3 scripts/check_improvements.py
python3 scripts/package_arxiv.py
```

The packager verifies that `main.pdf` matches the source, checks the metadata
abstract, and creates a deterministic archive containing exactly the current
`main.tex`. The archive can be recreated after cloning; generated archives
are not tracked in Git. The bibliography is inline, and there are no external
figures, custom styles, or BibTeX files to add. The Lean and Python code remain
in the linked repositories, outside the TeX upload.

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
We study the cost of evaluating one Boolean function on many independent inputs. For $f:\{0,1\}^n\to\{0,1\}$, let $f^{\times t}$ evaluate $f$ on $t$ such inputs. Uhlig showed that $t=2^{o(n/\log n)}$ copies preserve the sharp one-copy asymptotic. We retain the optimal order of growth throughout every fixed exponential range below the $2^n$-copy scale: for every fixed $0\le\gamma<1$, $C(f^{\times t})=O_\gamma(2^n/n)$ for all $t\le 2^{\gamma n}$. The bound is uniform in $f$ and $t$. Using high-rate lifted evaluation codes, we sharpen it to $(1/(1-\gamma)+o_\gamma(1))2^n/n$. We encode restrictions of $f$ as shorter resource functions with many affine-line recovery sets. A deterministic nonuniform scheduler chooses disjoint sets, allowing each resource function to be evaluated only once. Its size is $\widetilde O_\ell(tq)$, where $q$ is the field size and $\ell$ is the fixed geometric dimension. The scheduler tests fixed menus of candidate directions and serves half the remaining requests in each phase. The menus work for every input batch; their existence is proved, but no efficient uniform construction is given. All gates for schedule selection, resource evaluation, routing, and decoding are counted. We also retain an explicit greedy scheduler and its recursive proof of the order-of-growth bound. The Lean companion formally verifies both upper-bound variants, including the sharper coefficient.
```

Comments:

```text
27 pages, no figures. Lean 4 proofs of both the explicit recursive and nonuniform variants, including the sharp real-rate coefficient: https://github.com/SamuelSchlesinger/algebraic-circuits/tree/8dd82c96f44dbeeaca31f4cc96c687c6d87d1489
```

Journal reference: leave blank.

Report number: leave blank.

DOI: leave blank.

The abstract above is 1,414 ASCII characters, below arXiv's 1,920-character
limit. Paste the text from this guide rather than from the PDF, which may
introduce unsupported ligatures or Unicode. See arXiv's
[metadata instructions](https://info.arxiv.org/help/prep.html).

## Processing choices

- Processor: `pdflatex`.
- TeX Live: select 2025, the currently documented default. The source includes
  the documented `cleveref` aliases for theorem-like environments. See
  [TeX Live at arXiv](https://info.arxiv.org/help/faq/texlive.html).
- Upload the source archive, not `main.pdf`. arXiv will compile the source.
- The source is intentionally identified and names Samuel Schlesinger.

arXiv accepts compressed TeX archives and asks authors to exclude files not
needed to compile the paper. See its
[TeX submission instructions](https://info.arxiv.org/help/submit_tex.html).

## Submission steps

1. Sign in to the author's arXiv account and start a new submission. Complete
   any account or category-endorsement prompt; first-time category submissions
   may require [endorsement](https://info.arxiv.org/help/endorsement.html).
2. Select `cs.CC`, confirm authorship, and choose the distribution license.
3. Upload the archive above. At **Check Files**, verify `main.tex` as the
   top-level file and `pdflatex` as the processor.
4. Inspect the compilation log and arXiv-generated PDF, then paste the title,
   author, abstract, and comments from this sheet into the metadata form.
5. Complete the final checklist and use **Submit Article** only after the
   preview is correct. Record the assigned identifier and status afterward.

The current [submission overview](https://info.arxiv.org/help/submit/index.html)
describes these upload, file-check, compilation, metadata, and preview stages.

## Author decision still required

Choose the arXiv distribution license in the submission interface. This choice
is intentionally not preselected here: each version's license is irrevocable,
and the repository currently does not declare an open-content license. See
arXiv's [license choices](https://info.arxiv.org/help/license/index.html).

## Final submission checklist

- Confirm the title, author spelling, and abstract in the metadata preview.
- Confirm `cs.CC` as the primary category and omit a cross-list unless there is
  a specific audience reason to add one.
- Select the intended license.
- Compile with `pdflatex` under TeX Live 2025.
- Open arXiv's generated PDF and verify that it has 27 pages, identifies
  Samuel Schlesinger, and labels theorem, lemma, proposition, and section
  cross-references correctly.
- Check that the bibliography includes Guo--Kopparty--Sudan,
  Holmgren--Rothblum, Hiltgen--Paterson, and Polyanskii--Vorobyev.
- Confirm that both upper-bound variants reference Lean revision `8dd82c9`,
  including the nonuniform scheduler and sharp real-rate coefficient theorem.
- Check Section 8.1, which explains the cost, padding, and rounding invariants
  extracted from the formalization.
- Submit only after the arXiv preview matches the locally reviewed manuscript.

These instructions were checked against arXiv's official help on
September 4, 2026. Local compilation does not verify the hosted preview or
predict the moderation outcome.
