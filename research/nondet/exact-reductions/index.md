# Models, baselines, and the mass-production corollary

This chapter fixes the finite circuit model and proves the reductions that are available before using any special structure of the witness fibers. Results labelled **proved here** are elementary circuit transformations. Results labelled **imported** come from the companion manuscript and are cited by exact line range. No observation in this chapter is claimed to be new.

## 1. Circuit model and parameter map

All integers below are nonnegative unless stated otherwise, and `n=N+M>=1`. Put

``` text
n = N + M,
t = 2^M,
f : {0,1}^N x {0,1}^M -> {0,1},
g(x) = OR_{y in {0,1}^M} f(x,y).
```

Circuits are finite directed acyclic graphs over the basis `{AND_2, OR_2, NOT}`. Input wires and the constant wires zero and one are free. Fan-out is free. A multi-output circuit has an ordered list of output wires; an output wire may occur more than once in that list. Size is the number of gates. For a Boolean map `F`, let `C(F)` be its minimum size in this model. These are exactly the conventions of the companion manuscript ([main.tex], lines 129-132 and 344-353) [schlesinger26][schlesinger26].

For `h : {0,1}^r -> {0,1}` and `s >= 1`, define the independent-input product

``` text
h^{x s}(z_1,...,z_s) = (h(z_1),...,h(z_s))
```

and its mass-production complexity

``` text
MP_s(h) = C(h^{x s}).
```

The superscript `x s` denotes a Cartesian product of outputs, not exponentiation. The `s` input blocks are disjoint before any restriction is made.

The following dictionary prevents three different arities from being conflated.

| Symbol | Meaning | Number of input bits before restriction |
|----|----|---:|
| `f` | verifier relation | `n = N+M` |
| `f^{x t}` | `t=2^M` independent verifier evaluations | `tn` |
| `E_f` | all-witness evaluation map `x -> (f(x,y))_y` | `N` |
| `g` | existential projection `OR o E_f` | `N` |

Define also the worst-case one-output synthesis function

``` text
L(r) = max_{h : {0,1}^r -> {0,1}} C(h).
```

For `r -> infinity`, the standard-basis synthesis bound is

``` text
L(r) <= (1 + o(1)) 2^r/r.
```

Frandsen and Miltersen give an explicit proof, with the sharper displayed upper error term `1 + 3 log_2(r)/r + O(1/r)`, for this basis [fm05][fm05]. Lupanov's 1958 paper is the classical source of the synthesis method [lupanov58][lupanov58]. Only the upper bound is used below.

## 2. Free circuit operations

**Lemma 2.1 (restriction and identification; proved here).** Let `D` compute a multi-output Boolean map. Replacing any input source of `D` by a constant, identifying any collection of input sources, discarding outputs, or repeating an output does not increase its number of gates.

**Proof.** Keep the same directed acyclic graph and gate labels. Redirect each affected incoming edge to the chosen constant or common input source. The value at every gate is the corresponding restriction of its former value, by induction in topological order. Discarding an output only shortens the output list, and repeating one only repeats a wire designation. None of these operations creates a gate. QED.

**Lemma 2.2 (binary OR; proved here).** An ordered list of `s >= 1` bits can be ORed using `s-1` binary OR gates.

**Proof.** For `s=1`, designate the input itself as output. For `s>1`, a left-associated chain adds one OR gate for each input after the first. QED.

The count `s-1` is an upper bound for arbitrary input wires. Correlations among the wires can make the minimum circuit smaller, so no matching lower bound is asserted.

## 3. Exact reduction from enumeration to mass production

Fix once and for all an ordering `y_1,...,y_t` of `{0,1}^M`, and define

``` text
E_f(x) = (f(x,y_1),...,f(x,y_t)).
```

**Theorem 3.1 (enumeration reduction; proved here).** For every `N,M,f`,

``` text
C(E_f) <= MP_t(f),
C(g)   <= MP_t(f) + t - 1
       =  MP_{2^M}(f) + 2^M - 1.
```

**Proof.** Start with an optimal circuit for `f^{x t}`. In copy `i`, fix its `M` witness inputs to the constant string `y_i`. Identify the `N` deterministic-input wires of all copies with one common block `x`. Lemma 2.1 shows that the resulting circuit has no more than `MP_t(f)` gates, and its outputs are exactly `E_f(x)`. Compose it with the `t-1` gate OR circuit from Lemma 2.2. The composite computes `g`. QED.

