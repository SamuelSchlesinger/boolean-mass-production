# Dense fibers, epsilon-nets, and low witness degree

This chapter isolates a regime in which existential quantification can be
compressed without evaluating a coded parity or count.  The compressed
objects are still actual witnesses.  The gain comes from finding one small
set of witnesses that intersects every nonempty witness fiber.

The elementary density theorem and all of its circuit corollaries below are
proved here.  The VC-dimension epsilon-net theorem is a known input
[hw87][hw87].  The Reed-Muller weight bound is also given a self-contained
proof, so its use does not depend on a black-box coding theorem.

## Setup: the fiber set system

Fix

```text
f : {0,1}^N x {0,1}^M -> {0,1},
g(x) = OR over y in {0,1}^M of f(x,y).
```

Write

```text
Y     = {0,1}^M,
q     = |Y| = 2^M,
F_x   = {y in Y : f(x,y) = 1},
R_f   = {F_x : x in {0,1}^N and F_x is nonempty},
K     = |R_f|.
```

Thus `R_f` removes both the empty fiber and duplicate fibers.  Always
`0 <= K <= 2^N`.  Equip `Y` with the uniform counting measure

```text
mu(A) = |A| / 2^M.
```

A set `H subseteq Y` is a transversal, or hitting set, for `R_f` when
`H intersect F` is nonempty for every `F in R_f`.  Such an `H` gives the
exact identity

```text
g(x) = OR over y in H of f(x,y).
```

There is no approximation in this identity.  Empty fibers remain empty, and
every nonempty fiber is hit by at least one actual witness.

## A density-sensitive hitting theorem

The right counting parameter is `K`, the number of distinct nonempty fibers,
not the number `2^N` of possible values of `x`.

**Theorem (dense-fiber hitting, proved here).**  Suppose `K >= 1` and there is
a number `delta in (0,1]` such that

```text
mu(F) >= delta                 for every F in R_f.
```

If `0 < delta < 1`, define

```text
rho(delta) = -ln(1-delta),
h_count    = min(q, floor(ln(K) / rho(delta)) + 1).
```

Then `R_f` has a hitting set `H` with `|H| <= h_count`.  If `delta=1`,
one arbitrary point of `Y` is a hitting set.  Consequently, in all cases,

```text
|H| <= min(2^M, ln(K)/delta + 1)
     <= min(2^M, N*ln(2)/delta + 1).
```

In particular, the familiar coarse form is

```text
|H| = O((N+1)/delta).
```

**Proof.**  First assume `0 < delta < 1`.  Draw `h` points independently and
uniformly from `Y`.  For a fixed fiber `F`,

```text
Pr[all h points miss F]
  = (1-mu(F))^h
  <= (1-delta)^h
  = exp(-rho(delta)*h).
```

The union bound over the `K` distinct nonempty fibers gives failure
probability at most

```text
K * exp(-rho(delta)*h).
```

For `h=floor(ln(K)/rho(delta))+1`, this quantity is strictly smaller than
one.  Hence some sample hits every fiber.  Removing repeated sample points
does not destroy the hitting property.  If this value of `h` exceeds `q`, use
`H=Y` instead.  Finally, `rho(delta) >= delta` and `K <= 2^N`, which give the
displayed simpler bounds.  When `delta=1`, every nonempty fiber is all of
`Y`, so one point suffices.  QED.

The same argument has a greedy reading.  Among any `r` fibers not yet hit,
the average point `y in Y` belongs to at least `delta*r` of them.  Choosing a
point with at least this average coverage leaves at most `(1-delta)r`
fibers.  Iteration gives the same bound.  This is a truth-table algorithm,
not necessarily an efficient algorithm from a circuit for `f`.

If `K=0`, then `g` is the constant-zero function and the empty hitting set is
appropriate.

## The circuit consequence

Use the circuit convention of the companion manuscript: binary
`AND/OR/NOT` gates, free constants and fan-out, and size equal to the number
of non-input gates.  Fixing the `M` witness inputs of a circuit for `f` to a
constant `y` does not increase its size.  Replicating the resulting circuit
for all `y in H` and joining the outputs by a binary OR tree proves the
following.

**Corollary (dense-fiber determinization, proved here).**  For `K >= 1`, let
`h` be any of the valid hitting-set bounds above.  Then

```text
C(g) <= h*C(f) + h - 1
     = h*(C(f)+1) - 1.
```

In particular,

```text
C(g) <= (N*ln(2)/delta + 1)*(C(f)+1) - 1,
```

up to replacing the nonintegral coefficient by its ceiling.  This replaces
`2^M` copies of the verifier by `O((N+1)/delta)` copies.  It does not share
the internal gates of those remaining copies, so it is a witness-reduction
theorem rather than a size-sensitive mass-production theorem.

The dependence on the number of distinct fibers can be decisive.  If many
values of `x` induce the same witness set, replace `N*ln(2)` by `ln(K)`.
Equivalently, the relevant input-side information is `log_2 K`, not `N`
itself.

