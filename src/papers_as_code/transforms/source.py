from abc import abstractmethod
from typing import final

from papers_as_code.transforms.one_to_one import OneToOneTransform
from papers_as_code.type import Null, Type


class SourceTransform[T_out: Type](OneToOneTransform[Null, T_out]):
    """
    Produces an output from nothing, e.g. by reading a file.
    """
    input_type = Null

    @abstractmethod
    def produce(self) -> T_out:
        raise NotImplementedError

    @final
    def transform(self, value: Null) -> T_out:
        return self.produce()
