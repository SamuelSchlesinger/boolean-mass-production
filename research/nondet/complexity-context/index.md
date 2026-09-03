# Complexity-theoretic context: consequences, regimes, and limits

This chapter asks what a circuit bound for

```text
f : {0,1}^N x {0,1}^M -> {0,1},
g(x) = OR over y in {0,1}^M of f(x,y)
```

would mean in standard complexity language.  Its main conclusion is a boundary,
not a collapse: the companion mass-production theorem gives a valid circuit for
`g`, but generic synthesis of the `N`-input function `g` is always the stronger
worst-case upper bound.  The code and hitting-set ideas become genuine
determinization results only in structural regimes where their summaries can be
formed cheaply.

The status tags used below are:

- **[PROVED HERE]** for elementary reductions and parameter comparisons;
- **[IMPORTED]** for the unpublished mass-production theorem in `main.tex`;
- **[KNOWN]** for results supported by the primary references below;
- **[CONDITIONAL]** for an implication with an explicit additional hypothesis;
- **[OPEN]** for a research target, not a claimed theorem.

No statement in this chapter proves `P != NP`, `P = NP`, or a new circuit lower
bound.

## 1. The unconditional envelope

Put

```text
n = N + M,
S = C(f),
L(N) = max over h : {0,1}^N -> {0,1} of C(h),
MP_t(f) = C(f^{x t}).
```

Assume `N>=1`; the case with no deterministic input bits is a single constant
output and can be handled separately.

The circuit model is the fan-in-two basis `{AND, OR, NOT}`, with free fan-out,
free constants, and gate count as size.  The exact reductions are proved in the
[baseline chapter](../exact-reductions/index.md).

**Proposition 1.1 (baseline envelope, proved here).**  For every fixed finite
relation `f`,

```text
C(g) <= min {
  2^M*S + 2^M - 1,
  L(N),
  MP_(2^M)(f) + 2^M - 1
}.
```

The first term hardwires one witness into each of `2^M` copies of `f` and ORs
their outputs.  The second synthesizes `g` directly from its `N`-bit truth
table.  For the third, start with `2^M` independent evaluations of `f`, identify
all deterministic input blocks, hardwire the witness blocks to their distinct
values, and append the same OR tree.  None of these transformations has a
uniform running-time claim.

Classical synthesis gives

```text
L(N) <= (1 + o(1))*2^N/N                         (N -> infinity).
```

Consequently, after suppressing lower-order terms, replication is the stronger
generic bound exactly in the region

```text
2^M*(S+1) << 2^N/N,
```

or, at the exponent level,

```text
M + log_2(S+1) < N - log_2 N - omega(1).
```

Direct synthesis is stronger on the opposite side of this threshold.  Two easy
polynomial regimes are worth keeping separate:

1. If `M = O(log(N+S+1))`, replication is polynomial in the verifier
   description parameters.
2. If `N = O(log(S+1))`, direct synthesis is polynomial in `S`, regardless of
   the number of witness bits.

These are finite-circuit statements.  They do not say that the corresponding
circuits can be found efficiently from a succinct description of `f`.

## 2. What the companion mass-production theorem contributes

**Corollary 2.1 (imported fixed-ratio bound).**  Fix `gamma<1`.  If

```text
M/(N+M) <= gamma,
```

then the companion theorem implies

```text
C(g) <= A_gamma*2^(N+M)/(N+M) + 2^M - 1.
```

Equivalently, one fixed `gamma` works along any parameter sequence for which
the deterministic fraction `N/(N+M)` is bounded below by a positive constant.
If `M/(N+M) -> theta<1`, the high-rate coefficient calculation in the companion
manuscript can be optimized over fixed `gamma>theta`, giving

```text
C(g) <= (1 + o(1))*2^(N+M)/N.
```

**Proposition 2.2 (generic dominance by direct synthesis, proved here).**  Along
the same sequence, direct synthesis gives

```text
C(g) <= (1 + o(1))*2^N/N.
```

The displayed mass-production guarantee is therefore larger by the factor

```text
(1 + o(1))*2^M.
```

