# Hostile proof audit of `nondet.tex`

## Verdict

The main mathematical spine is sound: replication, information sets, dense
fiber hitting, Reed-Muller distance, exact and approximate parity
fingerprints, and the ideal-kernel classification all re-derive correctly.
The draft is not yet clean enough to call edge-case complete. I found four
statement-level errors, two proof/accounting gaps, and several smaller scope
issues. All are locally repairable; none invalidates the coding viewpoint or
the main research conclusion.

I used the circuit convention stated at lines 216-218: fan-in-two
`AND/OR/NOT`, free constants, free fan-out, free output designations, and gate
count as size. The finite checker also passes every family it tests, but the
issues below mostly concern cases or basis conventions outside those tests.

## Required corrections

### Error 1: the note silently fails at `N=0`

- **Lines:** 96-99, 135-138, 172-179, 521-522, 891-903.
- **Problem:** The theorem itself correctly restricts
  `r <= min{N,D}` to `N>=1` at line 521, but the abstract and summary table do
  not. If `N=0` and the unique fiber is nonzero, exact zero-testing by a linear
  fingerprint needs one output bit, whereas `min{N,D}=0`. The final envelope
  also contains `2^N/N`, which is undefined at `N=0`.
- **Repair:** State globally that `N>=1` and `M>=0`. Add one sentence that for
  `N=0`, `g` is a single free constant and is handled separately. This is the
  convention already used in the research corpus. Alternatively replace the
  fingerprint bound by `min{max(1,N),D}` in the nonzero-fiber case and isolate
  every occurrence of `2^N/N`.

### Error 2: the combined low-degree bound gives a negative circuit size

- **Lines:** 485-499.
- **Problem:** If `K=0`, then `R=0`, so the displayed minimum has `L_f=0` and
  (3.8) asserts `C(g) <= -1`. In fact `g` is constant zero and `C(g)=0`.
- **Repair:** Precede (3.8) with `If K=0, then C(g)=0. Assume K>=1 below.`
  Under `K>=1`, all four candidate hitting-set sizes are positive and the
  formula is correct. For `d=0`, explicitly assign the density branch the
  value one rather than leaving `0/infinity` implicit.

### Error 3: the ideal-kernel corollary has the same vacuous `K=0` failure

- **Lines:** 698-720.
- **Problem:** When `V_f` is empty, the separation hypothesis is vacuous. Take
  `A=0`, so `H` is empty. Then (5.3) again reads `C(g) <= -1`.
- **Repair:** Either assume `K>=1` in the corollary or split the conclusion:
  if `H=empty`, the hypothesis forces `g=0` and `C(g)=0`; otherwise the stated
  `|H|(C(f)+1)-1` bound holds. The underlying ideal and hitting assertions
  remain correct in both cases.

### Error 4: the profile-space gate count uses a gate absent from its basis

- **Lines:** 764-788, especially 766-775 and 786-788.
- **Problem:** Proposition 6.1 claims its exact count over the basis
  `{AND,XOR,NOT}`, but the final `max{0,k_out-1}` term is an OR tree. OR is not
  one gate in that basis. Already for two coefficient bits, one gate from
  `{AND,XOR,NOT}` cannot compute OR.
- **Repair:** The clean repair is to state the mixed basis as
  `{AND,OR,XOR,NOT}`. Then the displayed count is valid, and replacing every
  XOR by its four-gate `AND/OR/NOT` implementation proves the claimed
  factor-four standard-basis conversion. If the three-gate mixed basis is
  retained, charge an actual OR implementation, for example at most
  `3(k_out-1)` gates via `a OR b = a XOR b XOR (a AND b)`.

### Gap 1: the `O(S k^3+k)` corollary uses the wrong size parameter

- **Lines:** 764-776 and 778-789.
- **Problem:** The exact sums range over the gates of the supplied AND/NOT
  verifier. Their immediate consequence is `O(T k^3+k)`, where `T` is that
  verifier's size. Earlier, however, `S` was fixed to the unrestricted optimum
  `C(f)` at line 125. A supplied AND/NOT verifier need not have `S` gates, so
  the proof does not derive the displayed `O(S k^3+k)` from (6.2).
- **Repair:** Name the supplied verifier size `T` and conclude
  `O(T k^3+k)`. Then add a separate conditional sentence: converting a
  size-`S` standard-basis circuit to AND/NOT costs only a constant factor, so
  the `O(S k^3+k)` form holds if an admissible dimension-`k` family is supplied
  for that converted circuit. Independently, output-span dimension alone
  already gives the stronger witness bound discussed at lines 791-798.

