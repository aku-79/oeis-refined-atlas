"""A395436: the (S1, ns) class of the refined bracelet atlas."""

from __future__ import annotations

import sys
from typing import List

from .common import refined_dihedral_counts_for_n

TERMS: List[int] = [0, 0, 1, 0, 5, 0, 22, 0, 108, 0, 616, 0]


def term(n: int) -> int:
    """Return a(n) for A395436."""

    if 1 <= n <= len(TERMS):
        return TERMS[n - 1]
    return refined_dihedral_counts_for_n(n)[("S1", "ns")]


def terms_upto(max_n: int = 12) -> List[int]:
    """Return the first max_n terms, including leading zeros."""

    return [term(n) for n in range(1, max_n + 1)]


def main() -> None:
    """Print the sequence terms for a requested range."""

    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    print("n  a(n)")
    for n in range(1, max_n + 1):
        print(f"{n:>2}  {term(n)}")


if __name__ == "__main__":
    main()