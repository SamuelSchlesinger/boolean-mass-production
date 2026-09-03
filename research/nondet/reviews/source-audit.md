# Source, attribution, and provenance audit of `nondet.tex`

## Verdict

I found no fabricated bibliography entry and no citation key that fails to
resolve. The note cites 18 distinct works, and the author, title, venue, year,
page, and DOI or URL data are consistent with the source registry and the
primary records checked during this audit. The imported mass-production
theorem and its leading coefficient also match the current local companion
manuscript.

The note is not yet clean enough to make its present source-status declaration.
There are two errors to fix, four source-scope items that need explicit
verification or support, and several positioning improvements. Most important:

1. the epsilon-net display is false for legitimate values of its stated
   parameters;
2. the status legend says that known, conditional, and open statements are
   explicitly marked, but most of them are not;
3. the DNNF compilation-cost and weighted-counting sentences need sources that
   actually establish those claims; and
4. the exact fingerprint theorem should be situated next to standard linear
   hashing rather than leaving three relevant works uncited in the bibliography.

These are repairable. I found no citation problem that undermines the central
self-contained proofs.

## Audit boundary and method

I checked every `\cite{...}` occurrence in `nondet.tex` against
`research/nondet/sources.md` and the five authored corpus chapters. For claims
whose scope was not clear from the corpus, I checked the linked primary paper
or official publication record. I also compared the imported statements with
the current `main.tex` rather than treating the bibliography entry as evidence.

This is a source and attribution audit, not a second proof audit. I flag a
mathematical issue below only where it changes what the cited theorem actually
supports.

## Error

### E1. The displayed VC epsilon-net bound is not true over its stated range

Location: `nondet.tex:383-429`, especially `nondet.tex:421-425`.

The note states

```text
O((v/delta) log(1/delta)).
```

No restriction such as `v >= 1` and `delta <= 1/2` accompanies the display.
As written, it gives zero when `v=0`, even though a nonempty set system of VC
dimension zero can require one hitting point. It also tends to zero as
`delta -> 1` and is literally zero at `delta=1`, while the preceding theorem
explicitly allows that endpoint.

Haussler and Welzl do support the standard epsilon-net dependence, under the
usual positive-dimension and epsilon-range conventions. A safe all-parameter
form for this note is, for example,

```text
v_bar = max(1,v),
O((v_bar/delta) * (1 + log(1/delta))).
```

Alternatively, state the familiar formula only for `v >= 1` and
`0 < delta <= 1/2`, and handle the other cases separately. The corpus already
used a guarded form in `research/nondet/structural-regimes/index.md`.

