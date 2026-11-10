from dataclasses import dataclass
from typing import Any, TypeAlias, cast

from papers_as_code.transforms.shape import Shape
from papers_as_code.transforms.transform import Transform
from papers_as_code.type import Type
from papers_as_code.utils import Graph


Node: TypeAlias = Transform[Any, Any]


@dataclass(frozen=True)
class Edge:
    """Feeds one output slot of `source` into one input slot of `target`."""

    source: Node
    target: Node
    source_slot: int = 0
    target_slot: int = 0


Nodes: TypeAlias = list[Node]
Edges: TypeAlias = list[Edge]


class Pipeline[
    T_in: Type | tuple[Type, ...],
    T_out: Type | tuple[Type, ...],
](Transform[T_in, T_out]):
    """
    A graph of transforms, which is itself a transform.

    The pipeline's input feeds the root nodes, and its output comes from the
    leaf nodes
    """
    nodes: Nodes
    edges: Edges
    graph: Graph[Node]

    def __init__(self, nodes: Nodes, edges: Edges):
        self.nodes = nodes
        self.edges = edges
        self.graph = Graph(nodes, [(edge.source, edge.target) for edge in edges])

    def input_shape(self) -> Shape:
        return Shape.combine([self._input_shape(root) for root in self.graph.roots()])

    def output_shape(self) -> Shape | None:
        shapes = [leaf.output_shape() for leaf in self.graph.leaves()]
        known = [shape for shape in shapes if shape is not None]
        return Shape.combine(known) if len(known) == len(shapes) else None

    def transform(self, value: T_in) -> T_out:
        root_slots = [
            (root, slot)
            for root in self.graph.roots()
            for slot in range(self._input_shape(root).count)
        ]
        slot_values: dict[tuple[Node, int], Any] = dict(
            zip(root_slots, self.input_shape().unpack(value), strict=True)
        )
        results: dict[Node, Any] = {}

        for node in self.graph.topological_order():
            shape = self._input_shape(node)
            inputs = tuple(slot_values[(node, slot)] for slot in range(shape.count))
            results[node] = node.transform(shape.pack(inputs))

            for edge in self.edges:
                if edge.source is node:
                    output = _output_slots(results[node])[edge.source_slot]
                    slot_values[(edge.target, edge.target_slot)] = output

        leaves = self.graph.leaves()
        if len(leaves) == 1:
            return cast(T_out, results[leaves[0]])
        return cast(
            T_out,
            tuple(slot for leaf in leaves for slot in _output_slots(results[leaf])),
        )

    def _input_shape(self, node: Node) -> Shape:
        """Return a node's annotated input shape, or one inferred from its edges."""
        annotated = node.input_shape()
        if annotated is not None:
            return annotated

        fed_slots = [edge.target_slot for edge in self.edges if edge.target is node]
        count = max(fed_slots, default=0) + 1
        return Shape(many=count > 1, count=count)


def _output_slots(result: Any) -> tuple[Any, ...]:
    """Split a transform's result into one value per output slot."""
    return result if isinstance(result, tuple) else (result,)