This remains a fixed loss `2^M` when `M` is a fixed positive integer and grows
when `M` grows.  For `M=0` the two scales coincide.  This compares two upper
bounds; it is not a lower bound on a particular projection `g`.

The reason is conceptual.  Mass production keeps the full verifier arity
`N+M` in its Shannon scale while sharing work among many evaluations.  Once the
witnesses are existentially discarded, `g` is simply an arbitrary function on
only `N` inputs, and its own truth-table synthesis pays the smaller scale
`2^N/N`.  Thus the companion theorem alone does not improve unrestricted
deterministic circuit complexity for nondeterministic circuits.

The common-suffix observation still matters internally.  All witness branches
use the same `x`, so repeated calls to the same resource function at the same
input can be computed once and fanned out.  What remains can be exponentially
many *distinct* resource functions.  Free fan-out removes call multiplicity,
not the circuit cost of that distinct multi-output map.

## 3. Where structure really improves witness enumeration

Let

```text
F_x = {y : f(x,y)=1},
K   = number of distinct nonempty sets F_x.
```

If `K=0`, then `g` is constant zero and needs no gates.  The rest of this
section assumes `K>=1`.

The [structural-regimes chapter](../structural-regimes/index.md) proves that if
every nonempty fiber has density at least `delta` in the witness cube, then
there is a fixed actual-witness set of size at most one when `delta=1`, and,
when `0<delta<1`, of size

```text
h_delta = min {
  2^M,
  floor(ln K / -ln(1-delta)) + 1
}.
```

It follows exactly that

```text
C(g) <= h_delta*(S+1) - 1.                       (3.1)
```

This beats full replication when `h_delta << 2^M`, and it beats generic direct
synthesis when

```text
h_delta*(S+1) << 2^N/N.                          (3.2)
```

Neither comparison is automatic.  A structural theorem is useful only on the
side of both inequalities relevant to the intended application.

If the fiber set system has VC dimension `v`, the epsilon-net theorem gives an
alternative

```text
h_VC = O((v_bar/delta)*(1 + ln(v_bar/delta))),
v_bar = max(1,v),
```

and the same circuit bound with `h_VC` in place of `h_delta`.  This can replace
the `log K` dependence by a geometric parameter, but the logarithmic dependence
on inverse density cannot be removed for arbitrary bounded-VC set systems.

If every Boolean function `y |-> f(x,y)` has algebraic degree at most `d` over
`F_2`, Reed-Muller distance gives `delta >= 2^(-d)`.  Hence

```text
C(g) <= O(2^d*(log K+1)*(S+1)).                  (3.3)
```

There is also a universal information set, independent of `f`, consisting of
all witnesses of Hamming weight at most `d`.  It gives

```text
C(g) <= (S+1)*sum_(i=0)^d binom(M,i) - 1.        (3.4)
```

Equation (3.3) improves replication when

```text
2^d*(log K+1) << 2^M,
```

and improves direct synthesis when

```text
2^d*(log K+1)*(S+1) << 2^N/N.
```

In particular, merely having `d<M` is not enough: the factors `S` and `log K`
remain part of the comparison.

### Compact bound comparison

All entries suppress fixed-basis constants.  `R` denotes the size of a
structured verifier representation, not necessarily the unrestricted optimum
`S=C(f)`.

| Route | Additional hypothesis | Bound for `C(g)` | When it is a real gain |
|---|---|---:|---|
| Replication | none | `2^M*(S+1)-1` | Baseline; polynomial if `M=O(log(N+S))` |
| Direct synthesis | none | `(1+o(1))*2^N/N` | Baseline; ignores `S` and `M` |
| Companion mass production | `M/(N+M)<=gamma<1` fixed | `A_gamma*2^(N+M)/(N+M)+2^M` | No generic gain over direct synthesis |
| Dense actual fibers | every nonempty fiber has density `delta` | `h_delta*(S+1)-1` | `h_delta<<2^M`; beats direct only if (3.2) holds |
| VC-controlled fibers | density `delta`, VC dimension `v` | `O((v_bar/delta)*log(v_bar/delta)*(S+1))` | Useful when the VC expression is below both baselines |
| Witness degree at most `d` | semantic algebraic-degree promise | `O(2^d*(log K+1)*(S+1))` | Useful when `d+log_2(log K+1) << M` and (3.3) beats direct |
| DNNF | a DNNF of edge size `R` is supplied | `O(R)` | Strong if `R` is below both generic baselines |
| Complete structured d-DNNF | supplied width `w`, size `R` | `2^(O(w))*R` while preserving deterministic structure | Fixed-parameter in `w`, not in unrestricted `S` |
| Linear fingerprints | an `r`-summary circuit of size `B` is supplied | `B+O(r)`, with exact `r<=min(N,2^M)` for `N>=1` | A gain only when `B` itself is small |