### Gap 2: the VC-dimension formula is not valid at its boundary values

- **Lines:** 421-429.
- **Problem:** `O((v/delta) log(1/delta))` becomes zero when `v=0`, and tends
  to zero as `delta` tends to one, although a nonempty range family still
  needs a point. Standard epsilon-net statements include boundary-safe
  factors or assume `v>=1` and `delta` bounded away from one. The research
  corpus already has a safe formulation.
- **Repair:** Put `v_bar=max{1,v}` and state, for example,
  `O((v_bar/delta)(1+ln(v_bar/delta)))`. Retain the uniform witness-cube
  measure and the common density hypothesis, both of which are correctly
  stated.

## Smaller corrections and clarifications

### Gap: subsequent fingerprint displays implicitly assume `K>=1`

- **Lines:** 508-567 and 625-634.
- **Problem:** The theorem handles `K=0` with a zero-dimensional map, but the
  subsequent field notation would require the nonexistent field `F_{2^0}`,
  and an OR tree on `r=0` outputs makes `B+r-1` negative.
- **Repair:** Insert `For the rest of this section assume K>=1.` before line
  547. Handle `K=0` once as `g=0`. In the summary table, use
  `O(log(K+1))` rather than `O(log K)` so that `K=1` is also literal.

### Exposition: specify the approximation parameter range

- **Lines:** 574-600 and 176-179.
- **Problem:** `ceil(log_2(1/rho))` needs `0<rho<=1`; `rho=0` requires the
  exact theorem, and `rho>1` gives a meaningless negative row count. The
  theorem itself is correct for every integer `t>=0`.
- **Repair:** State `t>=0`, and state the corollary for `0<rho<=1`.

### Exposition: state the Reed-Muller parameter convention

- **Lines:** 439-499.
- **Problem:** The usual code statement assumes an integer `0<=d<=M`. The
  proof remains a weak true bound for `d>M`, but then `2^{M-d}` is fractional
  and `RM(d,M)` is normally identified with the full space. The induction also
  leaves its `M=0` base case implicit.
- **Repair:** Assume `0<=d<=M` without loss of generality, since higher degree
  bounds can be clamped to `M`, and add the one-line base case. This also makes
  the `d=0` convention easier to state.

### Exposition: define DNNF size and the width parameter precisely

- **Lines:** 814-835.
- **Problem:** Linear-time forgetting is correct, but to compare a DNNF of
  size `T` with fan-in-two circuit size, `T` should mean edge size or the DNNF
  should have bounded fan-in. Likewise, `bounded-treewidth CNF` should name the
  graph convention (primal, incidence, or the exact convention of the cited
  compiler); these widths are not interchangeable without parameter losses.
- **Repair:** Add `size is measured by edges` (or bounded fan-in), and state
  the cited `2^{O(w)} |F|` compilation using its precise treewidth convention.
  The basic literal-replacement proof at lines 821-826 is sound.

### Exposition: make asymptotic domains explicit

- **Lines:** 222-229, 274-290, and 891-919.
- **Problem:** The Lupanov expression and the optimized fixed-ratio comparison
  are asymptotic statements as `N` (and hence `N+M`) tends to infinity, not
  finite identities. The derivation of (2.5) also suppresses the added
  `2^M-1` OR tree.
- **Repair:** Say `along a sequence with N+M -> infinity`. Then note that
  `2^M / (2^{N+M}/N)=N/2^N=o(1)` because the fixed-ratio hypothesis forces
  `N->infinity`. Optimizing over fixed `gamma>theta` is valid by the usual
  epsilon/limsup argument; no `n`-dependent invocation of the imported theorem
  is needed.

### Optional: make multi-output complexity explicit

- **Lines:** 217-218 and 231-255.
- **Problem:** `C(h)` is introduced for a Boolean map, then immediately used
  for the multi-output map `f^{x t}`. The intended extension is standard but
  unstated.
- **Repair:** Define `C` for Boolean maps with any finite output length, with
  free output designations. This also makes the identical-call lemma formally
  self-contained.

### Optional: make the uniform compiler premise fully algorithmic

- **Lines:** 923-935.
- **Problem:** The complexity consequences are correct, but `polynomial-
  witness relation` and `polynomial-time uniform compiler` should explicitly
  mean `M<=poly(N)`, polynomial-size verifier descriptions, polynomial output
  size, and polynomial running time in that description.
