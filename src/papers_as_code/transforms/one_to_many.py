from abc import abstractmethod
from typing import final

from papers_as_code.transforms.base import BaseTransform, Slots
from papers_as_code.type import Type


class OneToManyTransform[T_in: Type, T_outs: tuple[Type, ...]](
    BaseTransform[tuple[T_in], T_outs]
):
    """
    Turns a single input into several outputs.

    To opt in to validation, also set `output_types`, e.g. `(A, B)`.
    """
    input_type: type[T_in] | None = None

    @property
    def input_types(self) -> Slots:
        return (self.input_type,)

    @abstractmethod
    def transform(self, value: T_in) -> T_outs:
        raise NotImplementedError

    @final
    def run(self, inputs: tuple[T_in]) -> T_outs:
        return self.transform(inputs[0])
