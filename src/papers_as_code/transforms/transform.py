"""
Transforms are the atoms of data pipelines. The composition of transforms is in
itself a transform, and a pipeline can be viewed as a transform with multiple
inputs.
"""
from typing import TYPE_CHECKING

from papers_as_code.transforms.base import BaseTransform
from papers_as_code.type import Type

if TYPE_CHECKING:
    from papers_as_code.transforms.pipeline import Pipeline


class Transform[T_in: Type, T_out: Type](BaseTransform[T_in, T_out]):
    """
    A transform.
    """
    input_type: type[T_in] | None = None
    output_type: type[T_out] | None = None

    def __rshift__[T_other: Type](
        self, other: "Transform[T_out, T_other]"
    ) -> "Pipeline[tuple[T_in], tuple[T_other]]":
        return Pipeline[tuple[T_in], tuple[T_other]](nodes=[self, other], edges={self: other})