Primary record: [Haussler--Welzl, 1987](https://doi.org/10.1007/BF02187876).

### E2. The source-status legend does not describe the actual document

Location: `nondet.tex:196-202`.

The paragraph says that DNNF, width, and coding facts are marked `known`, and
that candidate constructions are explicitly marked `conditional` or `open`.
In the current source, the only actual `known` marker is the DNNF proposition
at `nondet.tex:814-819`; no theorem, proposition, or paragraph is marked
`conditional` or `open`. The VC theorem invocation (`nondet.tex:421-429`),
small-bias discussion (`nondet.tex:608-613`), multiplication-friendly-code
discussion (`nondet.tex:800-806`), conditional aggregate reduction
(`nondet.tex:625-641`), and research targets (`nondet.tex:970-1000`) are not
marked in the promised manner.

Either apply the status labels consistently, or replace the legend by a
literal description of the organization. Until then, the note's provenance
claim is false even though the prose usually makes the epistemic status clear.

## Needs verification or stronger support

### N1. The cited Darwiche papers do not by themselves support the implied
unavoidable DNNF blow-up

Location: `nondet.tex:828-835`.

Darwiche's IJCAI paper directly supports linear-time forgetting and a
`2^O(k)`-by-linear compilation upper bound for clausal theories of bounded
interaction-graph treewidth. It does not, in the nearby citation as currently
used, establish the stronger reading that a small arbitrary circuit can
*require* exponentially large DNNF.

If `can be exponentially expensive` means only that the general compilation
algorithm may take exponential time/space, say so. If it means unavoidable
representation blow-up, add a direct lower-bound source. A particularly clean
source is Bova, Capelli, Mengel, and Slivovsky, whose small CNFs require
exponential DNNF size.

Primary sources:

- [Darwiche, IJCAI 1999](https://www.ijcai.org/Proceedings/99-1/Papers/042.pdf)
- [Bova--Capelli--Mengel--Slivovsky, IJCAI 2016](https://www.ijcai.org/Proceedings/16/Papers/147.pdf)

The second source should be added to the registry and bibliography if the
necessity claim remains.

### N2. Weighted model counting is not supported by the citation currently
nearest it

Location: `nondet.tex:838-843`.

The sentence that deterministic smooth DNNF supports bottom-up model counting
and weighted model counting has no direct citation. The citation at the end of
the paragraph is Valiant 1979, which supports the `#P` context, not the
representation-specific weighted evaluation claim. The registry already
contains the appropriate missing source, Chavira and Darwiche 2008, but that
work is absent from the note's bibliography.

Add a citation to a deterministic-DNNF counting source for ordinary model
counting and to Chavira--Darwiche for weighted model counting, or remove the
weighted claim. The authored corpus identifies both sources in
`research/nondet/synthesis-barriers/index.md`.

Primary source: [Chavira--Darwiche, 2008](https://doi.org/10.1016/j.artint.2007.11.002).

### N3. The imported theorem is not independently retrievable from the note

Location: `nondet.tex:198-200`, `nondet.tex:258-290`, and
`nondet.tex:1153-1157`.

The theorem and coefficient are accurately copied from the current
`main.tex:134-150` and `main.tex:1470-1477`. However, the bibliography entry
only says `Unpublished companion manuscript, September 2026` and gives no
stable locator, version, or repository path. An outside reader receiving
`nondet.pdf` alone cannot inspect the only imported technical theorem.

For review, distribute the companion manuscript with this note and say so in
the entry, or provide a stable repository/preprint URL and version date. If the
companion changes, recheck the theorem number, quantifiers, circuit basis, and
coefficient before circulating this note.

### N4. The AI-system names and origin story require author-side provenance

Location: `nondet.tex:204-211`.

These are private process facts and cannot be verified from the research
corpus. Confirm the exact model labels against session metadata. In particular,
`ChatGPT 5.6 Sol through Codex` may conflate the consumer product with the model
name; if the harness identified the model as `GPT-5.6 Sol`, use that exact
label. Likewise confirm that `Claude Fable 5` and `Claude Fable 5.1` are the
actual recorded names rather than informal aliases.

The claim that the author checked all arguments and citations should be
reaffirmed only after the present audit findings and the independent proof
audit have been resolved.

## Positioning

### P1. Cite the close hashing literature where the exact fingerprint appears

Location: `nondet.tex:508-545`.

The theorem is proved in full, so it does not require an external source for
validity. It is nevertheless the most contribution-looking statement in the
note. The source registry correctly describes it as an elementary
zero-avoidance specialization adjacent to universal and linear hashing, and
notes work on stronger sparse-set hashing and separation goals. The
bibliography already contains
`CarterWegman1979`, `AlonEtAl1999`, and `ChenJinWilliams2019`, but none is cited
anywhere in the body.

After the proof, add a sentence such as: the zero-collision argument is a
specialization of standard linear-hashing ideas; the cited works study broader
collision, load, or injectivity goals and are not being credited with the
exact displayed lemma. This both makes the non-novelty posture credible and
explains why those three entries exist.

Primary records:

- [Carter--Wegman, 1979](https://doi.org/10.1016/0022-0000(79)90044-8)
- [Alon et al., 1999](https://doi.org/10.1145/324133.324179)
- [Chen--Jin--Williams, 2019](https://doi.org/10.1109/FOCS.2019.00077)

If this context sentence is not wanted, delete the three uncited bibliography
entries.

### P2. Narrow `bounded-width inputs` in the abstract

Location: `nondet.tex:101-111`, especially `nondet.tex:107-109`.

The cited positive width result is not for arbitrary bounded-width verifier
circuits. It is for supplied complete structured deterministic DNNFs, with a
specific width notion, and the treewidth result is for clausal inputs under a
specified graph measure. Replace `bounded-width inputs` with something like
`supplied decomposable or bounded-width knowledge-compilation
representations`. This matches the scope of Capelli--Mengel.

Primary source: [Capelli--Mengel, STACS 2019](https://doi.org/10.4230/LIPIcs.STACS.2019.18).

### P3. Specify which CNF treewidth and which size is linear

Location: `nondet.tex:828-835`.

`Bounded-treewidth CNFs` is ambiguous because primal/interaction, incidence,
and other graph widths differ. Darwiche's cited statement is for the
interaction graph. Also, `linear ... in the remaining input size` can sound as
though the bound is linear in the formula left after projection. The source
states a bound exponential in the interaction-graph treewidth and linear in
the original clausal theory size.

A source-faithful form is:

```text
A CNF F of interaction-graph treewidth k compiles to DNNF in
2^O(k) |F| time and size (under the source's edge-size convention).
```

### P4. Qualify the open-problem language as internal to this framework

Location: `nondet.tex:970-1000`, especially `nondet.tex:970` and
`nondet.tex:996-1000`.

The registry explicitly says that the targeted search is not a specialist
priority review. Against that boundary, `a new technical target` and
`lower bounds ... remain open` can be read as global literature claims. Prefer
`a technical target for this approach` and `are not resolved here` or
`remain open within this framework`. The final sentence at
`nondet.tex:1014-1016` is already appropriately local (`left by this note`).

### P5. Make the local-recovery attribution precise

Location: `nondet.tex:318-324`.

The common-suffix conclusion is the note author's specialization of the
companion construction, not a theorem stated in that manuscript. The argument
is documented in `research/nondet/exact-reductions/index.md`, and it is
plausible when the coded prefix is the witness block and the suffix is `x`.
Say `Specializing the local-recovery construction of ... with the witness
block as prefix...` and cite the relevant section/proposition of the companion
manuscript. This avoids making the companion citation appear to contain the
new collapse observation verbatim.

### P6. The manual bibliography contains three uncited entries

Location: `nondet.tex:1031-1036`, `nondet.tex:1045-1050`, and
`nondet.tex:1060-1065`.

`AlonEtAl1999`, `CarterWegman1979`, and `ChenJinWilliams2019` never occur in a
`\cite`. Their metadata is sound, but a hand-built bibliography prints them
anyway. Cite them for the carefully bounded context in P1 or remove them.

## Optional improvements

### O1. Repair the `log K` shorthand at `K=1`

Location: `nondet.tex:91-99` and `nondet.tex:172-179`.

The exact theorem correctly uses `max(1, ceil(log_2 K))`, but the abstract says
`about (log K)/delta` and the table says `O(log K)`. Use `log(K+1)` or add the
constant term. This is not a source failure, but it prevents the overview from
contradicting the exact edge case.

### O2. Add the publication DOI for Morizumi

Location: `nondet.tex:1117-1122`.

The arXiv link is valid and the cited claims are present in Sections 3 and 4 of
that manuscript. The published COCOON version also has DOI
[10.1007/978-3-319-21398-9_23](https://doi.org/10.1007/978-3-319-21398-9_23).
Adding it would make the otherwise complete conference entry easier to check.

### O3. State the DNNF size convention

Location: `nondet.tex:814-835`.

Darwiche measures DNNF size by edges. The note's global Boolean-circuit model
counts fan-in-two gates. These conventions agree within a linear conversion,
but `size T` should say whether `T` is edge size or gate size. The proposition
only claims linear asymptotics, so no theorem changes.

### O4. Historical precision for Karp--Lipton

Location: `nondet.tex:929-934`.

The implication `NP subseteq P/poly => PH collapses to its second level` is
standard and the STOC citation is the canonical Karp--Lipton source. If the
note wants exact historical attribution, call it the Karp--Lipton theorem with
the usual Sipser refinement, or simply state `the Karp--Lipton theorem implies`
rather than making the paper itself sound like the only source of the final
form. This is optional and does not affect correctness.

## Citation-by-citation disposition

| Citation in `nondet.tex` | Nearby use | Disposition |
|---|---|---|
| `Schlesinger2026` | imported exponential-range theorem, coefficient, and local-recovery context (`:198-200`, `:260-271`, `:318-324`) | The theorem and coefficient match current `main.tex`; make the manuscript retrievable and present the common-suffix step as this note's specialization. |
| `FrandsenMiltersen2005` | sharp standard-basis synthesis upper bound (`:222-229`) | Supported. Its abstract explicitly gives the upper bound for `{not,and,or}`; metadata and DOI are correct. |
| `Lupanov1958` | origin of the synthesis method (`:227-229`) | Supported as historical attribution; official journal metadata matches. |
| `HausslerWelzl1987` | VC epsilon-net size (`:421-429`) | The theorem is relevant, but the note's unguarded displayed formula needs E1's endpoint repair. |
| `Muller1954`, `Reed1954` | Reed--Muller code origin (`:439-442`) | Supported. The weight and information-set claims used later are proved in the note rather than imported. Metadata and DOIs match the primary records. |
| `KannanEtAl2018` | broader `F_2` linear-sketch framework (`:600-605`) | Supported as context, not as the source of the note's exact finite-realized-set theorem. |
| `Gavinsky2025` | randomized-versus-deterministic parity-query contrast for OR (`:600-605`) | Supported; the paper's Claim 6 gives constant randomized parity-query complexity and deterministic complexity `D` for OR. A 2026 correction only adds funding information and does not affect the cited result. |
| `NaorNaor1993` | small-bias sample spaces for nearly unbiased nonzero parities (`:608-613`) | Supported. The note correctly says seed length/randomness is reduced, not aggregate gate cost. |
| `ValiantVazirani1986` | isolation comparison (`:615-623`, `:944-948`) | Supported. The note accurately distinguishes random constraints on witnesses from parity measurements of characteristic vectors. |
| `CascudoEtAl2012` | multiplication-friendly-code terminology (`:800-806`) | Supported as a candidate analogy. The paper embeds a smaller extension-field algebra into a longer base-field representation; the note correctly denies that it compresses the full witness algebra. |
| `Darwiche1999`, `Darwiche2001` | DNNF forgetting and bounded-treewidth compilation (`:814-835`) | Forgetting and the interaction-treewidth upper bound are supported. They should not carry the unavoidable-blow-up claim without N1's extra lower-bound source. |
| `CapelliMengel2019` | width-parameterized projection and limitations (`:833-836`) | Supported for complete structured d-DNNF: time `2^O(w)|D|` and output width at most `2^w`, with lower bounds on weakening the structural hypotheses. Narrow the abstract as in P2. |
| `Valiant1979` | exact counting/#P context (`:838-843`, `:937-942`) | Supported for counting-complexity context. It is not the source for weighted evaluation on smooth deterministic DNNF; see N2. |
| `KarpLipton1980` | conditional PH collapse (`:921-935`) | Supported in the standard Karp--Lipton sense; the note correctly labels the consequence conditional. |
| `MurrayWilliams2020` | easy-witness comparison (`:950-953`) | Supported. The primary abstract states conditional small witness circuits for each yes-instance, not one projected circuit for all inputs. |
| `Morizumi2015` | restricted-basis nondeterministic lower bounds and Tseitin 3-CNF map (`:953-957`) | Supported. The paper proves the `3(n-1)` nondeterministic `U_2` parity lower bound and states the size-`O(s)`, `s`-guess-input 3-CNF conversion. |
| `AlonEtAl1999`, `CarterWegman1979`, `ChenJinWilliams2019` | bibliography only | Real and relevant neighboring works, but currently uncited; resolve through P1/P6. |

## Imported versus proved claims after the audit

- Imported from another manuscript: only the mass-production theorem, its
  high-rate coefficient, and construction context at `nondet.tex:258-324`.
- Known external inputs: standard one-copy synthesis, epsilon-nets,
  Reed--Muller terminology/origin, linear-sketch and small-bias context,
  isolation, multiplication-friendly codes, DNNF results, counting context,
  Karp--Lipton, easy witnesses, and Morizumi's lower-bound/Tseitin results.
- Proved in this note: the envelope and common-input collapse, information-set
  and dense-fiber corollaries, the Reed--Muller facts actually used, exact and
  approximate fingerprints, the ideal-kernel classification, profile-space
  simulation, projection-error amplification, and elementary complexity
  reductions.
- Conditional or open: any gate-efficient evaluator for selected aggregates,
  changing-code constructions beyond the stated profile-space bound, succinct
  construction of relation-dependent hitting sets, and stronger restricted
  lower bounds.

That boundary is substantively sound. The document should make its visible
status markers conform to it before review circulation.

## Second-round source audit

### Needs verification: use the official OpenAI model name

Location: `nondet.tex:243-248`, especially `nondet.tex:246`.

The revision resolves every mathematical, citation-scope, bibliography, and
novelty-positioning issue from the first audit. The recovery-boundary lemma and
proposition are correctly marked `proved here`; the companion is cited only
for its Section 4 affine-line recovery identity; the new circuit consequence
is explicitly conditional on a cheap joint evaluator; and no literature
priority is claimed for the elementary identity. The Chavira--Darwiche entry
and use are accurate, the Morizumi publication DOI and pages are accurate, and
all 22 bibliography entries are now cited, with no unresolved citation key.

One provenance label remains imprecise. OpenAI calls the model
`GPT-5.6 Sol`, not `ChatGPT 5.6 Sol`; its official documentation separately
identifies ChatGPT and Codex as products through which GPT-5.6 is available.
Unless the retained session metadata literally displays the latter string,
change `ChatGPT 5.6 Sol through Codex` to `GPT-5.6 Sol through Codex`.
Anthropic's official materials do confirm the names `Claude Fable 5` and
`Claude Fable 5.1`. Actual use of these systems and the ChatGPT.com origin
story necessarily remain author-attested process facts.

Primary records:

- [OpenAI, GPT-5.6 in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-56-in-chatgpt/)
- [Anthropic, Claude Fable](https://www.anthropic.com/claude/fable)

Final delta check: the official `GPT-5.6 Sol` name and alphabetical
bibliography reorder resolve the last issue without changing citation scope,
so the final source and provenance verdict is clean with no remaining blocker.
