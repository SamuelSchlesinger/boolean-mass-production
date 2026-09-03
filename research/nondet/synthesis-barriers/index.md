# Producing the fingerprints: an algebraic barrier and structural escapes

The output-fingerprint theorem in the preceding chapter says that, for one
fixed verifier, a short linear image can distinguish every realized nonzero
witness fiber from zero. It does not say that this image can be propagated
through the verifier gate by gate. This chapter makes that distinction exact.

There are three levels of statement below.

1. Results marked **proved here** are elementary algebraic or circuit
   statements, with complete proofs.
2. Results marked **known** are established properties of DNNF, bounded-width
   knowledge compilation, weighted model counting, or multiplicative coding.
3. Results marked **conditional** or **open** identify possible synthesis
   routes. They are not asserted circuit upper bounds.

No novelty claim is made for the connections to knowledge compilation,
tensor contraction, or multiplication-friendly encodings.

## 1. Where the missing computation lives

Let

```text
Y = {0,1}^M,          D = |Y| = 2^M,
R = F_2^Y.
```

The vector space `R` is also a commutative algebra under coordinatewise, or
Hadamard, multiplication:

```text
(u * v)(y) = u(y)v(y).
```

Fix a Boolean circuit for `f(x,y)`. For every wire `w` and deterministic
input `x`, define its witness profile

```text
V_w(x) = (w(x,y))_{y in Y} in R.
```

At an AND gate `w = u AND v`,

```text
V_w(x) = V_u(x) * V_v(x).
```

At a NOT gate, `V_w(x) = 1 + V_u(x)`, where `1` is the all-one vector and
addition is over `F_2`. Finally,

```text
g(x) = exists y f(x,y) = 1  iff  V_out(x) != 0.
```

The short fingerprint theorem supplies a linear map `A` for the *output*
profiles. A gatewise simulation would additionally need a cheap update rule
that turns sketches of two input profiles into a sketch of their product.
The next theorem shows why one fixed universal linear sketch cannot do this.

## 2. A fixed-sketch obstruction for AND

The obstruction is stronger than a failure of linear or bilinear update: the
update rule below may be an arbitrary function.

**Theorem 2.1 (classification of universally multiplicative linear sketches;
proved here).** Let `A:R -> F_2^r` be linear. The following are equivalent.

1. There is a function

   ```text
   Phi : A(R) x A(R) -> A(R)
   ```

   such that, for every `u,v in R`,

   ```text
   A(u * v) = Phi(Au,Av).
   ```

2. `ker(A)` is an ideal of the coordinatewise algebra `R`.

Every ideal of `R` has the form

```text
I_S = {u in R : u(y)=0 for every y notin S}
    = span{e_y : y in S}
```

for a unique subset `S subseteq Y`, where `e_y` is the unit vector at
coordinate `y`.

**Proof.** Suppose the update rule exists, and put `I=ker(A)`. If `k in I`
and `v in R`, then

```text
A(k * v) = Phi(0,Av) = A(0 * v) = 0.
```

Thus `k*v in I`, so `I` is an ideal.

Conversely, suppose `I=ker(A)` is an ideal. If `Au=Au'` and `Av=Av'`, write
`u'=u+k` and `v'=v+l` with `k,l in I`. Over `F_2`,

```text
u' * v' + u * v = k * v + u * l + k * l,
```

and every term on the right lies in `I`. Hence
`A(u'*v')=A(u*v)`. The formula

```text
Phi(Au,Av) = A(u*v)
```

is therefore well defined on `A(R) x A(R)`.

It remains to classify the ideals. Let `I` be an ideal and define

```text
S = {y in Y : e_y in I}.
```

If `u in I` and `u(y)=1`, then `e_y=e_y*u` lies in `I`; therefore every
nonzero coordinate of `u` belongs to `S`. Conversely, all `e_y` with
`y in S` lie in `I`, and `I` is a linear space, so their span is contained in
`I`. This proves `I=I_S` and uniqueness is immediate. QED.

