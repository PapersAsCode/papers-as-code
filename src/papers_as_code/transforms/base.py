from abc import ABC, abstractmethod

from papers_as_code.type import Type
from papers_as_code.utils import Label


class BaseTransform[
    T_in: Type | tuple[Type, ...],
    T_out: Type | tuple[Type, ...],
](ABC):
    """
    Anything that maps an input to an output, each a Type or a tuple of Types.
    """
    labels: set[Label]

    @abstractmethod
    def transform(self, value: T_in) -> T_out:
        raise NotImplementedError
