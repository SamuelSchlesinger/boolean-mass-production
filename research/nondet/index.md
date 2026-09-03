# Compressing Nondeterminism with Codes and Shared Evaluation

This research corpus supports the standalone note `nondet.tex`. Its purpose is
to determine exactly what the mass-production construction says about a
Boolean relation

```text
f : {0,1}^N x {0,1}^M -> {0,1}
```

and the deterministic existential projection

```text
g(x) = exists y, f(x,y).
```

The final note must distinguish five epistemic levels:

1. elementary statements proved in the note;
2. results imported from the unpublished companion manuscript;
3. previously known results supported by primary sources;
4. conditional reductions whose hypotheses are explicit;
5. open directions that are not claimed as theorems.

## Planned subtopics

- [Exact reductions and baselines](exact-reductions/index.md): models,
  replication, direct synthesis, the imported mass-production corollary,
  identical-suffix sharing, and the distinction between compressing witnesses,
  measurements, and gates.
- [Codes, sketches, and isolation](codes-and-isolation/index.md): exact
  zero-detection maps, code-distance amplification, parity measurements,
  cancellation, isolation, and uniform versus nonuniform choice of sketches.
- [Verifier regimes admitting compression](structural-regimes/index.md):
  actual-witness hitting for dense fibers, refinements by the number or
  geometry of distinct fibers, low witness degree, and Reed-Muller distance.
- [Candidate synthesis routes and barriers](synthesis-barriers/index.md): the
  cost of producing summaries, precise gatewise obstructions, decomposable or
  bounded-width verifiers, joint resource synthesis, and
  multiplication-friendly encodings.
- [Complexity-theoretic context](complexity-context/index.md): consequences,
  limitations, a comparison table, explicit hypothetical simulations, and a
  literature novelty audit.

## Questions the final note must answer

- `[PROVE]` What is the exact envelope of replication, direct synthesis, and
  restricted mass-production bounds?
- `[IMPORTED -> COROLLARY]` Under exactly which fixed-ratio hypothesis does
  `main.tex` batch all `2^M` witnesses?
- `[PROVE]` What does identical-suffix sharing remove, and what
  distinct-resource cost remains?
- `[PROVE]` Does an `f`-dependent linear map with `N+1` rows detect all realized
  nonzero witness fibers?
- `[KNOWN INPUT + PROVE COROLLARY]` How do code distance and isolation relate
  to structured zero tests?
- `[PROVE]` What density or set-system assumptions yield a small fixed set of
  actual witnesses?
- `[KNOWN INPUT + PROVE COROLLARY]` What follows from bounded witness degree?
- `[KNOWN, MODEL-SPECIFIC]` Which verifier representations are closed under
  existential projection or support efficient counting?
- `[CONDITIONAL]` What circuit bound follows from an explicit
  aggregate-evaluation hypothesis?
- `[OPEN]` Can unrestricted parity or counting aggregates be evaluated
  size-sensitively?
- `[REDUCTION REQUIRED]` Which candidate routes imply one another, and with
  what parameter loss?
- `[NOVELTY AUDIT]` Which observations already occur in coding, isolation,
  knowledge-compilation, or simultaneous-realization literature?

## Supplementary code

- [`data/check_finite_claims.py`](data/check_finite_claims.py) exhaustively
  checks small instances of the zero-avoiding sketch bound, Reed-Muller
  distance and information sets, general subspace information sets, and the
  ideal-kernel characterization. It prints six `PASS` lines and then
  `all finite checks passed`.
- [`data/audit_corpus.py`](data/audit_corpus.py) checks ASCII-only Markdown,
  unresolved placeholders, reference definitions, and local link targets. It
  prints the file count and `corpus audit passed`.
- [`sources.md`](sources.md) is the canonical primary-source registry and
  records the boundary on each imported result.

## Known limitations

- The companion mass-production theorem is imported from an unpublished local
  manuscript. Its nondeterministic corollary is valid but is generically
  dominated by direct synthesis on the `N` deterministic variables.
- The exact and approximate parity fingerprints reduce the number of
  measurements, not automatically the number of gates used to form them.
- The exact fingerprint matrix and the density-based hitting set may depend on
  the complete relation. Their existence is nonuniform and does not give a
  polynomial-time compiler from a succinct verifier.
- The fixed-sketch obstruction has universal state-pair quantifiers. It does
  not rule out changing encodings or transition rules specialized to the
  profiles actually reached by one verifier.
- DNNF, bounded-width, low-degree, and dense-fiber results require their stated
  representation or semantic promises.
- No claim of literature novelty is made. The source search locates close
  hashing, sketching, isolation, coding, and knowledge-compilation work but is
  not a substitute for specialist priority review.
