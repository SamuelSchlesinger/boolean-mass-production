# Narrative audit of `nondet.tex`

## Overall verdict

The note has a strong mathematical spine and is already unusually candid about
what the coding idea does and does not prove. The best organizing sentence is
the boxed distinction "few summaries != few gates to produce them"
(`nondet.tex:188-194`). The exact-fingerprint theorem followed by the
ideal-kernel theorem gives the note a real center: first compress the realized
fiber set as information, then explain why that compression does not propagate
through a general verifier for free.

The main revision needed is presentational precision. A reader can reconstruct
the central move, but the note does not yet name it once, in one place, with all
of its quantifiers and its gate-complexity limitation. The overview table also
hides the hypotheses and nonuniform dependence of its rows. Those two issues
make the result look stronger on first reading than it does after Sections 4
and 5. Once they are repaired, this is a coherent standalone theory note rather
than a collection of adjacent observations.

The short proofs are generally in the right place. They make the elementary
claims independently checkable without interrupting the exposition. The two
possible candidates for relocation are the low-degree application and the
dense profile-space accounting, discussed below.

## Must fix

### 1. State the central technical move explicitly and distinguish it from a gate bound

The abstract calls the fiber-code viewpoint useful (`nondet.tex:84-99`), the
overview gives six rows (`nondet.tex:146-185`), and the final section finally
says that common-input branches should be treated as one coded object
(`nondet.tex:970-981`). The actual move is therefore present, but it is diffuse.
It should be unmistakable by the end of the first page.

Add a short named paragraph immediately before or after the box at
`nondet.tex:188-194`, along the following lines:

> **The coding move.** Regard the map `x -> v_x` as a codebook of at most
> `2^N` realized words. Choose an `f`-dependent linear map whose kernel avoids
> every realized nonzero word. This replaces `2^M` branch values by
> `O(log(K+1))` parity aggregates. It is an exact compression of the zero test,
> not yet a smaller circuit, because the aggregates still have to be computed
> from the succinct verifier.

Then point forward in the same paragraph: Theorem 4.1 proves the compression,
Theorem 5.1 rules out universal propagation by one fixed linear sketch, and
Section 6 lists the remaining structural escape routes. This makes the note's
answer to its title question explicit rather than requiring a reader to infer
it from the table.

### 2. Put hypotheses and quantifier dependence into the one-page map

The table at `nondet.tex:146-185` reports summary counts but omits the most
important comparison dimension: when each row applies and what may depend on
the full relation. In particular, a first-time reader cannot see from the table
that the span information set, dense-fiber hitting set, and exact deterministic
fingerprint may all depend nonuniformly on the complete fiber family; the
approximate fixed fingerprint may depend on both `f` and the input distribution;
and DNNF requires a supplied representation. The caveats appear later at
`nondet.tex:376-379`, `416-419`, `543-545`, `589-591`, and `814-835`, but by
then the overview has already set a stronger expectation.

Replace or supplement one existing column with "Hypothesis / dependence." At
minimum, distinguish:

- no promise (enumeration);
- `f`-dependent information set (span);
- density promise plus `f`-dependent hitting set (dense fibers);
- no structural promise, but `f`-dependent masks and unpaid aggregate cost
  (exact fingerprint);
- a fixed distribution or fresh randomness, with unpaid aggregate cost
  (approximate fingerprint);
- a supplied DNNF (forgetting).

This is the single most important safeguard against accidental overclaiming.
It also makes the map genuinely useful as a decision table.

### 3. Make the promised "one page" an actual self-contained page

In the compiled PDF, Section 1 begins halfway down page 2 after the table of
contents, and its table, status paragraph, and disclosure continue on page 3.
Thus "The question and the answer in one page" (`nondet.tex:114-116`) currently
straddles two physical pages. The mathematical overview through the boxed
distinction is close to one page of content; the status and research-process
paragraphs account for much of the spill.

Start the section on a fresh page, and move `Status of the claims` and
`Research-process disclosure` (`nondet.tex:196-211`) to a short front-matter
note, an unnumbered "About this note" section, or immediately after the
one-page overview. Keep the overview itself on one physical page and begin
Section 2 on the next page. This will let a reviewer read or share the map as a
standalone synopsis.