**Corollary 2.2 (a universal sketch only drops coordinates; proved here).**
If `A` satisfies Theorem 2.1, then, up to an injective linear recoding of its
image, `A` is the coordinate projection that retains `Y minus S` and drops
`S`. In particular,

```text
rank(A) = D - |S|.
```

If the sketch must also distinguish zero from *every* nonzero vector of `R`,
then `S` is empty, `A` is injective, and `r >= D`.

**Proof.** The quotient `R/I_S` is canonically the coordinate space on
`Y minus S`. Since `A` has kernel `I_S`, its induced map from this quotient
to `A(R)` is a linear isomorphism. Universal zero detection forces
`ker(A)={0}`; rank-nullity then gives `r >= D`. QED.

The relation-specific version gives an even more useful bridge to witness
hitting.

**Corollary 2.3 (universal AND update reduces to actual-witness hitting;
proved here).** Suppose `A` satisfies Theorem 2.1 and, only for the realized
output profiles of one relation `f`, satisfies

```text
A(V_out(x))=0  iff  V_out(x)=0.
```

Write `ker(A)=I_S` and let `H=Y minus S`. Then `H` intersects every realized
nonempty witness fiber,

```text
rank(A) = |H|,
```

and there is a linear isomorphism `B:F_2^H -> A(R)` such that

```text
A(v) = B((v(y))_{y in H})       for every v in R.
```

Consequently,

```text
g(x) = OR_{y in H} f(x,y),
C(g) <= |H| C(f) + |H| - 1
```

when `H` is nonempty.

**Proof.** A vector belongs to `I_S` exactly when its support is contained in
`S`. If a realized nonzero profile had no nonzero coordinate in `H`, its
support would lie in `S` and `A` would kill it, contrary to the zero-detection
hypothesis. Thus `H` hits every realized nonempty fiber. Corollary 2.2 gives
`rank(A)=D-|S|=|H|` and the factorization through coordinate restriction,
with an isomorphism onto `A(R)`. The displayed identity for `g` follows from
the hitting property; hardwire the witnesses in `H` into `|H|` verifier
copies and OR their outputs to get the circuit bound. QED.

If `H` is empty, the hypothesis forces every realized profile to be zero, so
`g` is the constant-zero function.

Thus, in the fixed-sketch, full-algebra update model, a relation-dependent
linear fingerprint is exactly no stronger than an actual-witness hitting set.
Any genuinely different code route must weaken the universal update demand,
change representations between wires, or exploit a restricted profile space.

This is the useful content of the ideal condition. A universally composable
linear sketch cannot obtain genuine compression by blending many witness
coordinates into parities. Up to a reversible linear recoding of its image,
it can only forget a fixed set of coordinates and retain the rest.

### The two-bit parity collision

For `D=2`, let `A(a,b)=a+b`. Take

```text
u  = (1,0),
u' = (0,1),
v  = (1,0).
```

Then `Au=Au'=Av=1`, but

```text
A(u*v)  = 1,
A(u'*v) = 0.
```

No function of the two input parity bits can produce both answers. In the
kernel language, `(1,1)` is killed by parity, but
`(1,1)*(1,0)=(1,0)` is not.

### Exact scope of the obstruction

The quantifiers are essential. The theorem assumes

```text
for all u,v in R,
```

uses the same map `A` at the two inputs and output, and asks for one update
rule valid on the full algebra. The relation-dependent output fingerprint
only promises zero detection on the finite family

```text
{V_out(x) : x in {0,1}^N}.
```

It may collide on every other vector. Likewise, a verifier-specific
simulation need only process pairs of profiles that actually arise from the
same `x`, and it may change representations from one wire to the next.
Theorem 2.1 does not rule out either escape. It rules out the tempting but
incorrect inference that an arbitrary short parity fingerprint can simply be
pushed through every AND gate.

