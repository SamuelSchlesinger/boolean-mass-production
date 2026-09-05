# Review and substantial improvements

The existing order-of-growth theorem has a coherent proof under its stated
nonuniform, bounded-fan-in, free-fan-out circuit model. The review did not find
a counterexample to its packing, greedy scheduling, routing, or equal-block
induction. Its largest avoidable costs were the quadratic greedy scheduler,
the product code's low rate, and rounding a single code's field size upward.

The revision adds two written results to `main.tex`:

1. **A nonuniform scheduler with linear dependence on the batch size.** For
   `512 g q <= D_q`, the circuit size is `~O_ell(g q)`, replacing
   `~O_ell(g^2 q)`. Its small fixed menus work for every target multiset and
   every occupied set described by at most `g` recovery lines. This supplies
   a direct proof of exponential-range mass production with no recursive
   resource evaluation.
2. **An explicit asymptotic coefficient.** For every fixed `0 <= gamma < 1`,
   uniformly in `f` and `t <= 2^(gamma n)`, the bound is
   `(1/(1-gamma) + o_gamma(1)) * 2^n/n`. This replaces an unspecified
   gamma-dependent constant. It is an upper coefficient, not a matching
   optimality theorem.

The elementary essential-input lower bound also improves from `tn/2` to
`t(n-1)`. After pruning unused gates, there are at most `t` connected
components. Comparing the minimum edge count `tn + s - t` with the fan-in
bound `2s` proves the claim. The near-endpoint asymptotic obstruction remains
`t = omega(2^n/n^2)`.

## Why the scheduler bound holds

For `k` active requests, independently sampled directions fail to leave half
the requests entirely collision-free with probability at most `2^-k`, under
the fixed slack condition. Collision indicators are not independent. The
proof instead two-colors a spanning forest and selects `ceil(k/4)` bad
requests from one color. Every selected request has a collision witness
outside that selected set. Fixing the complementary directions makes the
selected tests independent; a union bound over selected sets gives the tail.
This is the argument formalized in `CollisionCut` and `CollisionTail`.

An occupied set is described by at most `g` anchors and directions, regardless
of its `g(q-1)` enumerated points. There are at most
`2^(g(1+3 log2 N))` relevant states, including the active target list. A union
bound therefore gives a menu of
`ceil((g(1+3 log2 N)+1)/k)` candidates working for all states.

There are only `O(g log N)` candidate lines at each phase. The circuit checks
all candidates together against **one copy** of the occupied-point list,
using sorting and propagation along equal-key runs. Replicating the occupied
list for each candidate would destroy the desired bound at small `k`.
Accepting exactly `ceil(k/2)` clean requests gives fixed phase sizes and at
most `1 + floor(log2 g)` phases. Constants in the menus are fixed before any
input is supplied; the resulting circuit is deterministic and correct for
every input.

## Why better codes improve the coefficient

High-rate lifted Reed-Solomon codes and line recovery are established coding
ingredients. The manuscript includes an elementary subcode proof: retain
reduced monomials whose exponents share an all-zero binary block of length
`h = ceil(log2 ell)`. Their rate is
`1 - (1 - 2^(-ell h))^floor(b/h)`, tending to one for fixed `ell`.
Every monomial in a line restriction has either degree zero or positive degree
not divisible by `q-1`, which proves the required line-sum identity.

Two additional accounting steps matter:

- Pack into several slightly smaller codes, so unused capacity is `o(2^p)`.
  A high-rate code alone does not remove the power-of-two rounding loss.
- Read the arbitrary systematic information set through a batched hardwired
  table lookup. Replicating a size-`K` lookup for every request would be too
  expensive. Schedule all target points together and add the code number to
  the routing key, keeping only `t(q-1)` actual incidences.

There are then `(1+o(1))2^p` Boolean resources. Leaving `d = delta n + O(1)`
suffix bits costs `(1/delta + o(1))2^n/n`. Taking the infimum over fixed
`delta < 1-gamma` proves the stated coefficient. This is not a substitution
of growing parameters into a fixed-parameter estimate.

## Implementation and validation boundaries

`scripts/linear_scheduler.py` is a deterministic record-network evaluator
given fixed menus. It implements shared occupancy broadcast, collision checks,
priority selection, halving, and output restoration. It also constructs small
systematic codes by exact finite-field Gaussian elimination. Invalid menus
raise `MenuFailure`; there is no randomized or greedy fallback hidden in the
reported scheduler.

`python3 scripts/check_improvements.py` passes nine checks covering:

