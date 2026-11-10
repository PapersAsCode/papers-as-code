from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, TypeAlias, cast

from papers_as_code.transforms.base import BaseTransform, Slots
from papers_as_code.transforms.many_to_many import ManyToManyTransform
from papers_as_code.type import Type
from papers_as_code.utils import Graph


Node: TypeAlias = BaseTransform[Any, Any]


@dataclass(frozen=True)
class Edge:
    """Feeds one output slot of `source` into one input slot of `target`."""

    source: Node
    target: Node
    source_slot: int = 0
    target_slot: int = 0


Nodes: TypeAlias = list[Node]
Edges: TypeAlias = list[Edge]


class Pipeline[T_ins: tuple[Type, ...], T_outs: tuple[Type, ...]](
    ManyToManyTransform[T_ins, T_outs]
):
    """
    A graph of transforms, which is itself a transform.

    The pipeline's inputs feed the input slots of the root nodes, and its
    outputs are the outputs of the leaf nodes, both in the order of `nodes`.
    Outputs of other nodes that no edge consumes are discarded.
    """
    nodes: Nodes
    edges: Edges
    graph: Graph[Node]

    def __init__(self, nodes: Nodes, edges: Edges):
        self.nodes = nodes
        self.edges = edges
        self.graph = Graph(nodes, [(edge.source, edge.target) for edge in edges])

    @property
    def input_types(self) -> Slots:
        return _concatenate(node.input_types for node in self.graph.roots())

    @property
    def output_types(self) -> Slots:
        return _concatenate(node.output_types for node in self.graph.leaves())

    def transform(self, value: T_ins) -> T_outs:
        root_slots = [
            (root, slot)
            for root in self.graph.roots()
            for slot in range(self._input_count(root))
        ]
        slot_values: dict[tuple[Node, int], Type] = dict(
            zip(root_slots, value, strict=True)
        )
        outputs: dict[Node, tuple[Type, ...]] = {}

        for node in self.graph.topological_order():
            inputs = tuple(
                slot_values[(node, slot)] for slot in range(self._input_count(node))
            )
            outputs[node] = node.run(inputs)

            for edge in self.edges:
                if edge.source is node:
                    slot_values[(edge.target, edge.target_slot)] = outputs[node][
                        edge.source_slot
                    ]

        return cast(
            T_outs,
            tuple(output for leaf in self.graph.leaves() for output in outputs[leaf]),
        )

    def _input_count(self, node: Node) -> int:
        """Return a node's number of input slots, as declared or as wired."""
        if node.input_types is not None:
            return len(node.input_types)

        fed_slots = [edge.target_slot for edge in self.edges if edge.target is node]
        return max(fed_slots, default=-1) + 1


def _concatenate(all_slots: Iterable[Slots]) -> Slots:
    """Join the slots of several nodes, or None if any of them are unknown."""
    combined: list[type[Type] | None] = []

    for slots in all_slots:
        if slots is None:
            return None
        combined.extend(slots)

    return tuple(combined)
