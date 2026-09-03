# Codes, sketches, and isolation

For a fixed Boolean relation, exponentially many possible witnesses compress to at
most \(\min(N,2^M)\) parity measurements when \(N\ge1\).  This exact count is
relation-dependent and nonuniform: it compresses *measurements*, not their gate cost.

## Setup: sketch the witness fiber

Fix
\[
f:\{0,1\}^{N}\times\{0,1\}^{M}\to\{0,1\},\qquad g(x)=\bigvee_yf(x,y).
\]
Put \(D=2^M\), index \(\mathbb F_2^D\) by witnesses, and define
\[v_x=(f(x,y))_{y\in\{0,1\}^{M}}\in\mathbb F_2^D.\]
Thus \(g(x)=1\) exactly when \(v_x\ne0\).  Let
\[\mathcal V_f=\{v_x:x\in\{0,1\}^N,\ v_x\ne0\},\qquad K=|\mathcal V_f|\le2^N.\]
Only distinct nonzero fibers count in \(K\).  Separate three tasks:

1. **Witness compression:** retain a small fixed list of actual \(y\)'s.
2. **Measurement compression:** summarize \(v_x\) in a few bits while
   preserving \(v_x\ne0\) on realized fibers.
3. **Computational compression:** produce those bits without expanding all
   \(D=2^M\) verifier evaluations.

This chapter proves (2), not (1) or (3).

## Exact relation-dependent zero detection

**Theorem (linear fingerprint).**  If \(K=0\), the zero map suffices.  If
\(K\ge1\), set
\[r=\min\!\left(D,\max\!\left(1,\left\lceil\log_2K\right\rceil\right)\right).\]
There is an \(\mathbb F_2\)-linear map
\[A:\mathbb F_2^D\longrightarrow\mathbb F_2^r\]
such that \(\ker(A)\cap\mathcal V_f=\varnothing\).  Equivalently,
\[Av_x=0\quad\Longleftrightarrow\quad v_x=0\]
simultaneously for every \(x\).

**Proof.**  Since \(K\le2^D-1\), the formula gives \(1\le r\le D\) and
\(K\le2^r\).  Maintain \(S\subseteq\mathcal V_f\), the fibers killed by all prior rows.
For a uniform row \(a\), each fixed \(v\ne0\) is killed with
probability \(1/2\), so some row leaves at most \(\lfloor|S|/2\rfloor\) members.
After \(r-1\) choices, at most
\(\lfloor K/2^{r-1}\rfloor\le2\) survive.  One last functional can be one on
all survivors: two distinct nonzero vectors over \(\mathbb F_2\) are
independent, so define it on their span and extend it.  If none survive, use
zero.  \(\square\)

A uniform full-row-rank \(r\times D\) matrix gives a one-shot proof.  Its
kernel is a uniform \((D-r)\)-subspace, and for fixed \(v\ne0\),
\(\Pr[Av=0]=(2^{D-r}-1)/(2^D-1)<2^{-r}\).  Thus the expected number of
killed fibers is less than \(K2^{-r}\le1\).

