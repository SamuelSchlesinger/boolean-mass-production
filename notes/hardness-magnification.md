# Mass production and hardness magnification: research notes

These notes preserve the broader exploration removed from Section 12 on
September 13, 2026. The manuscript now concentrates on its proved local
hardness amplification application. The calculations below separate useful
synthesis consequences from requirements for a new magnification theorem;
the proposed applications remain research directions. The conditional
inverse-bit observation below was moved here during the subsequent scope
review.

## What the encoding result establishes

For every fixed $0\le\tau<1$ and $\eta>0$, the paper constructs an encoding
$g=E_n(f)$ on $cn$ input bits, for a fixed integer $c$, with

$$
K_{1/2-\varepsilon_n}(g)\ge K(f)-o(2^n),\qquad
C(g^{\times t})\le
\left(\frac{1}{1-\tau}+\eta\right)\frac{2^n}{n},
\quad t\le2^{\tau n},
$$

where $\varepsilon_n=2^{-\lfloor\alpha n\rfloor}$ for a sufficiently small
constant $\alpha>0$. A random source has $K(f)\ge2^n-n$ with probability
at least $1-2^{-n}$. Circuit counting then gives
$C_{1/2-\varepsilon_n}(g)\ge(1-o(1))2^n/n$.

The consequence is an exponential batch at a constant multiple of even the
approximate one-copy circuit cost. The amplification and reconstruction
ingredient is [Hirahara's Lemma 8.1](https://eccc.weizmann.ac.il/report/2022/119/);
the quantitative batch synthesis bound comes from this paper. The scale is
the source length $L=2^n$, rather than the encoded table length $2^{cn}$.
The source is random, so the result does not give an explicit exponential
circuit lower bound. A lower bound on $C(f)$ alone cannot replace the
Kolmogorov hypothesis: an unlimited-time short program can describe a
function with high circuit complexity.

## Oracle substitution and its limitation

Suppose a nonadaptive circuit $R^f$ makes $q$ queries to a fixed function
$f:\{0,1\}^m\to\{0,1\}$, with $s$ ordinary gates. Running $t$ copies
around one shared oracle batch gives

$$
C((R^f)^{\times t})\le ts+C(f^{\times qt}).
$$

Query addresses may repeat or share inputs. Preserve the ordinary values
computed before the oracle layer when routing answers to the remaining
gates. If the ordinary circuit has depth $d$, the resulting depth is at
most $2d+O_\gamma(m)$ when $qt\le2^{\gamma m}$. The linear-depth bound
and the sharp leading coefficient are separate guarantees.

Different fixed functions require separate batches unless they have a
common representation that permits additional sharing. Adaptive calls can
be grouped by round, with each round's cost and depth paid before the next.

For an $N$-bit problem $Q_N$ with a nonadaptive oracle implementation using
$s_N$ ordinary gates and $q_N$ calls to one fixed $h_m$, a circuit of size
$c_m$ for the oracle gives the accounting bound

$$
C(Q_N)\le s_N+
\min\left\{q_Nc_m,\ A_\gamma\frac{2^m}{m}\right\},
\qquad q_N\le2^{\gamma m}.
$$

There is a decisive limitation when a hypothesized complexity-class
collapse supplies polynomial-size oracle circuits. For every fixed $k$
and $\gamma<1$,

$$
\frac{q_Nm^k}{2^m/m}
\le m^{k+1}2^{-(1-\gamma)m}\longrightarrow0.
$$

Replication then beats the absolute mass-production bound throughout its
allowed range, regardless of the relationship between $m$ and $N$.
Consequently the present theorem does not improve the usual substitution
of polynomial-size oracle circuits under a class-collapse assumption.
Hirahara's random incompressible tables are a different case: they are
allowed to require close to the worst-case synthesis cost.

There is another logical distinction. If the oracle implementation itself
exists unconditionally, its absolute synthesis bound also holds
unconditionally. Lowering that bound establishes an upper bound on $Q_N$;
it cannot by itself yield a new attainable lower-bound threshold whose
violation magnifies to a separation. Conditional existence or additional
structure elsewhere in a reduction would have to do essential work.

## The parameters in Hirahara's partial-MCSP reduction

The reference is the ECCC full version of
[NP-Hardness of Learning Programs and Partial MCSP](https://eccc.weizmann.ac.il/report/2022/119/),
especially Lemmas 8.1–8.3 and Theorem 8.5. Hirahara attaches random tables
to variables of a monotone satisfiability instance, locally amplifies
them, and uses their pseudorandom outputs to mask secret shares. A
satisfying assignment identifies tables sufficient to recover the secret;
the soundness proof reconstructs information about those tables from a
successful short predictor.

Write $v$ for the number of variables, $\Delta$ for the degree parameter,
and $\varepsilon_0$ for the soundness parameter. A table for variable $i$
has length $w_i\lambda$, with $w_i\ge1$, and is padded to length
$L_i=2^{n_i}$ for $n_i=\lceil\log_2(w_i\lambda)\rceil$.
The completeness proof evaluates $\Delta$ encoded bits, using

$$
R=O\left(\frac{\Delta}{\varepsilon\delta}\right)
 =O\left(\frac{\Delta^3\log v}{\varepsilon_0}\right),
\qquad
\delta=\frac1{\log_2v},\quad
\varepsilon=\frac{\varepsilon_0}{2\Delta^2}
$$

nonadaptive queries per selected source table. Uhlig allows
$R=L_i^{o(1/\log\log L_i)}$ at size $O(L_i/\log L_i)$ and depth
$O(\log L_i)$. Our theorem permits $R\le L_i^\gamma$ for every fixed
$\gamma<1$, with the same size and depth orders.

The other local costs still matter. The ordinary circuitry in this part
costs $\operatorname{poly}(\Delta\log(w_{\max}\lambda)/(\varepsilon\delta))$.
The local reconstruction loses

$$
O\left(\sqrt{w_i\lambda}\,
       \operatorname{poly}(1/(\varepsilon\delta))\right)
 +H_2(\delta)w_i\lambda+O(\log(w_{\max}\lambda))
$$

description bits per table. If $\Delta,w_{\max},\varepsilon_0^{-1}$ are
polynomially bounded in $v$, taking $\lambda=v^B$ for sufficiently large
fixed $B$ makes $R\le\lambda^\gamma$, the displayed ordinary gate cost
$o(\lambda/\log\lambda)$, and the local description loss $o(w_i\lambda)$.
This calculation checks these local costs; it is not a restatement of the
entire reduction with an improved hardness theorem.

Theorem 8.5 uses $\Delta=(\log v)^{1/2}$, which already fits Uhlig's
query range. Its explicit partial truth table has length
$2^{O(\log v+\Delta^2)}$. Increasing the allowed local query count
therefore does not automatically improve the final approximation gap:
the source gap and output length must improve compatibly. The fixed
nonuniform menus are sufficient for the existential completeness
witness; the reduction computes its encoded table independently of
constructing that witness.

## Magnification, locality, and structured witnesses

[Oliveira–Santhanam](https://eccc.weizmann.ac.il/report/2018/139/) and
[Oliveira–Pich–Santhanam](https://theoryofcomputing.org/articles/v017a011/)
develop implications from modest lower bounds for meta-computational
problems to major complexity separations. Their results concern several
models. Our substitution supplies unrestricted Boolean circuits; it does
not preserve formula size, constant depth, or branching-program size.

The locality analysis of
[Chen, Hirahara, Oliveira, Pich, Rajgopal, and Santhanam](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70)
concerns efficient circuits with small-arity oracle gates and lower-bound
methods that extend to such circuits. Mass production gives an
implementation of repeated fixed oracles in a specified range. It supplies
no new lower-bound method that escapes their locality barrier.

A hypothesis supplied on a live input also cannot be hardwired separately
for each input to a learner or reduction. A universal evaluation function
can serve as a fixed oracle, but its input arity includes the hypothesis
description. That enlarged arity belongs in the synthesis bound.

Hirahara's
[meta-computational framework](https://toc.cs.uchicago.edu/articles/v019a004/),
particularly Section 1.3.4, relates structured promise problems and
hitting-set generators through non-black-box reconstruction. An application
of our encoding would have to match the framework's specified easy
functions and preserve its quantitative reconstruction bounds. Random
incompressible sources do not establish those requirements.

## Pseudorandom generators and uniform batch computation

For fixed sets $S_1,\ldots,S_r\subseteq[d]$ of size $n$, the
[Nisan–Wigderson construction](https://doi.org/10.1016/S0022-0000(05)80043-1)
has the form

$$
G_f(z)=(f(z|_{S_1}),\ldots,f(z|_{S_r})).
$$

The projections are free wiring. For $r\le2^{\gamma n}$, this map has
size $O_\gamma(2^n/n)$ and depth $O_\gamma(n)$. When the generator uses
$E_n(f)$, flatten its calls to $f$ and apply the encoding theorem's batch
bound. The circuit implements exactly the same map; security still
requires the generator's hardness and design hypotheses.

Uniform batch evaluation is also central to
[Doron et al. (2022)](https://doi.org/10.1145/3555307) and
[Chen–Tell (2021)](https://eccc.weizmann.ac.il/report/2020/148/revision/1/).
They need quantitative running-time guarantees, including the cost of
computing the source table. An unspecified polynomial-time constructor
from a supplied full table does not establish comparable speedups.

For a recent explicit example, the batch fine-grained assumption in
[Doron et al. (2026), Section 1.2](https://eccc.weizmann.ac.il/report/2026/082/revision/1/)
requires printing the entire hard truth table deterministically in time
$2^{(1+\xi)n}$ for a small constant $\xi>0$. This is enumeration of all
$2^n$ inputs. Our circuit theorem handles at most $2^{\gamma n}$ arbitrary
live queries to a specified table. Deterministic menu construction would
address only one part of the additional uniform requirements.

## A conditional inverse-bit bound

This elementary observation transfers an inversion assumption to a specified
Boolean family. It does not use the mass-production theorem.

Let $(P_m)_{m\ge2}$ be a polynomial-time computable family of permutations
of $\{0,1\}^m$. Suppose every nonuniform Boolean circuit
$I:\{0,1\}^m\to\{0,1\}^m$ satisfying

$$
\Pr_{y\text{ uniform in }\{0,1\}^m}[I(y)=P_m^{-1}(y)]\ge\tfrac12
$$

has at least $H(m)$ gates. Define a Boolean function on
$m+\lceil\log_2m\rceil$ input bits by

$$
h_m(y,j)=
\begin{cases}
(P_m^{-1}(y))_j,&0\le j<m,\\
0,&\text{otherwise}.
\end{cases}
$$

Then, for every integer $t\ge1$,

$$
C(h_m^{\times t})\ge\frac{H(m)}{\lceil m/t\rceil}.
$$

To prove this, let a circuit of size $S$ compute $h_m^{\times t}$ exactly.
Use $\lceil m/t\rceil$ copies of it, wiring the same $y$ into every request
slot and hardwiring the indices $0,\ldots,m-1$ across the slots. Pad any
remaining slots with index zero and discard their outputs. The retained
outputs give $P_m^{-1}(y)$ for every $y$, using at most
$\lceil m/t\rceil S$ gates. The inversion assumption gives the inequality.

For $1\le t\le m$, the lower bound is at least $tH(m)/(2m)$; for $t\ge m$,
it is $H(m)$. Exponential inversion hardness therefore gives an exponential
circuit lower bound, but this reduction supplies no further growth after
$t=m$. The predicate $h_m$ itself need not be efficiently evaluable.
The result neither compares $C(h_m^{\times t})$ with $tC(h_m)$ nor closes
the unrestricted leading-coefficient gap. These limitations motivated moving
the observation out of the manuscript.

## Directions worth returning to

1. **Use the larger local query budget in a stronger reduction.** The
   encoding permits inverse-polynomial prediction advantage in the source
   table length while retaining $L/\log L$ synthesis cost. A useful next
   theorem would improve a source gap while keeping the final output
   polynomially bounded. The query bound alone is not the bottleneck in
   Hirahara's published choice of parameters.
2. **Obtain sharing bounds sensitive to actual circuit size.** In a regime
   where absolute synthesis is too expensive, seek an improvement over
   $\min\{qC(h_m),O_\gamma(2^m/m)\}$. This could use structure shared by
   different local oracles as well. If $h_m$ depends on all its variables,
   the unavoidable input-dependence cost is $q(m-1)$ gates, as proved in
   the paper's discussion section.
3. **Match a structured reconstruction framework.** Specify the easy
   source family and the intended promise problem first, then check whether
   the local encoding preserves the needed witnesses and reconstruction
   costs. The current Kolmogorov argument does not do this for an explicit
   circuit-hard source.
4. **Develop uniform implementations with a concrete time target.** State
   the required costs for obtaining the source table, constructing menus,
   compiling the circuit, and evaluating it. Polynomial time in the full
   table length is insufficient when the intended application requires
   nearly linear time.