The degree row's shorthand `d+log_2(log K+1) << M` only expresses improvement
over the number of verifier copies.  The full gate comparison still includes
`S+1`.

## 4. Decomposability and width: known positive models

The distinction between an arbitrary circuit and a compiled representation is
essential.

**Known fact (DNNF forgetting).**  If `f(x,y)` is supplied as a decomposable
negation normal form, existentially forgetting all witness variables can be
done in linear time in that representation: replace witness literals by true
and simplify.  Decomposability is what prevents an inconsistent conjunction
such as `y AND NOT y` from becoming a spurious accepting branch.  Darwiche's
original DNNF work proves linear-time forgetting and satisfiability
[darwiche99][darwiche99], [darwiche01][darwiche01].  With bounded fan-in, or
with size measured by edges, the resulting DNNF is directly an `O(R)` Boolean
circuit for `g`.

This does **not** imply `C(g)=O(S)` for an arbitrary size-`S` verifier circuit.
Compiling an unrestricted circuit or CNF to DNNF can require exponential size.
The positive statement is representation-sensitive.  Darwiche also gives a
linear-size compilation guarantee for clausal theories of each fixed
treewidth, so fixed-treewidth CNF verifiers form one concrete regime where the
projection is linear in the input representation, with a constant depending
on the width.

There is a second subtlety: plain DNNF is closed under forgetting, but naive
forgetting can destroy *determinism*, which is needed for some counting tasks.
Capelli and Mengel prove that a complete structured d-DNNF of width `w` and
size `R` can be existentially projected in time `2^(O(w))*R`, producing width
at most `2^w` while retaining a deterministic structured representation
[cm19][cm19].  Their lower bounds also show that the structuredness and width
hypotheses cannot simply be dropped from that theorem.  This is a genuine
width-parameterized determinization result, but not a theorem about all
size-`S` circuits.

These results identify the useful hardware or algorithmic invariant: a
decomposition in which subcircuits under an AND use disjoint variable sets, or
a bounded-width state summary that survives projection.  They do not arise
from mass production alone.

## 5. Parity fingerprints, counting, and the aggregate barrier

The [codes chapter](../codes-and-isolation/index.md) proves that, for `N>=1`,
some relation-dependent linear map with at most `min(N,2^M)` output bits
detects zero exactly on all realized witness fibers.  Thus

```text
g(x) = OR_(i=1)^r h_i(x),
h_i(x) = XOR over selected y values of f(x,y),
r <= N+1.
```

This compresses the number of measurements.  It gives a circuit bound only
under the following explicit hypothesis.

**Proposition 5.1 (aggregate-evaluation reduction, proved here).**  Suppose the
chosen `r` parity aggregates can jointly be computed from `x` by a circuit of
size `B`.  Then

```text
C(g) <= B + r - 1.
```

**Proof.**  Append a binary OR tree to the `r` aggregate outputs.  QED.

The missing statement is a useful upper bound on `B` in terms of `S,N,M,r`.
Materializing all fiber bits first only gives roughly `2^M*S` gates, after
which the shorter zero test is cosmetic.

This obstruction has a standard complexity interpretation.  For a uniform
polynomial-size verifier family, the integer aggregate

```text
#f(x) = number of y such that f(x,y)=1
```

is a `#P` computation, while its least significant bit is a `ParityP`
computation.  Valiant's counting framework records the gap between existence
and exact counting [valiant79][valiant79], and Papadimitriou and Zachos study
the corresponding odd-acceptance class [pz83][pz83].