## 3. The realized-state escape, and its own cost

There is a precise criterion for when sketches can be updated on only the
realized profiles.

**Lemma 3.1 (realized-state congruence; proved here).** Let `X` be any finite
set, and for each `x in X` let

```text
a_x, b_x, c_x in R,          c_x = a_x * b_x.
```

Let `A_u,A_v,A_w` be arbitrary maps from `R` to finite sets. There is a
function `Phi` satisfying

```text
Phi(A_u(a_x), A_v(b_x)) = A_w(c_x)       for every x in X
```

if and only if, for every `x,x' in X`,

```text
A_u(a_x)=A_u(a_x') and A_v(b_x)=A_v(b_x')
    imply A_w(c_x)=A_w(c_x').
```

**Proof.** Necessity follows by applying `Phi` to the same input pair. For
sufficiency, define `Phi` on each realized pair by its required output. The
displayed implication makes this definition independent of the chosen
representative `x`. Extend `Phi` arbitrarily to unrealized pairs. QED.

This criterion avoids the universal-algebra obstruction, but it is only a
well-definedness criterion. It says nothing about the gate count of `Phi`.
If the three sketches have bit lengths `r_u,r_v,r_w`, a naive truth-table
implementation of an arbitrary extension of `Phi` can use

```text
O(r_w (r_u+r_v) 2^(r_u+r_v))
```

AND/OR/NOT gates: synthesize a DNF for each output bit. Short state names can
therefore hide exponentially expensive transition logic.

The exact circuit target can be stated without ambiguity.

**Conditional target 3.2 (compressed profile system).** For every wire `w`,
suppose there is a profile code

```text
q_w : {0,1}^N -> {0,1}^{r_w},
```

with free or explicitly bounded leaf encoders, a transition circuit of size
`tau_w` at every internal gate, and an output test `Z_out` of size `tau_out`
such that

```text
Z_out(q_out(x)) = 1  iff  V_out(x) != 0.
```

Then composing these transition circuits in the verifier DAG gives

```text
C(g) <= tau_out + sum_w tau_w + leaf-encoding cost.
```

This is a bookkeeping lemma, not a construction. It identifies what a code
trick must actually provide: short profiles, cheap updates, and an exact final
zero test, all at once. Proving only the first and third items is insufficient.

## 4. A rigorous changing-basis simulation

The next sufficient condition is deliberately stronger than Lemma 3.1, but
it gives explicit transition circuits instead of arbitrary lookup tables.

For linear subspaces `E,F subseteq R`, write

```text
E * F = span{u*v : u in E, v in F}.
```

An **admissible profile-space family** for an AND/NOT verifier assigns a
linear subspace `E_w subseteq R` to each wire so that all realized profiles
belong to it and:

- if `w=NOT u`, then `1 in E_w` and `E_u subseteq E_w`;
- if `w=u AND v`, then `E_u * E_v subseteq E_w`.

Such a family always exists by recursively taking these spans, but its
dimensions may grow all the way to `D`.

**Theorem 4.1 (profile-space simulation; proved here).** Put
`k_w=dim(E_w)`. In a basis with binary AND, XOR, and NOT gates, the
existential projection has a circuit of size at most

```text
T = sum_{w=NOT u} k_w (k_u+1)
  + sum_{w=u AND v} (k_w+1) k_u k_v
  + max(0,k_out-1).
```

Over the paper's basis `{AND_2,OR_2,NOT}`, the same construction has size at
most `4T`. Consequently, if every profile-space dimension is at most `k`
and the AND/NOT verifier has `S` gates, then

```text
C(g) = O(S k^3 + k).
```

Replacing each OR gate of an AND/OR/NOT verifier by
`NOT(NOT u AND NOT v)` changes `S` by only a constant factor before applying
the theorem.

**Proof.** Fix a basis

