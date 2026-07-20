"""A396051: the even-length (S0, sym) class of the refined atlas.

Every counted bracelet of underlying length ``2*n`` is a nontrivial power
of a unique primitive bracelet in the (S0, ns) class A396632.  Therefore

	a(n) = Sum_{d | n, d < n} A396632(d),

where A396632(d) counts the primitive class at underlying length ``2*d``.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from typing import List

from .a396632 import term as a396632_term
from .common import refined_dihedral_counts_for_n

OFFSET = 2

TERMS: List[int] = [
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

# A396632(d), d=1..10. These primitive terms cover every proper divisor
# needed to evaluate the formula throughout the DATA range a(2)..a(20).
A396632_TERMS: List[int] = [
	1,
	2,
	11,
	52,
	287,
	1758,
	12354,
	97685,
	861824,
	8427886,
]


def _proper_divisors(n: int) -> List[int]:
	"""Return the positive proper divisors of n."""

	return [d for d in range(1, n) if n % d == 0]


def _primitive_term(n: int) -> int:
	"""Return A396632(n), using cached DATA-range terms when available."""

	if 1 <= n <= len(A396632_TERMS):
		return A396632_TERMS[n - 1]
	return a396632_term(n)


@lru_cache(maxsize=None)
def formula_term(n: int) -> int:
	"""Return a(n) from the divisor formula (n >= 2)."""

	if n < OFFSET:
		raise ValueError(f"A396051 is indexed from n={OFFSET}")
	return sum(_primitive_term(d) for d in _proper_divisors(n))


def term(n: int) -> int:
	"""Return a(n) for A396051."""

	if n < OFFSET:
		raise ValueError(f"A396051 is indexed from n={OFFSET}")
	if n <= OFFSET + len(TERMS) - 1:
		return TERMS[n - OFFSET]
	return formula_term(n)


def enumerated_term(n: int) -> int:
	"""Recompute a(n) by Sawada enumeration (slow independent check)."""

	if n < OFFSET:
		raise ValueError(f"A396051 is indexed from n={OFFSET}")
	return refined_dihedral_counts_for_n(2 * n)[("S0", "sym")]


def terms_upto(max_n: int = 20) -> List[int]:
	"""Return a(2)..a(max_n)."""

	return [term(n) for n in range(OFFSET, max_n + 1)]


def verify_known_terms(enumeration_limit: int = 4, formula_limit: int = 20) -> None:
	"""Check the formula and a small independent Sawada enumeration."""

	formula = [formula_term(n) for n in range(OFFSET, formula_limit + 1)]
	expected_formula = TERMS[: formula_limit - OFFSET + 1]
	if formula != expected_formula:
		raise AssertionError((formula, expected_formula))

	enumerated = [enumerated_term(n) for n in range(OFFSET, enumeration_limit + 1)]
	expected_enumeration = TERMS[: enumeration_limit - OFFSET + 1]
	if enumerated != expected_enumeration:
		raise AssertionError((enumerated, expected_enumeration))


def main() -> None:
	"""Print sequence terms for a requested maximum index."""

	max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
	print("n  a(n)")
	for n in range(OFFSET, max_n + 1):
		print(f"{n:>2}  {term(n)}")


if __name__ == "__main__":
	main()