More explicitly, let a polynomial-time nondeterministic machine on `N`-bit
inputs use `M=p(N)` choice bits.  A polynomial-size circuit `f_N(x,y)` checks
one computation path.  Then

```text
XOR_y f_N(x,y)
```

is exactly the machine's odd-acceptance predicate.  Therefore:

- **[CONDITIONAL]** If the *full parity* `XOR_y f_N(x,y)` had polynomial-size
  circuits for every polynomial-size verifier family, then `ParityP` would be
  contained in `P/poly`.
- **[CONDITIONAL]** If a polynomial-time uniform compiler produced those full
  parity circuits from uniformly generated verifiers, then the corresponding
  parity computations would be in `P`.
- **[CONDITIONAL]** A polynomial-size exact integer-count aggregate for all
  such verifiers would analogously place `#P` functions in nonuniform
  polynomial-size arithmetic/Boolean output circuits; a uniform compiler would
  give polynomial-time exact counting.

A generic polynomial-size evaluator for the *chosen fingerprint rows* would
have a different consequence: Proposition 5.1 would compute existential
projection itself, leading to the `NP/poly` consequences in the next section.

These are implications, not impossibility proofs: no unconditional
superpolynomial lower bound for the required unrestricted aggregate circuits
is known.  They explain why propagating a short parity sketch through arbitrary
AND gates would be a major result rather than routine coding algebra.

Unambiguity does not remove this warning.  If every fiber has size at most one,
then `g(x)=XOR_y f(x,y)` exactly, but evaluating that parity can still be hard.
Valiant and Vazirani show through randomized isolation that general SAT reduces
to detecting unique solutions in a precise promise sense [vv86][vv86].  That
theorem is not a circuit upper bound here; it is evidence that `at most one
witness` should not be equated with `easy to find or aggregate the witness`.

## 6. Complexity-class implications of a hypothetical generic compiler

Witness bits are choices made separately for each input `x`; they are not a
single advice string that can simply be hardwired for all inputs.  A circuit
family `f_N(x,y)` of polynomial size with polynomially many witness bits is the
nonuniform verifier model underlying `NP/poly`.  If `f_N` is itself uniformly
generated from a polynomial-time verifier, its projection describes an `NP`
language.

**Proposition 6.1 (size-only generic determinization, conditional).**  Assume
there is a constant `c` such that every relation satisfies

```text
C(exists_y f) <= (N+M+C(f)+1)^c                 (6.1)
```

whenever `M` is polynomially bounded in `N`.  Then

```text
NP/poly = P/poly.
```

In particular, `NP` is contained in `P/poly`.

**Proof.**  Compile the polynomial advice and the polynomial-time verifier for
each input length into a polynomial-size relation circuit `f_N`.  The assumed
bound supplies a polynomial-size deterministic circuit for its existential
projection.  This proves `NP/poly` is contained in `P/poly`; the reverse
containment is immediate by using no witness bits.  QED.

By the Karp-Lipton theorem, the weaker consequence `NP subseteq P/poly` already
collapses the polynomial hierarchy to its second level [kl80][kl80].  It does
not by itself prove `P=NP`, because the resulting deterministic circuits may be
nonuniform.

**Proposition 6.2 (uniform generic determinization, conditional).**  If, in
addition to (6.1), a polynomial-time algorithm maps the description of `f` to
the projected circuit, then `P=NP`.

**Proof.**  For each input length, construct the standard polynomial-size
universal verifier circuit for SAT, run the compiler, and evaluate the
resulting projected circuit on the given formula.  Every step is polynomial
time.  QED.

None of the bounds in Sections 1--4 satisfies (6.1) for arbitrary polynomial
`M`: replication is exponential in `M`, direct synthesis is exponential in
`N`, the mass-production term is exponential in `N+M`, and the structural
bounds impose promises not shared by general NP verifiers.

