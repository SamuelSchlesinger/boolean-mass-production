# arXiv submission sheet

Use the source archive at
`output/exponential-range-mass-production-arxiv.tar.gz`. It contains only the
single required source file, `main.tex`.

The manuscript includes the Boolean upper bounds and a matching upper and
lower bound for approximate quantum state mass production. The pinned Lean
companion covers the Boolean upper bounds; the quantum arguments are written
proofs outside that formalization. This repository prepares an upload; it
does not record an arXiv submission or identifier. The author still completes the account, license,
preview, and final submission steps below.

## Rebuild the upload

From the repository root:

```sh
./build.sh
python3 scripts/check_improvements.py
python3 scripts/check_quantum.py
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
Exponential-Range Mass Production of Boolean Functions: Local recovery and optimal quantum state preparation
```

Authors:

```text
Samuel Schlesinger
```

Primary category:

```text
cs.CC - Computational Complexity
```

Suggested cross-list: `quant-ph`, for the optimal quantum state preparation
tradeoff. Keep `cs.CC` primary; the Boolean circuit theorem drives the application.

Abstract:

```text
The hardest Boolean functions on $n$ bits require $\Theta(2^n/n)$ gates to evaluate once. Must evaluating the same function on $t$ unrelated inputs cost $t$ times as much? We show that every Boolean function can be evaluated on any $t\le2^{\gamma n}$ inputs using a total of $O_\gamma(2^n/n)$ gates, for every fixed $0\le\gamma<1$. Thus exponentially many evaluations fit within a constant factor of the worst-case cost of one. In the standard AND, OR, NOT basis, our bound is $(1/(1-\gamma)+o_\gamma(1))2^n/n$ gates. Uhlig previously achieved $(1+o(1))2^n/n$ gates for the smaller range $t=2^{o(n/\log n)}$. Our construction encodes shorter restrictions of the function and recovers the requested outputs from disjoint sets of encoded functions. The gate bound includes choosing those sets, evaluating the functions, and routing the answers. The circuits are nonuniform; an efficient algorithm for constructing their fixed scheduling data remains open. A Lean companion verifies the Boolean upper bounds. As an application, we determine the optimal worst-case cost of preparing $t$ copies of a specified $n$-qubit pure state throughout the same range: $\Theta_\gamma((2^n/n)\log_2(t+1))$ elementary Clifford+$T$ gates. The error is at most $1/10$ in trace distance for the entire batch, and scratch qubits are restored to zero. Coherent Boolean evaluation gives the upper bound; a packing and circuit-counting argument gives the matching lower bound.
```

Comments:

```text
33 pages, no figures. Quantum state preparation tradeoff with matching bounds; quantum proofs are not formalized. Lean 4 proofs of the Boolean upper bounds: https://github.com/SamuelSchlesinger/algebraic-circuits/tree/8dd82c96f44dbeeaca31f4cc96c687c6d87d1489
```

Journal reference: leave blank.

Report number: leave blank.

DOI: leave blank.

The abstract above is 1,451 ASCII characters, below arXiv's 1,920-character
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
- Confirm `cs.CC` as the primary category and consider `quant-ph` as the cross-list
  for the quantum state preparation theorem.
- Select the intended license.
- Compile with `pdflatex` under TeX Live 2025.
- Open arXiv's generated PDF and verify that it has 33 pages, identifies
  Samuel Schlesinger, and labels theorem, lemma, proposition, and section
  cross-references correctly.
- Check that the bibliography includes Guo--Kopparty--Sudan,
  Holmgren--Rothblum, Hiltgen--Paterson, Polyanskii--Vorobyev,
  Kretschmer, Huggins--Khattar--Wiebe, and Gosset--Kothari--Wu.
- Confirm that both upper-bound variants reference Lean revision `8dd82c9`,
  including the nonuniform scheduler and sharp real-rate coefficient theorem.
  The quantum result is not included in this formalization.
- Check Appendix C, which explains the cost, padding, and rounding invariants
  extracted from the formalization.
- Check Section 10 for the quantum model, joint-error accounting, and matching
  upper and lower bounds; these results are outside the Lean companion.
- Confirm the acknowledgement to Shreyas Srinivas.
- Submit only after the arXiv preview matches the locally reviewed manuscript.

These instructions were checked against arXiv's official help on
September 4, 2026. Local compilation does not verify the hosted preview or
predict the moderation outcome.