## What density alone can and cannot buy

The exact optimum is the transversal number

```text
tau(R_f) = min{|H| : H hits every F in R_f}.
```

The theorem only upper-bounds this parameter.  It may be very loose: nested
fibers can all share one witness even when `K` is enormous.

The factor `1/delta` cannot be removed from a general statement.  Partition
`Y` into `r` disjoint blocks of equal size and take the blocks as fibers.
Here `delta=1/r`, but every hitting set has at least `r=1/delta` points.

Nor can bounded VC dimension alone generally reduce the answer to
`O(1/delta)`.  There are range spaces of VC dimension two whose smallest
`delta`-nets have size

```text
Omega((1/delta)*log(1/delta));
```

Pach and Tardos give geometric examples and explicit constants
[pt13][pt13].  Thus any stronger conclusion needs more structure than a bare
VC-dimension bound.

## VC dimension as a second compression parameter

For a set system `(Y,R_f)`, a subset `S subseteq Y` is shattered if

```text
{F intersect S : F in R_f} = {T : T subseteq S}.
```

The VC dimension `v` is the maximum size of a shattered set.  Since a family
of `K` ranges cannot realize `2^v` distinct traces,

```text
v <= floor(log_2 K)
```

whenever `K >= 1`.

A strong `delta`-net for the uniform measure on `Y` is exactly an
actual-witness set that hits every fiber of density at least `delta`.
The epsilon-net theorem of Haussler and Welzl therefore gives, for an
absolute constant `c`,

```text
|H| <= c * (v_bar/delta) * (1 + ln(v_bar/delta)),
v_bar = max(1,v).
```

This statement is existential; the original theorem also analyzes random
sampling [hw87][hw87].  Combining the two unrelated controls yields

```text
|H| <= min(
  2^M,
  floor(ln(K)/(-ln(1-delta))) + 1,
  c*(v_bar/delta)*(1+ln(v_bar/delta))
).
```

The corresponding circuit bound is again `|H|*(C(f)+1)-1`.  The VC branch
is useful when

```text
v_bar*(1+log(v_bar/delta)) << log K.
```

It need not improve the elementary union bound merely because `v` is finite.
For fixed `v >= 2`, the general epsilon-net logarithm in `1/delta` is real,
as the lower bounds above demonstrate [pt13][pt13].

The measure must be stated.  Here it is the single uniform measure on the
witness cube.  If every fiber is dense only under its own distribution
`mu_x`, no common hitting conclusion follows.  For example, each `mu_x`
could be concentrated on a different singleton fiber; every fiber then has
`mu_x`-measure one, while a common hitting set may need all `2^M` witnesses.

## Low witness degree: two complementary code arguments

If every fiber function `y |-> f(x,y)` has algebraic degree at most `d` over
`F_2`, Reed-Muller minimum distance gives `delta=2^(-d)`.  The density theorem
then yields an `f`-dependent hitting set of size

```text
O(2^d*(log K+1)) = O(2^d*(N+1)).
```

There is also a different, explicit set that works for every degree-`d`
fiber, independently of `f`:

```text
H_(M,d) = {y : HammingWeight(y) <= d},
|H_(M,d)| = sum from i=0 to d of binom(M,i).
```

The proofs, the optimality of this universal information set, and the exact
crossover against `2^M`-witness enumeration are in
[Low witness degree and Reed-Muller information sets](reed-muller.md).

## Uniformity and scope caveats

1. The density and VC arguments choose `H` from the complete fiber system of
   `f`.  This is valid for nonuniform circuit complexity, but neither proof
   gives a polynomial-time algorithm from a succinct circuit for `f`.

2. Greedy selection is effective only with access to the fibers or to the
   required coverage queries.  Such access may cost the full truth table.

3. These results compress the witness list, not the internal gates of the
   remaining verifier copies.  They do not prove a size-sensitive bound such
   as `C(f)+O(|H|*(N+M))` for unrestricted verifiers.

4. No literature-novelty claim is made.  The density proof is the standard
   probabilistic hitting-set argument, and the VC refinement is the classical
   epsilon-net theorem.

## Local References

- `[hw87]` David Haussler and Emo Welzl. "Epsilon-nets and simplex range
  queries." *Discrete & Computational Geometry* 2 (1987), 127-151.
  DOI: [10.1007/BF02187876](https://doi.org/10.1007/BF02187876).
- `[pt13]` Janos Pach and Gabor Tardos. "Tight lower bounds for the size of
  epsilon-nets." *Journal of the American Mathematical Society* 26(3)
  (2013), 645-658.
  DOI: [10.1090/S0894-0347-2012-00759-0](https://doi.org/10.1090/S0894-0347-2012-00759-0).

[hw87]: https://doi.org/10.1007/BF02187876
[pt13]: https://doi.org/10.1090/S0894-0347-2012-00759-0