The easy-witness work of Murray and Williams concerns a different kind of
compression.  Under an assumption such as `NP subseteq SIZE[n^k]`, it proves
that yes-instances have witnesses encoded by circuits of size
`n^(O(k^3))`, and uses this in algorithms-to-lower-bounds arguments
[mw20][mw20].  That is conditional compression of the *description of an
accepting witness*.  It does not construct a deterministic circuit for
`exists_y f(x,y)` for all `x`, and it does not supply the parity aggregates
above.  Valiant's earlier checking-versus-evaluating paper is a historical
source for the broader distinction [valiant76][valiant76]; no theorem from
that paper is used in our finite-circuit bounds.

## 7. Explicit lower-bound transfers and their weakness

The elementary upper bound can be read contrapositively.

**Proposition 7.1 (deterministic-to-nondeterministic lower-bound transfer,
proved here).**  If `C(g)>=L` and `g=exists_y f` with `M` witness bits, then

```text
C(f) >= (L+1)/2^M - 1.
```

**Proof.**  Rearrange `L<=C(g)<=2^M*(C(f)+1)-1`.  QED.

This loses a factor `2^M`, so known modest deterministic lower bounds become
vacuous once the witness budget is large.  It is useful only when `M` is
smaller than the logarithm of the deterministic lower bound one already has.
It is not a route to unrestricted circuit lower bounds by itself.

Morizumi gives two sharper pieces of context for restricted circuits
[morizumi15][morizumi15]:

1. For the basis `U_2` of all binary Boolean functions except XOR and
   equivalence, nondeterministic circuits for parity require exactly
   `3(N-1)` gates, matching deterministic `U_2` complexity.  This is a direct
   gate-elimination lower bound and does not lose `2^M`.
2. Every size-`s` general binary circuit can be transformed by Tseitin
   variables into a nondeterministic 3-CNF with the same `N` actual inputs,
   `s` guess inputs, and size `O(s)`, whose existential projection is the
   original circuit's function.

The second item gives an explicit parameter map

```text
(N actual inputs, deterministic size s)
    -> (N actual inputs, M=s guess bits, nondeterministic 3-CNF size O(s)).
```

Consequently, if one proves that every nondeterministic 3-CNF whose projection
is an explicit function `g_N` has size at least `B(N)`, then every unrestricted
deterministic circuit for `g_N` has size `Omega(B(N))`: a size-`s` circuit would
otherwise yield a size-`O(s)` projected 3-CNF.  This explains why lower bounds
for restricted nondeterministic representations can be powerful.  It does not
turn any upper bound in this note into such a lower bound.

Also note the quantifier trap: every deterministic circuit is a
nondeterministic circuit with `M=0`.  A lower bound against nondeterministic
circuits is automatically at least as hard as the corresponding deterministic
lower-bound task unless additional restrictions make the nondeterministic
model more tractable.

## 8. Approximation must be measured after projection

Approximation of the verifier under the uniform distribution on `(x,y)` does
not automatically approximate its existential projection.

**Proposition 8.1 (projection amplifies joint error, proved here).**  Let `f'`
approximate `f`, let

```text
epsilon = Pr over uniform (x,y) that f(x,y) != f'(x,y),
g'(x)   = exists y, f'(x,y).
```

Then

```text
Pr over uniform x that g(x) != g'(x)
  <= min(1, 2^M*epsilon).
```

The factor `2^M` is tight.

**Proof.**  For every `x` on which the projections differ, at least one pair
`(x,y)` is a disagreement between `f` and `f'`.  Hence the number of bad
`x` values is at most the number of bad pairs.  Divide by `2^N`.  For
tightness, take

```text
f(x,y)  = 1 iff y=0^M,
f'(x,y) = 0.
```

Their joint distance is `2^(-M)`, while `g` is constant one and `g'` is
constant zero, so their projected distance is one.  QED.

The correct positive approximation statements control error directly over
`x`:

- With `r` independent random parity-fingerprint rows, the sketched projection
  has no false positives and misses each fixed yes-input with probability
  `2^(-r)`.  For any fixed distribution on `x`, averaging fixes one
  relation-and-distribution-dependent matrix with false-negative mass at most
  `2^(-r)`.
  This is strong error control but still lacks a generic gate bound for forming
  the parities.
