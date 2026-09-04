#!/usr/bin/env python3
"""Fixed-menu affine-line scheduler and small exact coding experiments.

The evaluator is deterministic and uses sorting-network passes. Menus are
parameters, not fresh randomness. The paper proves that small universal menus
exist under its slack condition; it does not give an efficient uniform method
to construct them. A missing successful menu entry raises MenuFailure.

Python records simulate fixed-width circuit records. Comparator counts describe
the record networks, not a count of individual Boolean gates or Python runtime.
"""

from dataclasses import dataclass
from functools import lru_cache
from itertools import product


@dataclass(frozen=True)
class Field:
    bits: int
    modulus: int

    @property
    def q(self):
        return 1 << self.bits

    def mul(self, a, b):
        value = 0
        while b:
            if b & 1:
                value ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.modulus
        return value

    def power(self, a, exponent):
        value = 1
        while exponent:
            if exponent & 1:
                value = self.mul(value, a)
            a = self.mul(a, a)
            exponent >>= 1
        return value


def points(field, dimension):
    return tuple(product(range(field.q), repeat=dimension))


def directions(field, dimension):
    """Projective representatives with first nonzero coordinate equal to one."""
    return tuple(
        (0,) * leading + (1,) + tail
        for leading in range(dimension)
        for tail in product(range(field.q), repeat=dimension - leading - 1)
    )


def recovery(field, target, direction):
    return tuple(
        tuple(u ^ field.mul(scalar, v) for u, v in zip(target, direction))
        for scalar in range(1, field.q)
    )


@lru_cache(maxsize=None)
def bitonic_network(length):
    """Return a data-independent comparator sequence, padding to a power of two."""
    padded = 1 << max(0, (length - 1).bit_length())
    comparisons = []
    span = 2
    while span <= padded:
        stride = span // 2
        while stride:
            for left in range(padded):
                right = left ^ stride
                if right > left:
                    comparisons.append((left, right, (left & span) == 0))
            stride //= 2
        span *= 2
    return padded, tuple(comparisons)


@dataclass
class NetworkCost:
    comparisons: int = 0
    input_records: int = 0
    sorts: int = 0


def network_sort(records, key, cost):
    padded, comparisons = bitonic_network(len(records))
    decorated = [(0, key(record), index, record)
                 for index, record in enumerate(records)]
    decorated.extend((1, (), index, None)
                     for index in range(len(records), padded))
    for left, right, ascending in comparisons:
        if (decorated[left][:3] > decorated[right][:3]) == ascending:
            decorated[left], decorated[right] = decorated[right], decorated[left]
    cost.comparisons += len(comparisons)
    cost.input_records += len(records)
    cost.sorts += 1
    return [record[3] for record in decorated[:len(records)]]


class MenuFailure(ValueError):
    """The supplied menu has no entry making the required progress."""


def evaluate_menu(field, targets, occupied, menu, cost):
    """Check all candidates together, inserting the occupied list only once.

    A candidate is good for a request if its entire recovery set avoids both
    occupied points and all other recovery sets in that candidate. Return all
    per-candidate good flags; no candidate-dependent early exit is used.
    """
    width = len(targets)
    if not menu or any(len(row) != width for row in menu):
        raise ValueError("each menu row must have one direction per active request")
    records = []
    for candidate, row in enumerate(menu):
        for request, (target, direction) in enumerate(zip(targets, row)):
            for position, point in enumerate(recovery(field, target, direction)):
                # point, occupied type, candidate, request, position, bad flag
                records.append((point, 1, candidate, request, position, False))
    incidence_count = len(records)
    records.extend((point, 0, 0, 0, 0, False) for point in occupied)

    # Occupancy broadcast along each equal-point run. The occupied set need
    # not be copied once per candidate.
    records = network_sort(records, lambda r: (r[0], r[1]), cost)
    previous_point = None
    present = False
    marked = []
    for point, kind, candidate, request, position, _ in records:
        present = kind == 0 or (point == previous_point and present)
        marked.append((point, kind, candidate, request, position, present))
        previous_point = point

    # Fixed-wire compaction also sorts candidates by point for collision checks.
    records = network_sort(marked, lambda r: (-r[1], r[2], r[0]), cost)
    records = records[:incidence_count]
    marked = []
    for index, record in enumerate(records):
        point, kind, candidate, request, position, bad = record
        before = index > 0 and records[index - 1][2] == candidate \
            and records[index - 1][0] == point
        after = index + 1 < len(records) and records[index + 1][2] == candidate \
            and records[index + 1][0] == point
        marked.append((point, kind, candidate, request, position,
                       bad or before or after))
    records = network_sort(marked, lambda r: (r[2], r[3], r[4]), cost)
    good = []
    stride = field.q - 1
    for candidate in range(len(menu)):
        row = []
        for request in range(width):
            start = (candidate * width + request) * stride
            row.append(not any(r[5] for r in records[start:start + stride]))
        good.append(tuple(row))
    return tuple(good)