### 4. Remove imprecise language in the headline summary

Several small phrases matter because they occur before the reader has the
formal theorem.

- "Exponentially many witness bits" at `nondet.tex:135-138` is not the right
  object: there are `M` witness bits and `2^M` witness branches or fiber
  coordinates. Say "the `2^M` witness branches" or "the `2^M` fiber
  coordinates."
- The table's `O(log K)` at `nondet.tex:172-175` is misleading at `K=1`, where
  one row is needed although `log K=0`. Use the exact width from
  `nondet.tex:510-513`, or write `O(log(K+1))`.
- The claims "at most `N`" in `nondet.tex:135-138` and "at most
  `min{N,2^M}`" in `nondet.tex:96-99` need the theorem's `N>=1` qualification
  (`nondet.tex:521-522`), or an edge-case-safe formulation.
- Introduce the intended range of `rho` before the approximate row and theorem.
  For example, fix `0 < rho < 1` before using
  `ceil(log_2(1/rho))` at `nondet.tex:176-179` and `600-603`.

These are easy repairs, but leaving them in the abstract and overview weakens
confidence in the more delicate claims.

### 5. Remove companion-manuscript jargon from the standalone argument

The paragraph at `nondet.tex:318-324` invokes a "local-recovery construction,"
"recursive congestion," "suffixes," and "resource functions." None of those
objects is defined in this note. The final two sentences of the paragraph are
excellent, but the route to them assumes detailed knowledge of the companion
paper.

Either replace the paragraph by a self-contained specialization of Lemma 2.2,
or move the construction-specific observation to a footnote. A sufficient
self-contained version is: when all branches share `x`, duplicate requests for
the same restricted function can be coalesced by free fan-out, but up to `2^M`
distinct restricted functions of `x` may remain. Preserve the sharp contrast
between call multiplicity and function multiplicity at `nondet.tex:322-324`.

## Should fix

### 1. Align the title with the proved strength

"Compressing Nondeterminism with Codes and Shared Evaluation"
(`nondet.tex:56-57`) sounds as if a generic shared evaluator is constructed.
The note instead proves information-compression reductions, actual-witness
bounds under structure, and a barrier/open target for aggregate evaluation.
Consider a title such as:

> **Coding Witness Fibers: Exact Reductions and Barriers for Existential
> Circuit Projection**

or

> **Compressing Witness Fibers: Codes, Shared Evaluation, and Its Barriers**

If the present title is retained, add "reductions and barriers" to the subtitle
so the scope is visible before the abstract.

### 2. Separate contribution type from proof status and priority

The status paragraph at `nondet.tex:196-202` admirably distinguishes proved,
imported, known, conditional, and open claims. It does not tell a reviewer what
the paper claims as its contribution. "Proved here" is a provenance label, not
a novelty label. The abstract's disclaimer at `nondet.tex:109-111` is equally
admirable but leaves the positive contribution implicit.

Add a short "Contribution and scope" paragraph saying whether the contribution
is intended to be (a) an expository synthesis and research formulation, (b)
the particular exact realized-fiber fingerprint and ideal-kernel pairing, or
(c) some individually novel theorem. If no theorem-level priority is claimed,
say positively that the contribution is the integrated reduction/barrier
framework and the sharply specified aggregate-synthesis target. If priority is
intended for any theorem, position that theorem individually against the
linear-hashing/sketching literature rather than relying on a blanket novelty
sentence. The hashing references already in the bibliography would naturally
be discussed near Theorem 4.1 (`nondet.tex:508-545`).

### 3. Clarify "distance" as distance from zero, not code minimum distance

Section 3 is titled "dimension and distance" (`nondet.tex:326-345`) and
Subsection 3.2 says "Distance gives..." (`nondet.tex:381-385`), but the theorem
uses the minimum weight only among realized fibers. It does not require the
minimum pairwise distance of `V_f`, or even the minimum distance of the whole
linear span `U_f`. The distinction is eventually made very well at
`nondet.tex:431-435`.

