"""Shared combinatorial routines for refined bracelet atlas sequences."""

from __future__ import annotations

from typing import Dict, Iterator, List, Tuple


def partitions_nonincreasing(n: int, max_part: int | None = None) -> Iterator[Tuple[int, ...]]:
    """Yield the nonincreasing integer partitions of n."""

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


def sawada_necklaces(content: List[int], n: int) -> List[Tuple[int, ...]]:
    """Generate fixed-content necklaces using Sawada's algorithm."""

    k = len(content)
    remaining = list(content)
    word = [0] * (n + 1)
    output: List[Tuple[int, ...]] = []

    def generate(t: int, period: int) -> None:
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


def classify_necklace(rep: Tuple[int, ...]) -> Tuple[str, str]:
    """Return the refinement class (tau, sigma) of a cyclic canonical representative."""

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


def parts_to_content(parts: List[int]) -> List[int]:
    """Convert a partition to a multiplicity vector indexed by symbol."""

    return [int(part) for part in parts]


def refined_cyclic_counts_for_n(n: int) -> Dict[Tuple[str, str], int]:
    """Count refined cyclic orbits for a given n."""

    counts: Dict[Tuple[str, str], int] = {
        (tau, sigma): 0 for tau in ("D", "S0", "S1", "S2") for sigma in ("sym", "ns")
    }
    for parts in partitions_nonincreasing(n):
        content = parts_to_content(list(parts))
        for necklace in sawada_necklaces(content, n):
            counts[classify_necklace(necklace)] += 1
    return counts


def cyclic_to_dihedral(cyclic_counts: Dict[Tuple[str, str], int]) -> Dict[Tuple[str, str], int]:
    """Convert cyclic-orbit refined counts to dihedral-orbit refined counts."""

    dihedral_counts: Dict[Tuple[str, str], int] = {}
    for (tau, sigma), value in cyclic_counts.items():
        if tau == "D":
            if value % 2 != 0:
                raise ValueError(f"D-class count must be even: ({tau}, {sigma}) = {value}")
            dihedral_counts[(tau, sigma)] = value // 2
        else:
            dihedral_counts[(tau, sigma)] = value
    return dihedral_counts


def refined_dihedral_counts_for_n(n: int) -> Dict[Tuple[str, str], int]:
    """Return the refined dihedral-orbit counts for n."""

    return cyclic_to_dihedral(refined_cyclic_counts_for_n(n))