"""A395436: the odd-length (S1, ns) class of the refined bracelet atlas.

Indexed by half-length: term(n) is the count at length 2*n+1.  The class is
empty in even lengths.  Each counted orbit contains exactly one linear
palindrome, and that palindrome is aperiodic, giving the closed formula

    a(n) = Sum_{d | 2*n+1} mu((2*n+1)/d) * T(d),

where T(m) counts all linear palindromes of odd length m over
partition-indexed content (exactly one odd part, central multinomial).
"""

from __future__ import annotations

import sys
from functools import lru_cache
from math import factorial
from typing import List

from .common import partitions_nonincreasing, refined_dihedral_counts_for_n

TERMS: List[int] = [
    1,
    5,
    22,
    108,
    616,
    4034,
    29920,
    249925,
    2316316,
    23674817,
    264329176,
    3207278249,
    42011308543,
    591460307156,
    8905905152797,
    142897741683228,
    2433947385964345,
    43873382718719948,
    834402502632546553,
    16699964488044322204,
    350869837371828862606,
]


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


def term(n: int) -> int:
    """Return a(n) for A395436 (count at length 2*n+1)."""

    length = 2 * n + 1
    total = 0
    for d in range(1, length + 1, 2):
        if length % d == 0:
            total += _mobius(length // d) * _palindrome_total(d)
    return total


def enumerated_term(n: int) -> int:
    """Recompute a(n) by Sawada enumeration at length 2*n+1 (slow check)."""

    return refined_dihedral_counts_for_n(2 * n + 1)[("S1", "ns")]


def terms_upto(max_n: int = 21) -> List[int]:
    """Return the first max_n terms of the bisected sequence."""

    return [term(n) for n in range(1, max_n + 1)]


def main() -> None:
    """Print the sequence terms for a requested range."""

    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    print("n  a(n)")
    for n in range(1, max_n + 1):
        print(f"{n:>2}  {term(n)}")


if __name__ == "__main__":
    main()