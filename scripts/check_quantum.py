#!/usr/bin/env python3
"""Finite checks of quantum proof identities, not an asymptotic proof or compiler."""

import cmath
from fractions import Fraction
import math
import random
import unittest


IDENTITY = ((1, 0), (0, 1))
X = ((0, 1), (1, 0))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def adjoint(a):
    return tuple(tuple(complex(a[j][i]).conjugate() for j in range(2))
                 for i in range(2))


def ry(theta):
    c, s = math.cos(theta / 2), math.sin(theta / 2)
    return ((c, -s), (s, c))


def rz(theta):
    return ((cmath.exp(-0.5j * theta), 0), (0, cmath.exp(0.5j * theta)))


def distance(a, b):
    return math.sqrt(sum(abs(x - y) ** 2 for x, y in zip(a, b)))


def matrix_distance(a, b):
    return distance(sum(a, ()), sum(b, ()))


def random_state(qubits, rng):
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2**qubits)]
    norm = math.sqrt(sum(abs(z)**2 for z in v))
    return [z / norm for z in v]


def controlled(v, target, predicate, gate):
    """Apply a gate to an LSB-indexed target if a target-independent predicate holds."""
    out = v.copy()
    for i in range(len(v)):
        if i & (1 << target) or not predicate(i):
            continue
        j = i | (1 << target)
        out[i] = gate[0][0] * v[i] + gate[0][1] * v[j]
        out[j] = gate[1][0] * v[i] + gate[1][1] * v[j]
    return out


class QuantumIdentities(unittest.TestCase):
    def test_controlled_rotation_and_phase_cancellation(self):
        for rotation in (ry, rz):
            for theta in (-7.1, -math.pi, 0, 0.3, 2 * math.pi, 10.9):
                a = rotation(theta / 2)
                self.assertLess(matrix_distance(mul(mul(mul(a, X), adjoint(a)), X),
                                                rotation(theta)), 1e-12)
                # A deliberately perturbed unitary need not be an exact axial rotation.
                a = mul(rz(0.017), mul(a, ry(-0.013)))
                phase = cmath.exp(0.731j)
                phased = tuple(tuple(phase * z for z in row) for row in a)
                self.assertLess(matrix_distance(mul(a, adjoint(a)), IDENTITY), 1e-12)
                self.assertLess(matrix_distance(
                    mul(mul(mul(a, X), adjoint(a)), X),
                    mul(mul(mul(phased, X), adjoint(phased)), X)), 1e-12)

    def test_coherent_uncompute_on_entangled_inputs(self):
        rng = random.Random(20260905)
        # Six data qubits: two two-bit addresses and two targets.  Three
        # scratch qubits hold the answers and a value shared across addresses.
        initial = random_state(6, rng)

        def answers(data):
            first, second = (data >> 2) & 3, (data >> 4) & 3
            f1 = ((first >> 1) ^ first) & 1
            f2 = ((second >> 1) ^ second) & 1
            shared = (first ^ second) & 1
            return f1 | (f2 << 1) | (shared << 2)

        def lookup(v):
            out = [0j] * len(v)
            for i, amplitude in enumerate(v):
                data, scratch = i & 63, i >> 6
                out[data | ((scratch ^ answers(data)) << 6)] = amplitude
            return out

        for rotation in (ry, rz):
            a = mul(rz(0.019), rotation(0.39))
            gate = mul(mul(mul(a, X), adjoint(a)), X)
            actual = lookup(initial + [0j] * (512 - 64))
            expected = initial.copy()
            for target in range(2):
                actual = controlled(actual, target,
                                    lambda i, j=target: (i >> (6 + j)) & 1, gate)
                expected = controlled(expected, target,
                                      lambda i, j=target: (answers(i) >> j) & 1, gate)
            actual = lookup(actual)
            self.assertLess(distance(actual[:64], expected), 1e-12)
            self.assertLess(sum(abs(x)**2 for x in actual[64:]), 1e-24)

    def test_recursive_state_decomposition(self):
        rng = random.Random(731)

        def reconstruct(v):
            if len(v) == 1:
                return v.copy()
            reduced, rotations = [], []
            for a, b in zip(v[::2], v[1::2]):
                radius = math.hypot(abs(a), abs(b))
                if radius == 0:
                    reduced.append(0j)
                    rotations.append(IDENTITY)
                    continue
                theta = 2 * math.atan2(abs(b), abs(a))
                phi = cmath.phase(b) - cmath.phase(a)
                c = radius * cmath.exp(0.5j * (cmath.phase(a) + cmath.phase(b)))
                reduced.append(c)
                rotations.append(mul(rz(phi), ry(theta)))
            smaller = reconstruct(reduced)
            return [c * gate[row][0] for c, gate in zip(smaller, rotations)
                    for row in range(2)]

        for n in range(1, 6):
            samples = [random_state(n, rng) for _ in range(10)]
            samples += [[complex(i == j) for i in range(2**n)] for j in range(2**n)]
            for state in samples:
                self.assertLess(distance(state, reconstruct(state)), 1e-12)

    def test_error_and_cost_envelopes(self):
        for n in range(2, 41):
            for t in (1, n, 2 ** (n // 2), 2**n):
                deltas = [Fraction(1, 40 * t * 2 ** (n - k)) for k in range(n)]
                self.assertLess(2 * t * sum(deltas), Fraction(1, 10))
                m = (n + 1) // 2
                for length in (1, n // 2 + 1, n + 1):
                    cost = sum(Fraction((n-k+length) * 2**k, k) for k in range(m, n))
                    envelope = Fraction(2 * 2**n * (2 + length), n)
                    self.assertLessEqual(cost, envelope)

    def test_tensor_power_separation(self):
        for t in (1, 2, 3, 16, 255):
            squared = 1 - (1 - Fraction(1, 4 * t)) ** t
            self.assertGreater(squared, Fraction(1, 25))
            # Construct a pair attaining the overlap used in the packing proof.
            overlap = math.sqrt(1 - 1 / (4 * t))
            self.assertAlmostEqual(1 - overlap ** (2 * t), float(squared), places=11)


if __name__ == '__main__':
    unittest.main(verbosity=2)
