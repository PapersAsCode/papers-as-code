from abc import abstractmethod
from typing import final

from papers_as_code.transforms.shape import Shape, annotated_shapes
from papers_as_code.transforms.transform import Transform
from papers_as_code.type import Null, Type


class SourceTransform[T_out: Type | tuple[Type, ...]](Transform[Null, T_out]):
    """
    Produces an output from nothing, e.g. by reading a file.
    """
    transform_type = "source"

    @abstractmethod
    def produce(self) -> T_out:
        raise NotImplementedError

    @final
    def transform(self, value: Null) -> T_out:
        return self.produce()

    def output_shape(self) -> Shape | None:
        return annotated_shapes(self.produce)[1]