- **Repair:** State those conditions. Then the conclusions
  `NP/poly=P/poly`, `NP subseteq P/poly`, the Karp-Lipton collapse, and (with a
  uniform compiler) `P=NP` follow exactly as claimed.

## Statement-by-statement re-derivation

### Baselines and mass production

- **Proposition 2.1, lines 234-256: checked.** Hardwiring never adds gates;
  `D=2^M>=1` copies cost `D C(f)` and a binary OR tree costs `D-1`. Restricting
  a circuit for `f^{xD}` after identifying all `x` blocks gives the third
  term. This remains valid for `M=0` and `N=0`.
- **Imported Theorem 2.2, lines 262-272: cross-checked against `main.tex`.**
  Its quantifiers and `A_gamma 2^n/n` bound match the companion theorem, and
  the high-rate limsup coefficient is indeed at most `1/(1-gamma)` there.
  The derivation of (2.5) is correct subject to the asymptotic clarification
  above. The direct-synthesis comparison is explicitly only a comparison of
  upper bounds, as it should be.
- **Identical-call lemma, lines 303-316: checked.** With free fan-out and
  output designations, duplicate copies of the same extensional output can be
  added or deleted at zero gate cost. It does not identify distinct functions.

### Fiber dimension, density, and degree

- **Information-set lemma, lines 349-359: checked, including `R=0`.** A
  rank-`R` generator matrix has `R` independent columns; the empty restriction
  is injective on the zero space.
- **Span-dimension corollary, lines 364-379: checked.** Injectivity says a
  fiber is zero iff all `R` retained coordinates are zero. For `R>0`, the
  exact count is `R C(f)+R-1`; for `R=0`, `g=0` and costs zero.
- **Dense-fiber theorem, lines 387-414: checked.** With
  `h=floor(ln K/(-ln(1-delta)))+1`, one has
  `K(1-delta)^h<1`, including `K=1`. Removing sample repetitions preserves
  hitting, and using all `D` coordinates proves the minimum with `D`. The
  `delta=1` branch is correct because every nonempty fiber is the whole cube.
  Its gate count is valid because `K>=1` forces `|H|>=1`.
- **Greedy interpretation, lines 416-419: checked.** Averaging incidences over
  witness coordinates finds a coordinate covering at least a `delta` fraction
  of the uncovered fibers.
- **Reed-Muller weight lemma, lines 444-456: checked.** If the last-variable
  coefficient `b` vanishes, weight doubles; otherwise every point with
  `b(z)=1` contributes exactly one accepting extension, and induction at
  degree `d-1` gives `2^{M-d}`.
- **Low-weight information-set lemma, lines 468-483: checked.** Evaluation at
  `1_S` is the subset-zeta transform; induction recovers every coefficient.
  Rank-nullity proves that fewer than `B(M,d)` coordinates cannot be injective
  on the full degree-`d` space. Only the combined `K=0` formula needs repair.

### Exact and approximate fingerprints

- **Exact fingerprint theorem, lines 508-541: checked for its stated
  `K>=1` branch.** A random functional leaves exactly half of any current
  nonzero survivor set in expectation. After `r-1` halving rows there are at
  most two survivors. Two distinct nonzero vectors over `F_2` are linearly
  independent, so one last functional can equal one on both. The inequalities
  `K<=2^N` and `K<=2^D-1` give `r<=min{N,D}` for `N>=1`.
- **Worst-case optimality, lines 535-540: checked.** If `D<=N`, realizing all
  of `F_2^D` forces injectivity. If `D>N`, zero plus all nonzero vectors of an
  `N`-dimensional subspace uses exactly `2^N` inputs and forces injectivity on
  that subspace. The maximum required linear output dimension is therefore
  exactly `min{N,D}` for every `N>=1`.
- **Field reformulation, lines 547-567: checked when `r>=1`.** Identifying
  `F_2^r` with the additive vector space of `F_{2^r}` changes notation only;
  it does not change evaluation cost.
- **Approximate fingerprint theorem, lines 574-598: checked.** For every fixed
  nonzero fiber, each independent uniform row vanishes with probability one
  half, so all `t` vanish with probability `2^{-t}`. Fubini over the two finite
  spaces gives the exact expectation in (4.6). Zero fibers can never be false
  positives, and averaging fixes an `f`- and `mu`-dependent matrix.
