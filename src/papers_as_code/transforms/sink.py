from abc import abstractmethod
from typing import final

from papers_as_code.transforms.one_to_one import OneToOneTransform
from papers_as_code.type import Null, Type


class SinkTransform[T_in: Type](OneToOneTransform[T_in, Null]):
    """
    Consumes an input and outputs nothing, e.g. by writing a file.
    """
    output_type = Null

    @abstractmethod
    def consume(self, value: T_in) -> None:
        raise NotImplementedError

    @final
    def transform(self, value: T_in) -> Null:
        self.consume(value)
        return Null()
