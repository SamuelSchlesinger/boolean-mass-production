# Review and substantial improvements

The existing order-of-growth theorem has a coherent proof under its stated
nonuniform, bounded-fan-in, free-fan-out circuit model. The review did not find
a counterexample to its packing, greedy scheduling, routing, or equal-block
induction. Its largest avoidable costs were the quadratic greedy scheduler,
the product code's low rate, and rounding a single code's field size upward.

The Boolean construction establishes two refinements in `main.tex`:

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
formally proves both Boolean upper-bound variants. The original explicit endpoint
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

Appendix C integrates the formalization's exact accounting into the
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

The revised PDF builds without warnings and passes
`./build.sh --check`. Every page was rendered and visually inspected, with
the new theorem statements and central proofs also checked at full page size.
Cross-reference and bibliography checks, author/page metadata checks, and
`git diff --check` pass. The local submission archive was refreshed and checked
to contain exactly the current `main.tex`. The committed packager recreates
that archive from a fresh clone and checks the abstract's ASCII format and
1,920-character limit. The extracted source was also compiled independently,
with no repository-only support files.

## Exposition revision

The introduction now develops the sharing obstacle before introducing the
code: two requests can select the same restriction at different suffixes,
so one copy of each restriction circuit does not suffice. It then explains
alternative recovery sets and derives the leading coefficient from the
resource-count times synthesis-cost product. A concrete half-rate example
and a reading route connect the overview to the formal statements.

The two-copy section includes an explicit four-restriction, five-resource
example with unrelated suffixes. A parameter table distinguishes field symbols
from Boolean resources, and a second table explains the codeword and resource
views of the same encoded array. The scheduler section separates the random
partial schedule, universal-menu existence, and gate-counted menu evaluation.
The composition bound labels each cost, and the high-rate proof explains why
avoiding positive multiples of `q-1` is enough for line parity.

The full literature comparison is Section 2, immediately after the introduction,
and includes recent quantum mass-production and state-synthesis work. The paper
also distinguishes choices made when the circuit is built from operations on
live inputs, and states explicitly that replication may be better for a
particular easy function. The Boolean theorem statements and pinned Lean revision
are preserved. The abstract and arXiv metadata describe the revised exposition.

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

## Quantum application and exposition integration (September 5, 2026)

The abstract now states the worst-case cost of one Boolean evaluation before
comparing copy ranges. It gives explicit gate bounds instead of undefined
phrases such as "sharp one-copy asymptotic". The complete prior-work section
follows the introduction. The acknowledgement thanks Shreyas Srinivas for
exposition and literature feedback and, specifically, his suggestion to attack
the quantum variant.

The new quantum theorem determines the worst-case total elementary gate count
`M(n,t) = Theta_gamma((2^n/n) log2(t+1))` for every fixed `0 <= gamma < 1`
and `1 <= t <= 2^(gamma n)`. It uses `{H,T,T-dagger,CNOT}`, arbitrary
connectivity, no measurements or postselection, and scratch qubits initialized
and returned exactly to zero. The trace-distance error is at most `1/10`
for the entire `nt`-qubit output, not separately for each copy.

The proof accounts for:

- Exact coherent simulation of Boolean circuits, including output copying,
  constant sources, repeated controls, and uncomputation.
- Conditional rotation synthesis that preserves its control exactly even
  when the implemented rotation is approximate. Pairing a word with its
  exact inverse also cancels its global phase.
- Padding all short address tables to `ceil(alpha*n)` for fixed
  `gamma < alpha < 1`, so a single fixed Boolean copy-rate theorem applies
  at every stage.
- Geometrically allocated errors `delta_k = 2^(k-n)/(40t)` and precision
  `O(n-k+log(t+1))`, which give the logarithmic overhead without an extra
  `log n` factor. Finite-gate synthesis costs only `t poly(n)` extra gates.
- A packing of at least `(4t)^(2^n-1)` single-copy states whose tensor powers
  have constant pairwise trace distance. Gate counting includes all active
  ancillary wires by canonical relabeling, so unrestricted scratch space
  does not invalidate the lower bound.

The lower bound also includes `Omega(nt)` from touching all output wires
for the all-ones target. The proof settles the fixed-rate range; it leaves
`t = 2^(n-o(n))`, optimal constants, other resource tradeoffs, and arbitrary
unitary mass production open. It provides existence of worst-case hard states,
not an explicit hard family.

