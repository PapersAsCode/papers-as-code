from abc import abstractmethod
from typing import final

from papers_as_code.transforms.base import BaseTransform, Slots
from papers_as_code.transforms.pipeline import Edge, Pipeline
from papers_as_code.type import Type


class OneToOneTransform[T_in: Type, T_out: Type](
    BaseTransform[tuple[T_in], tuple[T_out]]
):
    """
    Turns a single input into a single output.
    """
    input_type: type[T_in] | None = None
    output_type: type[T_out] | None = None

    @property
    def input_types(self) -> Slots:
        return (self.input_type,)

    @property
    def output_types(self) -> Slots:
        return (self.output_type,)

    @abstractmethod
    def transform(self, value: T_in) -> T_out:
        raise NotImplementedError

    @final
    def run(self, inputs: tuple[T_in]) -> tuple[T_out]:
        return (self.transform(inputs[0]),)

    def __rshift__[T_other: Type](
        self, other: "OneToOneTransform[T_out, T_other]"
    ) -> Pipeline[tuple[T_in], tuple[T_other]]:
        return Pipeline[tuple[T_in], tuple[T_other]](
            nodes=[self, other], edges=[Edge(self, other)]
        )
