"""Consistent hashing with virtual nodes.

`hash(key) % N` remaps almost every key when N changes, so adding one node to a
ten-node cache cluster sends 90% of the keyspace to the origin at once.
Consistent hashing places nodes and keys on a ring, so adding a node moves only
the keys in its arc -- roughly 1/N.

Virtual nodes are not optional. With ten physical points the arcs are wildly
uneven; giving each node ~150 points evens the distribution and, more
importantly, spreads a dead node's keys across all survivors instead of dumping
them on one neighbour.
"""

from __future__ import annotations

import bisect
import hashlib
from typing import Dict, Iterable, List, Optional, Tuple


def _hash(value: str) -> int:
    return int.from_bytes(hashlib.sha1(value.encode()).digest()[:8], "big")


class HashRing:
    def __init__(self, nodes: Iterable[str] = (), vnodes: int = 150) -> None:
        if vnodes < 1:
            raise ValueError("vnodes must be at least 1")
        self.vnodes = vnodes
        self._ring: List[Tuple[int, str]] = []
        self._keys: List[int] = []
        self._nodes: set[str] = set()
        for node in nodes:
            self.add(node)

    def add(self, node: str) -> None:
        if node in self._nodes:
            return
        self._nodes.add(node)
        for i in range(self.vnodes):
            point = _hash(f"{node}#{i}")
            bisect.insort(self._ring, (point, node))
        self._keys = [p for p, _ in self._ring]

    def remove(self, node: str) -> None:
        if node not in self._nodes:
            return
        self._nodes.discard(node)
        self._ring = [(p, n) for p, n in self._ring if n != node]
        self._keys = [p for p, _ in self._ring]

    def get(self, key: str) -> Optional[str]:
        """The node that owns `key`: the first ring point clockwise from it."""
        if not self._ring:
            return None
        point = _hash(key)
        idx = bisect.bisect_left(self._keys, point)
        if idx == len(self._ring):
            idx = 0
        return self._ring[idx][1]

    def get_nodes(self, key: str, count: int = 2) -> List[str]:
        """`count` distinct nodes walking clockwise -- the replication set."""
        if not self._ring:
            return []
        point = _hash(key)
        idx = bisect.bisect_left(self._keys, point)
        seen: List[str] = []
        for offset in range(len(self._ring)):
            node = self._ring[(idx + offset) % len(self._ring)][1]
            if node not in seen:
                seen.append(node)
                if len(seen) == count:
                    break
        return seen

    def distribution(self, sample_keys: Iterable[str]) -> Dict[str, int]:
        """How many sampled keys land on each node. Used by the tests."""
        counts: Dict[str, int] = {n: 0 for n in self._nodes}
        for key in sample_keys:
            owner = self.get(key)
            if owner:
                counts[owner] += 1
        return counts