- **Aggregate reduction, lines 625-641: checked for `r>=1`.** A joint
  size-`B` circuit followed by an `r`-leaf OR tree costs `B+r-1`. Explicitly
  materializing the fiber costs at most `D C(f)`, and binary XORs add
  `O(rD)` gates. This is an upper bound, not a claim that sharing is impossible.

### Multiplicative barrier and profile simulation

- **Ideal-kernel theorem, lines 659-696: checked.** A universally well-defined
  product update makes the kernel closed under multiplication by arbitrary
  ring elements. Conversely, an ideal makes the product independent of the
  chosen coset representatives. In `F_2^D`, multiplying by `e_y` extracts a
  supported unit vector, so every ideal is exactly a coordinate-support
  subspace.
- **Universal-propagation corollary, lines 698-720: algebra checked.**
  Rank-nullity gives `rank A=|H|`, and a killed profile supported on the
  discarded coordinates would contradict separation. The only defect is its
  empty-family gate formula identified above.
- **Two-coordinate collision, lines 722-728: checked.** Both input sketch
  pairs are `(1,1)`, while the two product sketches are one and zero.
- **Profile-space proposition, lines 764-789: transition algebra checked.**
  NOT is affine in coefficient coordinates. At an AND, the `k_u k_v`
  coefficient products can be shared and each output coefficient is a fixed
  parity, yielding the two displayed sums. The output is nonzero iff its basis
  coefficient vector is nonzero. The two defects are exactly the missing OR
  gate in the stated basis and the `S`/supplied-size mismatch above.
- **Dominance check, lines 791-798: checked for positive output dimension.**
  The realized output span has dimension at most `k_out`, so an actual-witness
  information set gives at most `k_out` copies. If `k_out=0`, say separately
  that `g=0` instead of writing a `-1` formula.

### DNNF, approximation, and complexity consequences

- **DNNF forgetting, lines 814-826: checked.** Existential quantification
  distributes over OR. At a decomposable AND, the two sets of forgotten
  variables are disjoint, so witnesses can be selected independently.
  Replacing both polarities of a forgotten literal by true is therefore sound;
  `y AND NOT y` correctly demonstrates why decomposability is necessary.
- **Projection-error proposition, lines 852-868: checked.** Every bad `x`
  consumes at least one bad `(x,y)` pair, so division by `2^N` gives the
  factor `2^M`. The singleton-witness example attains equality at
  `epsilon=2^{-M}`; the factor is genuinely tight.
- **Dense sampled approximation, lines 876-880: checked for integer `t>=1`.**
  A yes fiber is missed with probability at most `(1-delta)^t`; there are no
  false positives; averaging over samples gives a fixed distribution-specific
  sample. The gate count `t C(f)+t-1` is exact as an upper bound.
- **Final comparisons, lines 891-919: checked as asymptotic shorthand.**
  Comparing `2^M(S+1)` with `2^N/N` gives precisely
  `M+log_2(S+1)<N-log_2 N`. Each structural term must separately beat both
  replication and direct synthesis, as the text says.
- **Complexity implications, lines 921-957: checked.** A uniform-exponent
  polynomial determinization bound sends nondeterministic polynomial-size
  circuit families to deterministic ones, hence `NP/poly=P/poly`; the easy
  reverse containment uses no witnesses. Karp-Lipton then applies. A
  polynomial-time compiler gives a uniform polynomial-time SAT algorithm.
  Parity/counting hardness is correctly presented only as context, not as a
  circuit lower bound, and unambiguity indeed makes OR equal parity without
  making that parity cheap.
- **Lower-bound transfer, lines 959-965: checked exactly.** Rearranging
  `L <= 2^M C(f)+2^M-1` gives
  `C(f)>=(L+1)/2^M-1`, including `M=0`.

## Edge-case ledger after the proposed repairs

- `N=0`: split off globally; `g` is a free constant. Do not claim the
  `min{N,D}` measurement bound or write `2^N/N`.
- `M=0`: all main exact claims work. Here `D=1`, every nonempty fiber has
  density one, the degree is zero, and one retained witness suffices.
- `K=0` (equivalently `R=0`): `g=0` and `C(g)=0`; do not apply any
  `h(S+1)-1` formula with `h=0`, use `log K`, or introduce `F_{2^0}`.
- `K=1`: one exact parity row is sometimes necessary; write
  `O(log(K+1))`, not literally `O(log K)`.
