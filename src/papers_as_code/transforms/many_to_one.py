from abc import abstractmethod
from typing import final

from papers_as_code.transforms.base import BaseTransform, Slots
from papers_as_code.type import Type


class ManyToOneTransform[T_ins: tuple[Type, ...], T_out: Type](
    BaseTransform[T_ins, tuple[T_out]]
):
    """
    Turns several inputs into a single output.

    To opt in to validation, also set `input_types`, e.g. `(A, B)`.
    """
    output_type: type[T_out] | None = None

    @property
    def output_types(self) -> Slots:
        return (self.output_type,)

    @abstractmethod
    def transform(self, value: T_ins) -> T_out:
        raise NotImplementedError

    @final
    def run(self, inputs: T_ins) -> tuple[T_out]:
        return (self.transform(inputs),)