- Every graph on the occupied-set vertex plus up to five request vertices:
  33,866 graphs for the forest and two-color cut witnesses.
- Exact tail and state-count inequalities.
- Record verification against an independent direct set-intersection oracle.
- All 256 ordered pairs of targets in `GF(4)^2`, including repeated targets,
  with an explicit universal menu and identical record-network counts.
- Fixed sampled menus at `q=4`, `ell=8`, `g=8`, which satisfy the theorem's
  slack condition, on repeated, collinear, and fixed-seed random batches.
- The zero-block monomial criterion, systematic rank, and every affine-line
  identity for basis monomials in `GF(4)^2` and `GF(8)^2`.
- All input pairs for three fixed-seed six-bit truth tables, packed across
  three codes, with exact bit recovery and unique resource keys.

Finite testing does not prove the asymptotic menu-existence theorem. Only the
two-request fixture is exhaustively certified universal by the implementation
checks; the larger sampled menus are not. The evaluator counts record-network
comparators, not individual Boolean gates, and does not implement an efficient
uniform constructor for the general existential menus.

The [pinned Lean companion at `8dd82c9`](https://github.com/SamuelSchlesinger/algebraic-circuits/tree/8dd82c96f44dbeeaca31f4cc96c687c6d87d1489)
now formally proves both upper-bound variants. The original explicit endpoint
is `BlockInduction.exponentialMassProduction`. The new endpoint,
`Nonuniform.realSharpMassProduction`, includes the complete circuit pipeline,
rate-one storage estimates, polynomial-overhead absorption, and the paper's
real-rate and additive-error quantifiers. The intermediate rational endpoint
is `Nonuniform.sharpExponentialMassProduction`.

The full `lake build Algebraic AlgebraicTests --wfail`, `lake test`,
`lake lint`, and whitespace checks pass at that revision. Axiom audits of
both final endpoints report only `propext`, `Classical.choice`, and
`Quot.sound`; there are no proof placeholders. The manuscript's counting
lower-bound refinement remains a written argument outside these upper-bound
formalizations. The circuit model now states explicitly that constant sources
are free, matching the formal De Morgan cost.

Section 8.1 now integrates the formalization's exact accounting into the
paper: distinct request identifiers even for repeated data, inactive zero
scalar slots, one-bit output restoration, shared prefix metadata lookup,
and a resource bank with no extra evaluations from routing padding. It also
gives the integer block/slopes construction, the finite code-rate inequality,
the degree-seven overhead envelope, and the passage from integer precision
to the paper's real-rate coefficient. The high-rate lemma now explicitly
allows every fixed block width at least `ceil(log2 ell)`, as used in Lean.

The formal endpoint uses a coarser polynomial envelope than the optimized
degree-five scheduler pass count in the written proof. Both preserve linear
incidence dependence up to polynomial bit-width factors and establish the
same sharp mass-production coefficient; the degree-five refinement is not
claimed as the exact bound emitted by Lean.

The revised 25-page PDF builds without warnings and passes
`./build.sh --check`. Every page was rendered and visually inspected, with
the new theorem statements and central proofs also checked at full page size.
Cross-reference and bibliography checks, author/page metadata checks, and
`git diff --check` pass. The local submission archive was refreshed and checked
to contain exactly the current `main.tex`. The committed packager recreates
that archive from a fresh clone and checks the abstract's ASCII format and
1,920-character limit. The extracted source was also compiled independently,
with no repository-only support files.

## Primary-source checks

- [Ishai, Kushilevitz, Ostrovsky, and Sahai (2004)](https://web.cs.ucla.edu/~sahai/work/web/2004%20Publications/STOC_Ishai2004.pdf):
  multiset batch codes, randomized geometric decoding, and the limited
  independence derandomization remark. These coding results do not themselves
  state the gate bound proved for the new menu evaluator.
- [Guo, Kopparty, and Sudan (2013)](https://arxiv.org/abs/1208.5413) and
  [Holzbaur et al. (2020)](https://arxiv.org/abs/2001.11981): high-rate lifted
  codes and their line-based recovery are prior work and are credited as such.
- [Frandsen and Miltersen (2005)](https://eccc.weizmann.ac.il/report/2005/032/download/):
  the one-copy upper coefficient `1` is valid for the paper's specified
  `{NOT, AND, OR}` basis.

This was a targeted source check, not an exhaustive priority search. The new
mathematical arguments still warrant independent research review. No claim is
made that the optimal positive-rate coefficient is known, that the
`t = 2^(n-o(n))` regime is settled, or that a practical general menu constructor
has been found.
