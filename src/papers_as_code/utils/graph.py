"""A small directed graph. It knows nothing about what its nodes are."""

from collections.abc import Hashable
from graphlib import TopologicalSorter


class Graph[N: Hashable]:
    """
    A directed graph over `nodes`, with `edges` as (source, target) pairs.

    `roots` and `leaves` follow the order in which `nodes` was given.
    """

    nodes: list[N]
    edges: list[tuple[N, N]]

    def __init__(self, nodes: list[N], edges: list[tuple[N, N]]):
        self.nodes = nodes
        self.edges = edges

    def roots(self) -> list[N]:
        """Return the nodes with no incoming edges."""
        targets = {target for _, target in self.edges}
        return [node for node in self.nodes if node not in targets]

    def leaves(self) -> list[N]:
        """Return the nodes with no outgoing edges."""
        sources = {source for source, _ in self.edges}
        return [node for node in self.nodes if node not in sources]

    def topological_order(self) -> list[N]:
        """Return every node after its predecessors, or raise a CycleError."""
        predecessors: dict[N, list[N]] = {node: [] for node in self.nodes}
        for source, target in self.edges:
            predecessors.setdefault(target, []).append(source)

        return list(TopologicalSorter(predecessors).static_order())