- If every nonempty fiber has density at least `delta`, sample `r` actual
  witnesses and OR their verifier values.  There are no false positives, and a
  fixed yes-input is missed with probability at most `(1-delta)^r`.  Averaging
  again gives a fixed sample with the same distributional false-negative
  bound, now implemented with at most `r*S+r-1` gates.

Thus uniform `(x,y)` approximation, parity-sketch approximation, and
dense-fiber sampling are three different guarantees.  Only the latter two
directly control the error metric relevant to `g`.

## 9. Targeted prior-work and novelty audit

The following audit records what the located primary sources establish and,
equally importantly, what they do not establish for this note.

| Primary source | Established there | Relevance and boundary here |
|---|---|---|
| Valiant 1976 [valiant76] | A foundational checking-versus-evaluating framework | Conceptual antecedent only; not the fixed-arity mass-production reduction or our circuit envelope |
| Valiant 1979 [valiant79] | The `#P` framework and completeness of natural counting problems | Explains why exact witness aggregates can be harder than existence; not an unrestricted circuit lower bound |
| Valiant-Vazirani 1986 [vv86] | Randomized isolation of unique satisfying assignments | Closest classical source for uniqueness/isolation; not an exact generic determinization or a cheap aggregate circuit |
| Darwiche 1999/2001 [darwiche99], [darwiche01] | Linear-time DNNF satisfiability and forgetting; bounded-treewidth compilation | Direct prior art for the decomposable positive regime |
| Morizumi 2015 [morizumi15] | Tight nondeterministic `U_2` parity lower bound and a Tseitin parameter map | Direct prior work on nondeterministic circuit size; model is restricted and conclusions are lower bounds |
| Capelli-Mengel 2019 [cm19] | Width-parameterized quantifier elimination for complete structured d-DNNF, with matching limitations | Direct prior art for the bounded-width positive regime |
| Murray-Williams 2020 [mw20] | Conditional easy-witness lemmas and circuit-lower-bound consequences | Compresses witness descriptions under circuit assumptions; does not eliminate existential quantifiers in arbitrary circuits |

The exact envelope, the factor-`2^M` comparison, Proposition 5.1, the
complexity-class implications in Section 6, and the approximation bound in
Section 8 are elementary deductions assembled here; no novelty is claimed for
them.  The targeted search did not locate a source that combines the
relation-dependent `min(N,2^M)`-row fingerprint with the identical-suffix
mass-production specialization.  That absence is **not** a priority claim: the
linear fingerprint is an immediate universal-hashing argument, and a broader
search of linear sketches, separating hash families, branching programs, and
knowledge compilation would be needed before making any novelty statement.

Valiant's title is particularly easy to overread.  This note does not claim to
resolve the general relative complexity of checking and evaluating.  Likewise,
the Murray-Williams results do not imply that every small verifier has a small
projection unless their substantial hypotheses and parameter losses are
included.

## 10. What would count as a new trick

The present synthesis points to four sharply stated targets.

1. **[OPEN] Size-sensitive aggregate evaluation.**  Given a size-`S` verifier
   and an `r`-row zero-detecting linear map, compute all `r` parities in
   `poly(S,N,M,r)` gates for a nontrivial verifier class substantially broader
   than decomposable or bounded-width circuits.
2. **[OPEN] Succinct actual-witness hitting.**  Under a checkable promise such
   as fiber density or low degree, construct or encode the hitting set from the
   succinct verifier without expanding all `2^(N+M)` values.
3. **[OPEN] Projection-stable representations.**  Find a representation class
   more expressive than current decomposable/width-bounded models for which
   existential projection preserves size up to a controlled parameter loss.
4. **[OPEN] Aggregate lower bounds.**  Exhibit a verifier family for which the
   measurement count is small but every circuit producing the required
   summaries is provably large in a restricted model.

The clean research message is therefore:

```text
Codes can compress the zero test.
Density can compress the actual witness list.
Neither fact generically compresses the gates that form the summaries.
Decomposability, width, or another propagation invariant is the missing bridge.
```

## Local References

<a id="valiant76"></a>

