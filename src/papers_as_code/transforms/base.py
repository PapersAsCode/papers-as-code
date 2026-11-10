"""
Transforms are the atoms of data pipelines. The composition of transforms is in
itself a transform, and a pipeline can be viewed as a transform with multiple
inputs.
"""
from abc import ABC, abstractmethod
from typing import TypeAlias

from papers_as_code.type import Type
from papers_as_code.utils import Label


Slots: TypeAlias = tuple[type[Type] | None, ...] | None
"""The type of each slot, None for a slot of unknown type or unknown slots."""


class BaseTransform[T_ins: tuple[Type, ...], T_outs: tuple[Type, ...]](ABC):
    """
    Anything a pipeline can run.

    Every transform is many-to-many as far as a pipeline is concerned. The
    subclasses let authors write the shape that suits them, and adapt it to
    this one in `run`.
    """
    labels: set[Label]

    @property
    def input_types(self) -> Slots:
        return None

    @property
    def output_types(self) -> Slots:
        return None

    @abstractmethod
    def run(self, inputs: T_ins) -> T_outs:
        raise NotImplementedError
