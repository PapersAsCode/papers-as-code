from abc import abstractmethod
from typing import final

from papers_as_code.transforms.base import BaseTransform
from papers_as_code.type import Type


class ManyToManyTransform[T_ins: tuple[Type, ...], T_outs: tuple[Type, ...]](
    BaseTransform[T_ins, T_outs]
):
    """
    Turns several inputs into several outputs.

    To opt in to validation, also set `input_types` and `output_types`, e.g.
    `(A, B)`.
    """

    @abstractmethod
    def transform(self, value: T_ins) -> T_outs:
        raise NotImplementedError

    @final
    def run(self, inputs: T_ins) -> T_outs:
        return self.transform(inputs)