```text
b_{w,1},...,b_{w,k_w}
```

of every `E_w`. Since `V_w(x) in E_w`, it has a unique coefficient vector
`c_w(x) in F_2^{k_w}`.

At a deterministic input wire `x_i`, the profile is `x_i*1`; its coefficient
vector consists only of copies of `x_i` and constants. A witness input wire
has a fixed profile `(y_i)_{y in Y}` and hence a constant coefficient vector.
Both use free fan-out and constants.

At `w=NOT u`, the map

```text
V_u |-> 1 + V_u
```

is affine from `E_u` to `E_w`. In the chosen bases, every one of its `k_w`
output coefficients is an affine parity of at most `k_u` input bits. It can
be computed with at most `k_u+1` XOR/NOT gates, giving the first sum.

At `w=u AND v`, coordinatewise multiplication is bilinear. Therefore there
are structure constants `m_{l,i,j} in F_2` such that

```text
c_w(x)_l = sum_{i=1}^{k_u} sum_{j=1}^{k_v}
           m_{l,i,j} c_u(x)_i c_v(x)_j.
```

Compute all `k_u k_v` pairwise products once with AND gates, then compute the
`k_w` indicated parities. This uses at most
`(k_w+1)k_u k_v` mixed-basis gates.

At the output, linear independence of the basis gives

```text
V_out(x) != 0  iff  c_out(x) != 0.
```

An OR of the `k_out` coefficient bits costs `k_out-1` gates. Finally, one
binary XOR can be implemented by four gates in the standard basis, while
AND, OR, and NOT are already available. Multiplying the whole mixed-basis
count by four is therefore safe. QED.

This is a nonuniform construction. The bases and transition tensors are
hardwired into the resulting circuit. The theorem does not bound the time
needed to discover suitable spaces or bases from a succinct verifier.

The coefficients `m_{l,i,j}` form a rank-three transition tensor. Sparse
tensors or low bilinear rank can improve the displayed dense bound: compute
only the products that occur and only the nonzero tensor entries. This is
the literal connection to tensor-network and dynamic-programming language.
It does not, by itself, bound the relevant dimensions or sparsities. The
standard relation between bounded graph width and efficient tensor
contraction is developed, in a different circuit-simulation setting, by
Markov and Shi [ms08][ms08].

### Why output-span dimension alone is not a new circuit bound

The profile simulation has an important elementary dominance check.

**Lemma 4.2 (information set; proved here).** If `W subseteq F_2^Y` has
dimension `r`, there is a set `H subseteq Y` of size `r` such that the
coordinate restriction

```text
pi_H : W -> F_2^H
```

is injective.

**Proof.** Put a basis of `W` in the rows of an `r by D` matrix. Its rank is
`r`, so it has `r` linearly independent columns. Take their coordinate
indices as `H`. Restriction to those columns maps the chosen basis to an
invertible `r by r` matrix and is therefore injective on `W`. QED.

**Corollary 4.3 (output span gives actual witnesses; proved here).** Let

```text
W_out = span{V_out(x) : x in {0,1}^N},
r_out = dim(W_out).
```

There is a fixed set `H` of `r_out` actual witnesses such that

```text
g(x) = OR_{y in H} f(x,y),
C(g) <= r_out C(f) + r_out - 1
     = r_out (C(f)+1) - 1
```

when `r_out>0`; if `r_out=0`, then `g` is constant zero.

**Proof.** Choose `H` by Lemma 4.2. A profile in `W_out` is nonzero if and
only if one of its coordinates in `H` is nonzero. Hardwire each `y in H`
into a copy of the verifier and OR the outputs. QED.

Thus a small linear output space already yields a small actual-witness set.
Under only a dimension hypothesis, the replication bound in Corollary 4.3 is
stronger than the dense `O(Sk^3)` profile-space bound. The profile formalism
is useful as a conceptual account of gatewise compression, as an algorithmic
representation when the transition tensors are already available, or when
their sparsity yields a sharper implementation. It should not be advertised
as a better nonuniform circuit theorem from output-span dimension alone.