- `rho=0`: use the exact fingerprint theorem. For `0<rho<=1`, the stated
  approximate width is valid (with zero rows allowed at `rho=1`).

After these local changes, I see no remaining mathematical obstruction to
circulating the note as a technically correct research note. The substantive
open point is exactly the one the draft identifies: the fingerprint output
width is small, but no generic bound is proved for the gates needed to produce
those aggregate bits.

## Second-round audit

### Verdict

**Pass on the mathematical claims.** I audited the revision whose SHA-256 was
`ba213e0a32f982d3f99ffc06f32e52ebc21924944b546576787f93914a2ded97`.
Every first-round Error and Gap is repaired, and the new symmetric-difference
lemma, affine-line specialization, and recovery-boundary circuit proposition
re-derive correctly. I found no remaining mathematical **Error** or **Gap** in
the audited revision.

### Resolution of the first-round findings

- **`N=0`: fixed.** Lines 78 and 132-134 now impose `N>=1`, `M>=0`, and split
  off `N=0` as a free constant. The abstract, table, exact fingerprint bound,
  and `2^N/N` comparisons are consequently consistent.
- **Low-degree `K=0`: fixed.** Lines 532-551 give `C(g)=0` first, assume
  `K>=1`, and define the `d=0` density term to be one. Thus (3.8) never produces
  a negative gate count. The restrictions `0<=d<=M` and the `M=0` induction
  base also appear explicitly at lines 482-498.
- **Ideal-kernel `K=0`: fixed.** Corollary 5.2 assumes `K>=1` at line 863, so
  its hitting set is nonempty and (5.3) is valid.
- **Profile-space basis: fixed.** Lines 936-961 use the mixed basis
  `{AND,OR,XOR,NOT}`. The last term in (6.2) is now genuinely an OR tree;
  replacing only XOR gates by four standard gates proves the factor-four
  conversion.
- **Verifier-size parameter: fixed.** Lines 936-948 use `T` for the supplied
  verifier size and derive `O(T k^3+k)`. The separate `O(S k^3+k)` statement is
  correctly conditional on an admissible family for a constant-factor
  AND/NOT conversion of a size-`S` circuit.
- **VC endpoint bound: fixed.** Lines 462-473 use
  `v_bar=max{1,v}` and include an additive one inside the logarithmic factor.
  This stays positive for `v=0` and as `delta` approaches one.
- **Fingerprint `K=0`: fixed.** Lines 607-608 isolate the zero relation before
  field notation and OR-tree accounting. The overview consistently uses
  `log(K+1)`.
- **Approximation range: fixed.** The theorem permits every integer `t>=0` at
  lines 637-660, and lines 663-664 state the row-count corollary only for
  `0<rho<=1`.
- **DNNF conventions: fixed.** Lines 985-1001 use edge size and state the
  `2^{O(w)}|F|` interaction-graph-treewidth compilation convention.
- **Asymptotic and multi-output conventions: fixed.** Lines 250-266 define
  multi-output circuit size, lines 256-263 state the synthesis limit, and
  lines 315-324 expose both the limiting regime and the lower-order OR tree.
- **Uniform compiler premise: fixed.** Lines 1094-1110 state polynomial
  witness length, input description, run time, and output size.
- **Zero output span: fixed.** Lines 919-925 explicitly assign `g=0` when the
  output-span dimension is zero.

### New Lemma 4.3: symmetric-difference recovery

Lines 696-721 are correct, including the empty-set edge case under the usual
empty-XOR convention.

Injectivity of `E:F_2^D -> F_2^Q` gives `rank(E)=D`; hence
`rank(E^*)=D`, so `E^*` is surjective and every requested recovery vector
`b_i` exists. For `b_T=sum_{i in T} b_i`,

```text
<b_T, Ev> = <E^* b_T, v>
           = <sum_{i in T} e_i, v>
           = XOR_{i in T} v_i.
```

In characteristic two, coordinate `z` belongs to `supp(b_T)` exactly when it
belongs to an odd number of the supports `R_i`. This is precisely membership
in their iterated symmetric difference, proving (4.7). For `T=empty`, both
sides are zero.

### Affine-line parity formula

Lines 723-739 are correct. Parameterize the affine line as
`a+t d`, `t in F_q`, with `d` nonzero. The restriction of `P` is a univariate
polynomial of degree at most `q-2`. Its sum over `F_q` vanishes: the constant
term sums to `q=0` in characteristic two, and for `1<=j<=q-2`,
`sum_t t^j=0`. Therefore

