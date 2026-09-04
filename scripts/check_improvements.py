#!/usr/bin/env python3
"""Exact finite checks for the new scheduler, forest witness, and lifted code.

These checks support the written proofs; they do not establish the asymptotic
menu-existence theorem or replace a Lean formalization.
"""

from fractions import Fraction
from itertools import combinations, product
from math import comb
import random
import unittest

from linear_scheduler import (
    Field, MenuFailure, NetworkCost, SystematicCode, directions, evaluate_menu,
    menu_size_bound, monomial, network_sort, points, recovery, schedule,
    two_request_menus, zero_block_exponents,
)


class ImprovementChecks(unittest.TestCase):
    def test_field_and_sorting_primitives(self):
        for field in (Field(2, 0b111), Field(3, 0b1011)):
            for value in range(1, field.q):
                self.assertEqual(field.mul(value, field.power(value, field.q - 2)), 1)
        for length in range(1, 9):
            for data in product((0, 1), repeat=length):
                self.assertEqual(network_sort(list(data), lambda r: r, NetworkCost()),
                                 sorted(data))

    def test_forest_witness_exhaustively(self):
        # Vertex 0 represents the fixed occupied set. Every non-isolated
        # request is bad. In a component without 0, choose one root; orient
        # all spanning-tree edges toward the root (toward 0 when present).
        graphs = 0
        for width in range(1, 6):
            edges = list(combinations(range(width + 1), 2))
            for mask in range(1 << len(edges)):
                parent = list(range(width + 1))
                bad = set()

                def root(vertex):
                    while parent[vertex] != vertex:
                        vertex = parent[vertex]
                    return vertex

                forest_edges = 0
                for index, (left, right) in enumerate(edges):
                    if mask & (1 << index):
                        bad.update(v for v in (left, right) if v != 0)
                        first, second = root(left), root(right)
                        if first != second:
                            parent[first] = second
                            forest_edges += 1
                if len(bad) >= (width + 1) // 2:
                    self.assertGreaterEqual(forest_edges, (width + 3) // 4)
                graphs += 1
        self.assertEqual(graphs, 33866)

    def test_menu_tail_and_union_bound_arithmetic(self):
        # The forest count is binom(k,h) * rho^h. At rho <= 1/256 it
        # is at most 2^-k; r independent candidates defeat the state count.
        field = Field(2, 0b111)
        for width in range(1, 65):
            witness_size = (width + 3) // 4
            bound = Fraction(comb(width, witness_size), 256 ** witness_size)
            self.assertLessEqual(bound, Fraction(1, 2 ** width))
            batch_size = 80
            dimension = 8
            rows = menu_size_bound(batch_size, width, field, dimension)
            description_bits = batch_size * (1 + 3 * field.bits * dimension)
            self.assertGreater(width * rows, description_bits)

    def test_record_verifier_against_set_oracle(self):
        field = Field(2, 0b111)
        space = points(field, 2)
        reps = directions(field, 2)
        rng = random.Random(20260904)
        for width in (1, 2, 3, 5):
            for _ in range(30):
                targets = [rng.choice(space) for _ in range(width)]
                occupied = rng.sample(space, rng.randrange(0, 8))
                menu = [tuple(rng.choice(reps) for _ in range(width))
                        for _ in range(7)]
                expected = []
                for row in menu:
                    sets = [set(recovery(field, u, v)) for u, v in zip(targets, row)]
                    expected.append(tuple(
                        not (current & set(occupied)) and all(
                            not (current & other) for j, other in enumerate(sets) if i != j
                        ) for i, current in enumerate(sets)))
                self.assertEqual(evaluate_menu(field, targets, occupied, menu, NetworkCost()),
                                 tuple(expected))

    def test_universal_two_request_menu_and_fixed_network_shape(self):
        field = Field(2, 0b111)
        space = points(field, 2)
        menus = two_request_menus(field, 2)
        counts = set()
        for targets in product(space, repeat=2):
            chosen, cost = schedule(field, targets, menus)
            first, second = [set(recovery(field, u, v)) for u, v in zip(targets, chosen)]
            self.assertFalse(first & second)
            for target, used in zip(targets, (first, second)):
                self.assertNotIn(target, used)
                self.assertEqual(len(used), field.q - 1)
            counts.add((cost.comparisons, cost.input_records, cost.sorts))
        self.assertEqual(len(counts), 1)
        # An invalid menu must fail visibly, including for repeated targets.
        direction = directions(field, 2)[0]
        with self.assertRaises(MenuFailure):
            schedule(field, (space[0], space[0]), {2: ((direction, direction),)})

    def test_fixed_sampled_menus_inside_the_slack_regime(self):
        # This checks evaluation at parameters covered by the theorem. These
        # particular sampled menus are NOT certified universal by this test.
        field = Field(2, 0b111)
        dimension, batch_size = 8, 8
        reps = directions(field, dimension)
        self.assertLessEqual(512 * batch_size * field.q, len(reps))
        rng = random.Random(20260904)
        menus = {}
        width = batch_size
        while width:
            menus[width] = tuple(
                tuple(rng.choice(reps) for _ in range(width))
                for _ in range(menu_size_bound(batch_size, width, field, dimension)))
            width //= 2
        batches = [
            ((0,) * dimension,) * batch_size,
            tuple((index % field.q,) + (0,) * (dimension - 1)
                  for index in range(batch_size)),
            tuple(tuple(rng.randrange(field.q) for _ in range(dimension))
                  for _ in range(batch_size)),
        ]
        counts = set()
        for targets in batches:
            chosen, cost = schedule(field, targets, menus)
            occupied = set()
            for target, direction in zip(targets, chosen):
                current = set(recovery(field, target, direction))
                self.assertFalse(occupied & current)
                occupied.update(current)
            counts.add((cost.comparisons, cost.input_records, cost.sorts))
        self.assertEqual(len(counts), 1)

    def test_zero_block_count_and_forbidden_line_degrees(self):
        for bits, dimension in ((2, 2), (3, 2), (3, 3), (3, 4)):
            exponents = zero_block_exponents(bits, dimension)
            block = (dimension - 1).bit_length()
            blocks = bits // block
            expected = (1 << (bits * dimension)) - \
                ((1 << (block * dimension)) - 1) ** blocks * \
                (1 << ((bits % block) * dimension))
            self.assertEqual(len(exponents), expected)
            for exponent in exponents:
                # Nonzero binomial coefficients in characteristic two have
                # precisely these bitwise sub-exponents.
                choices = [tuple(value for value in range(1 << bits)
                                 if value & entry == value) for entry in exponent]
                for subexponent in product(*choices):
                    degree = sum(subexponent)
                    self.assertFalse(degree > 0 and degree % ((1 << bits) - 1) == 0)

    def test_code_rank_systematic_encoding_and_all_line_identities(self):
        for field in (Field(2, 0b111), Field(3, 0b1011)):
            code = SystematicCode(field, 2)
            self.assertEqual(len(code.generator), field.q ** 2 - 3 ** field.bits)
            for row, pivot in enumerate(code.pivots):
                self.assertEqual(tuple(generator[pivot] for generator in code.generator),
                                 tuple(int(index == row) for index in range(len(code.generator))))
            # Check every basis monomial on every affine line, including all
            # target points. Linearity then covers every word of the code.
            for exponent in zero_block_exponents(field.bits, 2):
                values = {point: monomial(field, exponent, point) for point in code.points}
                for target in code.points:
                    for direction in directions(field, 2):
                        decoded = 0
                        for point in recovery(field, target, direction):
                            decoded ^= values[point]
                        self.assertEqual(decoded, values[target])

    def test_multiple_code_packing_end_to_end(self):
        field = Field(2, 0b111)
        code = SystematicCode(field, 2)
        menus = two_request_menus(field, 2)
        prefix_bits, suffix_bits = 5, 1
        capacity = len(code.generator) * field.bits
        blocks = ((1 << prefix_bits) + capacity - 1) // capacity
        self.assertEqual(blocks, 3)  # exercises block selection and zero padding
        target_map = []
        for prefix in range(1 << prefix_bits):
            block, position = divmod(prefix, capacity)
            symbol, bit = divmod(position, field.bits)
            target_map.append((block, code.information[symbol], bit))
        # Precompute deterministic schedules for all target pairs used below.
        schedules = {targets: schedule(field, targets, menus)[0]
                     for targets in product(code.information, repeat=2)}
        rng = random.Random(20260904)
        for _ in range(3):
            truth = [rng.randrange(2) for _ in range(1 << (prefix_bits + suffix_bits))]
            resources = {}
            for suffix in range(1 << suffix_bits):
                for block in range(blocks):
                    symbols = [0] * len(code.generator)
                    for position in range(capacity):
                        prefix = block * capacity + position
                        if prefix < 1 << prefix_bits:
                            symbol, bit = divmod(position, field.bits)
                            symbols[symbol] |= truth[(prefix << suffix_bits) | suffix] << bit
                    resources[block, suffix] = code.encode(symbols)
            for inputs in product(range(len(truth)), repeat=2):
                requests = [target_map[value >> suffix_bits] for value in inputs]
                targets = tuple(request[1] for request in requests)
                chosen = schedules[targets]
                result = []
                incidence_keys = set()
                for value, (block, target, bit), direction in zip(inputs, requests, chosen):
                    decoded = 0
                    for point in recovery(field, target, direction):
                        self.assertNotIn((block, point), incidence_keys)
                        incidence_keys.add((block, point))
                        decoded ^= resources[block, value & ((1 << suffix_bits) - 1)][point]
                    result.append((decoded >> bit) & 1)
                self.assertEqual(result, [truth[value] for value in inputs])


if __name__ == "__main__":
    unittest.main(verbosity=2)