def schedule(field, targets, menus):
    """Schedule every target, using a fixed menu for each halving stage.

    Accept exactly ceil(k/2) good requests and retain exactly floor(k/2).
    Original request identifiers survive compaction. The return value contains
    the chosen direction for each original request and the record-network cost.
    """
    active = [(index, target) for index, target in enumerate(targets)]
    occupied = []
    accepted = []
    cost = NetworkCost()
    while active:
        width = len(active)
        menu = menus[width]
        good = evaluate_menu(field, [r[1] for r in active], occupied, menu, cost)
        required = (width + 1) // 2
        successful = [sum(row) >= required for row in good]
        if not any(successful):
            raise MenuFailure(f"no successful candidate at width {width}")
        selected = successful.index(True)  # a priority circuit in the paper
        take = []
        count = 0
        for flag in good[selected]:
            chosen = flag and count < required
            take.append(chosen)
            count += chosen
        staged = []
        for slot, ((identifier, target), chosen) in enumerate(zip(active, take)):
            staged.append((not chosen, identifier, target, menu[selected][slot]))
        staged = network_sort(staged, lambda r: (r[0], r[1]), cost)
        for _, identifier, target, direction in staged[:required]:
            accepted.append((identifier, direction))
            occupied.extend(recovery(field, target, direction))
        active = [(identifier, target) for _, identifier, target, _
                  in staged[required:]]
    accepted = network_sort(accepted, lambda r: r[0], cost)
    return tuple(direction for _, direction in accepted), cost


def two_request_menus(field, dimension):
    """Explicit universal test fixture for two requests, q >= 4, dimension >= 2.

    For distinct targets a parallel direction other than their difference
    works. For equal targets the last candidate uses two distinct directions.
    The final one-request menu enumerates all directions; its occupied set has
    q-1 points, fewer than the number of directions.
    """
    reps = directions(field, dimension)
    return {2: tuple((v, v) for v in reps) + ((reps[0], reps[-1]),),
            1: tuple((v,) for v in reps)}


def zero_block_exponents(bits, dimension):
    """Independent monomials in the paper's elementary high-rate subcode."""
    block = (dimension - 1).bit_length()  # ceil(log2(dimension))
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    masks = [((1 << block) - 1) << start
             for start in range(0, bits - block + 1, block)]
    return tuple(exponent for exponent in product(range(1 << bits), repeat=dimension)
                 if any(all((entry & mask) == 0 for entry in exponent)
                        for mask in masks))


def monomial(field, exponent, point):
    value = 1
    for degree, coordinate in zip(exponent, point):
        value = field.mul(value, field.power(coordinate, degree))
    return value


def rref(field, matrix):
    matrix = [list(row) for row in matrix]
    pivots = []
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(len(pivots), len(matrix))
                      if matrix[row][column]), None)
        if pivot is None:
            continue
        row = len(pivots)
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inverse = field.power(matrix[row][column], field.q - 2)
        matrix[row] = [field.mul(value, inverse) for value in matrix[row]]
        for other in range(len(matrix)):
            if other != row:
                factor = matrix[other][column]
                matrix[other] = [value ^ field.mul(factor, basis)
                                 for value, basis in zip(matrix[other], matrix[row])]
        pivots.append(column)
        if len(pivots) == len(matrix):
            break
    return tuple(pivots), tuple(tuple(row) for row in matrix)


class SystematicCode:
    """Small exact implementation; Gaussian elimination is offline preprocessing."""

    def __init__(self, field, dimension):
        self.field = field
        self.points = points(field, dimension)
        exponents = zero_block_exponents(field.bits, dimension)
        if not exponents:
            raise ValueError("field too small for the zero-block subcode")
        matrix = [[monomial(field, exponent, point) for point in self.points]
                  for exponent in exponents]
        self.pivots, self.generator = rref(field, matrix)
        if len(self.pivots) != len(exponents):
            raise AssertionError("evaluation monomials must be independent")
        self.information = tuple(self.points[index] for index in self.pivots)

    def encode(self, symbols):
        if len(symbols) != len(self.generator):
            raise ValueError("incorrect information length")
        result = []
        for column in range(len(self.points)):
            value = 0
            for symbol, row in zip(symbols, self.generator):
                value ^= self.field.mul(symbol, row[column])
            result.append(value)
        return dict(zip(self.points, result))


def menu_size_bound(batch_size, active_size, field, dimension):
    """Ceiling of (g * (1 + 3 log2 N) + 1) / k, with exact arithmetic."""
    numerator = batch_size * (1 + 3 * field.bits * dimension) + 1
    return (numerator + active_size - 1) // active_size