This is only a one-way use of mass production. The independent-input problem contains `tN` unrelated deterministic inputs, while `E_f` has only one `N`-bit block. Hence this restriction does not show `MP_t(f) <= C(E_f)`, and equality should not be inferred.

## 4. The unconditional envelope

**Proposition 4.1 (replication and direct synthesis; proved here).** For every `N,M,f`,

``` text
MP_t(f) <= t C(f),
C(g) <= t C(f) + t - 1,
C(g) <= L(N).
```

**Proof.** Put `t` disjoint optimal circuits for `f` side by side to prove the first inequality. Restrict their inputs as in Theorem 3.1 and append the OR chain for the second. The function `g` is itself an `N`-input Boolean function, so the definition of `L(N)` proves the third. QED.

Combining the exact reduction with these two baselines gives

``` text
C(g) <= min {
  MP_{2^M}(f) + 2^M - 1,
  2^M C(f) + 2^M - 1,
  L(N)
}.
```

The replication entry is numerically redundant because `MP_t(f) <= t C(f)`. It is displayed because it is the actual-size-sensitive baseline: a mass-production theorem helps a small verifier only if its bound beats `t C(f)`, not merely if it beats worst-case truth-table synthesis.

## 5. What the current mass-production theorem imports

**Imported theorem 5.1.** For every fixed `0 <= gamma < 1`, there is a constant `A_gamma` such that, for every `n >= 1`, every `h : {0,1}^n -> {0,1}`, and every integer `1 <= s <= 2^(gamma n)`,

``` text
MP_s(h) <= A_gamma 2^n/n.
```

This is Theorem 1 of the companion manuscript ([main.tex], lines 134-162) [schlesinger26][schlesinger26]. In particular, `A_gamma` is chosen after `gamma` but before `n,h,s`; the theorem explicitly does not make it uniform as `gamma -> 1`.

**Corollary 5.2 (fixed-ratio witness enumeration; proved here from the imported theorem).** If one fixed constant `gamma < 1` satisfies

``` text
M/(N+M) <= gamma,
```

then

``` text
C(g) <= min {
  L(N),
  2^M C(f) + 2^M - 1,
  A_gamma 2^(N+M)/(N+M) + 2^M - 1
}.
```

**Proof.** The hypothesis is equivalent to `t=2^M <= 2^(gamma(N+M))`. Apply Imported Theorem 5.1 to `f`, then Theorem 3.1, and finally take the minimum with Proposition 4.1. QED.

The word "fixed" is essential for a family of instances. For one pair with `N>0`, one can choose `gamma=M/(N+M)<1`, but the resulting constant is allowed to change with that pair. A uniform asymptotic conclusion requires a single `gamma<1` that bounds the ratios eventually. When `N=0<M`, the ratio is one and the imported theorem does not cover the full witness batch.

## 6. Optimized coefficient and its conversion

The companion manuscript defines the worst-case normalized coefficient and proves, in the present basis,

``` text
Lambda_gamma <= 1/(1-gamma).
```

See [main.tex], lines 1155-1172 for the definition and one-copy coefficient, and lines 1470-1583 for the high-rate construction [schlesinger26][schlesinger26].

**Proposition 6.1 (optimized asymptotic corollary; proved here from the imported coefficient bound).** Consider any sequence with

``` text
n = N+M -> infinity,
M/n -> theta < 1.
```

Uniformly over the verifier `f` along this sequence, the mass-production route gives

``` text
C(g) <= (1/(1-theta) + o(1)) 2^n/n
     =  (1 + o(1)) 2^(N+M)/N.
```

**Proof.** Fix any `gamma` with `theta < gamma < 1`. Eventually `M/n <= gamma`, so the definition of `Lambda_gamma` and its imported bound give

``` text
MP_{2^M}(f) <= (1/(1-gamma) + o(1)) 2^n/n.
```

The final OR is negligible on this scale because `N/n -> 1-theta > 0`, hence

``` text
n 2^M/2^n = n/2^N -> 0.
```

Theorem 3.1 therefore gives a normalized limsup at most `1/(1-gamma)`. Taking the infimum over fixed `gamma>theta` yields `1/(1-theta)`. Finally, `N/n -> 1-theta`, so the two displayed forms are equal up to `1+o(1)`. QED.