## 5. Established structural routes

### 5.1 DNNF: existential quantification by forgetting

**Known result.** A negation normal form is decomposable (DNNF) when the
children of every AND gate mention disjoint variable sets. Given a DNNF for
`f(x,y)`, existentially forgetting all witness variables can be done in linear
time without increasing its asymptotic size: replace every literal on a
forgotten variable, positive or negative, by true and simplify. The result
computes `exists y f(x,y)` and remains a DNNF. Darwiche proves this operation
and its linear-time bound [darwiche99][darwiche99]; the full journal treatment
also proves the relevant compilation results [darwiche01][darwiche01].

The decomposability condition is exactly what makes replacement commute with
AND. If two conjuncts could both constrain the same forgotten variable, the
naive replacement would be unsound: `(y AND NOT y)` would become true. This
example is forbidden at a decomposable AND.

Therefore, if the verifier is already supplied as a DNNF of size `s`, then

```text
C(g) = O(s).
```

The qualification "already supplied" matters. An arbitrary small Boolean
circuit need not have a comparably small DNNF, so compilation cost cannot be
silently omitted.

### 5.2 Determinism, smoothness, and weighted model counting

**Known result.** A DNNF is deterministic when different children of every
OR gate have disjoint satisfying-assignment sets. In a smooth deterministic
DNNF, bottom-up arithmetic evaluation computes model counts: use addition at
OR gates and multiplication at decomposable AND gates. Determinism prevents
double counting, decomposability makes the product factorization valid, and
smoothness aligns the variable domains. Darwiche gives linear-time counting
algorithms for deterministic DNNF [darwiche-count01][darwiche-count01].
Literal weights turn the same sum-product evaluation into weighted model
counting; Chavira and Darwiche develop this compilation-based framework for
exact probabilistic inference [cd08][cd08].

For the present problem, fixing `x` and counting the satisfying `y` gives

```text
Z(x) = |{y : f(x,y)=1}|,
g(x) = 1 iff Z(x)>0.
```

Counting is stronger than the existential decision, and plain DNNF
forgetting is enough for the latter. Determinism and weighted counting become
relevant when the desired summary is a count, parity, weight, or when further
quantifier operations must preserve a structured representation.

### 5.3 Treewidth and structured width

**Known result.** Darwiche's DNNF compilation of a CNF is exponential only
in the CNF's treewidth and linear in the remaining input size; in particular,
fixed-treewidth CNFs have linear-size, linearly constructible DNNFs
[darwiche99][darwiche99] [darwiche01][darwiche01]. Combining compilation
with forgetting gives, schematically,

```text
size(exists y F) <= 2^O(k) |F|
```

for a CNF `F` of treewidth `k`, with the precise polynomial factors depending
on the graph and compilation conventions.

Capelli and Mengel study a more restrictive output requirement: preserving a
complete structured deterministic DNNF through quantification. For one
existential forgetting operation, their construction takes width `w` to at
most `2^w`; its size blow-up depends on width rather than on the input size.
They also prove lower bounds showing that several parts of the bounded-width
analysis are essentially optimal and that the structural hypotheses cannot
simply be discarded [cm19][cm19].

There is no contradiction with linear DNNF forgetting. Replacing literals by
true preserves DNNF, but it need not preserve determinism or a chosen
structure. The bounded-width result pays to remain in the stronger language,
which supports subsequent counting and quantifier elimination.

These methods instantiate the profile-space intuition with separator states:
only the behavior on a small boundary is retained, and decomposability tells
the dynamic program how independent pieces combine. Their power comes from
an explicit structural width bound, not from hashing an unrestricted
`2^M`-coordinate witness table.

### 5.4 Why generic counting hardness is only context

The parity aggregate