When \(N\ge1\), this gives \(r\le\min(N,D)\).  Padding with zero rows proves
the originally proposed \(N+1\)-row form
\[
A':\mathbb F_2^{2^M}\to\mathbb F_2^{N+1},\qquad
\ker(A')\cap\mathcal V_f=\varnothing.
\]
The spare row is useful only for the simpler independent-entry proof: a
uniform unrestricted \((N+1)\times D\) matrix has failure probability at most
\(K2^{-(N+1)}\le1/2\).

The worst-case bound \(\min(N,D)\) is exact.  If \(D\le N\), realize every
vector of \(\mathbb F_2^D\) among the fibers; any successful map is injective
and needs \(D\) rows.  If \(D>N\), realize zero and all nonzero vectors of an
\(N\)-dimensional subspace, using exactly \(2^N\) fibers; the map must be
injective on that subspace and needs \(N\) rows.  For the edge case \(N=0\),
there is one fiber: zero rows suffice if it is zero, and one row is necessary
and sufficient otherwise.

## Parity aggregates and the extension-field form

For \(K\ge1\), write the rows of \(A\) as \(a_1,\ldots,a_r\), and define
\[h_i(x)=\langle a_i,v_x\rangle=\bigoplus_{y:a_i(y)=1}f(x,y).\]
Then \(g(x)=\bigvee_{i=1}^{r}h_i(x)\).
Padding gives exactly \(N+1\) aggregates if that fixed width is convenient.
The masks are fixed for \(f\), not selected after seeing \(x\).

Cancellation still occurs in individual rows: a mask meeting the accepting
fiber in a positive even number of positions returns zero.  For \(D>1\),
every single linear functional has a nonzero kernel.  The theorem prevents
only *total* cancellation across all rows on the realized fiber set.

Choose an \(\mathbb F_2\)-basis of \(\mathbb F_{2^s}\), for \(s=r\) or
\(s=N+1\).  Regard column \(y\) of the matrix as the coordinates of
\(\alpha_y\in\mathbb F_{2^s}\), and put
\[H(x)=\sum_{y\in\{0,1\}^M}\alpha_y f(x,y)\in\mathbb F_{2^s}.\]
The coordinates of \(H(x)\) are \(Av_x\), hence
\[g(x)=1\quad\Longleftrightarrow\quad H(x)\ne0.\]
For \(s=N+1\), independent uniform coefficients give the unrestricted random
matrix proof: condition on all coefficients except one attached to an
accepting witness, and \(H(x)\) is uniform, so it vanishes with probability
\(2^{-s}\).  One field symbol still contains \(s\) Boolean coordinates; no
field multiplication or cheaper aggregation circuit has appeared.

## A distributional one-sided corollary

Exact simultaneous correctness can cost \(\Theta(\log(K+1))\) rows in the
worst case.  Approximation needs only logarithmically many rows in the desired
inverse error, independently of \(N\).

Let \(A\) have \(t\) independent uniform rows and define
\[\widetilde g_A(x)=\bigvee_{i=1}^{t}\langle a_i,v_x\rangle.\]
It has no false positives, because \(A0=0\).  For every fixed yes-input,
\[\Pr_A[\widetilde g_A(x)=0]=2^{-t}.\]
Thus it is a pointwise one-sided randomized parity sketch.  More strongly,
for any fixed distribution \(\mu\) on deterministic inputs, define
\[\operatorname{FN}_\mu(A)=\Pr_{x\sim\mu}[g(x)=1,\ \widetilde g_A(x)=0].\]
Interchanging the two finite expectations gives
\[\mathbb E_A\operatorname{FN}_\mu(A)=2^{-t}\Pr_{x\sim\mu}[g(x)=1]\le2^{-t}.\]
Hence some fixed \(A\), depending on \(f\) and \(\mu\), has false-negative
mass at most \(2^{-t}\) under \(\mu\).  For uniform \(x\), one fixed
\(f\)-dependent map disagrees with \(g\) on at most a \(2^{-t}\) fraction of
all inputs and never accepts a no-input.  This is distributional nonuniform
approximation, not exact determinization, and it still says nothing about the
gates required to evaluate the parities.

This guarantee approximates the *projection directly*.  Approximation of the
relation under uniform \((x,y)\) need not survive projection: for
\(f(x,y)=1[y=0^M]\), the zero relation differs from \(f\) on only a \(2^{-M}\)
fraction of pairs, but their existential projections disagree for every
\(x\).  The parity sketch instead has one-sided error measured over \(x\).

## Code distance plus coordinate sampling

**Lemma (coded zero test).**  Let
\(E:\mathbb F_2^D\to\mathbb F_2^L\) be linear with relative distance
\(\delta>0\).  Sample \(j_1,\ldots,j_t\) independently and uniformly from
\([L]\), and set
\[
B(v)=(E(v)_{j_1},\ldots,E(v)_{j_t}).
\]
Every nonzero codeword has at most \((1-\delta)L\) zero coordinates, so
\[
\Pr[B(v)=0]\le(1-\delta)^t
\]
and
\[
\Pr[\exists v\in\mathcal V_f:B(v)=0]\le K(1-\delta)^t.
\]
Therefore a fixed coordinate list succeeds if \(K(1-\delta)^t<1\), and
\(t=O(\log(K+1)/\delta)\) suffices.  Each sampled coordinate is a row of the
code's generator matrix, hence a parity mask.  Distance amplifies every
nonzero vector into many detection opportunities.

Chen, Jin, and Williams combine this mechanism with expander-walk sampling
to build succinct perfect linear hashes for sparse languages [cjw19][cjw19].
Their stronger guarantee separates every pair in a prescribed set.  Here only
\((0,v)\) for \(v\in\mathcal V_f\) must be separated, so there are \(K\), not
\(\binom{K}{2}\), bad events.  Even their linear-time construction charges the
*explicit vector length*, which here is \(D=2^M\).

## Small-bias rows shorten randomness, not computation

For an \(\varepsilon\)-biased distribution \(\mathcal D\) on
\(\mathbb F_2^D\), use the convention
\[
\left|\mathbb E_{a\sim\mathcal D}(-1)^{\langle a,v\rangle}\right|
\le\varepsilon\qquad(v\ne0).
\]
Then
\(\Pr[\langle a,v\rangle=0]\le(1+\varepsilon)/2\), so \(t\) independent
rows have simultaneous failure probability at most
\[
K\left(\frac{1+\varepsilon}{2}\right)^t.
\]
Thus \(t=O(\log(K+1))\) still suffices for fixed \(\varepsilon<1\).  Naor and
Naor construct such spaces using
\(O(\log D+\log(1/\varepsilon))\) random bits [nn93][nn93].  A short seed
reduces mask description and randomness; it does not make the parity of an
implicitly represented \(D\)-bit fiber cheap.

## Precise comparison with neighboring tricks

**Universal hashing.**  All binary linear maps to \(\mathbb F_2^s\) form a
universal family in the Carter--Wegman pair-collision sense [cw79][cw79]:
\[
\Pr_A[Au=Av]=\Pr_A[A(u-v)=0]=2^{-s}\qquad(u\ne v)
\]
for an unrestricted random matrix.  The \(N+1\)-row proof compares each
\(v\in\mathcal V_f\) only with zero and union-bounds.  A perfect hash on
\(\{0\}\cup\mathcal V_f\) also separates nonzero fibers from one another and
is strictly stronger.  Linear-hashing work studies those broader collision
and bucket-size questions [admp99][admp99].

**Valiant--Vazirani isolation.**  Valiant and Vazirani add random
\(\mathbb F_2\) inner-product constraints to a SAT instance.  At a suitable
number of constraints, a nonempty solution set has a unique survivor with
inverse-polynomial probability [vv86][vv86].  Their map acts on witness points
\(y\), intersects them with hyperplanes, and returns another NP instance.
Here the map acts on the characteristic vector \(v_x\), returns parities, and
need not preserve any witness.  Valiant--Vazirani is randomized per instance;
our exact statement has quantifier order
\[
\forall f\ \exists A\ \forall x.
\]
It is inaccurate to say that \(A\) isolates a witness.  It separates zero
from a relation-dependent list of vectors.

**Parity sketches.**  Kannan, Mossel, Sanyal, and Yaroslavtsev formalize
randomized \(\mathbb F_2\)-linear sketches for Boolean functions
[kmsy18][kmsy18].  On the full domain \(\mathbb F_2^D\), OR has a constant-row
randomized one-sided sketch, but an exact deterministic linear sketch must
have dimension \(D\).  Gavinsky records the corresponding parity-query facts
\(R^\oplus(\mathrm{OR})=O(1)\) and
\(D^\oplus(\mathrm{OR})=D\) [gavinsky25][gavinsky25].  The latter is immediate:
fewer than \(D\) linear answers leave a nonzero vector consistent with zero.
Our distributional corollary is the usual randomized OR sketch applied to
\(v_x\); our exact \(r\le N\) result escapes the deterministic lower bound
only by restricting the domain to the finite realized set \(\mathcal V_f\).

**Detecting matrices.**  Lindstr\"om's detecting-set problem uses \(0/1\)
measurement columns so all bounded-coefficient **integer** sums are distinct.
In binary coin weighing it recovers every unknown binary vector from
nonadaptive subset-sum measurements [lindstrom65][lindstrom65].  Outputs are
integer counts, not parities, and can carry \(\Theta(\log D)\) bits.  The
classical binary optimum satisfies
\[
\lim_{D\to\infty}\frac{m(D)\log D}{D}=\log4.
\]
Our map uses arithmetic modulo two, tests only zero versus nonzero, and handles
only \(\mathcal V_f\).  A binary linear map detecting every nonzero vector
would be injective and need \(D\) outputs.  Relation dependence, not a mod-two
version of quantitative coin weighing, permits the short exact sketch.

## Nonuniformity, description, and gate cost

Conditional expectation finds the halving rows from the explicit fiber table.
The obvious way to obtain that table from a small circuit for \(f\) uses
\(2^{N+M}\) evaluations, so no size-sensitive construction follows.  Keep three quantifier orders distinct:

- forall \(x\), exists \(A_x\): input-specific fingerprinting;
- forall \(f\), exists \(A\), forall \(x\): this nonuniform theorem;
- exists \(A\), forall \(f\), forall \(x\): a universal exact sketch.

The last forces injectivity: if \(0\ne v\in\ker(A)\), choose a relation with
fiber \(v\).  An arbitrary dense \(s\times D\) matrix also has \(sD\) raw
description bits.  Codes and small-bias spaces can shorten its seed, but
circuit size is not advice length.

If all \(D\) fiber bits were materialized, the obvious parity trees for dense
rows use \(O(sD)\) gates.  In the verifier problem those bits are implicit;
independent verifier copies give only
\[
D\,C(f)+O(sD).
\]
Free fan-out shares the \(x\) wires and the witnesses are constants, but it
does not share internal verifier work.  Few outputs, short seeds, and one
extension-field symbol therefore do not imply few gates.  A circuit
improvement needs a separate aggregate-synthesis theorem; see
[candidate synthesis routes and barriers](../synthesis-barriers/index.md).

## Literature-location result, not a novelty claim

The search checked the cited primary work on universal and linear hashing,
Valiant--Vazirani isolation, small-bias spaces, perfect linear hashes, parity
sketches, and detecting sets.  Targeted queries also used "simultaneous zero
detection," "linear sketch zero test finite set," "kernel disjoint from a
finite set," and "linear map separates zero."

The exact Boolean-relation formulation
\[
\{v_x\}_x\xrightarrow{\text{one }f\text{-dependent linear map}
\mathbb F_2^{O(N)},\qquad Av_x=0\Longleftrightarrow v_x=0
\]
was **not located in this search**.  This is not evidence of novelty: the
proof is an immediate universal-hashing argument, and stronger nearby work
makes a linear map injective on a prescribed sparse set [cjw19][cjw19].
A priority claim would require a broader search of separating hash families,
finite-geometry blocking sets, and coding-theoretic zero tests.

## Takeaway

For \(N\ge1\), exact measurement compression uses at most \(N\) parities;
\(N+1\) gives the simplest independent-row proof.  Distributional one-sided
error \(2^{-t}\) uses only \(t\) parities.  Neither statement reduces gate
cost without a way to synthesize the aggregates from the verifier.  Regimes
that instead admit a small set of actual witnesses appear in
[verifier regimes admitting compression](../structural-regimes/index.md).

## Local References

- **[cw79]** J. Lawrence Carter and Mark N. Wegman, "Universal Classes of Hash
  Functions," *Journal of Computer and System Sciences* 18(2), 143--154
  (1979). DOI:
  [10.1016/0022-0000(79)90044-8](https://doi.org/10.1016/0022-0000(79)90044-8).
- **[vv86]** Leslie G. Valiant and Vijay V. Vazirani, "NP Is as Easy as
  Detecting Unique Solutions," *Theoretical Computer Science* 47, 85--93
  (1986). DOI:
  [10.1016/0304-3975(86)90135-0](https://doi.org/10.1016/0304-3975(86)90135-0).
- **[nn93]** Joseph Naor and Moni Naor, "Small-Bias Probability Spaces:
  Efficient Constructions and Applications," *SIAM Journal on Computing*
  22(4), 838--856 (1993). DOI:
  [10.1137/0222053](https://doi.org/10.1137/0222053).
- **[admp99]** Noga Alon, Martin Dietzfelbinger, Peter Bro Miltersen, Erez
  Petrank, and G\'abor Tardos, "Linear Hash Functions," *Journal of the ACM*
  46(5), 667--683 (1999). DOI:
  [10.1145/324133.324179](https://doi.org/10.1145/324133.324179).
- **[cjw19]** Lijie Chen, Ce Jin, and R. Ryan Williams, "Hardness Magnification
  for All Sparse NP Languages," *2019 IEEE 60th Annual Symposium on
  Foundations of Computer Science (FOCS)*, 1240--1255 (2019). DOI:
  [10.1109/FOCS.2019.00077](https://doi.org/10.1109/FOCS.2019.00077).
- **[kmsy18]** Sampath Kannan, Elchanan Mossel, Swagato Sanyal, and Grigory
  Yaroslavtsev, "Linear Sketching over \(\mathbb F_2\)," *33rd Computational
  Complexity Conference (CCC 2018)*, LIPIcs 102, 8:1--8:37 (2018). DOI:
  [10.4230/LIPIcs.CCC.2018.8](https://doi.org/10.4230/LIPIcs.CCC.2018.8).
- **[gavinsky25]** Dmytro Gavinsky, "Unambiguous Parity-Query Complexity,"
  *Random Structures & Algorithms* 66(3), e70010 (2025). DOI: [10.1002/rsa.70010](https://doi.org/10.1002/rsa.70010).
- **[lindstrom65]** Bernt Lindstr\"om, "On a Combinatorial Problem in Number
  Theory," *Canadian Mathematical Bulletin* 8(4), 477--490 (1965). DOI:
  [10.4153/CMB-1965-034-2](https://doi.org/10.4153/CMB-1965-034-2).

[cw79]: https://doi.org/10.1016/0022-0000(79)90044-8
[vv86]: https://doi.org/10.1016/0304-3975(86)90135-0
[nn93]: https://doi.org/10.1137/0222053
[admp99]: https://doi.org/10.1145/324133.324179
[cjw19]: https://doi.org/10.1109/FOCS.2019.00077
[kmsy18]: https://doi.org/10.4230/LIPIcs.CCC.2018.8
[gavinsky25]: https://doi.org/10.1002/rsa.70010
[lindstrom65]: https://doi.org/10.4153/CMB-1965-034-2