## 7. Why this does not improve generic determinization

**Proposition 7.1 (dominance by direct synthesis; proved here).** Under the hypotheses of Proposition 6.1, generic synthesis of the projection gives

``` text
C(g) <= (1 + o(1)) 2^N/N.
```

The numerical upper bound obtained in Proposition 6.1 is larger by the factor

``` text
[(1+o(1)) 2^(N+M)/N] / [(1+o(1)) 2^N/N]
  = (1+o(1)) 2^M.
```

**Proof.** Since `theta<1`, we have `N -> infinity`. Apply the classical bound `L(N) <= (1+o(1))2^N/N` directly to the `N`-input function `g`. The ratio calculation is algebraic. QED.

Thus the present mass-production theorem does not improve the worst-case deterministic upper bound for existential projection. If `M -> infinity`, the gap between these two generic upper bounds diverges as `2^M`; if `M` is a fixed positive integer, the displayed factor is the fixed number `2^M`; and if `M=0`, the two scales coincide. This comparison concerns the bounds, not a lower bound on `C(g)`. A particular `g` can of course be much easier.

## 8. Exact simplification when every suffix is the same

The code construction in the companion manuscript writes an input as `(a,z)` and creates Boolean resource functions `H_{u,r}(z)`. It creates `q^ell b = Theta_ell(2^p)` such functions ([main.tex], lines 617-648). For unrelated batch inputs, one fixed resource function can receive up to `C` different suffixes; the composition theorem therefore pays for `H_{u,r}^{x C}` separately for every resource ([main.tex], lines 800-832 and 844-860) [schlesinger26][schlesinger26].

For witness enumeration, orient the split as

``` text
a = y in {0,1}^M,   z = x in {0,1}^N.
```

Every routed suffix is then the same wire block `x`. The following elementary lemma states exactly what becomes free.

**Lemma 8.1 (deduplication of identical calls; proved here).** Let `h_1,...,h_R : {0,1}^d -> {0,1}`, and let `i_1,...,i_s` be resource indices. Let `K` be a subset of these indices containing one representative of every distinct Boolean function among `h_{i_1},...,h_{i_s}`. Then

``` text
C(z -> (h_{i_1}(z),...,h_{i_s}(z)))
  = C(z -> (h_k(z))_{k in K}).
```

**Proof.** From right to left, repeat the representative output wire in every requested position. From left to right, retain one requested output for each representative and discard the rest. Both transformations are free by Lemma 2.1. QED.

**Corollary 8.2 (common-suffix refactoring; proved here).** After specializing all routed suffixes to `x`, every block

``` text
H^{x c}(x,...,x) = (H(x),...,H(x))
```

may be replaced by one circuit for `H(x)` and free fan-out. More globally, all resource calls may be replaced by one circuit for the multi-output map of their distinct extensional resource functions, evaluated once on `x`.

There are three different notions here.

1.  Repeating the same resource function on the same suffix is free after its first evaluation.
2.  Evaluating two distinct resource functions on the same suffix is not free. It asks for two coordinates of a multi-output map. Joint synthesis may share gates, but fan-out alone gives no such bound.
3.  Two distinct descriptions that define the same Boolean function can be merged, because their equality is extensional and fixed in the nonuniform circuit. Two functions that merely happen to return the same bit on one run cannot be merged on that basis.

Consequently the common suffix removes the companion construction's *multiplicity of suffix evaluations per fixed resource*. It does not remove the `Theta_ell(2^M)` indexed resource coordinates that may remain when the coded prefix has length `p=M`; some coordinates could still define the same function. Separate worst-case synthesis costs `Theta_ell(2^M)L(N) = Theta_ell(2^(N+M)/N)`. Improving that term requires a joint multi-output or structure-sensitive synthesis argument.

## 9. Recovery-boundary cancellation on a shared input

Let `E : F_2^D -> F_2^Q` be an injective linear encoding. Write `E*` for its
adjoint. For every message coordinate `i`, a linear recovery representation is
a vector `b_i in F_2^Q` with

``` text
E* b_i = e_i.
```

Such a vector always exists because `E` is injective, although its weight may
be large. If `R_i` is its support, then for every target set `T`,

``` text
XOR_{i in T} v_i
  = XOR_{z in symmetric_difference_{i in T} R_i} (Ev)_z.
```