```text
x |-> XOR_y f(x,y)
```

and the integer count `Z(x)` are standard parity-counting and model-counting
objects. Valiant's counting framework establishes the hardness of broad
families of exact counting problems [valiant79][valiant79]. This explains
why producing an aggregate should not be treated as a free wiring step.

It does not prove a Boolean circuit lower bound for the functions in this
note. Uniform `#P`-hardness and nonuniform circuit size are different claims.
The rigorous barrier supplied here is Theorem 2.1; complexity-class evidence
is only motivation for not assuming cheap aggregate evaluation.

## 6. Multiplication-friendly encodings: a candidate, not a theorem

Multiplication-friendly codes and multiplicative linear secret-sharing
schemes provide linear encodings for which products can be reconstructed from
coordinatewise products. In a typical multiplication-friendly pair, a
smaller extension-field algebra is linearly embedded into a longer base-field
coordinate vector, and a linear reconstruction recovers a product. Cascudo,
Cramer, Xing, and Yang formulate this viewpoint for finite-field
multiplication [ccxy12][ccxy12]. Cramer, Damgard, and Maurer develop the
closely related multiplicativity condition for linear secret sharing
[cdm00][cdm00].

The direction of compression matters. These constructions expand a
lower-dimensional algebra into enough coordinates to support multiplication.
Here the naive target would compress the full algebra

```text
R = F_2^{2^M}
```

to a few bits while retaining arbitrary coordinatewise products. An
injective linear encoding of all of `R` already needs `2^M` bits, and Theorem
2.1 shows that even an arbitrary universal product update cannot turn a
noninjective fixed linear sketch into a mixed parity representation: it can
only quotient out coordinate ideals.

There are still two honest candidate routes.

1. **Restricted product spaces.** If every reachable profile lies in a
   small space and products of child spaces land in a controlled next space,
   Theorem 4.1 applies. Low witness degree is a concrete example: degrees add
   at multiplication gates, and the degree-`d` multilinear space has dimension

   ```text
   sum_{i=0}^d binom(M,i).
   ```

   The preceding structural chapter analyzes the resulting Reed-Muller
   information sets. Corollary 4.3 must be checked before claiming any
   additional gain from propagation.

2. **Changing, realized-state codes.** Different wires may use different
   sketches, and transition rules may be required only on verifier-realizable
   state pairs. Lemma 3.1 gives the exact consistency condition. What is
   missing is a general method that simultaneously bounds sketch length and
   transition-circuit size.

This motivates the following open problem.

**Open problem 6.1 (multiplicative fingerprint systems).** Identify natural
verifier classes broader than decomposable or bounded-width representations
for which one can construct, from the verifier, relation-dependent profile
codes with:

```text
- exact zero detection at the output,
- total transition size substantially below 2^M C(f), and
- a construction or nonuniform existence proof whose cost model is explicit.
```

A satisfactory result must account for the Boolean gates that form the coded
summaries. A bound on the number of summaries, their field width, or their
description length alone is not enough.

## 7. Status summary

| Statement | Status | What it does and does not establish |
|---|---|---|
| Fixed linear sketch with universal AND update | Proved here | Kernel must be a coordinate ideal; mixed parity compression is impossible in this model |
| Relation-specific zero test plus universal AND update | Proved here | Exactly retains an actual-witness hitting set, up to reversible recoding |
| Realized-state congruence | Proved here | Characterizes existence of an update table, not its circuit size |
| Profile-space simulation | Proved here | Gives an explicit `O(Sk^3)` dense transition bound |
| Output-span information set | Proved here | Gives `r_out` actual witnesses and dominates the dense profile bound under span information alone |
| DNNF forgetting | Known | Gives linear-size projection when a DNNF representation is already available |
| Deterministic DNNF counting | Known | Computes counts or weights; requires stronger representation properties |
| Bounded treewidth/structured width | Known, model-specific | Gives width-parameterized compilation and quantification |
| Multiplication-friendly profile compression | Conditional/open | Requires restricted spaces or changing realized-state codes plus cheap updates |

