# Canonical source registry

This file records the primary sources selected for `nondet.tex`. The note does
not infer novelty from an unsuccessful search. Results proved directly in the
note are cited to outside work only for context or terminology.

| Key | Primary source | Used for | Boundary |
|---|---|---|---|
| `Schlesinger2026` | [Local companion manuscript](../../main.tex) | Exponential-range mass-production theorem and leading coefficient | Unpublished; imported, not reproved |
| `Lupanov1958` | [Official journal record](https://radiophysics.unn.ru/issues/1958/1/120) | Classical worst-case Boolean synthesis | Russian original; only the standard asymptotic upper bound is used |
| `FrandsenMiltersen2005` | [doi:10.1016/j.ipl.2005.03.009](https://doi.org/10.1016/j.ipl.2005.03.009) | Sharp standard-basis synthesis coefficient | Basis and cost convention matter |
| `CarterWegman1979` | [doi:10.1016/0022-0000(79)90044-8](https://doi.org/10.1016/0022-0000(79)90044-8) | Universal-hashing context for linear fingerprints | Does not supply the aggregate circuit |
| `ValiantVazirani1986` | [doi:10.1016/0304-3975(86)90135-0](https://doi.org/10.1016/0304-3975(86)90135-0) | Isolation comparison | Acts on witnesses, not characteristic-vector parities |
| `NaorNaor1993` | [doi:10.1137/0222053](https://doi.org/10.1137/0222053) | Small-bias mask selection | Short randomness does not imply cheap aggregation |
| `KannanEtAl2018` | [doi:10.4230/LIPIcs.CCC.2018.8](https://doi.org/10.4230/LIPIcs.CCC.2018.8) | Formal F_2-linear-sketch context | Full-domain sketching, unlike the realized-fiber restriction |
| `Gavinsky2025` | [doi:10.1002/rsa.70010](https://doi.org/10.1002/rsa.70010) | Parity-query OR comparison | Used only for the standard randomized/deterministic contrast |
| `ChenJinWilliams2019` | [doi:10.1109/FOCS.2019.00077](https://doi.org/10.1109/FOCS.2019.00077) | Succinct perfect linear hashing context | Stronger separation target, different cost model |
| `AlonEtAl1999` | [doi:10.1145/324133.324179](https://doi.org/10.1145/324133.324179) | Linear-hashing context | No claim that its result is the note's fingerprint lemma |
| `Lindstrom1965` | [doi:10.4153/CMB-1965-034-2](https://doi.org/10.4153/CMB-1965-034-2) | Detecting-matrix comparison | Integer sums, not parity zero tests |
| `Muller1954` | [doi:10.1109/IREPGELC.1954.6499441](https://doi.org/10.1109/IREPGELC.1954.6499441) | Reed-Muller code origin | The note reproves the weight fact it needs |
| `Reed1954` | [doi:10.1109/TIT.1954.1057465](https://doi.org/10.1109/TIT.1954.1057465) | Reed-Muller code origin | The note reproves the information-set fact it needs |
| `HausslerWelzl1987` | [doi:10.1007/BF02187876](https://doi.org/10.1007/BF02187876) | Epsilon-net refinement | Requires one common measure and a density promise |
| `PachTardos2013` | [doi:10.1090/S0894-0347-2012-00759-0](https://doi.org/10.1090/S0894-0347-2012-00759-0) | Epsilon-net lower-bound context | Not needed for the elementary union bound |
| `Darwiche1999` | [Primary IJCAI PDF](https://www.ijcai.org/Proceedings/99-1/Papers/042.pdf) | DNNF forgetting and bounded-treewidth compilation | Assumes a DNNF or a compilable structured input |
| `Darwiche2001` | [doi:10.1145/502090.502091](https://doi.org/10.1145/502090.502091) | Journal DNNF treatment | Does not imply small DNNF for every small circuit |
| `ChaviraDarwiche2008` | [doi:10.1016/j.artint.2007.11.002](https://doi.org/10.1016/j.artint.2007.11.002) | Weighted model-counting context | Counting needs stronger representation properties than existence |
| `CapelliMengel2019` | [doi:10.4230/LIPIcs.STACS.2019.18](https://doi.org/10.4230/LIPIcs.STACS.2019.18) | Width-parameterized quantifier elimination | Preserves a stronger structured deterministic representation |
| `Valiant1976` | [doi:10.1016/0020-0190(76)90097-1](https://doi.org/10.1016/0020-0190(76)90097-1) | Checking-versus-evaluating context | No theorem from it is imported into the finite bounds |
| `Valiant1979` | [doi:10.1137/0208032](https://doi.org/10.1137/0208032) | Counting-complexity context | Uniform hardness is not a Boolean circuit lower bound |
| `KarpLipton1980` | [doi:10.1145/800141.804678](https://doi.org/10.1145/800141.804678) | Consequence of a hypothetical generic determinizer | Conditional context only |
| `Morizumi2015` | [arXiv:1504.06731](https://arxiv.org/abs/1504.06731) | Nondeterministic circuit lower bounds and Tseitin parameter map | Restricted-model lower bounds, not a determinization theorem |
| `MurrayWilliams2020` | [doi:10.1137/18M1195887](https://doi.org/10.1137/18M1195887) | Easy-witness comparison | Compresses witness descriptions under assumptions, not projection circuits |
| `CascudoEtAl2012` | [doi:10.1109/TIT.2011.2180696](https://doi.org/10.1109/TIT.2011.2180696) | Multiplication-friendly-code terminology | Expands a small algebra; it does not compress the full witness algebra |

## Search conclusion

The targeted search covered universal and linear hashing, parity sketches,
isolation, detecting matrices, Reed-Muller codes, knowledge compilation,
counting complexity, and nondeterministic circuit complexity. It did not find
the exact combination of a realized-fiber zero fingerprint, common-input
mass-production specialization, and the fixed-sketch ideal-kernel barrier.
That negative search result is not a priority claim: the individual arguments
are elementary or close to established techniques, and a publication claim
would require a broader specialist literature review.