This follows from `E*(sum_i b_i)=sum_i e_i`. Over `F_2`, coordinates occurring
an even number of times cancel. When the same deterministic input `x` is used
on every branch, the repeated encoded coordinate is literally the same
resource bit, so it needs to be evaluated only once. With independent batch
inputs, equal coordinate names generally carry different values and do not
cancel.

For the affine-line identity in the companion manuscript, recovering every
`u in T` through one line `L` gives boundary

``` text
T       if |T| is even,
L \ T   if |T| is odd.
```

Since `q=|L|` is even, the parity of `q-1` target values collapses to the one
remaining line symbol. The finite checker verifies this identity for every
even-parity line word at line sizes 2, 4, and 8.

For fingerprint rows `a_j`, choose representations `E* b_j=a_j`, let `Z` be
the union of their supports, and let `B_E(Z)` be the joint circuit complexity
of the resource map

``` text
x -> ((E v_x)_z)_{z in Z}.
```

Then the standard-basis circuit bound is

``` text
C(g) <= B_E(Z) + 4 sum_j max(0, wt(b_j)-1) + r - 1.
```

This is an exact bridge from local recovery to nondeterministic sharing. It is
not a generic improvement: choosing an encoding whose coordinates are the
desired aggregates makes the boundary sparse tautologically, but may make
`B_E(Z)` just as hard as the original projection. A useful construction must
control the fingerprint, recovery boundary, and resource evaluator together.

## 10. Four compression claims that must not be conflated

| Claim | Formal quantity reduced | Does it by itself reduce gates? |
|----|----|----|
| Witness compression | number of actual `y` values tested | Yes, if the retained witnesses hit every nonempty fiber |
| Aggregate compression | number of summaries consumed by the zero test | No; forming the summaries may still enumerate all witnesses |
| Call-multiplicity compression | repeated occurrences of one `(resource,input)` pair | Yes, by Lemma 8.1, but only for repetitions |
| Gate compression | `C(E_f)`, the aggregate-map complexity, or the distinct-resource multi-output complexity | Yes; this is the required circuit statement |

In particular, replacing the `2^M` witness bits by a short list of parity or code aggregates is an aggregate-count statement. It becomes a determinization result only after one also bounds the gates required to compute those aggregates. Likewise, common-suffix fan-out solves repeated calls but leaves the distinct-resource synthesis problem intact.

The exact unconditional conclusion of this chapter is therefore the envelope

``` text
C(g) <= min {
  L(N),
  MP_{2^M}(f) + 2^M - 1,
  2^M C(f) + 2^M - 1
},
```

augmented, under one fixed ratio bound, by the imported `A_gamma 2^(N+M)/(N+M) + 2^M - 1` term. The remaining chapters investigate conditions under which witness or aggregate compression also yields genuine gate compression.

## Local References

<a id="schlesinger26"></a>

- **[schlesinger26]** Samuel Schlesinger. *Exponential-Range Mass Production of Boolean Functions: Local Recovery, Disjoint Scheduling, and Bounded Congestion*. Unpublished companion manuscript, September 2026. [Local TeX source][main.tex]. No DOI assigned. Line ranges cited above were verified against the local source on 2026-09-03.

<a id="fm05"></a>

- **[fm05]** Gudmund Skovbjerg Frandsen and Peter Bro Miltersen. "Reviewing Bounds on the Circuit Size of the Hardest Functions." *Information Processing Letters* 95(2):354-357, 2005. [doi:10.1016/j.ipl.2005.03.009]. Metadata and DOI verified via the publisher record and Aarhus University research portal on 2026-09-03.

<a id="lupanov58"></a>

- **[lupanov58]** Oleg B. Lupanov. "On a Method of Circuit Synthesis" (in Russian). *Izvestiya VUZ, Radiofizika* 1(1):120-140, 1958. [Official journal record]. No DOI is listed; URL and metadata verified on 2026-09-03.

[main.tex]: ../../../main.tex
[schlesinger26]: #schlesinger26
[fm05]: #fm05
[lupanov58]: #lupanov58
[doi:10.1016/j.ipl.2005.03.009]: https://doi.org/10.1016/j.ipl.2005.03.009
[Official journal record]: https://radiophysics.unn.ru/issues/1958/1/120