- **[valiant76]** Leslie G. Valiant. "The Relative Complexity of Checking and
  Evaluating." *Information Processing Letters* 5(1):20-23, 1976.
  [doi:10.1016/0020-0190(76)90097-1].

<a id="valiant79"></a>

- **[valiant79]** Leslie G. Valiant. "The Complexity of Enumeration and
  Reliability Problems." *SIAM Journal on Computing* 8(3):410-421, 1979.
  [doi:10.1137/0208032].

<a id="pz83"></a>

- **[pz83]** Christos H. Papadimitriou and Stathis K. Zachos. "Two Remarks on
  the Power of Counting." In *Proceedings of the 6th GI Conference on
  Theoretical Computer Science*, pages 269-276, 1983. [Primary technical
  report].

<a id="vv86"></a>

- **[vv86]** Leslie G. Valiant and Vijay V. Vazirani. "NP Is as Easy as
  Detecting Unique Solutions." *Theoretical Computer Science* 47:85-93, 1986.
  [doi:10.1016/0304-3975(86)90135-0].

<a id="darwiche99"></a>

- **[darwiche99]** Adnan Darwiche. "Compiling Knowledge into Decomposable
  Negation Normal Form." In *Proceedings of IJCAI 1999*, pages 284-289.
  [Primary proceedings PDF].

<a id="darwiche01"></a>

- **[darwiche01]** Adnan Darwiche. "Decomposable Negation Normal Form."
  *Journal of the ACM* 48(4):608-647, 2001. [doi:10.1145/502090.502091].

<a id="kl80"></a>

- **[kl80]** Richard M. Karp and Richard J. Lipton. "Some Connections Between
  Nonuniform and Uniform Complexity Classes." In *Proceedings of STOC 1980*,
  pages 302-309. [doi:10.1145/800141.804678].

<a id="morizumi15"></a>

- **[morizumi15]** Hiroki Morizumi. "Lower Bounds for the Size of
  Nondeterministic Circuits." In *Proceedings of COCOON 2015*, LNCS 9198,
  pages 289-296. [arXiv:1504.06731].

<a id="cm19"></a>

- **[cm19]** Florent Capelli and Stefan Mengel. "Tractable QBF by Knowledge
  Compilation." In *Proceedings of STACS 2019*, LIPIcs 126, Article 18,
  pages 18:1-18:16. [doi:10.4230/LIPIcs.STACS.2019.18].

<a id="mw20"></a>

- **[mw20]** Cody D. Murray and R. Ryan Williams. "Circuit Lower Bounds for
  Nondeterministic Quasi-Polytime from a New Easy Witness Lemma." *SIAM Journal
  on Computing* 49(2):STOC18-300-STOC18-322, 2020.
  [doi:10.1137/18M1195887].

[baseline chapter]: ../exact-reductions/index.md
[valiant76]: #valiant76
[valiant79]: #valiant79
[pz83]: #pz83
[vv86]: #vv86
[darwiche99]: #darwiche99
[darwiche01]: #darwiche01
[kl80]: #kl80
[morizumi15]: #morizumi15
[cm19]: #cm19
[mw20]: #mw20
[doi:10.1016/0020-0190(76)90097-1]: https://doi.org/10.1016/0020-0190(76)90097-1
[doi:10.1137/0208032]: https://doi.org/10.1137/0208032
[Primary technical report]: https://publications.csail.mit.edu/lcs/pubs/pdf/MIT-LCS-TM-228.pdf
[doi:10.1016/0304-3975(86)90135-0]: https://doi.org/10.1016/0304-3975(86)90135-0
[Primary proceedings PDF]: https://www.ijcai.org/Proceedings/99-1/Papers/042.pdf
[doi:10.1145/502090.502091]: https://doi.org/10.1145/502090.502091
[doi:10.1145/800141.804678]: https://doi.org/10.1145/800141.804678
[arXiv:1504.06731]: https://arxiv.org/abs/1504.06731
[doi:10.4230/LIPIcs.STACS.2019.18]: https://doi.org/10.4230/LIPIcs.STACS.2019.18
[doi:10.1137/18M1195887]: https://doi.org/10.1137/18M1195887
