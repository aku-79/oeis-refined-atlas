"""Self-contained program for OEIS A396575.

For an integer partition lambda of n, let c(lambda) be the decreasing
partition of the multiplicities of its distinct part sizes, and let C(n)
be the set of distinct collapse profiles.  If M(Q) is the fixed-content
necklace count for Q, then

	a(n) = Sum_{Q in C(n)} M(Q).

M(Q) is evaluated by Burnside's formula.  Sawada fixed-content necklace
generation is retained as an independent check on small indices.
"""

from __future__ import annotations

import sys
from collections import Counter
from functools import lru_cache
from math import factorial, gcd


OFFSET = 1

KNOWN_TERMS = [
	1,
	2,
	3,
	5,
	5,
	12,
	14,
	26,
	39,
	68,
	108,
	220,
	372,
	677,
	1191,
	2368,
	4167,
	8125,
	15163,
	28453,
	52865,
	103208,
	190573,
	368201,
	703725,
	1362555,
	2567667,
	5056536,
	9579999,
	18464908,
	36075194,
	69357848,
	132567002,
	262039898,
	499210661,
	976415792,
	1913373472,
	3717786264,
	7176336716,
	14184357576,
]  # a(1)..a(40)


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


def divisors(n):
	return [d for d in range(1, n + 1) if n % d == 0]


def totient(n):
	result = n
	prime = 2
	remaining = n
	while prime * prime <= remaining:
		if remaining % prime == 0:
			result -= result // prime
			while remaining % prime == 0:
				remaining //= prime
		prime += 1
	if remaining > 1:
		result -= result // remaining
	return result


def collapse_shape(profile):
	"""Return the decreasing multiplicities of distinct part sizes."""

	return tuple(sorted(Counter(profile).values(), reverse=True))


@lru_cache(maxsize=None)
def collapse_profiles(n):
	"""Return the distinct multiplicity-collapse profiles at total n."""

	if n < OFFSET:
		raise ValueError(f"A396575 is indexed from n={OFFSET}")
	return frozenset(collapse_shape(profile) for profile in partitions_nonincreasing(n))


@lru_cache(maxsize=None)
def necklace_count(profile):
	"""Return the fixed-content necklace count by Burnside's formula."""

	length = sum(profile)
	common_divisor = 0
	for multiplicity in profile:
		common_divisor = gcd(common_divisor, multiplicity)

	numerator_sum = 0
	for divisor in divisors(common_divisor):
		numerator = factorial(length // divisor)
		denominator = 1
		for multiplicity in profile:
			denominator *= factorial(multiplicity // divisor)
		numerator_sum += totient(divisor) * (numerator // denominator)

	if numerator_sum % length:
		raise ArithmeticError("Burnside numerator must be divisible by the length")
	return numerator_sum // length


@lru_cache(maxsize=None)
def a(n):
	"""Return A396575(n)."""

	if n < OFFSET:
		raise ValueError(f"A396575 is indexed from n={OFFSET}")
	return sum(necklace_count(profile) for profile in collapse_profiles(n))


def sawada_necklaces(content, n):
	"""Generate fixed-content necklaces using Sawada's algorithm."""

	symbol_count = len(content)
	remaining = list(content)
	word = [0] * (n + 1)
	output = []

	def generate(position, period):
		if position > n:
			if n % period == 0:
				output.append(tuple(word[1 : n + 1]))
			return

		symbol = word[position - period]
		if remaining[symbol] > 0:
			word[position] = symbol
			remaining[symbol] -= 1
			generate(position + 1, period)
			remaining[symbol] += 1

		for next_symbol in range(word[position - period] + 1, symbol_count):
			if remaining[next_symbol] > 0:
				word[position] = next_symbol
				remaining[next_symbol] -= 1
				generate(position + 1, position)
				remaining[next_symbol] += 1

	for symbol in range(symbol_count):
		if remaining[symbol] > 0:
			word[1] = symbol
			remaining[symbol] -= 1
			generate(2, 1)
			remaining[symbol] += 1
			break
	return output


def enumerated_term(n):
	"""Recompute a(n) by direct Sawada enumeration."""

	if n < OFFSET:
		raise ValueError(f"A396575 is indexed from n={OFFSET}")
	return sum(
		len(sawada_necklaces(list(profile), sum(profile)))
		for profile in collapse_profiles(n)
	)


def verify_known_terms(enumeration_limit=12):
	"""Check all formula terms and direct enumeration on small n."""

	formula = [a(n) for n in range(OFFSET, OFFSET + len(KNOWN_TERMS))]
	if formula != KNOWN_TERMS:
		raise AssertionError((formula, KNOWN_TERMS))

	enumerated = [enumerated_term(n) for n in range(OFFSET, enumeration_limit + 1)]
	expected = KNOWN_TERMS[:enumeration_limit]
	if enumerated != expected:
		raise AssertionError((enumerated, expected))
	return enumerated


def main():
	max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
	for n in range(OFFSET, max_n + 1):
		print(n, a(n))


if __name__ == "__main__":
	main()