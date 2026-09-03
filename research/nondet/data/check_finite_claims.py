#!/usr/bin/env python3
"""Finite checks for claims used in nondet.tex.

Validates:
  1. Every family of K nonzero D-bit vectors in the tested range has a
     zero-avoiding binary linear sketch with max(1, ceil(log2 K)) rows.
  2. The minimum nonzero weight of RM(d, M) is 2^(M-d), in the tested range.
  3. Points of Hamming weight at most d form an information set for RM(d, M).
  4. Every tested binary linear subspace has a coordinate information set.
  5. A fixed linear sketch supports coordinatewise-AND updates exactly when
     its kernel is a coordinate ideal, in the tested range.
  6. A one-row dense parity sketch need not commute with coordinatewise AND.
  7. Same-line local recoveries cancel by symmetric difference.

Expected output: seven PASS lines followed by "all finite checks passed".
"""

from __future__ import annotations

from itertools import combinations, product
from math import ceil, comb, log2


def parity(value: int) -> int:
    return value.bit_count() & 1


def sketch(rows: tuple[int, ...], vector: int) -> tuple[int, ...]:
    return tuple(parity(row & vector) for row in rows)


def has_zero_avoiding_sketch(dimension: int, vectors: tuple[int, ...]) -> bool:
    row_count = max(1, ceil(log2(len(vectors))))
    rows = range(1 << dimension)
    return any(
        all(any(sketch(matrix, vector)) for vector in vectors)
        for matrix in product(rows, repeat=row_count)
    )


def check_zero_avoiding_sketches() -> None:
    # Exhaust all families through D=4 and K=4.  This includes the extremal
    # K=2^N case for N=1,2 and is deliberately independent of the proof.
    for dimension in range(1, 5):
        nonzero = range(1, 1 << dimension)
        for count in range(1, min(4, (1 << dimension) - 1) + 1):
            for vectors in combinations(nonzero, count):
                assert has_zero_avoiding_sketch(dimension, vectors), (
                    dimension,
                    vectors,
                )
    print("PASS zero-avoiding sketches")


def monomials(variable_count: int, degree: int) -> tuple[int, ...]:
    return tuple(
        mask
        for mask in range(1 << variable_count)
        if mask.bit_count() <= degree
    )


def evaluate_polynomial(coefficient_mask: int, mons: tuple[int, ...], point: int) -> int:
    value = 0
    for index, monomial in enumerate(mons):
        if (coefficient_mask >> index) & 1 and (point & monomial) == monomial:
            value ^= 1
    return value


def check_reed_muller() -> None:
    for variable_count in range(1, 6):
        # Keep exhaustive enumeration small while covering nontrivial degrees.
        for degree in range(min(2, variable_count) + 1):
            mons = monomials(variable_count, degree)
            minimum_weight = 1 << variable_count
            low_weight_points = tuple(
                point
                for point in range(1 << variable_count)
                if point.bit_count() <= degree
            )
            assert len(low_weight_points) == sum(
                comb(variable_count, index) for index in range(degree + 1)
            )
            for coefficients in range(1, 1 << len(mons)):
                values = tuple(
                    evaluate_polynomial(coefficients, mons, point)
                    for point in range(1 << variable_count)
                )
                minimum_weight = min(minimum_weight, sum(values))
                assert any(values[point] for point in low_weight_points), (
                    variable_count,
                    degree,
                    coefficients,
                )
            assert minimum_weight == 1 << (variable_count - degree), (
                variable_count,
                degree,
                minimum_weight,
            )
    print("PASS Reed-Muller minimum weight")
    print("PASS low-weight information sets")


def span(generators: tuple[int, ...]) -> frozenset[int]:
    values = {0}
    for generator in generators:
        values |= {value ^ generator for value in tuple(values)}
    return frozenset(values)


