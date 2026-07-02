"""A396085: the (S1, sym) class of the refined bracelet atlas.

Every counted word of length n is a power U^(n/d) with d a proper divisor of
n and U an aperiodic (S1, ns) word of length d; such U exist only for odd d,
where they are counted by aperiodic linear palindromes.  Hence

    a(n) = Sum_{d | n, d < n, d odd} g(d),

with g(d) the aperiodic odd-palindrome count (the A395436 bisection).
"""

from __future__ import annotations

import sys
from functools import lru_cache
from math import factorial
from typing import List

from .common import partitions_nonincreasing, refined_dihedral_counts_for_n

TERMS: List[int] = [
    1, 1, 1, 1, 2, 1, 1, 2, 6, 1, 2, 1, 23, 7, 1, 1, 110, 1, 6, 24, 617,
    1, 2, 6, 4035, 110, 23, 1, 29927, 1, 1, 618, 249926, 28, 110, 1,
    2316317, 4036, 6, 1, 23674841, 1, 617, 30035, 264329177, 1, 2, 23,
    3207278255, 249927, 4035, 1, 42011308653, 622, 23,
]  # a(2)..a(56)


@lru_cache(maxsize=None)
def _palindrome_total(m: int) -> int:
    """T(m): linear palindromes of odd length m over partition content."""

    half = (m - 1) // 2
    total = 0
    for lam in partitions_nonincreasing(m):
        if sum(1 for part in lam if part % 2 == 1) != 1:
            continue
        denominator = 1
        for part in lam:
            denominator *= factorial(part // 2)
        total += factorial(half) // denominator
    return total


def _mobius(n: int) -> int:
    result = 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            n //= d
            if n % d == 0:
                return 0
            result = -result
        d += 1
    if n > 1:
        result = -result
    return result


@lru_cache(maxsize=None)
def _aperiodic_palindromes(d: int) -> int:
    """g(d): aperiodic (S1, ns) orbits of odd length d."""

    if d % 2 == 0:
        return 0
    total = 0
    for e in range(1, d + 1, 2):
        if d % e == 0:
            total += _mobius(d // e) * _palindrome_total(e)
    return total


def term(n: int) -> int:
    """Return a(n) for A396085 (n >= 2)."""

    total = 0
    for d in range(1, n, 2):
        if n % d == 0:
            total += _aperiodic_palindromes(d)
    return total


def enumerated_term(n: int) -> int:
    """Recompute a(n) by Sawada enumeration (slow check)."""

    return refined_dihedral_counts_for_n(n)[("S1", "sym")]


def terms_upto(max_n: int = 56) -> List[int]:
    """Return a(2)..a(max_n)."""

    return [term(n) for n in range(2, max_n + 1)]


def main() -> None:
    """Print the sequence terms for a requested range."""

    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 56
    print("n  a(n)")
    for n in range(2, max_n + 1):
        print(f"{n:>2}  {term(n)}")


if __name__ == "__main__":
    main()