Rename the subsection "Realized-fiber density gives a hitting set" and say on
first use that `delta` is the minimum normalized Hamming distance of a realized
fiber from zero. This will prevent coding-theory readers from importing the
wrong invariant.

### 4. Smooth the exact-fingerprint proof's survivor terminology

At `nondet.tex:525-532`, "killed" alternates between "mapped to zero" and
"removed from the bad survivor set." A final functional that is one on the
remaining bad vectors does not "kill" them; it separates or eliminates them.
Call the maintained set the "unseparated vectors," say a random row leaves half
of them unseparated in expectation, and say the last row separates the final
one or two. The proof is short and elegant once the polarity is uniform.

### 5. Explain the circuit-basis bridge before declaring AND the obstruction

The global model uses `{AND, OR, NOT}` (`nondet.tex:216-218`), while the profile
discussion says XOR and NOT are affine and "AND is the obstruction"
(`nondet.tex:646-657`). A reader will reasonably ask where OR went. State that
OR is `u XOR v XOR (u AND v)` coordinatewise, or first convert to an
`{AND, XOR, NOT}` basis at constant cost. Then qualify the sentence as "AND is
the nonlinear obstruction to propagating one fixed linear fingerprint in this
basis." This aligns the headline with the exact quantifiers later emphasized at
`nondet.tex:730-736`.

Also give a one-sentence operational definition of an ideal before
Theorem 5.1: a subspace `I` is an ideal if `u had v` lies in `I` whenever
`u` lies in `I` and `v` is arbitrary. The proof uses precisely this property.

### 6. Define acronyms and local jargon at first use

- Write "decomposable negation normal form (DNNF)" at
  `nondet.tex:808-815`; the present sentence defines the property but never
  explicitly expands the acronym.
- "Transition tensors" at `nondet.tex:791-798` is not defined. Replace it with
  "the bilinear coefficient tables used by the gate transitions" or define the
  term when the coefficient expansion is introduced.
- Define `B_agg` before, not after, it appears in the final envelope
  (`nondet.tex:891-907`).
- "High-rate" and "normalized leading coefficient" at
  `nondet.tex:262-286` are not defined in this note. Include the one-line
  substitution showing how `1/(1-gamma)` and
  `gamma -> M/(N+M)` yield `2^(N+M)/N`. That calculation is the point of the
  subsection and should not depend on familiarity with the companion paper.

### 7. Consider moving the low-degree application behind the main fingerprint theorem

The path from the fiber definition to the note's central unrestricted
measurement result is interrupted by the Reed--Muller development at
`nondet.tex:437-499`. The material is clean and worth keeping, but it reads as
an application of the dimension/density framework rather than part of the main
conceptual sequence.

For a stronger narrative, move "Low witness degree" after the exact and
approximate fingerprints, or to a short applications section after the AND
barrier. The resulting main line would be:

1. actual-witness compression from fiber structure;
2. unconditional measurement compression of the realized codebook;
3. the gate-propagation obstruction;
4. positive structural applications.

If it stays in place, add one sentence at its start explaining why low witness
degree is the canonical concrete example of the density route.

### 8. Frame profile-space simulation as a tested escape route

Proposition 6.1 (`nondet.tex:743-789`) is useful, but the reader learns only
after its proof that span dimension already gives a stronger nonuniform circuit
bound (`nondet.tex:791-798`). Signal that fact before the proposition. Rename
the subsection to something like "Changing profile spaces: a natural route and
its dominance check," and say that the proposition is retained because it
isolates transition cost and uniform access, not because its dense bound beats
the information-set argument.

If the main note needs shortening, move the coefficient-level proof to an
appendix and retain the statement plus the dominance paragraph in the body.

### 9. Make the complexity-class consequences self-contained

The paragraph at `nondet.tex:921-942` is appropriately conditional, but
`NP/poly` is not defined and "a polynomial-time uniform compiler" does not say
what its input and output guarantees are. Add one sentence defining the
nonuniform verifier interpretation of `NP/poly`, then state that `P/poly` is the
trivial reverse inclusion. Specify that the uniform compiler takes a
polynomial-size verifier circuit and outputs a polynomial-size circuit for its
projection in polynomial time. This turns an appeal to expert shorthand into a
complete implication.