The central conclusion is narrow but useful:

```text
A short exact output fingerprint is not yet a short deterministic circuit.
AND forces either retained witness coordinates, restricted profile geometry,
or explicitly synthesized verifier-specific transition logic.
```

## Local references

- **[darwiche99]** Adnan Darwiche. "Compiling Knowledge into Decomposable
  Negation Normal Form." *Proceedings of IJCAI 1999*, 284-289. The primary
  IJCAI paper contains the linear-time forgetting operation and the
  treewidth-sensitive compilation statement. [Primary PDF][darwiche99].
- **[darwiche01]** Adnan Darwiche. "Decomposable Negation Normal Form."
  *Journal of the ACM* 48(4):608-647, 2001.
  [doi:10.1145/502090.502091][darwiche01].
- **[darwiche-count01]** Adnan Darwiche. "On the Tractable Counting of Theory
  Models and its Application to Belief Revision and Truth Maintenance."
  *Journal of Applied Non-Classical Logics* 11(1-2):11-34, 2001.
  [Primary preprint][darwiche-count01].
- **[cd08]** Mark Chavira and Adnan Darwiche. "On Probabilistic Inference by
  Weighted Model Counting." *Artificial Intelligence* 172(6-7):772-799,
  2008. [doi:10.1016/j.artint.2007.11.002][cd08].
- **[cm19]** Florent Capelli and Stefan Mengel. "Tractable QBF by Knowledge
  Compilation." *36th Symposium on Theoretical Aspects of Computer Science
  (STACS 2019)*, LIPIcs 126, 18:1-18:16.
  [doi:10.4230/LIPIcs.STACS.2019.18][cm19].
- **[ccxy12]** Ignacio Cascudo, Ronald Cramer, Chaoping Xing, and An Yang.
  "Asymptotic Bound for Multiplication Complexity in the Extensions of Small
  Finite Fields." *IEEE Transactions on Information Theory* 58(7):4930-4935,
  2012. [doi:10.1109/TIT.2011.2180696][ccxy12].
- **[cdm00]** Ronald Cramer, Ivan Damgard, and Ueli Maurer. "General Secure
  Multi-Party Computation from any Linear Secret-Sharing Scheme."
  *EUROCRYPT 2000*, LNCS 1807, 316-334.
  [Primary author record and paper][cdm00].
- **[valiant79]** Leslie G. Valiant. "The Complexity of Enumeration and
  Reliability Problems." *SIAM Journal on Computing* 8(3):410-421, 1979.
  [doi:10.1137/0208032][valiant79].
- **[ms08]** Igor L. Markov and Yaoyun Shi. "Simulating Quantum Computation by
  Contracting Tensor Networks." *SIAM Journal on Computing* 38(3):963-981,
  2008. [doi:10.1137/050644756][ms08]. It is cited only for the standard
  treewidth/tensor-contraction connection, not as a result about the present
  classical nondeterministic-circuit model.

All metadata and links in this reference list were checked against primary
publisher, proceedings, author, or repository records on 2026-09-03.

[darwiche99]: https://www.ijcai.org/Proceedings/99-1/Papers/042.pdf
[darwiche01]: https://doi.org/10.1145/502090.502091
[darwiche-count01]: https://arxiv.org/abs/cs/0003044
[cd08]: https://doi.org/10.1016/j.artint.2007.11.002
[cm19]: https://doi.org/10.4230/LIPIcs.STACS.2019.18
[ccxy12]: https://doi.org/10.1109/TIT.2011.2180696
[cdm00]: https://crypto-test.ethz.ch/publications/CrDaMa00.html
[valiant79]: https://doi.org/10.1137/0208032
[ms08]: https://doi.org/10.1137/050644756