```text
P(u) = sum_{z in L minus {u}} P(z).
```

For a fixed `z in L`, its multiplicity among the sets `L minus {u}` is
`|T|-1` when `z in T` and `|T|` otherwise. Reducing these multiplicities
modulo two gives exactly

```text
triangle_{u in T}(L minus {u})
  = T             if |T| is even,
  = L minus T     if |T| is odd.
```

Because a finite field of characteristic two has even `q`, choosing
`|T|=q-1` leaves the single complementary code symbol. Expanding an
`F_q` symbol in any `F_2` basis turns field addition into bitwise XOR, so the
last sentence at lines 737-739 is also exact. The formula includes `q=2`,
where it reduces to equality of the two values of a constant polynomial.

### New Proposition 4.4: recovery-boundary circuit bound

Lines 741-781 are correct. Surjectivity of `E^*` supplies a preimage `b_j` of
every fingerprint row `a_j`. Computing the joint map `G_Z` once costs
`B_E(Z)`. The adjoint identity then recovers fingerprint bit `j` as the parity
of exactly the resource wires in `supp(b_j)`.

For support size `s>=1`, a binary parity tree uses `s-1` XOR gates. One XOR
has the four-gate standard-basis realization

```text
(p OR q) AND NOT(p AND q),
```

so the parity costs at most `4(s-1)` standard gates. If `s=0`, the fingerprint
bit is the free constant zero and the `max{0,s-1}` term correctly charges
nothing. Since the section assumes `K>=1`, it has `r>=1`; a final binary OR
tree therefore costs exactly `r-1` gates. Summing these costs proves (4.9).
Repeated resource coordinates are outputs of the single joint circuit
`G_Z` and are reused by free fan-out, so they are not charged again.

The edge cases are sound:

- `M=0` gives `D=1`; injective encodings and their adjoints behave exactly as
  above.
- A redundant zero row of `A` may choose `b_j=0`; it is handled by the
  zero-support clause. Separation guarantees that not all rows are zero.
- `Z` is nonempty whenever `K>=1` and `A` separates the fibers, although the
  displayed upper bound would remain meaningful with an empty multi-output
  resource map.
- Different `b_j` parities may share resource wires without extra evaluation
  cost. The formula does not claim to exploit possible sharing among the XOR
  gates themselves, so it is a valid upper bound rather than an optimality
  claim.

The conditionality warning at lines 774-781 is essential and correct:
choosing an encoding that exposes the desired aggregates as coordinates can
make the recovery vectors sparse while merely transferring all cost into
`B_E(Z)`.

### Revised complexity-class statements

Lines 1094-1110 are correct. The size-only hypothesis sends every
polynomial-size nonuniform verifier with polynomial witness length to a
polynomial-size deterministic circuit, proving
`NP/poly subseteq P/poly`; the reverse containment uses no witnesses.
Karp-Lipton then gives the stated second-level collapse. If the transformation
is also a polynomial-time compiler with polynomial output, a uniform NP
verifier can be compiled and evaluated in polynomial time, giving `P=NP`.

The parity statement at lines 1113-1119 is also valid under its natural
universal reading. A polynomial circuit bound for the parity aggregate of
every polynomial-size uniform verifier gives `ParityP subseteq P/poly`.
Adding polynomial advice does not break the conclusion: treat the advice as
additional deterministic input to the uniform verifier, obtain a circuit for
that larger-input aggregate, and hardwire the advice. Thus
`ParityP/poly subseteq P/poly`; the reverse inclusion is obtained with no
nondeterministic bits, proving the displayed equality. One sentence with this
advice-as-input argument would make the implication easier to verify.

### Follow-up fixes made during the audit

The final audited revision also addresses the two minor presentation points
noticed during the pass. Lines 711-713 now state that injectivity of `E` makes
`E^*` surjective, and lines 768-771 explicitly handle a zero-support parity.
The malformed cross-references formerly near lines 203-205 now use proper
`\Cref`/`\cref` commands. The parity-complexity sentence at lines 1113-1119
also now explicitly quantifies over nonuniform verifier families, removing any
possible ambiguity in the `ParityP/poly=P/poly` consequence.

The second-round verdict is therefore unconditional at the level of the
formal mathematical content: no Error or Gap remains from this audit, and the
note is ready for external mathematical review.