The following statement that a generic aggregate compiler has "strong
nonuniform consequences" (`nondet.tex:937-942`) is too vague to teach anything.
Either name the exact class containment under the exact compiler hypothesis or
trim the sentence and retain only the warning that uniform counting hardness is
not a circuit lower bound.

## Optional refinements

### 1. Give a two-by-two mental model before the six-row table

The results naturally divide along two axes:

- actual witnesses versus mixed parity summaries;
- unconditional information compression versus gate-efficient computation
  under structure.

A two-sentence introduction of those axes would make the larger table easier to
scan. DNNF is currently the only row that is a representation transformation
rather than a summary family, so a separator above that row or a distinct
"structural representation" block would help.

### 2. Add a tiny running example

A two-witness or three-fiber example could carry the reader through the three
levels: an information set selects coordinates, a parity fingerprint mixes
them, and the `D=2` AND collision shows why the mixed sketch does not propagate.
The collision at `nondet.tex:722-728` is already a good endpoint; introducing
the same tiny fiber family in Section 3 would make the algebra less abstract.

### 3. Tighten the final-envelope presentation

Equation (8.1) at `nondet.tex:891-909` is useful, but its mixture of asymptotic
terms and exact quantities makes it look more uniform than it is. A compact
table with columns "promise," "summary count," "gate conclusion," and
"constructibility" could replace either this display or the earlier overview
table. Avoid maintaining two broad envelopes unless each has a distinct job.

### 4. Reduce peripheral literature context if the note must become shorter

The easy-witness and nondeterministic-lower-bound comparison at
`nondet.tex:950-957` is accurate in tone but peripheral to the fiber-code
argument. It can become a short related-work footnote if space or momentum is a
concern. The DNNF comparison is much more directly useful and should remain.

## Strongest passages to preserve

1. **The two-layer answer and the boxed distinction**
   (`nondet.tex:135-144`, `188-194`). This is the clearest pedagogical statement
   of the entire problem, after correcting "witness bits."

2. **The false-start check on mass production**
   (`nondet.tex:274-296`). Showing that the imported bound is worse than direct
   synthesis by `2^M` prevents the reader from mistaking batching for
   determinization. Keep the explicit comparison of upper bounds.

3. **Call multiplicity versus function multiplicity**
   (`nondet.tex:320-324`). This is a memorable formulation of exactly what the
   common input buys. Preserve it after removing the undefined companion-paper
   jargon.

4. **The aggregate-cost reality check**
   (`nondet.tex:547-567`, `625-641`). The field-symbol warning and the exact
   conditional reduction make the informational result honest and useful.

5. **The scope paragraph after the ideal-kernel theorem**
   (`nondet.tex:730-736`). This is exemplary theorem hygiene: it lists the
   quantifiers and all genuine escape routes without weakening the theorem.

6. **The profile-space dominance check**
   (`nondet.tex:791-798`). The willingness to show that a natural construction
   is dominated under its most obvious parameter is analytically valuable.

7. **The projection-error distinction**
   (`nondet.tex:848-886`). The tight `2^M` amplification example turns a common
   approximation mistake into a reusable lesson.

8. **The four-part research program and final hierarchy**
   (`nondet.tex:970-1016`). This is a strong conclusion because every open route
   is constrained by a previously proved reduction or barrier.

## Recommended revised spine

For the cleanest standalone version, use the following order:

1. A literal one-page synopsis naming the coding move, displaying the decision
   table with hypotheses, and stating the gate-compression caveat.
2. Baselines: replication, synthesis, and why independent-input mass production
   is dominated after existential projection.
3. Fiber codes: information sets and realized-fiber density as genuine
   actual-witness circuit bounds.
4. Exact and approximate zero-preserving fingerprints as measurement
   compression.
5. The ideal-kernel obstruction, immediately followed by its quantifier-limited
   escape routes.
