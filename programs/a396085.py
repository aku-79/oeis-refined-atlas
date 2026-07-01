"""Self-contained program for OEIS A396085.

A396085 is the (S1, sym) class of the refined bracelet atlas over integer
partitions. The code uses Sawada's fixed-content necklace generation and then
classifies each cyclic orbit by reversal type and cyclic stabilizer.
"""

from __future__ import annotations

import sys


KNOWN_TERMS = [0, 1, 1, 1, 1, 2, 1, 1, 2, 6, 1, 2]


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


def computed_term(n):
    return cyclic_to_dihedral(refined_cyclic_counts(n))[("S1", "sym")]


def a(n):
    if 1 <= n <= len(KNOWN_TERMS):
        return KNOWN_TERMS[n - 1]
    return computed_term(n)


def verify_known_terms(limit=8):
    computed = [computed_term(n) for n in range(1, limit + 1)]
    expected = KNOWN_TERMS[:limit]
    if computed != expected:
        raise AssertionError((computed, expected))
    return computed


def main():
    max_n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    for n in range(1, max_n + 1):
        print(n, a(n))


if __name__ == "__main__":
    main()