def check_subspace_information_sets() -> None:
    for dimension in range(1, 5):
        subspaces = {
            span(generators)
            for count in range(dimension + 1)
            for generators in combinations(range(1, 1 << dimension), count)
        }
        for subspace in subspaces:
            rank = (len(subspace)).bit_length() - 1
            assert 1 << rank == len(subspace)
            assert any(
                all(
                    vector == 0
                    or any((vector >> coordinate) & 1 for coordinate in chosen)
                    for vector in subspace
                )
                for chosen in combinations(range(dimension), rank)
            ), (dimension, subspace)
    print("PASS subspace information sets")


def multiplication_descends(dimension: int, rows: tuple[int, ...]) -> bool:
    outputs: dict[tuple[tuple[int, ...], tuple[int, ...]], tuple[int, ...]] = {}
    for left in range(1 << dimension):
        for right in range(1 << dimension):
            key = (sketch(rows, left), sketch(rows, right))
            value = sketch(rows, left & right)
            if key in outputs and outputs[key] != value:
                return False
            outputs[key] = value
    return True


def kernel_is_ideal(dimension: int, rows: tuple[int, ...]) -> bool:
    kernel = tuple(
        vector
        for vector in range(1 << dimension)
        if not any(sketch(rows, vector))
    )
    return all(
        not any(sketch(rows, element & multiplier))
        for element in kernel
        for multiplier in range(1 << dimension)
    )


def kernel_is_coordinate_subspace(dimension: int, rows: tuple[int, ...]) -> bool:
    kernel = {
        vector
        for vector in range(1 << dimension)
        if not any(sketch(rows, vector))
    }
    support = 0
    for vector in kernel:
        support |= vector
    coordinate_subspace = {
        vector
        for vector in range(1 << dimension)
        if vector & ~support == 0
    }
    return kernel == coordinate_subspace


def check_ideal_kernel_characterization() -> None:
    for dimension in range(1, 4):
        possible_rows = range(1 << dimension)
        for row_count in range(dimension + 1):
            for rows in product(possible_rows, repeat=row_count):
                descends = multiplication_descends(dimension, rows)
                is_ideal = kernel_is_ideal(dimension, rows)
                is_coordinate = kernel_is_coordinate_subspace(dimension, rows)
                assert descends == is_ideal == is_coordinate, (dimension, rows)
    print("PASS ideal-kernel characterization")


def check_and_obstruction() -> None:
    # A(u) = u_0 XOR u_1.  The two input pairs have identical sketches but
    # their coordinatewise products have different sketches.
    row = (0b11,)
    first = (0b01, 0b01)
    second = (0b01, 0b10)
    assert sketch(row, first[0]) == sketch(row, second[0]) == (1,)
    assert sketch(row, first[1]) == sketch(row, second[1]) == (1,)
    first_product = first[0] & first[1]
    second_product = second[0] & second[1]
    assert sketch(row, first_product) == (1,)
    assert sketch(row, second_product) == (0,)
    print("PASS parity-sketch AND obstruction")


def check_recovery_boundary() -> None:
    # A characteristic-two affine line has even size q.  The recovery set for
    # position u is every other position on the line.  XORing the recovery
    # vectors leaves T when |T| is even and its complement when |T| is odd.
    for line_size in (2, 4, 8):
        full_line = (1 << line_size) - 1
        recoveries = tuple(full_line ^ (1 << point) for point in range(line_size))
        for target_set in range(1 << line_size):
            boundary = 0
            for point, recovery in enumerate(recoveries):
                if (target_set >> point) & 1:
                    boundary ^= recovery
            expected = (
                full_line ^ target_set
                if target_set.bit_count() & 1
                else target_set
            )
            assert boundary == expected, (line_size, target_set, boundary)

            # Verify the corresponding parity identity on every even-parity
            # line word, the binary form of sum_{z in L} P(z) = 0.
            for codeword in range(1 << line_size):
                if parity(codeword) == 0:
                    assert parity(target_set & codeword) == parity(
                        boundary & codeword
                    )
    print("PASS same-line recovery cancellation")


def main() -> None:
    check_zero_avoiding_sketches()
    check_reed_muller()
    check_subspace_information_sets()
    check_ideal_kernel_characterization()
    check_and_obstruction()
    check_recovery_boundary()
    print("all finite checks passed")


if __name__ == "__main__":
    main()
