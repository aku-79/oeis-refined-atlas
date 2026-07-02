"""Self-contained program for OEIS A396085.

A396085 is the (S1, sym) class of the refined bracelet atlas over integer
partitions: reversal-closed cyclic orbits with exactly one palindromic
rotation and a nontrivial cyclic stabilizer.

Every counted word is a power U^(n/d) where the rotational period d is a
proper divisor of n and U is an aperiodic (S1, ns) word of length d.  Such U
exist only for odd d, where they are counted by aperiodic linear palindromes.
This gives the closed formula

    a(n) = Sum_{d | n, d < n, d odd} g(d),
    g(d) = Sum_{e | d} mu(d/e) * T(e),
    T(m) = Sum_{lambda |- m, exactly one odd part}
           ((m-1)/2)! / Product_i floor(lambda_i / 2)!.

The Sawada fixed-content necklace enumeration is kept as an independent
verification of the formula on small lengths.
"""

from __future__ import annotations

import sys
from functools import lru_cache
from math import factorial


KNOWN_TERMS = [
    1, 1, 1, 1, 2, 1, 1, 2, 6, 1, 2, 1, 23, 7, 1, 1, 110, 1, 6, 24, 617,
    1, 2, 6, 4035, 110, 23, 1, 29927, 1, 1, 618, 249926, 28, 110, 1,
    2316317, 4036, 6, 1, 23674841, 1, 617, 30035, 264329177, 1, 2, 23,
    3207278255, 249927, 4035, 1, 42011308653, 622, 23,
]  # a(2)..a(56)


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
def palindrome_total(m):
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


def mobius(n):
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
def aperiodic_palindromes(d):
    """g(d): aperiodic (S1, ns) orbits of odd length d."""
    if d % 2 == 0:
        return 0
    total = 0
    for e in range(1, d + 1, 2):
        if d % e == 0:
            total += mobius(d // e) * palindrome_total(e)
    return total


def a(n):
    """a(n): the (S1, sym) bracelet count at length n (n >= 2)."""
    total = 0
    for d in range(1, n, 2):
        if n % d == 0:
            total += aperiodic_palindromes(d)
    return total


def sawada_necklaces(content, n):
    k = len(content)
    remaining = list(content)
    word = [0] * (n + 1)
    output = []

    def generate(t, period):
        if t > n:
            if n % period == 0:
                output.append(tuple(word[1 : n + 1]))
            return

        j = word[t - period]
        if remaining[j] > 0:
            word[t] = j
            remaining[j] -= 1
            generate(t + 1, period)
            remaining[j] += 1

        for next_symbol in range(word[t - period] + 1, k):
            if remaining[next_symbol] > 0:
                word[t] = next_symbol
                remaining[next_symbol] -= 1
                generate(t + 1, t)
                remaining[next_symbol] += 1

    for j in range(k):
        if remaining[j] > 0:
            word[1] = j
            remaining[j] -= 1
            generate(2, 1)
            remaining[j] += 1
            break
    return output


def classify_necklace(rep):
    n = len(rep)
    reversal = rep[::-1]
    rotations = {rep[s:] + rep[:s] for s in range(n)}
    sigma = "sym" if len(rotations) < n else "ns"
    if reversal not in rotations:
        return ("D", sigma)

    palindromic_rotations = sum(1 for rotation in rotations if rotation == rotation[::-1])
    if palindromic_rotations == 0:
        tau = "S0"
    elif palindromic_rotations == 1:
        tau = "S1"
    else:
        tau = "S2"
    return (tau, sigma)


def refined_cyclic_counts(n):
    counts = {(tau, sigma): 0 for tau in ("D", "S0", "S1", "S2") for sigma in ("sym", "ns")}
    for parts in partitions_nonincreasing(n):
        for necklace in sawada_necklaces(list(parts), n):
            counts[classify_necklace(necklace)] += 1
    return counts


def cyclic_to_dihedral(cyclic_counts):
    dihedral_counts = {}
    for (tau, sigma), value in cyclic_counts.items():
        if tau == "D":
            if value % 2 != 0:
                raise ValueError(f"D-class count must be even: ({tau}, {sigma}) = {value}")
            dihedral_counts[(tau, sigma)] = value // 2
        else:
            dihedral_counts[(tau, sigma)] = value
    return dihedral_counts


def enumerated_term(n):
    """a(n) recomputed by Sawada enumeration (slow check)."""
    return cyclic_to_dihedral(refined_cyclic_counts(n))[("S1", "sym")]


def verify_known_terms(limit=12):
    computed = [enumerated_term(n) for n in range(2, limit + 1)]
    expected = KNOWN_TERMS[: limit - 1]
    if computed != expected:
        raise AssertionError((computed, expected))
    formula = [a(n) for n in range(2, len(KNOWN_TERMS) + 2)]
    if formula != KNOWN_TERMS:
        raise AssertionError((formula, KNOWN_TERMS))
    return computed


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 56
    for n in range(2, max_n + 1):
        print(n, a(n))


if __name__ == "__main__":
    main()
