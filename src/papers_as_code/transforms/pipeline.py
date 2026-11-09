from typing import Literal, TypeAlias

from papers_as_code.transforms.base import BaseTransform
from papers_as_code.transforms.transform import Transform
from papers_as_code.type import Type
from papers_as_code.utils.logger import get_logger


logger = get_logger(__name__)


Nodes: TypeAlias = list[Transform]
Edges: TypeAlias = dict[Transform, list[Transform]]


ValidationLevel: TypeAlias = Literal["throw", "warn"]


class GraphTopologyException(Exception):
    """The transforms in a pipeline do not fit together."""


class Pipeline[T_ins: tuple[Type, ...], T_outs: tuple[Type, ...]](
    BaseTransform[T_ins, T_outs]
):
    nodes: Nodes
    edges: Edges

    def __init__(self, nodes: Nodes, edges: Edges, validate: ValidationLevel = "throw"):
        self.nodes = nodes
        self.edges = edges

        try:
            self.validate_graph()
        except GraphTopologyException as e:
            if validate == "throw":
                raise e
            elif validate == "warn":
                logger.warning("Pipeline failed validation: %s", e)

    def transform(self, value: T_ins) -> T_outs:
        pass

    def validate_graph(self) -> None:
        """Check that each transform's output fits the input of the next."""
        mismatches: list[str] = []

        for source, targets in self.edges.items():
            for target in targets:
                produced = source.output_type
                expected = target.input_type

                edge = f"{type(source).__name__} -> {type(target).__name__}"
                if produced is None or expected is None:
                    logger.info("Skipping validation of %s: type not specified", edge)
                elif not issubclass(produced, expected):
                    mismatches.append(
                        f"{edge}: {produced.__name__} does not fit {expected.__name__}"
                    )

        if mismatches:
            raise GraphTopologyException("; ".join(mismatches))
