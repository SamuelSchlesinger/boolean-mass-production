# Low witness degree and Reed-Muller information sets

This detail proves two actual-witness reductions for verifier fibers of low
algebraic degree over `F_2`.  The first uses minimum distance plus the density
theorem in the [parent chapter](index.md).  The second uses an explicit
information set and can be much stronger.

## Algebraic-degree promise

Every Boolean function on `{0,1}^M` has a unique multilinear polynomial over
`F_2`, its algebraic normal form.  Assume that for every `x`,

```text
p_x(y) = f(x,y) in F_2
```

has total degree at most `d`, where `0 <= d <= M`.  This is a semantic
condition on every witness fiber.  It is not a claim about Boolean circuit
depth, size, or the syntactic degree of one representation.

The evaluation vectors of degree-at-most-`d` polynomials form the classical
binary Reed-Muller code [muller54][muller54] [reed54][reed54].

## Minimum weight, proved directly

**Lemma (Reed-Muller weight, proved here).**  If a nonzero multilinear
polynomial `p` in `M` variables has degree `r`, then

```text
|{y in {0,1}^M : p(y)=1}| >= 2^(M-r).
```

Hence every nonzero polynomial of degree at most `d` has relative weight at
least `2^(-d)`.

**Proof.**  Induct on `M`.  The case `M=0` is immediate.  Write

```text
p(y_1,...,y_M) = a(y_1,...,y_(M-1))
                  + y_M*b(y_1,...,y_(M-1)).
```

If `b=0`, then `p` is independent of `y_M`, and induction gives

```text
weight(p) = 2*weight(a) >= 2*2^((M-1)-r) = 2^(M-r).
```

If `b` is nonzero, then `deg(b) <= r-1`.  Whenever `b(z)=1`, the pair

```text
(p(z,0),p(z,1)) = (a(z),a(z)+1)
```

contains exactly one `1`.  Therefore

```text
weight(p) >= weight(b)
          >= 2^((M-1)-deg(b))
          >= 2^(M-r).
```

This completes the induction.  QED.

The bound is exact: `p(y)=y_1*...*y_d` has weight `2^(M-d)`.  More strongly,
the `2^d` indicator polynomials for assignments to the first `d` coordinates
have disjoint supports.  Some degree-`d` fiber families therefore require at
least `2^d` actual witnesses.

## The density corollary

Let `K` be the number of distinct nonempty fibers.  The lemma makes every
such fiber `2^(-d)`-dense.  The parent chapter's theorem gives an
`f`-dependent hitting set of size

```text
h_deg = 1                                            if d=0,
h_deg = min(2^M,
            floor(ln(K)/(-ln(1-2^(-d)))) + 1)        if d>=1.
```

Since `-ln(1-z) >= z`,

```text
h_deg <= min(2^M, 2^d*ln(K)+1)
      <= min(2^M, 2^d*N*ln(2)+1).
```

Under the companion manuscript's free-fan-out binary-gate convention,
restriction and replication give

```text
C(g) <= h_deg*(C(f)+1)-1.
```

This proves the advertised `O(2^d*(N+1)*(C(f)+1))` bound, with `N` refined
to `log_2 K`.

## An explicit universal information set

Minimum distance is not the only useful code property.  Define

```text
H_(M,d) = {y in {0,1}^M : HammingWeight(y) <= d},
D(M,d) = |H_(M,d)| = sum from i=0 to d of binom(M,i).
```

**Proposition (information set, proved here).**  If a multilinear polynomial
`p` of degree at most `d` vanishes on `H_(M,d)`, then `p=0`.  Thus
`H_(M,d)` hits the support of every nonzero degree-at-most-`d` polynomial.

**Proof.**  Write

```text
p(y) = sum over A subseteq [M], |A|<=d of
       c_A * product over i in A of y_i.
```

For `S subseteq [M]`, let `1_S` be its indicator vector.  Then

```text
p(1_S) = sum over A subseteq S of c_A.
```

Suppose these values vanish for all `|S|<=d`.  Induction on `|S|` gives
`c_S=0`: it is immediate for `S=emptyset`, and after all proper-subset
coefficients vanish, the equation for `S` reduces to `c_S=0`.  Every
coefficient vanishes.  QED.

