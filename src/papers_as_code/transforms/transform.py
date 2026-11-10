"""
Transforms are the atoms of data pipelines. The composition of transforms is in
itself a transform, and a pipeline can be viewed as a transform with multiple
inputs.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from papers_as_code.transforms.shape import Shape, annotated_shapes
from papers_as_code.type import Type
from papers_as_code.utils import Label, TransformType
from papers_as_code.transforms.pipeline import Edge, Pipeline

if TYPE_CHECKING:
    from papers_as_code.transforms.pipeline import Pipeline


class Transform[
    T_in: Type | tuple[Type, ...],
    T_out: Type | tuple[Type, ...],
](ABC):
    """
    Turns an input into an output.
    """
    labels: set[Label]
    transform_type: TransformType = "transformation"

    @abstractmethod
    def transform(self, value: T_in) -> T_out:
        raise NotImplementedError

    def input_shape(self) -> Shape | None:
        """Return the input shape `transform` is annotated with, if any."""
        return annotated_shapes(self.transform)[0]

    def output_shape(self) -> Shape | None:
        """Return the output shape `transform` is annotated with, if any."""
        return annotated_shapes(self.transform)[1]

    def __rshift__[T_next: Type | tuple[Type, ...]](
        self, other: "Transform[T_out, T_next]"
    ) -> "Pipeline[T_in, T_next]":
        """Chain two transforms, feeding each output slot to the same input slot."""
        shape = other.input_shape() or self.output_shape() or Shape.one()
        edges = [Edge(self, other, slot, slot) for slot in range(shape.count)]

        return Pipeline[T_in, T_next]([self, other], edges)
