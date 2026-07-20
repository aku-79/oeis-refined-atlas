"""Self-contained program for OEIS A396051.

A396051 is the periodic (S0, sym) class of the refined fixed-content
bracelet atlas.  The index n represents underlying bracelet length 2*n.
Every counted object is a nontrivial power of a unique primitive object
counted by A396632, hence

	a(n) = Sum_{d | n, d < n} A396632(d).

The formula produces the extended data efficiently.  Sawada fixed-content
necklace generation is included as an independent check on small indices.
"""

from __future__ import annotations

import sys
from functools import lru_cache


OFFSET = 2

KNOWN_TERMS = [
	1,
	1,
	3,
	1,
	14,
	1,
	55,
	12,
	290,
	1,
	1824,
	1,
	12357,
	299,
	97740,
	1,
	863596,
	1,
	8428228,
]  # a(2)..a(20)

# A396632(d), d=1..10.  These are sufficient for the proper-divisor
# formula throughout the DATA range a(2)..a(20).
A396632_TERMS = [1, 2, 11, 52, 287, 1758, 12354, 97685, 861824, 8427886]


def partitions_nonincreasing(n, max_part=None):
	if n < 0:
		return
	if n == 0:
		yield ()
		return
	if max_part is None or max_part > n:
		max_part = n
	for first in range(max_part, 0, -1):
		for tail in partitions_nonincreasing(n - first, first):
			yield (first,) + tail


def sawada_necklaces(content, n):
	"""Generate fixed-content necklaces using Sawada's algorithm."""

	k = len(content)
	remaining = list(content)
	word = [0] * (n + 1)
	output = []

	def generate(t, period):
		if t > n:
			if n % period == 0:
				output.append(tuple(word[1 : n + 1]))
			return

		symbol = word[t - period]
		if remaining[symbol] > 0:
			word[t] = symbol
			remaining[symbol] -= 1
			generate(t + 1, period)
			remaining[symbol] += 1

		for next_symbol in range(word[t - period] + 1, k):
			if remaining[next_symbol] > 0:
				word[t] = next_symbol
				remaining[next_symbol] -= 1
				generate(t + 1, t)
				remaining[next_symbol] += 1

	for symbol in range(k):
		if remaining[symbol] > 0:
			word[1] = symbol
			remaining[symbol] -= 1
			generate(2, 1)
			remaining[symbol] += 1
			break
	return output


def classify_necklace(rep):
	"""Return the refinement class (tau, sigma) of a necklace."""

	n = len(rep)
	reversal = rep[::-1]
	rotations = {rep[shift:] + rep[:shift] for shift in range(n)}
	sigma = "sym" if len(rotations) < n else "ns"
	if reversal not in rotations:
		return ("D", sigma)

	palindrome_representatives = sum(
		1 for rotation in rotations if rotation == rotation[::-1]
	)
	if palindrome_representatives == 0:
		tau = "S0"
	elif palindrome_representatives == 1:
		tau = "S1"
	else:
		tau = "S2"
	return (tau, sigma)


def refined_cyclic_counts(n):
	counts = {
		(tau, sigma): 0
		for tau in ("D", "S0", "S1", "S2")
		for sigma in ("sym", "ns")
	}
	for parts in partitions_nonincreasing(n):
		for necklace in sawada_necklaces(list(parts), n):
			counts[classify_necklace(necklace)] += 1
	return counts


def cyclic_to_dihedral(cyclic_counts):
	dihedral_counts = {}
	for (tau, sigma), value in cyclic_counts.items():
		if tau == "D":
			if value % 2 != 0:
				raise ValueError(
					f"D-class count must be even: ({tau}, {sigma}) = {value}"
				)
			dihedral_counts[(tau, sigma)] = value // 2
		else:
			dihedral_counts[(tau, sigma)] = value
	return dihedral_counts


def enumerated_class_term(n, tau, sigma):
	"""Compute a refined class at underlying length 2*n by enumeration."""

	cyclic = refined_cyclic_counts(2 * n)
	return cyclic_to_dihedral(cyclic)[(tau, sigma)]


@lru_cache(maxsize=None)
def a396632(n):
	"""Primitive (S0, ns) term A396632(n)."""

	if 1 <= n <= len(A396632_TERMS):
		return A396632_TERMS[n - 1]
	return enumerated_class_term(n, "S0", "ns")


def proper_divisors(n):
	return [d for d in range(1, n) if n % d == 0]


@lru_cache(maxsize=None)
def a(n):
	"""Return a(n) from the A396632 proper-divisor formula."""

	if n < OFFSET:
		raise ValueError(f"A396051 is indexed from n={OFFSET}")
	return sum(a396632(d) for d in proper_divisors(n))


def enumerated_term(n):
	"""Recompute a(n) directly by Sawada enumeration (slow check)."""

	if n < OFFSET:
		raise ValueError(f"A396051 is indexed from n={OFFSET}")
	return enumerated_class_term(n, "S0", "sym")


def verify_known_terms(enumeration_limit=4):
	"""Verify all formula terms and direct enumeration on small indices."""

	formula = [a(n) for n in range(OFFSET, OFFSET + len(KNOWN_TERMS))]
	if formula != KNOWN_TERMS:
		raise AssertionError((formula, KNOWN_TERMS))

	enumerated = [enumerated_term(n) for n in range(OFFSET, enumeration_limit + 1)]
	expected = KNOWN_TERMS[: enumeration_limit - OFFSET + 1]
	if enumerated != expected:
		raise AssertionError((enumerated, expected))
	return enumerated


def main():
	max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
	for n in range(OFFSET, max_n + 1):
		print(n, a(n))


if __name__ == "__main__":
	main()