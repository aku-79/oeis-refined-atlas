"""A396575: cyclic multiplicity-collapse spectrum.

For an integer partition lambda of n, let c(lambda) be the decreasing
partition of the multiplicities of its distinct part sizes, and let C(n)
be the set of distinct collapse profiles.  If M(Q) denotes the number of
fixed-content necklaces with content profile Q, then

	a(n) = Sum_{Q in C(n)} M(Q).

Each distinct collapse profile contributes exactly once.
"""

from __future__ import annotations

import sys
from collections import Counter
from functools import lru_cache
from math import factorial, gcd
from typing import FrozenSet, List, Tuple

from .common import partitions_nonincreasing, sawada_necklaces

Shape = Tuple[int, ...]

OFFSET = 1

TERMS: List[int] = [
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


def _divisors(n: int) -> List[int]:
	"""Return the positive divisors of n."""

	return [d for d in range(1, n + 1) if n % d == 0]


def _totient(n: int) -> int:
	"""Return Euler's totient function."""

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


def collapse_shape(profile: Shape) -> Shape:
	"""Return the decreasing multiplicities of distinct part sizes."""

	return tuple(sorted(Counter(profile).values(), reverse=True))


@lru_cache(maxsize=None)
def collapse_profiles(n: int) -> FrozenSet[Shape]:
	"""Return C(n), the set of distinct collapse profiles at total n."""

	if n < 1:
		raise ValueError("collapse profiles are indexed by positive integers")
	return frozenset(collapse_shape(profile) for profile in partitions_nonincreasing(n))


@lru_cache(maxsize=None)
def necklace_count(profile: Shape) -> int:
	"""Return M(profile) by the fixed-content Burnside formula."""

	length = sum(profile)
	common_divisor = 0
	for multiplicity in profile:
		common_divisor = gcd(common_divisor, multiplicity)

	numerator_sum = 0
	for divisor in _divisors(common_divisor):
		numerator = factorial(length // divisor)
		denominator = 1
		for multiplicity in profile:
			denominator *= factorial(multiplicity // divisor)
		numerator_sum += _totient(divisor) * (numerator // denominator)

	if numerator_sum % length:
		raise ArithmeticError("Burnside numerator must be divisible by the length")
	return numerator_sum // length


@lru_cache(maxsize=None)
def formula_term(n: int) -> int:
	"""Return a(n) from the multiplicity-collapse formula."""

	if n < OFFSET:
		raise ValueError(f"A396575 is indexed from n={OFFSET}")
	return sum(necklace_count(profile) for profile in collapse_profiles(n))


def term(n: int) -> int:
	"""Return a(n) for A396575."""

	if n < OFFSET:
		raise ValueError(f"A396575 is indexed from n={OFFSET}")
	if n <= len(TERMS):
		return TERMS[n - OFFSET]
	return formula_term(n)


def enumerated_term(n: int) -> int:
	"""Recompute a(n) by direct Sawada necklace enumeration."""

	if n < OFFSET:
		raise ValueError(f"A396575 is indexed from n={OFFSET}")
	return sum(
		len(sawada_necklaces(list(profile), sum(profile)))
		for profile in collapse_profiles(n)
	)


def terms_upto(max_n: int = 40) -> List[int]:
	"""Return a(1)..a(max_n)."""

	return [term(n) for n in range(OFFSET, max_n + 1)]


def verify_known_terms(enumeration_limit: int = 12) -> None:
	"""Check all formula terms and a direct enumeration on small n."""

	formula = [formula_term(n) for n in range(OFFSET, OFFSET + len(TERMS))]
	if formula != TERMS:
		raise AssertionError((formula, TERMS))

	enumerated = [enumerated_term(n) for n in range(OFFSET, enumeration_limit + 1)]
	expected = TERMS[:enumeration_limit]
	if enumerated != expected:
		raise AssertionError((enumerated, expected))


def main() -> None:
	"""Print sequence terms for a requested maximum index."""

	max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
	print("n  a(n)")
	for n in range(OFFSET, max_n + 1):
		print(f"{n:>2}  {term(n)}")


if __name__ == "__main__":
	main()