6. Positive structure: low witness degree, changing profile spaces, DNNF, and
   bounded width.
7. Approximation metrics, complexity consequences, and the concrete research
   program.

That order makes the note read as one argument: identify the codebook, compress
its zero test, encounter the multiplication barrier, and then ask which
structures make the compressed measurements cheap to evaluate.

## Second-round audit

The major first-round issues are resolved. In the current compiled PDF,
Section 1 occupies exactly page 2, with clean page breaks before and after it.
The revised abstract immediately states the recovery cancellation and the
unpaid joint-resource cost (`nondet.tex:103-118`), the overview names the coding
move and denies a generic gate conclusion (`nondet.tex:197-214`), and the table
now exposes the principal hypotheses and relation dependence
(`nondet.tex:155-195`). The revised title, contribution statement, survivor
terminology, distance-from-zero wording, AND-basis bridge, DNNF definition,
profile-space dominance check, and `NP/poly` definition all address their
first-round concerns.

### Remaining must fix

1. **Repair two malformed cross-references on the one-page overview.** At
   `nondet.tex:203` and `nondet.tex:205`, `Cref{thm:exact-fingerprint}` and
   `cref{thm:ideal-kernel}` are missing their leading backslashes. The compiled
   page visibly prints `Crefthm:exact-fingerprint` and
   `crefthm:ideal-kernel`. Use `\Cref{...}` at the sentence opening and
   `\cref{...}` after "and."

2. **Match the parity-complexity conclusion to its quantifiers.** The paragraph
   at `nondet.tex:1107-1113` begins with a *uniform* verifier family, but then
   says that polynomial circuits for every such parity aggregate imply
   `oplus P/poly = P/poly`. A bound only for uniform verifier families yields
   `oplus P subseteq P/poly`; it does not cover the advice/nonuniform verifiers
   in `oplus P/poly`. Either weaken the conclusion to that containment, or
   explicitly assume the aggregate bound for every polynomial-size nonuniform
   verifier family, in which case `oplus P/poly subseteq P/poly` follows and
   the reverse inclusion is trivial. As written, the sentence overclaims its
   stated premise.

### Remaining should fix

1. **Make the recovery-boundary move self-contained on the overview page.** The
   abstract explains it well, but the actual one-page synopsis merely says that
   Proposition 4.4 "identifies a common-input cancellation trick"
   (`nondet.tex:203-206`). Replace that phrase with one compact operational
   sentence: representing each fingerprint parity by local-recovery equations
   cancels resource coordinates used an even number of times, leaving a
   symmetric-difference boundary whose joint evaluator is still charged. This
   will make the title's "shared-evaluation trick" understandable from page 2
   alone, without waiting until `nondet.tex:685-775`.

2. **Finish the dependency information in the approximate table row.** The row
   at `nondet.tex:185-188` says "fixed input distribution or fresh randomness,"
   but it does not distinguish the two quantifier orders proved later. For a
   fixed distribution, the deterministic mask obtained by averaging may depend
   on both `f` and `mu`; for pointwise randomized error, fresh masks are sampled
   per evaluation (`nondet.tex:633-660`). State that distinction in the
   hypothesis cell and include `0 < rho <= 1`, so the supposedly standalone
   page defines every parameter it uses.

3. **Remove the front-matter widow after the table of contents.** In the
   compiled PDF, "Scope, contribution, and research process" begins at the
   bottom of page 3, and its first paragraph breaks so that page 4 starts with
   the two words "of priority." This comes from `nondet.tex:217-228`. Start the
   unnumbered scope section on a fresh page after the contents, or otherwise
   keep its first paragraph together.

4. **Qualify the approximation subsection title.** "One-sided approximation
   needs only constant width" at `nondet.tex:628` is true for a fixed target
   error, while the theorem's width is `ceil(log_2(1/rho))`. A title such as
   "One-sided approximation needs width only logarithmic in the target error"
   or "Width depends only on target error" is exact even when `rho` varies with
   the parameters.

Final delta check: the current rebuilt PDF resolves every must/should item above, keeps Section 1 literally on one page, and has no remaining narrative or layout blocker.
