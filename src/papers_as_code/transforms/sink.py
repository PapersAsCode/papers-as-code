from abc import abstractmethod
from typing import final

from papers_as_code.transforms.shape import Shape, annotated_shapes
from papers_as_code.transforms.transform import Transform
from papers_as_code.type import Null, Type


class SinkTransform[T_in: Type | tuple[Type, ...]](Transform[T_in, Null]):
    """
    Consumes an input and outputs nothing, e.g. by writing a file.
    """
    transform_type = "sink"

    @abstractmethod
    def consume(self, value: T_in) -> None:
        raise NotImplementedError

    @final
    def transform(self, value: T_in) -> Null:
        self.consume(value)
        return Null()

    def input_shape(self) -> Shape | None:
        return annotated_shapes(self.consume)[0]
