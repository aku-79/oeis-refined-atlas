"""A396229: the even-length (S2, ns) class of the refined atlas.

Let ``H(n)`` count all S2 cyclic orbits of underlying length ``2*n``.
Every such orbit contains two linear-palindrome representatives, while the
even-length S1 class is entirely periodic and counted by A396085.  Thus

	H(n) = (A005651(n) - A396085(2*n)) / 2.

Möbius inversion over the rotational period extracts the full-period class:

	a(n) = Sum_{d | n} mu(n/d) * H(d).
"""

from __future__ import annotations

import sys
from functools import lru_cache
from math import factorial
from typing import List

from .a396085 import term as a396085_term
from .common import partitions_nonincreasing, refined_dihedral_counts_for_n

OFFSET = 2

TERMS: List[int] = [
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


def _mobius(n: int) -> int:
	"""Return the Möbius function of a positive integer."""

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


def _divisors(n: int) -> List[int]:
	"""Return the positive divisors of n."""

	return [d for d in range(1, n + 1) if n % d == 0]


@lru_cache(maxsize=None)
def _strongly_normal_words(n: int) -> int:
	"""Return A005651(n), the strongly normal words of length n."""

	total = 0
	numerator = factorial(n)
	for profile in partitions_nonincreasing(n):
		denominator = 1
		for multiplicity in profile:
			denominator *= factorial(multiplicity)
		total += numerator // denominator
	return total


@lru_cache(maxsize=None)
def _s2_total(n: int) -> int:
	"""Return all S2 orbits at underlying length 2*n."""

	remainder = _strongly_normal_words(n) - a396085_term(2 * n)
	if remainder % 2:
		raise ArithmeticError("A005651(n) - A396085(2*n) must be even")
	return remainder // 2


@lru_cache(maxsize=None)
def formula_term(n: int) -> int:
	"""Return a(n) from the Möbius formula (n >= 2)."""

	if n < OFFSET:
		raise ValueError(f"A396229 is indexed from n={OFFSET}")
	return sum(_mobius(n // d) * _s2_total(d) for d in _divisors(n))


def term(n: int) -> int:
	"""Return a(n) for A396229."""

	if n < OFFSET:
		raise ValueError(f"A396229 is indexed from n={OFFSET}")
	if n <= OFFSET + len(TERMS) - 1:
		return TERMS[n - OFFSET]
	return formula_term(n)


def enumerated_term(n: int) -> int:
	"""Recompute a(n) by Sawada enumeration (slow independent check)."""

	if n < OFFSET:
		raise ValueError(f"A396229 is indexed from n={OFFSET}")
	return refined_dihedral_counts_for_n(2 * n)[("S2", "ns")]


def terms_upto(max_n: int = 20) -> List[int]:
	"""Return a(2)..a(max_n)."""

	return [term(n) for n in range(OFFSET, max_n + 1)]


def verify_known_terms(enumeration_limit: int = 4) -> None:
	"""Check all formula terms and a small independent enumeration."""

	formula = [formula_term(n) for n in range(OFFSET, OFFSET + len(TERMS))]
	if formula != TERMS:
		raise AssertionError((formula, TERMS))

	enumerated = [enumerated_term(n) for n in range(OFFSET, enumeration_limit + 1)]
	expected = TERMS[: enumeration_limit - OFFSET + 1]
	if enumerated != expected:
		raise AssertionError((enumerated, expected))


def main() -> None:
	"""Print sequence terms for a requested maximum index."""

	max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
	print("n  a(n)")
	for n in range(OFFSET, max_n + 1):
		print(f"{n:>2}  {term(n)}")


if __name__ == "__main__":
	main()