The set is optimal among witness sets required to hit the entire degree
class.  The polynomial space has dimension `D(M,d)`.  If `H` hits every
nonzero polynomial, the restriction map

```text
p |-> (p(y) : y in H)
```

is injective from a `D(M,d)`-dimensional space into `F_2^|H|`; hence
`|H| >= D(M,d)`.

This also computes the VC dimension of the full support family.  It has
`2^D(M,d)` members, so its VC dimension is at most `D(M,d)`.  Restriction to
`H_(M,d)` is an injective linear map between two spaces of dimension
`D(M,d)`, hence a bijection; all labelings of `H_(M,d)` occur.  The VC
dimension is exactly `D(M,d)`.  A realized subfamily from one verifier can
have much smaller VC dimension and much smaller `K`.

For the verifier, this explicit set gives the exact identity and bound

```text
g(x) = OR over y with HammingWeight(y)<=d of f(x,y),
C(g) <= D(M,d)*(C(f)+1)-1.
```

Unlike `h_deg`, this witness set is independent of `f` and directly
enumerable.  Combining the arguments gives

```text
L = min(2^M, h_deg, D(M,d)),
C(g) <= L*(C(f)+1)-1.
```

## Exact crossover with full enumeration

Full witness enumeration has the replication bound

```text
C(g) <= 2^M*(C(f)+1)-1.
```

The combined result is strictly smaller exactly when the selected value
`L` is below `2^M`.  Each branch has a transparent crossover.

For the information set,

```text
D(M,d) < 2^M    iff    d < M.
```

Thus every genuine degree restriction saves at least one copy.  Quantitative
savings depend on the binomial tail: for fixed `d`, `D(M,d)=Theta(M^d)`;
for `d <= alpha*M` with fixed `alpha<1/2`, the standard entropy estimate
makes it exponentially smaller than `2^M`.

For the density branch with `d>=1`, the untruncated `h_deg` is below `2^M`
exactly when

```text
ln(K) < (2^M-1)*(-ln(1-2^(-d))).
```

A simpler sufficient condition is

```text
2^d*ln(K) < 2^M-1.
```

Using only `K <= 2^N`, it suffices that

```text
2^d*N*ln(2) < 2^M-1.
```

At exponent scale this is

```text
d + log_2(max(1,N)) < M + O(1),
```

not the stronger informal requirement `d+log_2 N << M`.  When `K>1` and the
density branch controls the minimum, the factor saved is approximately
`2^(M-d)/ln(K)`.  Near the threshold, use the exact minimum with `D(M,d)`.

## Uniformity and limitations

- The density hitting set depends on `f` and is only existential unless the
  fibers can be inspected.  This is sufficient for nonuniform circuit
  complexity, not for a uniform determinization algorithm.
- `H_(M,d)` is uniform, explicit, and independent of `f`, but using it still
  requires a valid degree promise.  Recognizing that promise from an
  arbitrary succinct circuit is a separate problem.
- Algebraic degree over `F_2` is not real degree, approximate degree, circuit
  depth, or syntactic degree.
- These arguments reduce verifier copies.  They do not share the internal
  work of each remaining copy.
- No novelty claim is made.  The terminology and code family are classical;
  the proofs here record the exact implication needed by this corpus.

## Local References

- `[muller54]` David E. Muller. "Application of Boolean algebra to switching
  circuit design and to error detection." *Transactions of the I.R.E.
  Professional Group on Electronic Computers* EC-3(3) (1954), 6-12.
  DOI: [10.1109/IREPGELC.1954.6499441](https://doi.org/10.1109/IREPGELC.1954.6499441).
- `[reed54]` Irving S. Reed. "A class of multiple-error-correcting codes and
  the decoding scheme." *Transactions of the IRE Professional Group on
  Information Theory* 4(4) (1954), 38-49.
  DOI: [10.1109/TIT.1954.1057465](https://doi.org/10.1109/TIT.1954.1057465).

[muller54]: https://doi.org/10.1109/IREPGELC.1954.6499441
[reed54]: https://doi.org/10.1109/TIT.1954.1057465