The quantum proof is outside the pinned Lean companion. The five tests in
`scripts/check_quantum.py` pass: they check controlled rotations, phase
cancellation, cleanup on entangled data with shared intermediate values,
recursive preparation including zero amplitudes, exact finite error/cost
inequalities, and tensor-power separation. Numerical identities use double
precision, while the arithmetic inequalities use exact rational arithmetic.
These finite checks are neither an asymptotic proof nor a quantum compiler.
The nine existing Boolean checks also pass.

Primary sources checked for the quantum revision:

- [Kretschmer (2023)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2023.10):
  exact state and unitary mass production, conditional-rotation decomposition,
  and the different continuous-gate model.
- [Huggins, Khattar, and Wiebe (2025)](https://arxiv.org/html/2506.00132v1):
  QROM mass production, larger-copy cost analysis, and the QROM-to-state
  preparation connection in Appendix B.5.
- [Gosset, Kothari, and Wu (2026)](https://arxiv.org/html/2411.04790v3):
  optimal T-count, the known single-copy total-gate endpoint, and geometric
  allocation of precision in Appendix B.
- [Shende, Bullock, and Markov (2006)](https://arxiv.org/abs/quant-ph/0406176):
  quantum logic synthesis and conditional rotations.
- [Dawson and Nielsen (2006)](https://arxiv.org/abs/quant-ph/0505030):
  polynomial-logarithmic finite-gate approximation.

These sources do not state the matching exponential-range total-gate curve
proved here. This targeted comparison does not establish priority; the new
written theorem and its proof still warrant independent mathematical review.

Validation of this revision: the 33-page PDF builds without warnings and
passes the reproducible freshness check. All pages were rendered and visually
inspected, with the abstract, theorem statement, and quantum proofs also
inspected at higher resolution. All 57 labels are unique and all 21 cited
bibliography entries resolve. The 1,451-character ASCII submission abstract
exactly matches the manuscript abstract. The regenerated source-only archive
compiles independently without warnings and reproduces the reviewed PDF text.
`git diff --check` passes.


## Simultaneous size and depth (September 10, 2026)

Theorem 1.3 and Section 10 add a written proof that, for every fixed
`0 <= gamma < 1`, every n-bit Boolean function admits simultaneous evaluation
on `1 <= t <= 2^(gamma*n)` inputs with `O_gamma(2^n/n)` gates and
`O_gamma(n)` depth in the same circuit. NOT gates count toward both resources.
The sharp leading coefficient is not claimed for these circuits, and this
refinement is outside the pinned Lean companion. No priority claim is made.

The proof strengthens the existing forest-conditioning collision estimate.
If a phase may leave v requests unfinished, a bad outcome yields a set of
`h = ceil((v+1)/2)` requests with collision witnesses outside that set.
Conditioning on outside directions gives failure probability at most
`binom(k,h)*(2*g*q/D_q)^h`. Under `4*e*g*q/D_q <= alpha^2`, this supports
menus leaving exactly `floor(alpha*k)` requests, with at most
`g + 2*(E_g+1)/(alpha*log2(1/alpha))` candidate directions per phase.
The exponential geometric slack permits `alpha = 2^(-floor(rho*n))`:
there are only constantly many phases, and the larger menus still have
negligible total gate count.

The proof also accounts for parallel occupancy propagation, fixed-wire
selection and compaction, a power-of-two information packing that removes
live division from the prefix map, and resource circuits with simultaneous
`O(2^d/d)` size and `d+O(log(d+2))` depth. The local proof audit checked the
collision conditioning, rounding and final phase, state-count union bound,
record widths, and the strict exponential margins. These are written
arguments, not claims of new Lean verification or finite computational proof.

The depth implementation uses Justin Holmgren and Ron Rothblum,
[Linear-Size Boolean Circuits for Multiselection, CCC 2024](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2024.11),
Lemma 6 and its Section 4 proof. Their sorting construction credits Ajtai,
Komlos, and Szemeredi. Lemma 26's related prefix propagation credits Ladner
and Fischer. The main theorem and these selected sections were read; the
entire multiselection proof was not audited. Batcher's original sorting
network construction was also consulted during the initial depth estimate;
the sharper Holmgren-Rothblum bound is the one used here. Sources and reading
scope are also recorded in the depth workspace's SOURCES.md.

Validation: the 37-page manuscript builds without warnings. All pages were
rendered for layout review, and the theorem and new proof were inspected at
higher resolution. The README and local submission metadata identify the
new result and its formalization boundary; the 1,561-character ASCII abstract
matches the manuscript. These changes are local and have not been submitted.

## Additional corollaries and lower bounds (September 10, 2026)

Corollary 10.4 gives a randomized construction from the full truth table,
polynomial in its length, with size `O_gamma(2^n/n)` and depth `O_gamma(n)`.
Enlarged menus fail on any state in any phase with probability at most
`2^(-n-2)`. Capped rejection sampling adds at most the same failure probability,
so the stated correctness probability is at least `1 - 2^(-n)`. Success means
one deterministic circuit is correct on every input batch. The proof chooses
rational fixed parameters above the requested rate and uses the log-space
uniform sorting circuits of Holmgren and Rothblum, Lemmas 8-9. Efficient
deterministic menu construction and certification remain open. This is a
written algorithmic result; no general circuit generator was implemented.

Lemma 11.1 now accounts for quantum depth and scratch space: separate control
qubits for all wire uses, supplied by balanced CNOT trees, preserve linear
gate overhead and give depth `O((D+1) log(s+t+2))`. Reversing both the gate
computations and fan-out trees restores all scratch qubits. Corollary 11.2
therefore gives exact coherent Boolean batch evaluation at quadratic depth.
No depth bound for the full state-preparation construction is inferred.

Proposition 12.1 states the quantitative nonuniform inversion assumption
explicitly and proves `C(h_m^t) >= H(m)/ceil(m/t)` by recovering all inverse
bits with repeated images and hardwired indices. Its growth stops at `t=m`;
it neither proves a general direct-sum theorem nor closes the leading-constant
gap. The secure-computation discussion distinguishes gate hardness from
communication hardness, with references to Couteau and Damgaard-Schwartzbach.

Appendix D promotes the existing restricted module-counting argument into
the manuscript. Theorem D.1 allows function-dependent modules and wiring,
at most `2^(mu*n)` modules for fixed `mu<1`, and polynomial input/output
interfaces. It cuts the largest modules, applies a VC-dimension bound with
a self-contained proof of Sauer's inequality, and counts the remaining
modules and the entire exterior, including free interconnections. The result
matches the coefficient `1/(1-gamma)` only when the exterior is negligible
under these architecture restrictions. None of these additions is covered
by the pinned Lean companion.

Validation: the final 42-page PDF builds without warnings and passes
`./build.sh --check`. All pages were inspected in rendered overview sheets;
the added statements and proofs were inspected at full-page resolution, and
the final changed pages were re-rendered after pagination adjustments.
All 71 labels are unique, all references resolve, and all 27 bibliography
entries resolve. The existing cut-family audit passes 45,404 exact finite
cases; this checks the finite combinatorial implication, not the asymptotic
theorem. The abstract, construction discussion, and README now distinguish
randomized construction from deterministic construction and certification.

## Expositional coherence pass (September 10, 2026)

Reviewed the complete manuscript, including the appendices, after the new
corollaries and lower bounds. The introduction and reading guide now separate
the Boolean size and depth results, the quantum application, and the later
implications. The circuit conventions distinguish construction time from
evaluation size and depth. The scheduler discussion explains which version
feeds the main proof and which feeds the recursive appendix.

Section 10 now previews the packing and scheduling changes needed for linear
depth. Section 11 gives a proof roadmap, distinguishes state preparation from
coherent subroutines, and places the precision-allocation intuition before its
proof. The repeated formalization qualifications are consolidated while
retaining the distinction between Lean-checked size bounds and written proofs.

Section 12 is organized into secure evaluation, lower bounds and the leading
coefficient, and open problems. The restricted lower-bound summary now states
its fixed exponential batch size explicitly. The inverse-bit result follows
that discussion with its reduction mechanism and limitations together. The
menu question now asks for deterministic construction, reflecting the new
randomized construction. Appendix D explains the cutting strategy before the
counting lemmas, defines shattering and VC dimension, and clarifies that the
description bound is a logarithm of a count. The README follows this structure.

Validation: comparison with the manuscript at the start of this pass preserves
the formulas in all 33 formal statements and all 141 displayed calculations.
All 74 labels are unique, all cross-references resolve, and all 27 bibliography
entries remain cited and resolve. The 42-page PDF builds without warnings and
passes `./build.sh --check`. All pages were inspected in rendered overviews,
and the revised passages were inspected at reading size. `git diff --check`
passes. This was an editorial and consistency review, not a new independent
proof audit or an extension of the Lean companion.
