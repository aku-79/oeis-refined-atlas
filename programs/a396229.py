"""Self-contained program for OEIS A396229.

A396229 is the full-period (S2, ns) class of the refined fixed-content
bracelet atlas.  The index n represents underlying bracelet length 2*n.

Let H(n) count all S2 cyclic orbits of underlying length 2*n.  Even linear
palindromes are determined by their first half, giving A005651(n) in total;
the S1 contribution is A396085(2*n), and every S2 orbit contributes two
linear-palindrome representatives.  Hence

	H(n) = (A005651(n) - A396085(2*n)) / 2,
	a(n) = Sum_{d | n} mu(n/d) * H(d).

The formula produces the extended data efficiently.  Sawada fixed-content
necklace generation is included as an independent check on small indices.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from math import factorial


OFFSET = 2

KNOWN_TERMS = [
	1,
	4,
	22,
	120,
	795,
	5729,
	47728,
	435456,
	4439655,
	49164467,
	595788438,
	7771511356,
	109334263479,
	1642874543650,
	26350406591960,
	448348912480608,
	8080221295377684,
	153591670339286219,
	3073725730106911950,
]  # a(2)..a(20)


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


@lru_cache(maxsize=None)
def strongly_normal_words(n):
	"""A005651(n): sum of multinomial coefficients over partitions."""

	total = 0
	numerator = factorial(n)
	for profile in partitions_nonincreasing(n):
		denominator = 1
		for multiplicity in profile:
			denominator *= factorial(multiplicity)
		total += numerator // denominator
	return total


@lru_cache(maxsize=None)
def palindrome_total(m):
	"""Strongly normal linear palindromes of odd length m."""

	half = (m - 1) // 2
	total = 0
	for profile in partitions_nonincreasing(m):
		if sum(1 for part in profile if part % 2 == 1) != 1:
			continue
		denominator = 1
		for part in profile:
			denominator *= factorial(part // 2)
		total += factorial(half) // denominator
	return total


def mobius(n):
	if n < 1:
		raise ValueError("mobius is defined here only for positive integers")
	result = 1
	divisor = 2
	while divisor * divisor <= n:
		if n % divisor == 0:
			n //= divisor
			if n % divisor == 0:
				return 0
			result = -result
		divisor += 1
	if n > 1:
		result = -result
	return result


def divisors(n):
	return [d for d in range(1, n + 1) if n % d == 0]


@lru_cache(maxsize=None)
def aperiodic_odd_palindromes(d):
	"""Aperiodic S1 count at odd length d."""

	if d % 2 == 0:
		return 0
	return sum(mobius(d // e) * palindrome_total(e) for e in divisors(d))


@lru_cache(maxsize=None)
def a396085(n):
	"""Periodic S1 count at length n."""

	return sum(aperiodic_odd_palindromes(d) for d in divisors(n) if d < n)


@lru_cache(maxsize=None)
def s2_total(n):
	"""All S2 orbits at underlying length 2*n."""

	remainder = strongly_normal_words(n) - a396085(2 * n)
	if remainder % 2:
		raise ArithmeticError("A005651(n) - A396085(2*n) must be even")
	return remainder // 2


@lru_cache(maxsize=None)
def a(n):
	"""Return A396229(n) from the Möbius formula."""

	if n < OFFSET:
		raise ValueError(f"A396229 is indexed from n={OFFSET}")
	return sum(mobius(n // d) * s2_total(d) for d in divisors(n))


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
	for profile in partitions_nonincreasing(n):
		for necklace in sawada_necklaces(list(profile), n):
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


def enumerated_term(n):
	"""Recompute a(n) directly by Sawada enumeration (slow check)."""

	if n < OFFSET:
		raise ValueError(f"A396229 is indexed from n={OFFSET}")
	cyclic = refined_cyclic_counts(2 * n)
	return cyclic_to_dihedral(cyclic)[("S2", "ns")]


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
